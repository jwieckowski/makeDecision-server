from flask_restx import reqparse

def get_locale_parser():
    """
    Creates and returns a parser for extracting locale information from request headers.

    Returns
    -------
    flask_restx.reqparse.RequestParser
        The configured request parser that extracts the 'locale' header.
    """
    parser = reqparse.RequestParser()
    parser.add_argument('locale', location='headers', required=True)

    return parser