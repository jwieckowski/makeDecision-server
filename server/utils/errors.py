# Copyright (c) 2023 Jakub Więckowski

import json
from config import dir_path

project_home = dir_path
error_file_en = open(project_home+'public/errors/errors-en.json', encoding='utf-8')
errors_en = json.load(error_file_en)
error_file_en.close()
error_file_pl = open(project_home+'/public/errors/errors-pl.json', encoding='utf-8')
errors_pl = json.load(error_file_pl)
error_file_pl.close()

error_codes = {
    'en': errors_en,
    'pl': errors_pl
}

def get_error_message(locale, key):
    if locale not in list(error_codes.keys()):
        return error_codes['en']['locale-error'] 
    if key not in list(error_codes[locale].keys()):
        return error_codes[locale]['key-error']
    
    return error_codes[locale][key]