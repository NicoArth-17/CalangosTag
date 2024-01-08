from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Criar aplicação
app = Flask(__name__)

# Banco de dados
    # Local armazenado
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://comunidade.db'
    # Base de dados
database = SQLAlchemy(app)

from scripts import routes