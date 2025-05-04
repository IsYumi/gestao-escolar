from flask import Blueprint, jsonify, request
from ..models.aluno_model import (
    listar_alunos,
    buscar_aluno,
    adicionar_aluno,
    atualizar_aluno,
    deletar_aluno,
    limpar_alunos,
    AlunoNaoEncontrado
)

aluno_blueprint = Blueprint('aluno_routes', __name__)

@aluno_blueprint.route('/alunos', methods=['GET'])
def listar_alunos_view():
    return jsonify(listar_alunos())

@aluno_blueprint.route('/alunos/<int:id_aluno>', methods=['GET'])
def buscar_aluno_view(id_aluno):
    try:
        return jsonify(buscar_aluno(id_aluno))
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

@aluno_blueprint.route('/alunos', methods=['POST'])
def adicionar_aluno_view():
    try:
        dados = request.json
        resultado, status = adicionar_aluno(dados)
        return jsonify(resultado), status
    except AlunoNaoEncontrado as error:
        return jsonify({'Mensagem':f'Erro na rota de alunos {error}'}),404

@aluno_blueprint.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno_view(id_aluno):
    dados = request.json
    try:
        resultado, status = atualizar_aluno(id_aluno, dados)
        return jsonify(resultado), status
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

@aluno_blueprint.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def deletar_aluno_view(id_aluno):
    try:
        resultado, status = deletar_aluno(id_aluno)
        return jsonify(resultado), status
    except AlunoNaoEncontrado:
        return jsonify({'erro': 'Aluno não encontrado'}), 404

@aluno_blueprint.route('/alunos/delete_all', methods=['DELETE'])
def limpar_alunos_view():
    resultado, status = limpar_alunos()
    return jsonify(resultado), status
