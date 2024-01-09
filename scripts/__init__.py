from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

# Criar aplicação
app = Flask(__name__)

# Banco de dados
    # Local armazenado
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
    # Base de dados
database = SQLAlchemy(app)

# Cryptografia
app.config['SECRET_KEY'] = 'c288f19ad5eeb35fcebfefc1c47e1f48'
bcrypt = Bcrypt(app)

# Login
login_gerenciador = LoginManager(app)
login_gerenciador.login_view = 'home'

from scripts import routes