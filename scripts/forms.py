from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from scripts.models import Usuario, Post

# Formulário login
class FormLogin(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8)])
    botao_submit = SubmitField('Confirmar')

    def validate_email(self, email):
        user = Usuario.query.filter_by(e_mail=email.data).first()
        if not user:
            ValidationError('Email não encontrado, faça o cadastro!')


# Formulário cadastro
class FormCadastro(FlaskForm):
    email = StringField('Email', validators=[Email(), DataRequired()])
    username = StringField('Usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8,16)])
    senha_confirm = PasswordField('Senha', validators=[EqualTo('senha')])
    botao_submit = SubmitField('Confirmar')

    def validate_username(self, username):
        user = Usuario.query.filter_by(user_name=username).first()
        if user:
            ValidationError('Usuário já existente!')
    
    def validate_email(self, email):
        user = Usuario.query.filter_by(e_mail=email.data).first()
        if user:
            ValidationError('Email já cadastrado, faça o login!')