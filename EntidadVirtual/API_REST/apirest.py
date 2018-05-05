# mongo.py
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)


#CONJUNTO
@app.route('/conjunto', methods=['GET'])
def get_all_conjuntos():
    conjunto = mongo.db.conjuntos
    output = []
    for c in conjunto.find():
        output.append({'nombre': c['nombre'], 'direccion': c['direccion'], 'estado': c['estado']})
    return jsonify({'result': output})


@app.route('/conjunto/<name>', methods=['GET'])
def get_one_conjunto(name):
    conjunto = mongo.db.conjuntos
    c = conjunto.find_one({'nombre': name})
    if c:
        output = {'nombre': c['nombre'], 'direccion': c['direccion'], 'estado': c['estado']}
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/conjunto', methods=['POST'])
def add_conjunto():
    conjunto = mongo.db.conjuntos
    data = request.get_json()
    conjunto.insert(data)
    return get_one_conjunto(data['nombre'])


@app.route('/conjunto/<name>', methods=['PUT'])
def put_conjunto(name):
    data = request.get_json()
    mongo.db.conjuntos.update_one({'nombre': name}, {'$set': data})
    return get_one_conjunto(name)


@app.route('/conjunto/<name>', methods=['DELETE'])
def delete_conjunto(name):
    mongo.db.conjuntos.update_one({'nombre': name}, {'$set': {'estado': 'Inactivo'}})
    return get_one_conjunto(name)


# INMUEBLE

@app.route('/conjunto/<name>/inmueble', methods=['GET'])
def get_all_inmuebles_in_conjunto(name):
    conjunto = mongo.db.conjuntos
    c = conjunto.find_one({'nombre': name})
    output = []
    if c:
        inmueble = mongo.db.inmuebles
        for i in inmueble.find():
            if i['conjunto'] == c['nombre']:
                output.append(
                    {'numero': i['numero'], 'conjunto': i['conjunto'], "id_hub": i['id_hub'], "estado": i['estado']})
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/conjunto/<conjunto_nombre>/inmueble', methods=['POST'])
def add_inmueble(conjunto_nombre):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c and data['conjunto'] == conjunto_nombre:

        inmueble_id = inmueble.insert(data)
        new_inmueble = inmueble.find_one({'_id': inmueble_id})
        output = {'numero': new_inmueble['numero'],
                  'conjunto': new_inmueble['conjunto'], 'id_hub': new_inmueble['id_hub'],
                  "estado": new_inmueble['estado']}
    else:
        output = "No such conjunto"
    return jsonify({'result': output})


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>', methods=['GET'])
def get_one_inmueble(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c:
        i = inmueble.find_one({'numero': inmueble_numero, 'conjunto': conjunto_nombre})
        if i:
            output = {'numero': i['numero'], 'conjunto': i['conjunto'], 'id_hub': i['id_hub'], "estado": i['estado']}
        else:
            output = "No such inmueble"
    else:
        output = "No such conjunto"
    return jsonify({'result': output})


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>', methods=['PUT'])
def put_inmueble(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c and data['conjunto'] == conjunto_nombre:
        mongo.db.inmuebles.update_one({'numero': inmueble_numero}, {'$set': data})
    return get_one_inmueble(conjunto_nombre, inmueble_numero)


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>', methods=['DELETE'])
def delete_inmueble(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c and data['conjunto'] == conjunto_nombre:
        mongo.db.inmuebles.update_one({'numero': inmueble_numero}, {'$set': {'estado': 'Inactivo'}})
    return get_one_inmueble(conjunto_nombre, inmueble_numero)


#Cerradura
@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura/<numero_cerradura>', methods=['GET'])
def get_one_cerradura(conjunto_nombre, inmueble_numero, numero_cerradura):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c:
        i = inmueble.find_one({'numero': inmueble_numero, 'conjunto': conjunto_nombre})
        if i:
            b = mongo.db.cerraduras.find_one({'num_inmueble': inmueble_numero, 'id_cerradura': numero_cerradura})
            if b:
                output = {'id_cerradura': b['id_cerradura'], 'tipo': b['tipo'], 'num_inmueble': b['num_inmueble'],
                          "estado": b['estado']}
            else:
                output = "No such cerradura"
        else:
            output = "No such inmueble"
    else:
        output = "No such conjunto"
    return jsonify({'result': output})


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura', methods=['GET'])
def get_all_cerraduras_in_inmueble(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    c = conjunto.find_one({'nombre': conjunto_nombre})
    i = inmueble.find_one({'numero': inmueble_numero})

    output = []
    if c and i:
        cerradura = mongo.db.cerraduras
        for l in cerradura.find():
            if i['conjunto'] == c['nombre'] and l['num_inmueble'] == i['numero']:
                output.append({'id_cerradura': l['id_cerradura'], 'tipo': l['tipo'], 'num_inmueble': i['numero'],
                               "estado": l['estado']})
    else:
        output = "No such name"
    return jsonify({'result': output})


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura', methods=['POST'])
def add_cerradura(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    cerradura = mongo.db.cerraduras
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    i = inmueble.find_one({'numero': inmueble_numero})
    if c and i and data['num_inmueble'] == inmueble_numero and i['conjunto'] == conjunto_nombre:
        cerradura.insert(data)
    return get_one_cerradura(conjunto_nombre, inmueble_numero, data['id_cerradura'])


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura/<numero_cerradura>', methods=['PUT'])
def put_cerradura(conjunto_nombre, inmueble_numero, numero_cerradura):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    i = inmueble.find_one({'numero': inmueble_numero})
    if c and i and data['num_inmueble'] == inmueble_numero and i['conjunto'] == conjunto_nombre:
        mongo.db.cerraduras.update_one({'id_cerradura': numero_cerradura}, {'$set': data})
    return get_one_cerradura(conjunto_nombre, inmueble_numero, numero_cerradura)


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura/<numero_cerradura>', methods=['DELETE'])
def delete_cerradura(conjunto_nombre, inmueble_numero, numero_cerradura):
    conjunto = mongo.db.conjuntos
    inmueble = mongo.db.inmuebles
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    i = inmueble.find_one({'numero': inmueble_numero})
    if c and i and data['num_inmueble'] == inmueble_numero and i['conjunto'] == conjunto_nombre:
        mongo.db.cerraduras.update_one({'id_cerradura': numero_cerradura},{'$set': {'estado': 'Inactivo'}})
    return get_one_cerradura(conjunto_nombre, inmueble_numero, numero_cerradura)


##ALARMA
@app.route('/alarma', methods=['GET'])
def get_all_alarmas():
    alarma = mongo.db.alarmas
    output = []
    for a in alarma.find():
        output.append({'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                       'conjunto': a['conjunto']})
    return jsonify({'result': output})


@app.route('/alarma/conjunto/<conjunto_nombre>', methods=['GET'])
def get_all_alarmas_in_conjunto(conjunto_nombre):
    alarma = mongo.db.alarmas
    output = []
    for a in alarma.find():
        if conjunto_nombre == a['conjunto']:
            output.append(
                {'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                 'conjunto': a['conjunto']})
    return jsonify({'result': output})

#la funcion necesita como entrada el mes
@app.route('/alarma/conjunto/<conjunto_nombre>/<pmes>', methods=['GET'])
def get_all_alarmas_in_conjunto_by_Month(conjunto_nombre,pmes):
    alarma = mongo.db.alarmas
    output = []
    for a in alarma.find():
        año, mes, dia = a['fecha'].split("-")
        if conjunto_nombre == a['conjunto'] and mes == pmes :
            output.append(
                {'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                 'conjunto': a['conjunto']})
    return jsonify({'result': output})


@app.route('/alarma/inmueble/<num_inmueble>', methods=['GET'])
def get_all_alarmas_in_inmueble(num_inmueble):
    alarma = mongo.db.alarmas
    output = []
    for a in alarma.find():
        if num_inmueble == a['inmueble']:
            output.append(
                {'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                 'conjunto': a['conjunto']})
    return jsonify({'result': output})

@app.route('/alarma/inmueble/<num_inmueble>/<pmes>', methods=['GET'])
def get_all_alarmas_in_inmueble_by_Month(num_inmueble, pmes):
    alarma = mongo.db.alarmas
    output = []
    for a in alarma.find():
        año, mes, dia = a['fecha'].split("-")
        if num_inmueble == a['inmueble'] and mes == pmes :
            output.append(
                {'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                 'conjunto': a['conjunto']})
    return jsonify({'result': output})

@app.route('/alarma', methods=['POST'])
def add_alarma():
    alarma = mongo.db.alarmas
    data = request.get_json()
    alarma.insert(data)
    return jsonify({'result': "Se agrego la alarma"})


##USUARIO
@app.route('/alarma/propietario/<id_propietario>', methods=['GET'])
def get_all_alarmas_of_propietario(id_propietario):
    alarma = mongo.db.alarmas
    output = []
    for a in alarma.find():
        if id_propietario == a['propietario']:
            output.append(
                {'nombre': a['nombre'], 'apellido': a['apellido'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                 'conjunto': a['conjunto']})
    return jsonify({'result': output})


@app.route('/propietario/<id_propietario>', methods=['GET'])
def get_one_propietario(id_propietario):
    propietario = mongo.db.propietarios
    p = propietario.find_one({'id_propietario': id_propietario})
    if p:
        output = {'id_propietario': p['id_propietario'], 'nombre': p['nombre'], 'apellido': p['apellido']}
    else:
        output = "No such id"
    return jsonify({'result': output})


@app.route('/propietario/<id_propietario>', methods=['PUT'])
def put_propietario(id_propietario):
    data = request.get_json()
    mongo.db.propietarios.update_one({'id_propietario': id_propietario}, {'$set': data})
    return get_one_propietario(id_propietario)


@app.route('/propietario/<id_propietario>/hub', methods=['POST'])
def add_hub(id_propietario):
    propietario = mongo.db.propietarios
    hub = mongo.db.hubs
    data = request.get_json()
    p = propietario.find_one({'id_propietario': id_propietario})
    if p and data['id_propietario'] == id_propietario:

        hub_id = hub.insert(data)
        new_hub = hub.find_one({'_id': hub_id})
        output = {'puerto': new_hub['puerto'],
                  'cantidad_puertos': new_hub['cantidad_puertos'], 'estado': new_hub['estado']}
    else:
        output = "No such propietario"
    return jsonify({'result': output})



if __name__ == '__main__':
    app.run(debug=True)
