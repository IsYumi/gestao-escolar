from flask_restx import Namespace,Resource,fields
from ...models.aluno_model import ( limpar_alunos,listar_alunos,adicionar_aluno,atualizar_aluno,buscar_aluno,deletar_aluno)

aluno_ns = Namespace('alunos',description='Operação relacionada a alunos')

aluno_model = aluno_ns.model("Aluno",{
     "nome":fields.String(required=True,description="Nome do aluno"),
     "idade":fields.Integer(required=True,description='Idade do aluno'),
     "nota_primeiro_semestre": fields.Float(required=True,description="Nota do primeiro semestre"),
     "nota_segundo_semestre":fields.Float(required=True,description="Nota do segundo semestre"),
     "turma_id":fields.Integer(required=True,description="Id da turma ao qual aluno pertence")
   
})

aluno_output_model = aluno_ns.model("AlunoOutput",{
"id":fields.Integer(description="Id do aluno"),
"nome":fields.String(description='Nome do aluno'),
"idade":fields.Integer(description="Idade do aluno"),
"nota_primeiro_semestre":fields.Float(description='Nota do primeiro semestre'),
'nota_segundo_semestre':fields.Float(description='Nota do segundo semestre'),
'turma_id':fields.Integer(description='O id da turma do qual está associdado')
})

@aluno_ns.route("/")
class AlunoResource(Resource):
    @aluno_ns.marshal_list_with(aluno_output_model)
    def get(self):
        return listar_alunos()

    @aluno_ns.expect(aluno_model)
    def post(self):
        aluno = aluno_ns.payload
        response,status_code = adicionar_aluno(aluno)
        return response,status_code

@aluno_ns.route('/<int:id>')
class AlunoIdResource(Resource):
    @aluno_ns.marshal_with(aluno_output_model)
    def get(self,id_aluno):
        return buscar_aluno(id_aluno)
    
    @aluno_ns.expect(aluno_model)
    def put(self,id):
        dados = aluno_ns.payload
        atualizar_aluno(id,dados)
        return dados,201
    
    def delete(self,id):
        deletar_aluno(id)
        return {'Mensagem':f'O aluno com id {id} foi excluído!!'},200
    
   