
def get_matrix_model(api):
    # SCHEMA IS OK BUT FLASK ERROR
    matrix_data_item = api.schema_model('MatrixData', {
        "properties": {
            "matrix": {
            "type": "array",
            "items": {
                "type": "array",
                "items": {
                    "type": "number"
                }
            }
            },
            "extension": {
            "type": "string"
            }
        },
        "type": "object"
    })

    return matrix_data_item