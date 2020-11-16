
from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

lista_nomes = ['João', 'Maria', 'Paulo', 'José', 'Francisca', 'Silas', 'Luciana', 'Tiago', 'Katia']
lista_projetos = ['Sementinha', 'Natal', 'Catarina']

assistidos = [{"id": e, "nome":str(random.choice(lista_nomes)), "idade":str(random.randint(18, 60)), "projeto":str(random.choice(lista_projetos)), "foto":"https://i.imgur.com/KHu8SpP.png"} for e in range(1,11)]   

@app.route("/assistidos", methods=['GET'])
def get():
    return jsonify(assistidos)


@app.route("/assistidos/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in assistidos if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/assistidos", methods=['POST'])
def post():
    global assistidos
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in assistidos]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        assistidos.append(content)
        return jsonify({"status":"OK", "msg":"assistido cadastrado com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/assistidos/<int:id>", methods=['DELETE'])
def delete(id):
    global assistidos
    try:
        assistidos = [e for e in assistidos if e["id"] != id]
        return jsonify({"status":"OK", "msg":"assistido removido com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	d = random.choice(assistidos)
	data = {
		"to": token,
		"notification" : {
			"title":d["nome"],
			"body":"Você tem nova atividade em "+d['nome']
		},
		"data" : {
			"assistidoId":d['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')