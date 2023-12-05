# Copyright (c) 2023 Jakub Więckowski

from utils.errors import get_error_message
from routes.namespaces import v1 as api

def assessment_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)

        except Exception as err:
            locale = kwargs.get('locale')
            api.logger.info(str(err))
            raise ValueError(f'{get_error_message(locale, "assessment-error")}')
            
    return wrapper

