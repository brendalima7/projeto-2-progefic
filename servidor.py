from flask import Flask, request, jsonify
import utils

app = Flask(__name__)


@app.route("/imoveis", methods=['GET'])
def listar_imoveis_rota():

    dados = utils.listar_imoveis()
    return jsonify(dados), 200

if __name__ == '__main__':
    app.run(debug=True)