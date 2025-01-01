from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Definindo o caminho do banco de dados
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'denuncia.sqlite3')}"
db = SQLAlchemy(app)

class Denuncia(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100))
    denuncia = db.Column(db.String(10000))

    def __init__(self, email, denuncia):
        self.email = email
        self.denuncia = denuncia

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        denuncia_texto = request.form['denuncia']
        denuncia = Denuncia(email, denuncia_texto)
        db.session.add(denuncia)
        db.session.commit()
        print("Dados adicionados ao banco de dados")

    denuncia = Denuncia.query.all()
    for d in denuncia:
        print(f'ID: {d.id}, Email: {d.email}, Denúncia: {d.denuncia}')
    return render_template('index.html', denuncia=denuncia)

# Garantir que o banco de dados e as tabelas sejam criados antes de rodar o app
with app.app_context():
    db.create_all()  # Cria o banco de dados e as tabelas
    print("Banco de dados e tabelas criados com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)
