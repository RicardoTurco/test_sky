from flask_restplus import Resource, Namespace
from .serializers import user, create_user
from .models import Users


api = Namespace('users', 'Users Endpoint')


@api.route('')
class UserList(Resource):

    @api.marshal_list_with(user)
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


@api.route('/email/<string:email>')
class UserEmail(Resource):

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

        Users.insert_user(api.payload)
        return {"mensagem": "User created"}, 201
