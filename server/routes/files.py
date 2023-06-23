from flask import request, jsonify
from __main__ import app
from __main__ import project_home

from utilities.files import Files

@app.route('/api/v1/files/about', methods=['GET'])
def about_files():
    images = [
        project_home+'public/files/json_data.png',
        project_home+'public/files/fuzzy_json_data.png',
        project_home+'public/files/xlsx_data.png',
        project_home+'public/files/fuzzy_xlsx_data.png',
        project_home+'public/files/csv_data.png',
        project_home+'public/files/fuzzy_csv_data.png'
    ]
    encoded_images = []
    for image_path in images:
        encoded_images.append(Files.get_response_image(image_path))
    return jsonify({'result': encoded_images})
