turmas = [
    {
        'id': 101,
        'descricao': 'Turma de Geografia - 1º Ano',
        'professor_id': 1,  
        'ativo': True
    },
    {
        'id': 102,
        'descricao': 'Turma de Matemática - 2º Ano',
        'professor_id': 4,  
        'ativo': True
    },
    {
        'id': 103,
        'descricao': 'Turma de Física - 3º Ano',
        'professor_id': 2,  
        'ativo': False 
    },
    {
        'id': 104,
        'descricao': 'Turma de Português - 1º Ano',
        'professor_id': 3, 
        'ativo': True
    }
]

class TurmaNaoEncontrada(Exception):
    pass

def listar_turmas():
    return turmas

def buscar_turma(id_turma):
    for turma in turmas:
        if turma['id'] == id_turma:
            return turma
    raise TurmaNaoEncontrada

def adicionar_turma(dado):
    if not dado.get('descricao'):
        return {'erro': 'turma sem descricao'}, 400 # "400" - Bad Request (entrada inválida)
    for turma in turmas:
        if turma['id'] == dado['id']:
            return {'erro': 'id ja utilizada'}, 400
    turmas.append(dado)
    return dado, 200    # "200" - OK (requisição feita com sucesso)

def atualizar_turma(id_turma, novo_dado):
    if 'descricao' not in novo_dado:
        return {'erro': 'turma sem descricao'}, 400
    for turma in turmas:
        if turma['id'] == id_turma:
            turma['descricao'] = novo_dado['descricao']
            turma['professor_id'] = novo_dado.get('professor_id', turma['professor_id'])
            turma['ativo'] = novo_dado.get('ativo', turma['ativo'])
            return turma, 200
    raise TurmaNaoEncontrada

def deletar_turma(id_turma):
    for turma in turmas:
        if turma['id'] == id_turma:
            turmas.remove(turma)
            return {}, 200
    raise TurmaNaoEncontrada

def limpar_turmas():
    turmas.clear()
    return {}, 200