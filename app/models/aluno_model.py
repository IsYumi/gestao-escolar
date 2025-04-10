from flask import Flask, jsonify, request

app = Flask(__name__)

alunos = [
    {
        'id': 1,
        'nome': 'João',
        'idade': 18,
        'turma_id': 101,
        'data_nascimento': '2007-03-15',
        'nota_primeiro_semestre': 7.5,
        'nota_segundo_semestre': 8.0,
        'media_final': 7.75
    },
    {
        'id': 2,
        'nome': 'Maria',
        'idade': 17,
        'turma_id': 102, 
        'nota_primeiro_semestre': 8.0,
        'nota_segundo_semestre': 7.5,
        'media_final': 7.75
    },
    {
        'id': 3,
        'nome': 'José',
        'idade': 19,
        'turma_id': 103,
        'nota_primeiro_semestre': 6.0,
        'nota_segundo_semestre': 5.5,
        'media_final': 5.75
    },
    {
        'id': 4,
        'nome': 'Ana',
        'idade': 18,
        'turma_id': 104,
        'nota_primeiro_semestre': 9.0,
        'nota_segundo_semestre': 8.5,
        'media_final': 8.75
    }
]

class AlunoNaoEncontrado(Exception):
    pass

def listar_alunos():
    return alunos

def buscar_aluno(id_aluno):
    for aluno in alunos:
        if aluno['id'] == id_aluno:
            return aluno
    raise AlunoNaoEncontrado

def adicionar_aluno(dado):
    if not dado.get('nome'):
        return {'erro': 'aluno sem nome'}, 400  # "400" - Bad Request (entrada inválida)
    for aluno in alunos:
        if aluno['id'] == dado['id']:
            return {'erro': 'id ja utilizada'}, 400
    alunos.append(dado)
    return dado, 200    # "200" - OK (requisição feita com sucesso)

def atualizar_aluno(id_aluno, novo_dado):
    if 'nome' not in novo_dado:
        return {'erro': 'aluno sem nome'}, 400
    for aluno in alunos:
        if aluno['id'] == id_aluno:
            aluno['nome'] = novo_dado['nome']
            return aluno, 200
    raise AlunoNaoEncontrado

def deletar_aluno(id_aluno):
    for aluno in alunos:
        if aluno['id'] == id_aluno:
            alunos.remove(aluno)
            return {}, 200
    raise AlunoNaoEncontrado

def limpar_alunos():
    alunos.clear()
    return {}, 200