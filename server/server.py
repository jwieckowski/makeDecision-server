# Copyright (c) 2023 Jakub Więckowski

from flask import Flask
from flask_cors import CORS
import logging

# routes
from routes import api

# configure root logger
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

# ROUTES
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
