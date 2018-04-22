# mongo.py
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)


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
