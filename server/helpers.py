# Copyright (c) 2023 Jakub Więckowski

def validate_locale(locale):
    valid = ['en', 'pl']
    if locale in valid:
        return locale
    return 'en'
