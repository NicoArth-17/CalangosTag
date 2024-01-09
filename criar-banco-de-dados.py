from scripts import database, app
from scripts.models import Usuario, Post

# Criar banco de dados
with app.app_context():
    database.create_all()