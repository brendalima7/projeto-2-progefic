from flask import Flask, request, jsonify
import utils

app = Flask(__name__)


@app.route("/imoveis", methods=['GET'])
def listar_imoveis_rota():

    dados = utils.listar_imoveis()
    return jsonify(dados), 200

@app.route("/imoveis/<int:id>", methods=['GET'])
def listar_um_imovel(id):

    imovel = utils.buscar_imovel_por_id(id)

    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    return jsonify(imovel), 200

if __name__ == '__main__':
    app.run(debug=True)