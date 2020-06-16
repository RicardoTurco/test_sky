from api.v1 import api
from flask_restplus import fields


user = api.model('User', {
    'iduser': fields.String(readonly=True, description='Nome of User'),
    'nome': fields.String(readonly=True, description='Nome of User'),
    'email': fields.String(readonly=True, description='Email of User'),
    'senha': fields.String(readonly=True, description='Senha of User'),
    'telefone': fields.String(readonly=True, description='Telefone of User')
})

create_user = api.model('User', {
    'nome': fields.String(readonly=True, description='Nome of User'),
    'email': fields.String(readonly=True, description='Email of User'),
    'senha': fields.String(readonly=True, description='Senha of User'),
    'telefone': fields.String(readonly=True, description='Telefone of User')
})
