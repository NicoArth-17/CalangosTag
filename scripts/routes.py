from scripts import app, bcrypt, database
from flask import render_template, url_for, redirect
from flask_login import login_required, login_user, logout_user
from scripts.models import Usuario, Post
from scripts.forms import FormLogin, FormCadastro

# Back-end da página home
@app.route('/', methods=['GET', 'POST'])
def home():
    form_login = FormLogin()
    return render_template('home.html', formPy=form_login)

# Back-end da página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    form_cadastro = FormCadastro()

    # Se as informações do formulário de cadastro forem enviadas
    if form_cadastro.validate_on_submit():

        # Senha cryptografada
        senha_crypt = bcrypt.generate_password_hash(form_cadastro.senha.data)

        # Inserindo informações do formulário de cadastro na class/tabela Usuário
        User = Usuario(user_name = form_cadastro.username.data,
                       e_mail = form_cadastro.email.data,
                       password = senha_crypt)
        
        # Adicionado Usuario cadastrado ao banco de dados
        database.session.add(User)
        database.session.commit()

        # Logar usuário cadastrado
        login_user(User, remember=True)

        return redirect(url_for('page_perfil', usuarioX=User.user_name))

    # Retornando a página de cadastro
    return render_template('cadastro.html', formPy=form_cadastro)

# Back-end da página de perfil
@app.route('/perfil/<usuarioX>')
@login_required
def page_perfil(usuarioX):
    return render_template('perfil.html', usuario=usuarioX)