from scripts import database, login_gerenciador
from datetime import datetime
from flask_login import UserMixin

# Decorator e function obrigatórios para utilizar LoginManager()
@login_gerenciador.user_loader
def load_user(id_user):
    return Usuario.query.get(int(id_user))

# Tabela de Usuário para o banco de dados
class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    user_name = database.Column(database.String, nullable=False, unique=True)
    e_mail = database.Column(database.String, nullable=False, unique=True)
    password = database.Column(database.String, nullable=False)
    posts = database.relationship('Post', backref='usuario', lazy=True)

# Tabela de Posts para o banco de dados
class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default='default.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)