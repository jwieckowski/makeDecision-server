# Copyright (c) 2023 - 2024 Jakub Więckowski

from flask import Flask
from flask_cors import CORS
import logging
import matplotlib
# Agg, is a non-interactive backend that can only write to files.
matplotlib.use('agg')

# ROUTES
from routes import api

# ROOT LOGGER
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config['RESTX_VALIDATE'] = True

# ENABLE CORS
CORS(app, resources={r'/*': {'origins': '*'}})

api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
