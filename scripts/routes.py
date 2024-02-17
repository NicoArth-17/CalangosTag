from scripts import app, bcrypt, database
from flask import render_template, url_for, redirect, session
from flask_login import login_required, login_user, logout_user, current_user
from scripts.models import Usuario, Post
from scripts.forms import FormLogin, FormCadastro, FormPost
import os
from werkzeug.utils import secure_filename
import uuid
from email.message import EmailMessage
import smtplib
import yagmail

# Back-end da página home
@app.route('/', methods=['GET', 'POST'])
def home():

    form_login = FormLogin()

    # Se as informações do formulário de login forem enviadas
    if form_login.validate_on_submit():

        # Encontrando Usuário cadastrado no banco de dados pelo email inserido no formulário de login
        User = Usuario.query.filter_by(e_mail=form_login.email.data).first()

        # Se o Usuário for encontrado e senha for verificada
        if User and bcrypt.check_password_hash(User.password, form_login.senha.data):

            # Fazendo login
            login_user(User, remember=True)

            # Direcionar página de perfil
            return redirect(url_for('page_perfil', usuarioX=User.user_name))

    # Retornando a página home
    return render_template('home.html', formPy=form_login)


# Back-end da página de cadastro
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():

    form_cadastro = FormCadastro()

    # Se as informações do formulário de cadastro forem enviadas
    if form_cadastro.validate_on_submit():

        # Senha cryptografada
        senha_crypt = bcrypt.generate_password_hash(form_cadastro.senha.data)

        # Conferindo email válido
            # Token acossiado ao link de confirmação
        Token = str(uuid.uuid4())

            # Link de confirmação completo
        link = url_for('email_confirm', token=Token, form_cadastro=form_cadastro,
                       senha_crypt=senha_crypt, _external=True)

            # Enviar email
        # msg = EmailMessage()
        # msg.set_content(f'Hey hey Calango(a), acesse o link para finalizar seu cadastro: {link}')
        # msg['Subject'] = 'Confirme seu cadastro'
        # msg['From'] = 'nicoartur17@gmail.com'
        # msg['To'] = form_cadastro.email.data

            # Servidor email
        yag = yagmail.SMTP('nicoartur17@gmail.com', oauth2_file='OAuth2_Email/credencial.json')

            # Enviar email
        yag.send(to=form_cadastro.email.data, 
                 subject='Confirme seu cadastro', 
                 contents=f'Hey hey Calango(a), acesse o link para finalizar seu cadastro:{link}')

        # with smtplib.SMTP('smtp.gamil.com', 587, timeout=60) as smtp:
        #     smtp.starttls()
        #     smtp.login('nicoartur17@gmail.com', 'peai jubc agzu nfis')
        #     smtp.send_message(msg)

            # Salvar token para verificar posteriormente
        session['token'] = Token
        session['email'] = form_cadastro.email.data

        return redirect(url_for('home'))

    # Retornando a página de cadastro
    return render_template('cadastro.html', formPy=form_cadastro)

@app.route('/cadastro/confirmar-email/<token>', methods=['GET', 'POST'])
def email_confirm(token, form_cadastro, senha_crypt):

    # Verificar se o token na sessão é igual ao token na url
    if 'token' in session and session['token'] == token:

        # Recuperar token e o email da sessão
        token = session.pop('token')

        # Completar cadastro
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
    
    else:
        return '<h1>Link de confirmação inválido!</h1>'


# Back-end da página de perfil
@app.route('/perfil/<usuarioX>', methods=['GET', 'POST'])
@login_required
def page_perfil(usuarioX):

    form_post = FormPost()

    # Verificando se o usuário está no próprio perfil
    if usuarioX == current_user.user_name:

        # Verificando envio do formulário de post
        if form_post.validate_on_submit():

            # Criando um nome seguro para o arquivo
            arquivo = form_post.imagem.data
            nome_arquivo_seguro = secure_filename(arquivo.filename)

            # Direcionando local de salvamento
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                              app.config['UPLOAD_FOLDER'],
                              nome_arquivo_seguro)
            
            # Salvando arquivo
            arquivo.save(caminho)

            # Registrando nome do arquivo no banco de dados
            img = Post(imagem=nome_arquivo_seguro, id_usuario=current_user.id)
            database.session.add(img)
            database.session.commit()

        # Retornar página do próprio perfil
        return render_template('perfil.html', usuario=current_user, formPy=form_post)
    
    # Caso o usuário esteja em outro perfil
    else:
        User = Usuario.query.filter_by(user_name=usuarioX).first()
        
        # Se existir a user_name deste outro usuário, retornar o perfil dele
        if User:
            return render_template('perfil.html', usuario=User, formPy = None)
        
        # Se não existir a user_name deste outro usuário, fazer logout e retornar a página home
        else:
            return redirect(url_for('sair'))


# Back-end da página de feed
@app.route('/feed')
@login_required
def timeline():

    # Buscando todas as fotos no banco de dados e ordeando pela data de criação de forma decrescente
    imagens = Post.query.order_by(Post.data_criacao.desc()).all()
    
    # Retornar a página de feed
    return render_template('feed.html', imgs=imagens)

# Função de logout
@app.route('/logout')
@login_required
def sair():

    # Deslogar
    logout_user()

    # Retornando pra página home
    return redirect(url_for('home'))