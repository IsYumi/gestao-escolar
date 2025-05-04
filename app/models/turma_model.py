from ..config import db
from ..models.docente_model import Docente

class Turma(db.Model):
    __tablename__ = 'turma'

    id = db.Column(db.Integer,primary_key=True)
    descricao = db.Column(db.String,nullable=False)
    professor_id = db.Column(db.Integer,db.ForeignKey('docente.id'))
    ativo = db.Column(db.Boolean,nullable=False)

    def __init__(self,id,descricao,professor_id,ativo):
        self.id = id
        self.descricao = descricao
        self.professor_id = professor_id
        self.ativo = ativo

    def to_dicionario(self):
        return {'id':self.id,'descricao':self.descricao,'professor_id':self.professor_id,'ativo':self.ativo}
    
class TurmaNaoEncontrada(Exception):
    pass

def buscar_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        raise TurmaNaoEncontrada ('A turma não foi encontrada!')
    return turma.to_dicionario()

def listar_turmas():
    turmas = Turma.query.all()
    return [turma.to_dicionario() for turma in turmas]
    
def adicionar_turma(dados):
    professor = Docente.query.get(dados['professor_id'])
    if professor is None:
        return {'Mensagem de erro': 'O professor não existe!'},404
    nova_turma = Turma(
        id=dados['id'],
        descricao=dados['descricao'],
        professor_id=int(dados['professor_id']),
        ativo=bool(dados['ativo'])
    )
    db.session.add(nova_turma)
    db.session.commit()
    return{'Mensagem':'Turma foi adicionada!'},201

def atualizar_turma(id,new_data):
    turma = Turma.query.get(id)
    if not turma:
        raise TurmaNaoEncontrada ('A turma não foi encontrada!')
    turma.id = new_data['id']
    turma.descricao = new_data['descricao']
    turma.professor_id = new_data['professor_id']
    turma.ativo = new_data['ativo']
    db.session.commit()
    return {'Mensagem de atualização':'Turma atualizada'},201

def deletar_turma(id):
    turma = Turma.query.get(id)
    if not turma:
        raise TurmaNaoEncontrada ("A turma não foi encontrada!!")
    db.session.delete(turma)
    db.session.commit()
    return {'Mensagem de exclusão':'Turma deletada !'},200

def limpar_turmas():
    turmas = Turma.query.all()
    for turma in turmas:
        db.session.delete(turma)
        db.session.commit()
    return {},200

