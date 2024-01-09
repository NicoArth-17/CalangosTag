from scripts import database, login_gerenciador
from datetime import datetime
from flask_login import UserMixin

@login_gerenciador.user_loader
def load_user(id_user):
    return Usuario.query.get(int(id_user))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    posts = database.relationship('Post', backref='usuario', lazy=True)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    imagem = database.Column(database.String, default='default.png')
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow())
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)