from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route("/")
def hello_world():
    return "<p>Hello, ISI</p>"

@app.route("/api/v1", methods=['GET'])
def helloapi():
    return jsonify({"result":"hello API ISI v1"})

"""
@app.route("/api/v1/login/<username>", methods=['PUT'])
def login(username):
    print("Hola "+username+"! \n")
    msgresult= username+" logged"
    return jsonify({"result": msgresult}) """

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

