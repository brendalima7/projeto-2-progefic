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

@app.route("/imoveis", methods=['POST'])
def criar_imovel():

    dados = request.get_json(silent=True)

    campos_faltantes = utils.validar_campos_faltantes(dados)
    if campos_faltantes:
        return jsonify({
            "erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"
        }), 400

    novo_id = utils.criar_imovel(dados)
    return jsonify({"id": novo_id}), 201

if __name__ == '__main__':
    app.run(debug=True)