from flask import request


class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_from_auth_header():
    """
    Returns the access token from the authorization header
    """
    
    auth_header = request.headers.get("Authorization", None)

    if not auth_header:
        raise AuthError({
            "code": 'authorization_header_missing',
            "description": "Authorization header is expected."
        }, 401)


    parts = auth_header.split()


    if len(parts) is not 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be a valid bearer token.'
        }, 401)


    if parts[0].lower() != 'bearer':
        print('wrong header', parts[0].lower())
        raise AuthError({
            "code": "invalid_header",
            "description": "Authorization header must start with 'Bearer'"
        }, 401)

    token = parts[1]
    return token