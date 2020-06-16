import uuid
import datetime
from flask import current_app
from api.helpers import encrypt_password


# Connect to 'users' collection in Firebase
def set_users():
    db = current_app.config.get('SKY_DB', None)
    users_ref = db.collection('users')
    return users_ref


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

            user_json = {
                "iduser": user.get('iduser'),
                "nome": user.get('nome'),
                "email": user.get('email'),
                "senha": user.get('senha'),
                "telefone": user.get('telefone')
            }
            users_ref.document(user_json['iduser']).set(user_json)
        except Exception as e:
            return f"An Error Ocurred: {e}"

    @staticmethod
    def delete_user(id):
        users_ref = set_users()

        users_ref.document(id).delete()
