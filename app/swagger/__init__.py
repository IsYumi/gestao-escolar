from flask_restx import Api

api = Api(
    version='1.0',
    title='Api de Gerenciamento Escolar',
    description='Documentação de uma API para alunos,docentes e turmas',
    doc='/docs',
    mask_swagger=False,
    prefix='/api'
    )
