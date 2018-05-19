# mongo.py
import http.client
from flask import Flask
from flask import Flask,redirect
import paho.mqtt.client as paho
from flask import jsonify
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from flask_pymongo import PyMongo
from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
import requests
from functools import wraps

app = Flask(__name__, static_url_path='/public', static_folder='./public', template_folder='templates')
app.secret_key = 'estaesunaclavesecreta'

##cosas del mqtt
topico = "conjunto1/residencia1/cerradura"
client = paho.Client()
client.connect("broker.mqtt-dashboard.com", 1883)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='KbPC5q-VuaUwBrkEP9_DY2-gWj-5t-Kt',
    client_secret='hM_dr9PBWS8fQ9Ijyd3veM-8lmJ43SF8BKFkFwuWu9ArKpnlle8197m4ajopCtY6',
    api_base_url='https://isis2503-softsecurity.auth0.com',
    access_token_url='https://isis2503-softsecurity.auth0.com/oauth/token',
    authorize_url='https://isis2503-softsecurity.auth0.com/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)

##Cerradura TEST

#Insertar una cerradura
@app.route("/cerradura", methods=["POST"])
def insert_cerradura():
    password = request.json['password']
    posicion = request.json['posicion']
    hora_inicio = request.json['hora_inicio']
    hora_fin = request.json['hora_fin']

    nuevo_candado = "0;"+password+";"+posicion;

    #hl.agregar_candado(hora_inicio, hora_fin, posicion)
    client.publish("horariocandado", hora_inicio+";"+hora_fin+";"+posicion)
    client.publish(topico, nuevo_candado)
    return jsonify(nuevo_candado)


@app.route("/cerradura", methods=["PUT"])
def update_cerradura():
    password = request.json['password']
    posicion = request.json['posicion']
    nuevo_candado = "1;"+password+";"+posicion;
    client.publish(topico, nuevo_candado)
    return jsonify(nuevo_candado)


@app.route("/cerradura", methods=["DELETE"])
def delete_clave_cerradura():
    posicion = request.json['posicion']
    nuevo_candado = "2;" + posicion
    client.publish(topico, nuevo_candado)
    return jsonify(nuevo_candado)



@app.route("/cerradura_all", methods=["DELETE"])
def delete_all_cerraduras():
    mensaje = "3"
    client.publish(topico,mensaje)
    return jsonify(mensaje)


@app.route("/cerraduraHorario", methods = ["PUT"])
def change_state_cerradura():
    posicion = request.json['posicion']
    mensaje = "4;"+posicion
##FIN CERRADURA TEST


# Controllers API
@app.route('/')
def home():
    return render_template('home.html')

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    resp = auth0.authorize_access_token()

    url = 'https://isis2503-softsecurity.auth0.com/userinfo'
    headers = {'authorization': 'Bearer ' + resp['access_token']}
    resp = requests.get(url, headers=headers)
    userinfo = resp.json()

    # Store the tue user information in flask session.
    session['jwt_payload'] = userinfo

    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }

    return redirect('/dashboard')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='http://127.0.0.1:4200', audience='https://isis2503-softsecurity.auth0.com/userinfo')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('home', _external=True), 'client_id': 'KbPC5q-VuaUwBrkEP9_DY2-gWj-5t-Kt'}
    return redirect('https://isis2503-softsecurity.auth0.com/v2/logout')

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'profile' not in session:
            # Redirect to Login page here
            return redirect('/')
        return f(*args, **kwargs)

    return decorated

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

#CONJUNTO
@app.route('/conjunto', methods=['GET'])
#@requires_auth
def get_all_conjuntos():
    if 'admin' or 'Yale' in str(session['jwt_payload']):
        conjunto = mongo.db.conjuntos
        output = []
        for c in conjunto.find():
            output.append({'nombre': c['nombre'], 'direccion': c['direccion'], 'estado': c['estado']})
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1

@app.route('/conjunto/<name>', methods=['GET'])
#@requires_auth
def get_one_conjunto(name):
    if 'admin' or 'Yale' in str(session['jwt_payload']):
        conjunto = mongo.db.conjuntos
        c = conjunto.find_one({'nombre': name})
        if c:
            output = {'nombre': c['nombre'], 'direccion': c['direccion'], 'estado': c['estado']}
        else:
         output = "No such name"
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1


@app.route('/conjunto', methods=['POST'])
#@requires_auth
def add_conjunto():
    conjunto = mongo.db.conjuntos
    data = request.get_json()
    conjunto.insert(data)
    return get_one_conjunto(data['nombre'])


@app.route('/conjunto/<name>', methods=['PUT'])
#@requires_auth
def put_conjunto(name):
    if 'admin' in str(session['jwt_payload']):
        data = request.get_json()
        mongo.db.conjuntos.update_one({'nombre': name}, {'$set': data})
        return get_one_conjunto(name)
    else:
        msg1 = "no eres admin"
        print("sirve")
        return msg1

@app.route('/conjunto/<name>', methods=['DELETE'])
#@requires_auth
def delete_conjunto(name):
    mongo.db.conjuntos.update_one({'nombre': name}, {'$set': {'estado': 'Inactivo'}})
    return get_one_conjunto(name)


# INMUEBLE

@app.route('/conjunto/<name>/inmueble', methods=['GET'])
#@requires_auth
def get_all_inmuebles_in_conjunto(name):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
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
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1

@app.route('/conjunto/<conjunto_nombre>/inmueble', methods=['POST'])
#@requires_auth
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
#@requires_auth
def get_one_inmueble(conjunto_nombre, inmueble_numero):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
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
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1

@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>', methods=['PUT'])
#@requires_auth
def put_inmueble(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c and data['conjunto'] == conjunto_nombre:
        mongo.db.inmuebles.update_one({'numero': inmueble_numero}, {'$set': data})
    return get_one_inmueble(conjunto_nombre, inmueble_numero)


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>', methods=['DELETE'])
#@requires_auth
def delete_inmueble(conjunto_nombre, inmueble_numero):
    conjunto = mongo.db.conjuntos
    data = request.get_json()
    c = conjunto.find_one({'nombre': conjunto_nombre})
    if c and data['conjunto'] == conjunto_nombre:
        mongo.db.inmuebles.update_one({'numero': inmueble_numero}, {'$set': {'estado': 'Inactivo'}})
    return get_one_inmueble(conjunto_nombre, inmueble_numero)


#Cerradura
@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura/<numero_cerradura>', methods=['GET'])
#@requires_auth
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
#@requires_auth
def get_all_cerraduras_in_inmueble(conjunto_nombre, inmueble_numero):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
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
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1


@app.route('/conjunto/<conjunto_nombre>/inmueble/<inmueble_numero>/cerradura', methods=['POST'])
#@requires_auth
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
#@requires_auth
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
#@requires_auth
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
#@requires_auth
def get_all_alarmas():
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
        alarma = mongo.db.alarmas
        output = []
        for a in alarma.find():
            output.append({'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                           'conjunto': a['conjunto']})
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1

@app.route('/alarma/conjunto/<conjunto_nombre>', methods=['GET'])
#@requires_auth
def get_all_alarmas_in_conjunto(conjunto_nombre):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
        alarma = mongo.db.alarmas
        output = []
        for a in alarma.find():
            if conjunto_nombre == a['conjunto']:
                output.append(
                    {'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                     'conjunto': a['conjunto']})
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1


# la funcion necesita como entrada el mes
@app.route('/alarma/conjunto/<conjunto_nombre>/<pmes>', methods=['GET'])
@requires_auth
def get_all_alarmas_in_conjunto_by_month(conjunto_nombre, pmes):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
        alarma = mongo.db.alarmas
        output = []
        for a in alarma.find():
            año, mes, dia = a['fecha'].split("-")
            if conjunto_nombre == a['conjunto'] and mes == pmes:
                output.append(
                    {'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                     'conjunto': a['conjunto']})
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1

@app.route('/alarma/inmueble/<num_inmueble>', methods=['GET'])
#@requires_auth
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
#@requires_auth
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
#@requires_auth
def add_alarma():
    alarma = mongo.db.alarmas
    data = request.get_json()
    alarma.insert(data)
    return jsonify({'result': "Se agrego la alarma"})


##USUARIO
@app.route('/alarma/propietario/<id_propietario>', methods=['GET'])
#@requires_auth
def get_all_alarmas_of_propietario(id_propietario):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
        alarma = mongo.db.alarmas
        output = []
        for a in alarma.find():
            if id_propietario == a['propietario']:
                output.append(
                    {'nombre': a['nombre'], 'apellido': a['apellido'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                     'conjunto': a['conjunto']})
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1

@app.route('/propietario/<id_propietario>', methods=['GET'])
#@requires_auth
def get_one_propietario(id_propietario):
    if 'admin' or 'Yale' or 'Segurirdad privada' in str(session['jwt_payload']):
        propietario = mongo.db.propietarios
        p = propietario.find_one({'id_propietario': id_propietario})
        if p:
            output = {'id_propietario': p['id_propietario'], 'nombre': p['nombre'], 'apellido': p['apellido']}
        else:
            output = "No such id"
        return jsonify({'result': output})
    else:
        msg1 = "no tiene permisos para acceder a esta informacion"
        return msg1


@app.route('/propietario/<id_propietario>', methods=['PUT'])
#@requires_auth
def put_propietario(id_propietario):
    data = request.get_json()
    mongo.db.propietarios.update_one({'id_propietario': id_propietario}, {'$set': data})
    return get_one_propietario(id_propietario)


@app.route('/propietario/<id_propietario>/hub', methods=['POST'])
#@requires_auth
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
