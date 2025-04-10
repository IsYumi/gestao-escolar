docentes = [
    {
        'id': 1,
        'nome': 'Diego',
        'idade': 46,
        'materia': 'Geografia',
        'observacoes': 'Tende a usar métodos interativos e debates em sala de aula.'
    },
    {
        'id': 2,
        'nome': 'Marcelo',
        'idade': 62,
        'materia': 'Física',
        'observacoes': 'Profissional com 10 anos de experiência no ensino de Física'
    },
    {
        'id': 3,
        'nome': 'Luiza',
        'idade': 55,
        'materia': 'Português',
        'observacoes': 'Excelente em gerenciar turmas e motivar os alunos.'
    },
    {
        'id': 4,
        'nome': 'Vanessa',
        'idade': 32,
        'materia': 'Matemática',
        'observacoes': 'Excelente em gerenciar turmas e motivar os alunos.'
    }
]

class DocenteNaoEncontrado(Exception):
    pass

def listar_docentes():
    return docentes

def buscar_docente(id_docente):
    for docente in docentes:
        if docente['id'] == id_docente:
            return docente
    raise DocenteNaoEncontrado

def adicionar_docente(dado):
    if not dado.get('nome'):
        return {'erro': 'docente sem nome'}, 400    # "400" - Bad Request (entrada inválida)
    for docente in docentes:
        if docente['id'] == dado['id']:
            return {'erro': 'id ja utilizada'}, 400
    docentes.append(dado)
    return dado, 200    # "200" - OK (requisição feita com sucesso)

def atualizar_docente(id_docente, novo_dado):
    if 'nome' not in novo_dado:
        return {'erro': 'docente sem nome'}, 400
    for docente in docentes:
        if docente['id'] == id_docente:
            docente['nome'] = novo_dado['nome']
            docente['idade'] = novo_dado.get('idade', docente['idade'])
            docente['materia'] = novo_dado.get('materia', docente['materia'])
            docente['observacoes'] = novo_dado.get('observacoes', docente['observacoes'])
            return docente, 200
    raise DocenteNaoEncontrado

def deletar_docente(id_docente):
    for docente in docentes:
        if docente['id'] == id_docente:
            docentes.remove(docente)
            return {}, 200
    raise DocenteNaoEncontrado

def limpar_docentes():
    docentes.clear()
    return {}, 200