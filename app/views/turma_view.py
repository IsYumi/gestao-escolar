from flask import Blueprint, request, jsonify
from ..models.turma_model import (
    TurmaNaoEncontrada, 
    adicionar_turma, 
    buscar_turma, 
    listar_turmas, 
    deletar_turma, 
    limpar_turmas, 
    atualizar_turma
        )

turmas_blueprint = Blueprint('/turmas', __name__)

@turmas_blueprint.route('/turma', methods=['GET'])
def listar_turma_view():
    return jsonify(listar_turmas())

@turmas_blueprint.route('/turma/<int:id_turma>', methods=['GET'])
def get_turma(id_turma):
    try:
        turma = buscar_turma(id_turma)
        return jsonify(turma)
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'A turma selecionada não foi encontrada'}), 404

@turmas_blueprint.route('/turma', methods=['POST'])
def adicionar_turma_view():
        try:
            dados = request.json
            resultado, status = adicionar_turma(dados)
            return jsonify(resultado), status
        except TurmaNaoEncontrada as erro:
            return jsonify({'Mensagem':f'Erro na rota de turma:{str(erro)}'})

@turmas_blueprint.route('/turma/<int:id_turma>', methods=['PUT'])
def update(id_turma):
    dados = request.json
    try:
        resultado, status = atualizar_turma(id_turma, dados)
        return jsonify(resultado), status
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'A turma selecionada não foi encontrada'}), 404

@turmas_blueprint.route('/turma/<int:id_turma>', methods=['DELETE'])
def deletar_turma_view(id_turma):
    try:
        resultado, status = deletar_turma(id_turma)
        return jsonify(resultado), status
    except TurmaNaoEncontrada:
        return jsonify({'erro': 'A turma selecionada não foi encontrada'}), 404

@turmas_blueprint.route('/turmas/delete_all', methods=['DELETE'])
def limpar_turma():
    resultado, status = limpar_turmas()
    return jsonify(resultado), status
