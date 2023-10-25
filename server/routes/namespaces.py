
# Copyright (c) 2023 Jakub Więckowski

from flask_restx import Namespace

# instead of @api.route => @ns.route
v1 = Namespace('api/v1', description='REST API v1 endpoints for Multi-Criteria Decision Analysis evaluations and graphical tool for modelling decision models structures')
