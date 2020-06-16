from flask import Blueprint
from flask_restplus import Api


v1_blueprint = Blueprint('v1', __name__, url_prefix='/api/v1')

authorizations = {
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
}

api = Api(v1_blueprint,
          doc='/docs',
          title='Test for evaluating API development (SKY).',
          version='1.0',
          description='Test for evaluating API development (SKY).',
          security='Bearer Auth',
          authorizations=authorizations)
