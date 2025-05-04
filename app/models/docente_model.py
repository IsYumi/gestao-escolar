from ..config import db

class Docente(db.Model):
    __tablename__ = 'docente'

    id = db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100),nullable=False)
    idade = db.Column(db.Integer,nullable=False)
    materia = db.Column(db.String(50),nullable=False)
    observacoes = db.Column(db.String(150),nullable=False)
    
    def __init__(self,id,nome,idade,materia,observacoes):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.materia = materia
        self.observacoes = observacoes

    def to_dicionario(self):
        return {'id':self.id,'nome':self.nome,'idade':self.idade,'materia':self.materia,'observacoes':self.observacoes}

class DocenteNaoEncontrado(Exception):
    pass

def buscar_docente(id):
    docente = Docente.query.get(id)
    if not docente:
        raise DocenteNaoEncontrado
    return docente.to_dicionario()

def listar_docentes():
    docentes = Docente.query.all()
    print(docentes)
    return[docente.to_dicionario() for docente in docentes]
    
def adicionar_docente(novos_dados):
    novo_docente = Docente(id=novos_dados['id'],nome=novos_dados['nome'],idade=novos_dados['idade'],materia=novos_dados['materia'],observacoes=novos_dados['observacoes'])
    db.session.add(novo_docente)
    db.session.commit()
    return {'Mensagem':'Docente Adicionado !!'},201

def atualizar_docente(id,dados):
    docente = Docente.query.get(id)
    if not docente:
        raise DocenteNaoEncontrado
    docente.id = dados['id']
    docente.nome = dados['nome']
    docente.idade = dados['idade']
    docente.materia = dados['materia']
    docente.observacoes = dados['observacoes']
    db.session.commit()
    return {'Menssagem':'Docente atualizado(a)!!'},201

def deletar_docente(id):
    docente = Docente.query.get(id)
    if not docente:
        raise DocenteNaoEncontrado
    db.session.delete(docente)
    db.session.commit()
    return {'Mensagem':'Docente deletado(a)!!'},200

def limpar_docentes():
    docentes = Docente.query.all()
    for docente in docentes:
        db.session.delete(docente)
        db.session.commit()
        return {},200
        

