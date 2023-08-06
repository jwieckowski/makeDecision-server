# Copyright (c) 2023 Jakub Więckowski

from flask import Flask
from flask_restx import fields, Resource, Api, reqparse
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask_cors import CORS
import numpy as np
import json
import logging

# UTILS
from utilities.interface import Calculations
from utilities.validator import Validator 
from utilities.files import Files

# ERROR CODES
from utilities.errors import get_error_message

# configure root logger
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True

api = Api(app, 
    version='1.0.0',
    title='MakeDecision.it calculation server',
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
ns = api.namespace('api/v1', description='REST API v1 endpoints for Multi-Criteria Decision Analysis evaluations and graphical tool for modelling decision models structures')

# MODELS
dictionary_additional_data_item_model = api.model("AdditionalDataItem", {
    "id": fields.Integer(description='Element id'),
    "method": fields.String(description="Name of technique used in Multi-Criteria Decision Analysis method for additional measures"),
    "parameter": fields.String(description='Name of parameter used in evaluations package in Python'),
    "default": fields.String(description='Default technique used in Multi-Criteria Decision Analysis method calculation for given parameter')
})

dictionary_additional_data_model = api.model("AdditionalData", {
    "extension": fields.String(description="Data type representation"),
    "data": fields.List(fields.Nested(dictionary_additional_data_item_model, skip_none=True))
})

dictionary_data_model = api.model('DictionaryData', {
    "id": fields.Integer(description='Element id'),
    "type": fields.String(description='Type of method'),
    "label": fields.String(description='Label representing the variant of method used for visualization purposes'),
    "name": fields.String(description='Name of method variant'),
    "abbreviation": fields.String(description='Full name of the method'),
    "extensions": fields.List(fields.String(description="Data type representation")),
    "formats": fields.List(fields.String(description="Accepted data formats")),
    "order": fields.String(description="Order for ranking calculation"),
    "functionName": fields.String(description="Name of parameter used in evaluations package in Pythonn"),
    "requiredData": fields.List(fields.String(description='Required data needed for block usage')),
    "additional": fields.List(fields.Nested(dictionary_additional_data_model, skip_none=True)),
    "hints": fields.String(description="Hints for user about how to use given method")
})

dictionary_model = api.model('Dictionary', {
    'id': fields.Integer(description='Element id'),
    "key": fields.String(description="Name of the method categories"),
    "label": fields.String(description="Label representing the variant of method categories used for visualization purposes"),
    "type": fields.String(description="Type of method category"),
    "inputConnections": fields.List(fields.String(description="List of methods type that can be used as the input data for the element")),
    "outputConnections": fields.List(fields.String(description="List of methods type that can be used as the output data for the element")),
    "data": fields.List(fields.Nested(dictionary_data_model, skip_none=True))
})

description_item = api.model('Description', {
    'id': fields.Integer(description='Element id'),
    'text': fields.String(description="Description content")
})

method_data_item = api.model('MethodData', {
    "id": fields.Integer(description='Element id'),
    "name": fields.String(description="Name of the method"),
    "description": fields.List(fields.Nested(description_item))
})

methods_description_item = api.model('MethodsDescription', {
    "id": fields.Integer(description='Element id'),
    "key": fields.String(description="Name of the method categories"),
    "data": fields.List(fields.Nested(method_data_item))
})


# ARGUMENTS PARSERS
locale_parser = reqparse.RequestParser()
locale_parser.add_argument('locale', location='headers', required=True)

matrix_parser = reqparse.RequestParser()
matrix_parser.add_argument('locale', location='headers', required=True)
matrix_parser.add_argument('matrix', type=FileStorage, location='files', required=True)
matrix_parser.add_argument('extension', type=str, location='form', required=True)

calculation_parser = reqparse.RequestParser()
calculation_parser.add_argument('locale', location='headers', required=True)
calculation_parser.add_argument('matrix',  required=True, type=list, action='append')
calculation_parser.add_argument('extensions',  required=True, type=str, action='append')
calculation_parser.add_argument('types',  required=True, type=list, action='append')
calculation_parser.add_argument('method',  required=True, type=list, action='append')
calculation_parser.add_argument('methodCorrelations',  required=False, type=list, action='append')
calculation_parser.add_argument('methodRankings',  required=False, type=list, action='append')
calculation_parser.add_argument('rankingCorrelations',  required=False, type=list, action='append')
calculation_parser.add_argument('params',  required=True, type=list, action='append')

# ROUTES
@ns.route('/dictionary/all-methods')
class AllMethodsDictionary(Resource):
    @ns.expect(locale_parser)
    @ns.marshal_with(dictionary_model)
    def get(self):
        args = locale_parser.parse_args()
        locale = validate_locale(args['locale'])
        with open(project_home+f'public/dictionary/all-methods-{locale}.json',  encoding='utf-8') as file:
            data = json.load(file)
        # filtering keys
        filters = ['Visualization', 'Preference function']
        data = [d for d in data if d['key'] not in filters]
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
        locale = validate_locale(args['locale'])

        matrix = args['matrix']
        extension = args['extension']
        filename = secure_filename(matrix.filename)

        items = filename.split('.')
        try:
            m, ct = Files.read_matrix_from_file(locale, matrix, items[-1], extension)

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
        locale = validate_locale(args['locale'])
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

        if len(np.unique([len(matrixes), len(extensions), len(types)])) != 1:
            ns.logger.info(f'{get_error_message(locale, "matrix-criteria-extensions-shapes-mismatch")}')
            e = BadRequest(f'{get_error_message(locale, "matrix-criteria-extensions-shapes-mismatch")}')
            raise e

        
        # check if need to generate random matrix or convert input matrix
        for idx, (m, ext) in enumerate(zip(matrixes, extensions)):
            if np.array(m).shape[0] == 0:
                ns.logger.info(f'{get_error_message(locale, "empty-matrix")}')
                e = BadRequest(f'{get_error_message(locale, "empty-matrix")}')
                raise e
                
            try:
                # random
                if np.array(m).ndim == 1 and len(m) == 2:
                    calculationMatrixes.append(Calculations.generate_random_matrix(locale, m[0], m[1], ext))
                    calculationTypes.append(types[idx])
                # input
                else:

                    # fuzzy
                    if isinstance(m[0][0], str):
                        fuzzy_matrix = [[[float(c.replace(',', '')) for c in col.split(',')] for col in row] for row in m]
                        calculationMatrixes.append(np.array(fuzzy_matrix, dtype=float))
                    # crisp
                    else:
                        calculationMatrixes.append(np.array(m, dtype=float))
                    
                    try:
                        Validator.validate_matrix(locale, calculationMatrixes[-1], ext)
                    except Exception as err:
                        raise ValueError(err)

                    try:
                        Validator.validate_types(locale, types[idx])
                    except Exception as err:
                        raise ValueError(err)

                    try:
                        Validator.validate_dimensions(locale, calculationMatrixes[-1], types[idx])
                    except Exception as err:
                        raise ValueError(err)

                    calculationTypes.append(types[idx])

            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e


        # verification of input data
        for m, ext in zip(calculationMatrixes, extensions):
            try:
                Validator.validate_matrix(locale, m, ext)
            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e

        for m, t in zip(calculationMatrixes, calculationTypes):
            try:
                Validator.validate_types(locale, t)
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
                Validator.validate_dimensions(locale, m, t)
            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e


        results = {
            'matrices': [], 
            'method': [],
            'methodCorrelations': [],
            'methodRankings': [],
            'rankingCorrelations': [],
        }

        if len(method) == 0:
            ns.logger.info(f'{get_error_message(locale, "no-assessment-method-error")} : {err}')
            e = BadRequest(str(err))
            raise e

        try:
            # return matrices
            results['matrices'] = [m.tolist() for m in calculationMatrixes]

            # MCDA evaluation
            try:
                results['method'] = Calculations.calculate_preferences(locale, calculationMatrixes, extensions, calculationTypes, method, params)
            except Exception as err:
                ns.logger.info(str(err))
                e = BadRequest(str(err))
                raise e
                
            # MCDA preferences correlation
            if methodCorrelations is not None and len(methodCorrelations) > 0:
                try:
                    results['methodCorrelations'] = Calculations.calculate_preference_correlations(locale, methodCorrelations, results['method'])
                except Exception as err:
                    ns.logger.info(str(err))
                    e = BadRequest(str(err))
                    raise e

            # MCDA ranking calculation
            if methodRankings is not None and len(methodRankings) > 0:
                try:
                    results['methodRankings'] = Calculations.calculate_ranking(locale, methodRankings, results['method'])
                except Exception as err:
                    ns.logger.info(str(err))
                    e = BadRequest(str(err))
                    raise e
                
            # MCDA ranking correlation
            if rankingCorrelations is not None and  len(rankingCorrelations) > 0:
                try:
                    results['rankingCorrelations'] = Calculations.calculate_ranking_correlations(locale, rankingCorrelations, results['methodRankings'])
                except Exception as err:
                    ns.logger.info(str(err))
                    e = BadRequest(str(err))
                    raise e
                
            return results
        except Exception as err:
            ns.logger.info(f'{get_error_message(locale, "assessment-error")}  {err}')
            e = BadRequest(str(err))
            raise e

if __name__ == '__main__':
    app.run(debug=True)