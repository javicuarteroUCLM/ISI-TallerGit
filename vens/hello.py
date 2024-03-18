from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import  check_password_hash ,generate_password_hash

import jwt
from datetime import datetime, timedelta


app = Flask(__name__)

app.config['SECRET_KEY'] = 'ItsIsNotAgoodIdeaToPutYourSecretKEYhere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/javi/ISI/ISI-TallerGit/vens/usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db= SQLAlchemy(app)

class User(db.Model):
    id= db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    password= db.Column(db.String(80))
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable= False)

@app.route("/")
def micro():
    return "<p>Hola, microservice ISI</p>"

@app.route("/api/v1/register", methods=['POST'])
def register():
    if request.headers.get('Content-Type') == 'application/json':
        data=request.get_json()
    user = User(
        username = data["username"],
        password = generate_password_hash(data["password"]),
        fs_uniquifier=str(uuid.uuid4())
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"result":"ok"})
    

@app.route("/api/v1/login", methods=['GET'])
def login():
    users= User.query.all()
    for user in users:
        if(user.username==request.args["username"] and 
           check_password_hash(user.password, request.args["password"])):
           token = jwt.encode({
               'user_id' : user.fs_uniquifier,
               'exp' : datetime.utcnow() + timedelta(minutes=60)
           }, app.config['SECRET_KEY'])
           return make_response(jsonify({'token': token.decode('UTF-8')}),201)

    return make_response(jsonify({"reesult":"User not found or password incorrect"}),400)

@app.route("/api/v1/getsecrets", methods=['GET'])
def getsecrets():
    return jsonify({"result": "ok"})

"""
def hello_world():
    return "<p>Hello, ISI</p>"

@app.route("/api/v1", methods=['GET'])
def helloapi():
    return jsonify({"result":"hello API ISI v1"})

@app.route("/api/v1/login/<username>", methods=['PUT'])
def login(username):
    print("Hola "+username+"! \n")
    msgresult= username+" logged"
    return jsonify({"result": msgresult})

@app.route("/api/v1/test", methods=['GET','PUT'])
def testinginput():
    print("El método empleado: " +request.method)
    print ("\nCon argumentos:")
    print(request.args)
    print("Si fuera un formulario:")
    print(request.form)
    print("\nSI adjuntrara un objeto:")
    print(request.data)
    print(request.headers)
    return jsonify({"result":"ok"})
"""

