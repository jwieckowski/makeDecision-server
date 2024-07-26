# Copyright (c) 2023 Jakub Więckowski

def validate_locale(locale):
    """
    Validate the provided locale code.

    Parameters
    ----------
    locale : str
        The locale code to be validated. Expected values are 'en' for English and 'pl' for Polish.

    Returns
    -------
    str
        The validated locale code. Returns 'en' if the provided locale is not valid.
    """
    valid = ['en', 'pl']
    if locale in valid:
        return locale
    return 'en'
