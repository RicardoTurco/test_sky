from api.v1 import api
from flask_restplus import fields


user_list = api.model('User', {
    'iduser': fields.String(readonly=True, description='ID of User'),
    'nome': fields.String(readonly=True, description='Nome of User'),
    'email': fields.String(readonly=True, description='Email of User'),
    'telefone': fields.String(readonly=True, description='Telefone of User'),
    'data_criacao': fields.Date(readonly=True, description='Dt.Criacao of User'),
    'data_atualizacao': fields.Date(readonly=True, description='Dt.Atualizacao of User'),
    'ultimo_login': fields.Date(readonly=True, description='Dt.Ultimo Login of User')
})

user = api.model('User', {
    'iduser': fields.String(readonly=True, description='ID of User'),
    'nome': fields.String(readonly=True, description='Nome of User'),
    'email': fields.String(readonly=True, description='Email of User'),
    'telefone': fields.String(readonly=True, description='Telefone of User'),
    'data_criacao': fields.Date(readonly=True, description='Dt.Criacao of User'),
    'data_atualizacao': fields.Date(readonly=True, description='Dt.Atualizacao of User'),
    'ultimo_login': fields.Date(readonly=True, description='Dt.Ultimo Login of User'),
    'access_token': fields.String(readonly=True, description='Access_token of User'),
    'refresh_token': fields.String(readonly=True, description='Refrersh_token of User')
})

create_user = api.model('User', {
    'nome': fields.String(readonly=True, description='Nome of User'),
    'email': fields.String(readonly=True, description='Email of User'),
    'senha': fields.String(readonly=True, description='Senha of User'),
    'telefone': fields.String(readonly=True, description='Telefone of User')
})

update_user = api.model('User', {
    'nome': fields.String(readonly=True, description='Nome of User'),
    'email': fields.String(readonly=True, description='Email of User'),
    'telefone': fields.String(readonly=True, description='Telefone of User')
})

user_signin = api.model('SignIn', {
    'email': fields.String(readonly=True, description='Email of User'),
    'senha': fields.String(readonly=True, description='Senha of User')
})

acc_token = api.model('JWT Access Token', {
    'access_token': fields.String(description='Access Token')
})
