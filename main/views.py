from flask import Flask, jsonify, request # importando o Flask
from flask import render_template

dici = {
    "alunos":[
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
    ],

    "professores":[
        {
            "id":1,
            "nome":"Rafael",
            "data_nascimento":"20/01/1998",
            "disciplina":"Matemática",
            "salario":3000
        },
        {
            "id":2,
            "nome":"Julia",
            "data_nascimento":"12/11/1988",
            "disciplina":"Quimica",
            "salario":10000
        },
        {
            'id': 3,
            'nome': 'Diego',
            'idade': 46,
            'materia': 'Geografia',
            "salario":10000
        },
        {
            'id': 4,
            'nome': 'Luiza',
            'idade': 55,
            'materia': 'Português',
            "salario":10000
        },
    ],

     "turmas":[
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
        },

    ],
}


app = Flask(__name__)

@app.route("/professores", methods=['GET']) #GET LISTA DE PROFESSORES
def loadProfessores():
    dados = dici['professores']
    return render_template("professores.html", professores=dados)

@app.route("/professores", methods=['POST']) #POST LISTA DE PROFESSORES
def inputProfessores():
    dados = request.json
    dici['professores'].append(dados)
    return jsonify(dados)

@app.route("/alunos", methods=['GET'])
def loadAlunos():
    dados = dici['alunos']
    return render_template("alunos.html", alunos=dados)

@app.route("/alunos", methods=['POST'])
def inputAlunos():
    dados = request.json
    dici['alunos'].append(dados)
    return jsonify(dados)

@app.route("/turmas", methods=['GET']) #GET LISTA DE TURMAS
def loadTurmas():
    dados = dici['turmas']
    return render_template("turmas.html", turmas=dados)

@app.route("/turmas", methods=['POST']) #POST LISTA DE TURMAS
def inputTurmas():
    dados = request.json
    dici['turmas'].append(dados)
    return jsonify(dados)
 
@app.route("/alunos/<int:idAluno>", methods=['GET'])
def getAluno(idAluno):
    alunos = dici['alunos']
    for aluno in alunos:
        if aluno['id'] == idAluno:
            return jsonify(aluno)
    return jsonify({"erro": "Aluno(a) não encontrado"}), 404

@app.route("/alunos/<int:idAluno>", methods=['PUT'])
def updateAluno(idAluno):
    alunos = dici['alunos']
    for aluno in alunos:
        if aluno['id'] == idAluno:
            dados = request.json
            aluno.update(dados)
            return jsonify(aluno)
    return jsonify({"erro": "Aluno(a) não encontrado"}), 404

@app.route("/alunos/<int:idAluno>", methods=['DELETE'])
def deleteAluno(idAluno):
    for aluno in dici['alunos']:
        if aluno['id'] == idAluno:
            dici['alunos'].remove(aluno)
            return jsonify({"mensagem": "Aluno(a) removido com sucesso"}), 200
    return jsonify({"erro": "Aluno não encontrado"}), 404

@app.route("/turmas/<int:idTurma>", methods=['GET']) #GET TURMA
def getTurma(idTurma):
    turmas = dici['turmas']
    for turma in turmas:
        if turma['id'] == idTurma:
            return jsonify(turma)  # Retorna a turma encontrada
    return jsonify({"erro": "Turma não encontrada"}), 404  # Caso a turma não seja encontrada

@app.route("/turmas/<int:idTurma>", methods=['PUT']) #PUT TURMA
def updateTurma(idTurma):
    for turma in dici['turmas']:
        if turma['id'] == idTurma:
            dados = request.json
            turma.update(dados)
            return jsonify(turma)  # Retorna a turma atualizada
    return jsonify({"erro": "Turma não encontrada"}), 404  # Caso a turma não seja encontrada

@app.route("/turmas/<int:idTurma>", methods=['DELETE'])
def deleteTurma(idTurma):
    for turma in dici['turmas']:
        if turma['id'] == idTurma:
            dici['turmas'].remove(turma)
            return jsonify({"mensagem": "Turma removido com sucesso"}), 200
    return jsonify({"erro": "Turma não encontrado"}), 404

@app.route("/professores/<int:idProfessor>", methods=['GET'])  # Rota para obter um professor
def getProfessor(idProfessor):
    professores = dici['professores']
    for professor in professores:
        if professor['id'] == idProfessor:
            return jsonify(professor)  # Retorna o professor específico em formato JSON
    return jsonify({"erro": "Professor(a) não encontrado"}), 404  # Retorna erro caso o professor não seja encontrado

@app.route("/professores/<int:idProfessor>", methods=['PUT']) # PUT PROFESSOR
def updateProfessor(idProfessor):
    for professor in dici['professores']:
        if professor['id'] == idProfessor:
            dados = request.json
            professor.update(dados)  # Atualiza todos os dados com os novos valores
            return jsonify(professor)  # Retorna o objeto atualizado
    return jsonify({"erro": "Professor(a) não encontrado"}), 404  # Retorna erro se não encontrar o professor
        
@app.route("/professores/<int:idProfessor>", methods=['DELETE'])
def deleteProfessor(idProfessor):
    for professor in dici['professores']:
        if professor['id'] == idProfessor:
            dici['professores'].remove(professor)
            return jsonify({"mensagem": "Professor(a) removido com sucesso"}), 200
    return jsonify({"erro": "Professor(a) não encontrado"}), 404

if __name__=="__main__":
    app.run(debug=True)