from flask import Flask, request, jsonify, url_for
import utils

app = Flask(__name__)


@app.route("/imoveis", methods=['GET'])
def listar_imoveis_rota():

    dados = utils.listar_imoveis()

    for imovel in dados:
        imovel["links"] = [
            {'rel': 'self', 'href': url_for('listar_um_imovel_rota', id=imovel['id'], _external=True), 'method': 'GET'},
            {'rel': 'atualizar', 'href': url_for('alterar_imovel_rota', id=imovel['id'], _external=True), 'method': 'PUT'},
            {'rel': 'deletar', 'href': url_for('deletar_imovel_rota', id=imovel['id'], _external=True), 'method': 'DELETE'}
        ]
    return jsonify({
        "imoveis": dados,
        "links": [
            {'rel': 'self', 'href': url_for('listar_imoveis_rota', _external=True), 'method': 'GET'},
            {'rel': 'create', 'href': url_for('criar_imovel_rota', _external=True), 'method': 'POST'}
        ]
    }), 200


@app.route("/imoveis/<int:id>", methods=['GET'])
def listar_um_imovel_rota(id):

    imovel = utils.buscar_imovel_por_id(id)

    if not imovel:
        return jsonify({
            "erro": "Imóvel não encontrado",
            "links": [
                {"rel": "resource", "href": url_for("listar_um_imovel_rota", id=id, _external=True), "method": "GET"},
                {"rel": "collection", "href": url_for("listar_imoveis_rota", _external=True), "method": "GET"}
            ]
        }), 404

    imovel["links"] = [
        {"rel": "self", "href": url_for("listar_um_imovel_rota", id=id, _external=True), "method": "GET"},
        {"rel": "atualizar", "href": url_for("alterar_imovel_rota", id=id, _external=True), "method": "PUT"},
        {"rel": "deletar", "href": url_for("deletar_imovel_rota", id=id, _external=True), "method": "DELETE"},
        {"rel": "collection", "href": url_for("listar_imoveis_rota", _external=True), "method": "GET"}
    ]

    return jsonify(imovel), 200

@app.route("/imoveis", methods=['POST'])
def criar_imovel_rota():

    dados = request.get_json(silent=True)

    campos_faltantes = utils.validar_campos_faltantes(dados)
    if campos_faltantes:
        return jsonify({
            "erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"
        }), 400

    novo_id = utils.criar_imovel(dados)
    return jsonify({"id": novo_id}), 201

@app.route("/imoveis/<int:id>", methods=['PUT'])
def alterar_imovel_rota(id):

    dados = request.get_json(silent=True)

    campos_faltantes = utils.validar_campos_faltantes(dados)
    if campos_faltantes:
        return jsonify({
            "erro": "Campos obrigatórios: logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao"
        }), 400

    imovel = utils.buscar_imovel_por_id(id)
    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404
    
    utils.alterar_imovel(id, dados)

    return jsonify({"mensagem": "Imóvel atualizado com sucesso"}), 200

@app.route("/imoveis/<int:id>", methods=['DELETE'])
def deletar_imovel_rota(id):

    imovel = utils.buscar_imovel_por_id(id)
    if not imovel:
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    utils.deletar_imovel(id)

    return jsonify({"mensagem": "Imóvel excluído com sucesso"}), 200

@app.route("/imoveis/<tipo>", methods=['GET'])
def listar_imoveis_por_tipo_rota(tipo):

    tipo_normalizado = tipo.lower() # normaliza para minusculo -> "Casa" -> "casa"
    validacao = utils.validar_tipo(tipo_normalizado) # retorna True ou False
    
    if not validacao:
        return jsonify({
            "erro": "Tipo inválido",
            "links": [
                {"rel": "collection", "href": url_for("listar_imoveis_rota", _external=True), "method": "GET"}
            ]
        }), 400

    dados = utils.listar_imoveis_por_tipo(tipo_normalizado)

    for imovel in dados:
        imovel["links"] = [
            {"rel": "self", "href": url_for("listar_um_imovel_rota", id=imovel["id"], _external=True), "method": "GET"},
            {"rel": "atualizar", "href": url_for("alterar_imovel_rota", id=imovel["id"], _external=True), "method": "PUT"},
            {"rel": "deletar", "href": url_for("deletar_imovel_rota", id=imovel["id"], _external=True), "method": "DELETE"}
        ]

    return jsonify({
        "imoveis": dados,
        "links": [
            {"rel": "self", "href": url_for("listar_imoveis_por_tipo_rota", tipo=tipo_normalizado, _external=True), "method": "GET"},
            {"rel": "collection", "href": url_for("listar_imoveis_rota", _external=True), "method": "GET"}
        ]
    }), 200

@app.route("/imoveis/cidade/<cidade>", methods=['GET'])
def listar_imoveis_por_cidade_rota(cidade):

    dados = utils.listar_imoveis_por_cidade(cidade)
    return jsonify(dados), 200

if __name__ == '__main__':
    app.run(debug=True)