from flask import Blueprint, request, jsonify
from ..models.docente_model import(
     DocenteNaoEncontrado, 
     listar_docentes, 
     buscar_docente, 
     adicionar_docente, 
     deletar_docente, 
     limpar_docentes, 
     atualizar_docente
)

docentes_blueprint = Blueprint('professor', __name__)

@docentes_blueprint.route('/docentes', methods=['GET'])
def listar_docentes_view():
    return jsonify(listar_docentes())

@docentes_blueprint.route('/docente/<int:id_docente>', methods=['GET'])
def get_docente(id_docente):
    try:
        docente = buscar_docente(id_docente)
        return jsonify(docente)
    except DocenteNaoEncontrado:
        return jsonify({'erro': 'Docente não encontrado'}), 404

@docentes_blueprint.route('/docente', methods=['POST'])
def adicionar_docente_view():
    dados = request.get_json()
    resultado,status = adicionar_docente(dados)
    return jsonify(resultado), status

@docentes_blueprint.route('/docente/<int:id_docente>', methods=['PUT'])
def update_aluno(id_docente):
    dados = request.json
    try:
        resultado, status = atualizar_docente(id_docente, dados)
        return jsonify(resultado), status
    except DocenteNaoEncontrado:
        return jsonify({'erro': 'Docente não encontrado'}), 404

@docentes_blueprint.route('/docente/<int:id_docente>', methods=['DELETE'])
def deletar_docente_view(id_docente):
    try:
        resultado, status = deletar_docente(id_docente)
        return jsonify(resultado), status
    except DocenteNaoEncontrado:
        return jsonify({'erro': 'Docente não encontrado'}), 404

@docentes_blueprint.route('/docentes/delete_all', methods=['DELETE'])
def limpar_docente():
    resultado, status = limpar_docentes()
    return jsonify(resultado), status
