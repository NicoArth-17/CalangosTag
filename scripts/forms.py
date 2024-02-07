from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from scripts.models import Usuario, Post

# Formulário login
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8)])
    botao_submit = SubmitField('Entrar')

    # Validação com mensagem de erro caso email inserido não seja encontrado no banco de dados
    def validate_email(self, email):
        user = Usuario.query.filter_by(e_mail=email.data).first()
        if not user:
            raise ValidationError('Email não encontrado, faça o cadastro!')


# Formulário cadastro
class FormCadastro(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    username = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8,16)])
    senha_confirm = PasswordField('Senha', validators=[EqualTo('senha')])
    botao_submit = SubmitField('Confirmar')

    # Validação com mensagem de erro caso username inserido já esteja no banco de dados
    def validate_username(self, username):
        user = Usuario.query.filter_by(user_name=username.data).first()
        if user:
            raise ValidationError('Usuário já existente!')

    # Validação com mensagem de erro caso email inserido já esteja no banco de dados
    def validate_email(self, email):
        user = Usuario.query.filter_by(e_mail=email.data).first()
        if user:
            raise ValidationError('Email já cadastrado, faça o login!')


# Formulário post
class FormPost(FlaskForm):
    imagem = FileField('Adicionar imagem', validators=[DataRequired()])
    botao_submit = SubmitField('Enviar')