# Copyright (c) 2023 Jakub Więckowski

import io
from PIL import Image
from base64 import encodebytes
import matplotlib.pyplot as plt

from utils.errors import get_error_message
from routes.namespaces import v1 as api

def graphs_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)

            pil_img = Image.open(buffer)
            byte_arr = io.BytesIO()
            pil_img.save(byte_arr, format='PNG')
            encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii')
            
            return f'data:image/jpeg;base64,{encoded_img}'
        except Exception as err:
            locale = 'en'
            api.logger.info(str(err))
            raise ValueError(f'{get_error_message(locale, "graph-error")}')

    return wrapper

