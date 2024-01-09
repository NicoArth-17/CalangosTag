from scripts import app
from flask import render_template, url_for
from flask_login import login_required

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/perfil/<usuarioX>')
@login_required
def perfil(usuarioX):
    return render_template('perfil.html', usuario=usuarioX)