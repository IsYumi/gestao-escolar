from flask_restx import Namespace,Resource,fields
from ...models.docente_model import (adicionar_docente,atualizar_docente,buscar_docente,deletar_docente,limpar_docentes,listar_docentes)

docente_ns = Namespace('docentes',description='Operações relacionadas aos professores')

docente_model = docente_ns.model('Docente',{
    'id':fields.Integer(required=True,description='Id do docente'),
    'nome':fields.String(required=True,description='Nome do docente'),
    'idade':fields.Integer(required=True,description='Idade do Docente'),
    'materia': fields.String(required=True,description='Matéria ao qual o docente leciona'),
    'observacoes':fields.String(required=True,description='Observações sobre o docente')
})

docente_output_model = docente_ns.model('DocenteOutput',{
    'id':fields.Integer(description='Id do Docente'),
    'nome':fields.String(description='Nome do Docente'),
    'idade':fields.Integer(description='Idade do Docente'),
    'materia':fields.String(description='Matéria ao qual o docente leciona'),
    'observacoes':fields.String(description='Observações sobre o docente')
})

@docente_ns.route('/')
class DocenteResource(Resource):
    @docente_ns.marshal_list_with(docente_output_model)
    def get(self):
        return listar_docentes()
    
    @docente_ns.expect(docente_model)
    def post(self):
        novo_docente = docente_ns.payload
        response,status_code = adicionar_docente(novo_docente)
        return response,status_code
    

@docente_ns.route('/<int:id>')
class DocenteIdResource(Resource):
    @docente_ns.marshal_with(docente_output_model)
    def get(self,id):
        return buscar_docente(id)

    @docente_ns.expect(docente_model)
    def put(self,id):
        dados = docente_ns.payload
        atualizar_docente(id,dados)
        return dados,201
    
    def delete(self,id):
        deletar_docente(id)
        return {'Mensagem':'Docente excluído '},200