from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from flask_mail import Mail, Message

app = Flask(__name__)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'falajusta@gmail.com'  # Seu e-mail
# app.config['MAIL_PASSWORD'] = '12345@abcde' # Senha do e-mail
app.config['MAIL_PASSWORD'] = 'fatsavonwkuvcidekk'
# app.config['MAIL_DEFAULT_SENDER'] = 'seu_email@gmail.com'

mail = Mail(app)

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
        mnsg = Message("Fala justa de" + email, sender = 'pedrovelosoj5@gmail.com',
                       recipients=['falajusta@gmail.com'])
        mnsg.body = denuncia_texto
        mail.send(mnsg)
        return "sent email" 
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
