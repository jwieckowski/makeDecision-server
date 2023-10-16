from flask_restx import Resource, Namespace

api = Namespace('', description='Default')

@api.route('/')
class MatrixConverter(Resource):
    def post(self):
        return {"message": "Welcome to Make-Decision.it REST API"}
