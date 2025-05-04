from ..config import db 
from datetime import date
from ..models.turma_model import Turma

class Aluno(db.Model):
    __tablename__ = 'aluno'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100),nullable=False)
    idade = db.Column(db.Integer,nullable=False)
    turma_id = db.Column(db.Integer,db.ForeignKey('turma.id'),nullable=False)
    nota_primeiro_semestre = db.Column(db.Float)
    nota_segundo_semestre = db.Column(db.Float,nullable=False)
    media_final = db.Column(db.Float,nullable = False)


    def __init__(self,id,nome,idade,turma_id,nota_primeiro_semestre,nota_segundo_semestre,media_final):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.turma_id = turma_id
        self.nota_primeiro_semestre = nota_primeiro_semestre
        self.nota_segundo_semestre = nota_segundo_semestre
        self.media_final = media_final

    def to_dicionario(self):
        return {'id':self.id,'nome':self.nome,'idade':self.idade,'turma_id':self.turma_id,'nota_primeiro_semestre':self.nota_primeiro_semestre,'nota_segundo_semestre':self.nota_segundo_semestre,'media_final':self.media_final}

class AlunoNaoEncontrado(Exception):
    pass

def listar_alunos():
    alunos = Aluno.query.all()
    return [aluno.to_dicionario() for aluno in alunos]
    
def buscar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        raise AlunoNaoEncontrado
    return aluno.to_dicionario()

def adicionar_aluno(dados_aluno):
    turma = Turma.query.get(dados_aluno['turma_id'])
    if(turma is None):
        return {'Mensagem':'A turma não existe'}, 404 
    novo_aluno = Aluno(id=dados_aluno['id'],nome=dados_aluno['nome'],idade=dados_aluno['idade'],turma_id=dados_aluno['turma_id'],nota_primeiro_semestre=dados_aluno['nota_primeiro_semestre'],nota_segundo_semestre=dados_aluno['nota_segundo_semestre'],media_final=dados_aluno['media_final'])
    db.session.add(novo_aluno)
    db.session.commit()
    return {'Mensagem de criação':'Aluno(a) foi adicionado !!'},201

def atualizar_aluno(id,novos_dados):
    aluno = Aluno.query.get(id)
    if not aluno:
        raise AlunoNaoEncontrado
    aluno.id =novos_dados['id']
    aluno.nome = novos_dados['nome']
    aluno.idade = novos_dados['idade']
    aluno.turma_id = novos_dados['turma_id']
    aluno.nota_primeiro_semestre = novos_dados['nota_primeiro_semestre']
    aluno.nota_segundo_semestre = novos_dados['nota_segundo_semestre']
    aluno.media_final =( novos_dados['nota_primeiro_semestre'] + novos_dados['nota_segundo_semestre']) / 2
    db.session.commit()
    return {'Mensagem de atualização':'Aluno(a) atualizado(a)!!'},201

def deletar_aluno(id):
    aluno = Aluno.query.get(id)
    if not aluno:
        raise AlunoNaoEncontrado(f'O aluno com id:{id},não foi achado!')
    db.session.delete(aluno)
    db.session.commit()
    return {'Mensagem de exclusão':'Aluno(a) deletado(a)'},200  

def limpar_alunos():
    alunos = Aluno.query.all()
    for aluno in alunos:
     db.session.delete(aluno)
     db.session.commit()
    return {},200

