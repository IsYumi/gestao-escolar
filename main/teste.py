from flask import Flask, request, abort, url_for, redirect, render_template, jsonify
import unittest
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

# 1º tratamento - Acesso restrito 401
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect(url_for('sucesso'), code=200)  # Redireciona para a página de sucesso
        else:
            abort(401) 
    else:
        abort(403) 

# 2º Tratamento - Se username e password == admin, retorna a mensagem de sucesso mas não vai diretamente
# porque não possui o status não é 302, e sim 200.
@app.route('/sucesso')
def sucesso():
    return 'Login realizado com sucesso!'

# 3º Tratamento - Se username e password errados
@app.errorhandler(401)
def unauthorized_error(error):
    return "Erro 401: Credenciais incorretas. Tente novamente.", 401

@app.errorhandler(403)
def forbidden_error(error):
    return "Erro 403: Acesso proibido. Você deve usar o método POST.", 403

# 4º Tratamento - Erro interno no servidor 500
@app.errorhandler(500)
def internal_server_error(error):
    return "Ocorreu um erro interno em nosso servidor!. Tente novamento após alguns minutos.", 500

@app.route('/forcar_erro_500')
def forcar_erro_500():
    try:
        result = 1 / 0  # Isso causará um erro 500
    except ZeroDivisionError as erro:
        abort(500)

# 5º Tratamento - Recurso não encontrado 404
@app.errorhandler(404)
def nao_encontrado(error):
    return jsonify({"erro": "A página acessada não foi encontrado"}), 404

# 6º Tratamento - Método não permitido 405
@app.errorhandler(405)
def method_not_allowed_error(error):
    return jsonify({"erro": "Método não permitido para esta rota!"}), 405

# 7º Tratamento - Requisição malformada 400
@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"erro": "A requisição está incorreta! Verifique os dados fornecidos."}), 400

# 8º Tratamento - Erro interno no servidor 500
@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({"erro": "Houve um erro interno! Volte mais tarde."}), 500

# 9º Tratamento - Entidade não processável 422
@app.errorhandler(422)
def unprocessable_entity_error(error):
    return jsonify({"erro": "Os dados fornecidos são inválidos ou não podem ser processados."}), 422

if __name__ == "__main__":
    app.run(debug=True)