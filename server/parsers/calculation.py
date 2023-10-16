from flask_restx import reqparse

def get_calculation_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)
    parser.add_argument('matrix',  required=True, type=list, action='append')
    parser.add_argument('extensions',  required=True, type=str, action='append')
    parser.add_argument('types',  required=True, type=list, action='append')
    parser.add_argument('method',  required=True, type=list, action='append')
    parser.add_argument('methodCorrelations',  required=False, type=list, action='append')
    parser.add_argument('methodRankings',  required=False, type=list, action='append')
    parser.add_argument('rankingCorrelations',  required=False, type=list, action='append')
    parser.add_argument('params',  required=True, type=list, action='append')

    return parser