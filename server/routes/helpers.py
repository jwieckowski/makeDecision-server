def get_locale(request):
    locale = request.headers.get('locale')
    valid = ['en', 'pl']
    if locale in valid:
        return locale
    return 'en'
