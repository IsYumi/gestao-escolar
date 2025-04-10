import os
from config import app
from views.aluno_view import aluno_blueprint
from views.docente_view import docentes_blueprint
from views.turma_view import turmas_blueprint
from flask import Flask

app = Flask(__name__)

app.register_blueprint(aluno_blueprint)
app.register_blueprint(docentes_blueprint)
app.register_blueprint(turmas_blueprint)

if __name__ == '__main__':
    app.run(debug=True)



