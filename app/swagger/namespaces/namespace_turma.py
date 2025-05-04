from flask_restx import Resource,Namespace,fields
from ...models.turma_model import (adicionar_turma,atualizar_turma,buscar_turma,deletar_turma,limpar_turmas,listar_turmas)

turma_ns = Namespace('Turmas',description='Operação relacionada as turmas')

turma_model = turma_ns.model('Turma',{
    'id':fields.Integer(required=True,description='Id da turma'),
   'descricao':fields.String(required=True,description='Descrições sobre a turma '),
   'professor_id':fields.Integer(required=True,description='Id do Professor responsável pela turma'),
   'ativo':fields.Boolean(required=True,description='Situação da turma(ativa ou não)')
})

turma_output_model = turma_ns.model('TurmaOutput',{
  'id':fields.Integer(description='Id da turma'),
  'descrição':fields.String(description='Descrição sobre a turma'),
  'professor_id':fields.Integer(description='Id do professor responsável pela turma'),
  'ativo':fields.Boolean(description='Situação da turma')
})


@turma_ns.route('/')
class TurmaResource(Resource):
    @turma_ns.marshal_list_with(turma_output_model)
    def get(self):
        return listar_turmas()

    @turma_ns.expect(turma_model)
    def post(self):
        nova_turma = turma_ns.payload
        response,status_code = adicionar_turma(nova_turma)
        return response,status_code
    
@turma_ns.route('<int:id>')
class TurmaIdResource(Resource):
    @turma_ns.marshal_with(turma_output_model)
    def get(self,id):
        return buscar_turma(id)
    
    @turma_ns.expect(turma_model)
    def put(self,id):
        data = turma_ns.payload
        atualizar_turma(id,data)
        return data,201
    
    def delete(self,id):
        deletar_turma(id)
        return {'Mensagem':'Turma deletada !!'},200
    