from flask import Flask
from flask_restx import fields, Resource, Api, reqparse
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_cors import CORS, cross_origin
import numpy as np
import json
import logging

# UTILS
from utilities.interface import Calculations
from utilities.validator import Validator 
from utilities.files import Files

# configure root logger
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True

api = Api(app, 
    version='1.0',
    title='GUI MCDA server',
    description='REST API server to handle MCDA calculations',
    base_url='/',
    doc='/api/v1/documentation',
)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

project_home = '/home/jwieckowski/mysite/'
project_home = ''

def validate_locale(locale):
    valid = ['en', 'pl']
    if locale in valid:
        return locale
    return 'en'

# instead of @api.route => @ns.route
ns = api.namespace('api/v1', description='API v1 endpoints')

# MODELS
dictionary_additional_data_item_model = api.model("AdditionalDataItem", {
    "id": fields.Integer,
    "method": fields.String,
    "parameter": fields.String
})

dictionary_additional_data_model = api.model("AdditionalData", {
    "extension": fields.String,
    "data": fields.List(fields.Nested(dictionary_additional_data_item_model, skip_none=True))
})

dictionary_data_model = api.model('DictionaryData', {
    "id": fields.Integer(description='1'),
    "type": fields.String,
    "label": fields.String,
    "name": fields.String,
    "abbreviation": fields.String,
    "extensions": fields.List(fields.String),
    "formats": fields.List(fields.String),
    "order": fields.String,
    "requiredData": fields.List(fields.String),
    "additional": fields.List(fields.Nested(dictionary_additional_data_model, skip_none=True)),
    "hints": fields.String
})

dictionary_model = api.model('Dictionary', {
    'id': fields.Integer,
    "key": fields.String,
    "label": fields.String,
    "type": fields.String,
    "inputConnections": fields.List(fields.String),
    "outputConnections": fields.List(fields.String),
    "data": fields.List(fields.Nested(dictionary_data_model, skip_none=True))
})

description_item = api.model('Description', {
    'id': fields.Integer,
    'text': fields.String
})

method_data_item = api.model('MethodData', {
    "id": fields.Integer,
    "name": fields.String,
    "description": fields.List(fields.Nested(description_item))
})

methods_description_item = api.model('MethodsDescription', {
    "id": fields.Integer,
    "key": fields.String,
    "data": fields.List(fields.Nested(method_data_item))
})

# SCHEMA IS OK BUT FLASK ERROR
# matrix_data_item = api.schema_model('MatrixData', {
#     "properties": {
#         "matrix": {
#           "type": "array",
#           "items": {
#             "type": "array",
#             "items": {
#                 "type": "number"
#             }
#           }
#         },
#         "extension": {
#           "type": "string"
#         }
#     },
#     "type": "object"
# })


# ARGUMENTS PARSERS
locale_parser = reqparse.RequestParser()
locale_parser.add_argument('locale', location='headers', required=True)

matrix_parser = reqparse.RequestParser()
matrix_parser.add_argument('matrix', type=FileStorage, location='files', required=True)
matrix_parser.add_argument('extension', type=str, location='form', required=True)

calculation_parser = reqparse.RequestParser()
calculation_parser.add_argument('matrix',  required=True, type=list, action='append')
calculation_parser.add_argument('extensions',  required=True, type=str, action='append')
calculation_parser.add_argument('types',  required=True, type=list, action='append')
calculation_parser.add_argument('method',  required=True, type=list, action='append')
calculation_parser.add_argument('methodCorrelations',  required=False, type=list, action='append')
calculation_parser.add_argument('methodRankings',  required=False, type=list, action='append')
calculation_parser.add_argument('rankingCorrelations',  required=False, type=list, action='append')
calculation_parser.add_argument('params',  required=True, type=list, action='append')

# ROUTES
@api.route('/home')
class Home(Resource):
    def get(self):
        return {'message': 'Hello'}

@ns.route('/dictionary/all-methods')
class AllMethodsDictionary(Resource):
    @ns.expect(locale_parser)
    @ns.marshal_with(dictionary_model)
    def get(self):
        args = locale_parser.parse_args()
        locale = validate_locale(args['locale'])
        with open(project_home+f'public/dictionary/all-methods-{locale}.json',  encoding='utf-8') as file:
            data = json.load(file)
        return data

@ns.route('/descriptions/methods')
class MethodsDescription(Resource):
    @ns.expect(locale_parser)
    @ns.marshal_list_with(methods_description_item)
    def get(self):
        args = locale_parser.parse_args()
        locale = validate_locale(args['locale'])
        with open(project_home+f'public/descriptions/methods-{locale}.json', encoding='utf-8') as file:
            data = json.load(file)
        return data


@ns.route('/matrix')
class MatrixConverter(Resource):
    @ns.expect(matrix_parser)
    # @ns.marshal_with(matrix_data_item)
    def post(self):
        args = matrix_parser.parse_args()

        matrix = args['matrix']
        extension = args['extension']
        filename = secure_filename(matrix.filename)

        items = filename.split('.')
        try:
            m, ct = Files.read_matrix_from_file(matrix, items[-1], extension)

            return {
                "matrix": m.tolist(),
                "criteriaTypes": ct.tolist()
            }
        except Exception as err:
            ns.logger.info(str(err))
            e = BadRequest(str(err))
            raise e

@ns.route('/results')
class CalculationResults(Resource):
    @ns.expect(calculation_parser)
    # @ns.marshal_with(images_model)
    def post(self):
        args = calculation_parser.parse_args()
        matrixes = np.array([args['matrix']][0], dtype='object')
        extensions = np.array([args['extensions']][0])
        types = np.array([args['types']][0])
        method = np.array([args['method']][0], dtype='object')

        methodCorrelations = args['methodCorrelations']
        if methodCorrelations is not None:
            methodCorrelations = np.array(methodCorrelations)

        methodRankings = args['methodRankings']
        if methodRankings is not None:
            methodRankings = np.array(methodRankings)
            
        rankingCorrelations = args['rankingCorrelations']
        if rankingCorrelations is not None:
            rankingCorrelations = np.array(rankingCorrelations)

        calculationMatrixes = []
        calculationTypes = []

        # check if need to generate random matrix or convert input matrix
        for idx, (m, ext) in enumerate(zip(matrixes, extensions)):
            try:
                # random
                if np.array(m).ndim == 1 and len(m) == 2:
                    calculationMatrixes.append(Calculations.generate_random_matrix(m[0], m[1], ext))
                    calculationTypes.append(types[idx])
                # input
                else:
                    # fuzzy
                    if isinstance(m[0][0], str):
                        fuzzy_matrix = [[[float(c.replace(',', '')) for c in col.split()] for col in row] for row in m]
                        calculationMatrixes.append(np.array(fuzzy_matrix, dtype=float))
                    # crisp
                    else:
                        calculationMatrixes.append(np.array(m, dtype=float))
                    
                    calculationTypes.append(types[idx])

            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest('Something went wrong while retrieving decision matrix')
                raise e


        # verification of input data
        for m, ext in zip(calculationMatrixes, extensions):
            try:
                Validator.validate_matrix(m, ext)
            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e

        for m, t in zip(calculationMatrixes, calculationTypes):
            try:
                Validator.validate_types(t)
            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e

        # retrieve additional params for assessment
        try:
            params = np.array([args['params']][0], dtype='object')
        except:
            params = None
        
        for m, t in zip(calculationMatrixes, calculationTypes):
            try:
                Validator.validate_dimensions(m, t)
            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e


        results = {
            'matrices': [], 
            'method': [],
            'methodCorrelations': [],
            'methodRankings': [],
            'rankingCorrelations': []
        }
        if len(method) == 0:
            raise ValueError('No MCDA method was given')

        try:
            # return matrices
            results['matrices'] = [m.tolist() for m in calculationMatrixes]

            # MCDA evaluation
            try:
                results['method'] = Calculations.calculate_preferences(calculationMatrixes, extensions, calculationTypes, method, params)
            except Exception as err:
                raise ValueError(err)
                
            # MCDA preferences correlation
            if methodCorrelations is not None and len(methodCorrelations) > 0:
                try:
                    results['methodCorrelations'] = Calculations.calculate_preference_correlations(methodCorrelations, results['method'])
                except Exception as err:
                    raise ValueError(err)

            # MCDA ranking calculation
            if methodRankings is not None and len(methodRankings) > 0:
                try:
                    results['methodRankings'] = Calculations.calculate_ranking(methodRankings, results['method'])
                except Exception as err:
                    raise ValueError(err)
                
            # MCDA ranking correlation
            if rankingCorrelations is not None and  len(rankingCorrelations) > 0:
                try:
                    results['rankingCorrelations'] = Calculations.calculate_ranking_correlations(rankingCorrelations, results['methodRankings'])
                except Exception as err:
                    raise ValueError(err)
                
            return results
        except Exception as err:
            raise ValueError(f'Evaluation error: {err}')

if __name__ == '__main__':
    app.run(debug=True)