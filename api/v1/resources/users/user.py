import datetime
from flask_restplus import Resource, Namespace
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_jwt_claims, create_access_token
from .serializers import user, user_list, create_user, user_signin, update_user, acc_token
from .models import Users

from api.helpers import check_password, refresh_parser


api = Namespace('users', 'Users Endpoint')


@api.route('')
class UserList(Resource):

    @jwt_required
    @api.marshal_list_with(user_list)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        500: 'Internal Server Error'})
    def get(self):
        """
        Get all Users
        """
        return Users.get_all_users(), 200


@api.route('/id/<string:id>')
class UserId(Resource):

    @jwt_required
    @api.marshal_with(user)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'User not found',
        500: 'Internal Server Error'
    }, params={'id': 'User ID'})
    def get(self, id):
        """
        Get User by ID
        """
        user = Users.get_user_id(id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @jwt_required
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'User not found',
        500: 'Internal Server Error'
    }, params={'id': 'User ID'})
    def delete(self, id):
        """
        Delete User by ID
        """
        user = Users.get_user_id(id)
        if not user:
            api.abort(404, 'User not found')

        Users.delete_user(id)
        return {"mensagem": "User deleted."}, 200

    @jwt_required
    @api.expect(update_user)
    @api.doc(responses={
        200: 'OK',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        404: 'User not found',
        422: 'No user updated',
        500: 'Internal Server Error'
    }, params={'id': 'User ID'})
    def put(self, id):
        """
        Updates the user
        """
        user = Users.get_user_id(id)
        if not user:
            api.abort(404, 'User not found')

        Users.update_user(id, api.payload)
        return {"mensagem": "User Updated."}, 200


@api.route('/email/<string:email>')
class UserEmail(Resource):

    @jwt_required
    @api.marshal_with(user)
    @api.doc(responses={
        200: 'OK',
        401: 'Unauthorized',
        404: 'User not found',
        500: 'Internal Server Error'
    }, params={'email': 'User EMAIL'})
    def get(self, email):
        """
        Get User by EMAIL
        """
        user = Users.get_user_email(email)
        if not user:
            api.abort(404, 'User not found')
        return user, 200


@api.route('/sign-up')
class UserSignUp(Resource):

    @api.expect(create_user)
    @api.doc(responses={
        201: 'Created',
        400: 'Input payload validation failed',
        401: 'Unauthorized',
        409: 'E-mail já existente',
        422: 'Cannot create User',
        500: 'Internal Server Error'})
    def post(self):
        """
        Creates a new User
        """
        # Verify if exists a USER with same "email" ...
        user = Users.get_user_email(api.payload.get('email'))
        if user:
            api.abort(409, 'E-mail já existente')

        user_ins = Users.insert_user(api.payload)
        return user_ins, 201


@api.route('/sign-in')
class UserSignIn(Resource):

    @api.expect(user_signin)
    @api.marshal_with(user)
    @api.doc(responses={
        200: 'Success',
        400: 'Email or Senha is a required property',
        401: 'Unauthorized',
        404: 'Usuário e/ou senha inválidos.'
    }, security=None)
    def post(self):
        """
        Authentication endpoint
        """
        email = api.payload.get('email')
        senha = api.payload.get('senha')

        user = Users.get_user_email(email)

        if not user:
            api.abort(404, 'Usuário e/ou senha inválidos.')

        if not check_password(senha, user.get('senha')):
            api.abort(401, 'Unauthorized')

        return user, 200


@api.route('/refresh-token')
class TokenRefresh(Resource):

    @jwt_refresh_token_required
    @api.expect(refresh_parser)
    @api.doc(responses={
        424: 'Invalid refresh token'
    }, security=None)
    @api.response(200, 'Sucess', acc_token)
    def post(self):
        """
        Retrieve Access Token using Refresh Token
        """
        claims = get_jwt_claims()
        claims['user'] = get_jwt_identity()

        expires = datetime.timedelta(days=1)
        access_token = create_access_token(identity=claims, expires_delta=expires)

        Users.update_access_token(claims['user']['iduser'], access_token)
        return {'access_token': access_token}
