# mongo.py

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/restdb'

mongo = PyMongo(app)

@app.route('/alarma', methods=['GET'])
#@requires_auth
def get_all_alarmas():

        alarma = mongo.db.alarmas
        output = []
        for a in alarma.find():
            output.append({'fecha': a['fecha'], 'tipo': a['tipo'], 'cerradura': a['cerradura'], 'inmueble': a['inmueble'],
                           'conjunto': a['conjunto']})
        return jsonify({'result': output})
  

@app.route('/alarma', methods=['POST'])
def add_alarma():
    alarma = mongo.db.alarmas
    data = request.get_json()
    alarma.insert(data)
    return jsonify({'result': "Se agrego la alarma"})

@app.route('/star', methods=['GET'])
def get_all_stars():
  star = mongo.db.stars
  output = []
  for s in star.find():
    output.append({'name' : s['name'], 'distance' : s['distance']})
  return jsonify({'result' : output})

@app.route('/star/', methods=['GET'])
def get_one_star(name):
  star = mongo.db.stars
  s = star.find_one({'name' : name})
  if s:
    output = {'name' : s['name'], 'distance' : s['distance']}
  else:
    output = "No such name"
  return jsonify({'result' : output})

@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  name = request.json['name']
  distance = request.json['distance']
  star_id = star.insert({'name': name, 'distance': distance})
  new_star = star.find_one({'_id': star_id })
  output = {'name' : new_star['name'], 'distance' : new_star['distance']}
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)