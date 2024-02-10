from flask_restx import Api

from .dictionary import api as dictionaryApi
from .descriptions import api as descriptionsApi
from .matrix import api as matrixApi
from .calculations import api as calculationsApi
from .graphs import api as graphsApi
from .statistics import api as statsApi
from .surveys import api as surveysApi

api = Api( 
    version='1.1.0',
    title='MakeDecision.it calculation server',
    description='REST API server to handle MCDA calculations',
    base_url='/',
    doc='/api/v1/documentation',
)


api.add_namespace(dictionaryApi)
api.add_namespace(descriptionsApi)
api.add_namespace(matrixApi)
api.add_namespace(calculationsApi)
api.add_namespace(graphsApi)
api.add_namespace(statsApi)
api.add_namespace(surveysApi)
