from . import api
from ..swagger.namespaces.namespace_aluno import aluno_ns
from ..swagger.namespaces.namespace_docente import docente_ns
from ..swagger.namespaces.namespace_turma import turma_ns

def configure_swagger(app):
    api.init_app(app)
    api.add_namespace(aluno_ns,path='/alunos')
    api.add_namespace(docente_ns,path='/docentes')
    api.add_namespace(turma_ns,path='/turmas')
    api.mask_swagger = False