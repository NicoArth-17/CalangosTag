from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
import os

# Criar aplicação
app = Flask(__name__)

# Banco de dados
    # Se estiver Online (deploy pelo render)
if os.getenv("DEBUG") == 0:
    link_sql = os.getenv("DATABASE_URL")

    # Se estiver Local (para modificações)
else:
    link_sql = 'sqlite:///comunidade.db'

    # Setando link do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = link_sql

    # Base de dados
database = SQLAlchemy(app)

# Cryptografia
app.config['SECRET_KEY'] = 'c288f19ad5eeb35fcebfefc1c47e1f48'
bcrypt = Bcrypt(app)

# Login
login_gerenciador = LoginManager(app)
login_gerenciador.login_view = 'home'

# Upload de posts
app.config['UPLOAD_FOLDER'] = 'static/img_posts'

# Email de confirmação
# app.config['MAIL_SERVER']: 'localhost'
app.config['MAIL_PORT'] : 25
app.config['MAIL_USE_TLS'] : False
app.config['MAIL_USE_SSL'] : True
app.config['MAIL_DEBUG'] : 
app.config['MAIL_USERNAME'] : 
app.config['MAIL_PASSWORD'] : 
app.config['MAIL_DEFAULT_SENDER'] : None
app.config['MAIL_MAX_EMAILS'] : None
app.config['MAIL_SUPPRESS_SEND'] : True
app.config['MAIL_ASCII_ATTACHMENTS'] : False

mail = Mail(app)

# Importar rotas por último
from scripts import routes