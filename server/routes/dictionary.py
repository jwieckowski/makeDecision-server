from flask import request, jsonify
from __main__ import app
from __main__ import project_home

from helpers import get_locale

# DICTIONARIES
@app.route('/api/v1/dictionary/all-methods', methods=['GET'])
def dictionary_all_methods():
    locale = get_locale(request)
    with open(project_home+f'public/dictionary/all-methods-{locale}.json',  encoding='utf-8') as file:
        data = file.read()
    return data

@app.route('/api/v1/descriptions/home', methods=['GET'])
def descriptions_home():
    locale = get_locale(request)
    with open(project_home+f'public/descriptions/home-{locale}.json', encoding='utf-8') as file:
        data = file.read()
    return data

@app.route('/api/v1/descriptions/methods', methods=['GET'])
def descriptions_methods():
    locale = get_locale(request)
    with open(project_home+f'public/descriptions/methods-{locale}.json', encoding='utf-8') as file:
        data = file.read()
    return data

@app.route('/api/v1/descriptions/about', methods=['GET'])
def about_description():
    locale = get_locale(request)
    with open(project_home+f'public/descriptions/about-{locale}.json', encoding='utf-8') as file:
        data = file.read()
    return data