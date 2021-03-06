import uuid
import datetime
from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token
from api.helpers import encrypt_password


# Connect to 'users' collection in Firebase
def set_users():
    db = current_app.config.get('SKY_DB', None)
    users_ref = db.collection('users')
    return users_ref


def date_in(date):
    date_str = str(date) + ' 00:00:00'
    date_f = datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    return date_f


def invalid_session_user(ultimo_login):
    """
    The last access cannot have been more than 30 minutes ago ...
    """
    limit = datetime.datetime.now() - datetime.timedelta(minutes=30)

    # Formatting dates ...
    limita = datetime.datetime.strftime(limit, '%Y-%m-%d %H:%M')
    limitb = datetime.datetime.strptime(limita, '%Y-%m-%d %H:%M')
    ultimo_logina = datetime.datetime.strftime(ultimo_login, '%Y-%m-%d %H:%M')
    ultimo_loginb = datetime.datetime.strptime(ultimo_logina, '%Y-%m-%d %H:%M')

    if ultimo_loginb < limitb:
        return True
    return False


class Users:

    def __init__(self):
        pass

    @staticmethod
    def get_all_users():
        users_ref = set_users()

        all_users = [doc.to_dict() for doc in users_ref.stream()]
        return all_users

    @staticmethod
    def get_user_email(email):
        users_ref = set_users()

        userf = {}
        users = users_ref.where('email', '==', email).stream()
        for user in users:
            userf = user.to_dict()

        if not userf:
            return None
        return userf

    @staticmethod
    def get_user_id(id):
        users_ref = set_users()

        userf = {}
        users = users_ref.where('iduser', '==', id).stream()
        for user in users:
            userf = user.to_dict()

        if not userf:
            return None
        return userf

    @staticmethod
    def insert_user(user):
        users_ref = set_users()

        try:
            user['iduser'] = str(uuid.uuid4())
            user['senha'] = encrypt_password(user.get('senha', 'changeme'))
            user['data_criacao'] = date_in(datetime.datetime.now().date())
            user['data_atualizacao'] = date_in(datetime.datetime.now().date())
            user['ultimo_login'] = datetime.datetime.now()

            user_json = {
                "iduser": user.get('iduser'),
                "nome": user.get('nome'),
                "email": user.get('email'),
                "senha": user.get('senha'),
                "telefone": user.get('telefone'),
                "data_criacao": user.get('data_criacao'),
                "data_atualizacao": user.get('data_atualizacao'),
                "ultimo_login": user.get('ultimo_login')
            }

            expires = datetime.timedelta(days=1)
            access_token = create_access_token(identity=user_json, expires_delta=expires)
            user_json['access_token'] = access_token

            # Will be used to retrieve the token when it has expired ...
            refresh_token = create_refresh_token(identity=user_json, expires_delta=False)
            user_json['refresh_token'] = refresh_token

            users_ref.document(user_json['iduser']).set(user_json)

            user_json['data_criacao'] = datetime.datetime.date(user_json['data_criacao'])
            user_json['data_atualizacao'] = datetime.datetime.date(user_json['data_atualizacao'])

            user_ins_json = {
                "iduser": user_json.get('iduser'),
                "nome": user_json.get('nome'),
                "email": user_json.get('email'),
                "telefone": user_json.get('telefone'),
                "data_criacao": str(user_json.get('data_criacao')),
                "data_atualizacao": str(user_json.get('data_atualizacao')),
                "ultimo_login": datetime.datetime.strftime(user_json.get('ultimo_login'), '%Y-%m-%d %H:%M'),
                "access_token": user_json.get('access_token')
            }

            return user_ins_json
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def update_user(id, user):
        users_ref = set_users()

        try:
            user['data_atualizacao'] = date_in(datetime.datetime.now().date())

            user_json = {
                "iduser": id,
                "nome": user.get('nome'),
                "email": user.get('email'),
                "telefone": user.get('telefone'),
                "data_atualizacao": user.get('data_atualizacao')
            }
            users_ref.document(user_json['iduser']).set(user_json, merge=True)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_user(id):
        users_ref = set_users()

        users_ref.document(id).delete()

    @staticmethod
    def update_access_token(iduser, access_token):
        users_ref = set_users()

        try:
            user_json = {
                "iduser": iduser,
                "access_token": access_token
            }
            users_ref.document(user_json['iduser']).set(user_json, merge=True)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def update_ultimo_login(iduser):
        users_ref = set_users()

        try:
            user_json = {
                "iduser": iduser,
                "ultimo_login": datetime.datetime.now()
            }
            users_ref.document(user_json['iduser']).set(user_json, merge=True)
            return user_json['ultimo_login']
        except Exception as e:
            return f"An Error Ocurred: {e}"
