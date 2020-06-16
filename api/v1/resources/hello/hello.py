from flask_restplus import Resource, Namespace


api = Namespace('hello', 'Hello Endpoint')


@api.route('/')
class Hello(Resource):


    def get(self):
        """
        Return msg "This is Test to evaluate the development of an API (SKY)."
        """
        return {"mensagem": "This is Test to evaluate the development of an API (SKY)."}, 200
