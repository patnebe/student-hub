import json
from flask import request, _request_ctx_stack, abort
from functools import wraps
import jose
from jose import jwt
from urllib.request import urlopen
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


AUTH0_DOMAIN = os.environ.get('AUTH0_TENANT_DOMAIN')
ALGORITHMS = os.environ.get('AUTH0_ALGORITHMS')
API_AUDIENCE = os.environ.get('AUTH0_API_AUDIENCE')


class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
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


def check_permissions(permission, payload):
    """
    Returns True if requested permission string is included in the payload, otherwise it raises an AuthError
    """

    if 'permissions' not in payload:
        raise AuthError({
            "code": "invalid_claims",
            "description": "Permissions not included in JWT"
        }, 403)

    if permission not in payload["permissions"]:
        raise AuthError({
            "code": "unauthorized",
            "description": "Permission not found."
        }, 403)

    return True


def verify_decode_jwt(token):
    """
    Validates a JWT and returns the decoded payload.
    """
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    unverified_header = None

    try:
        unverified_header = jwt.get_unverified_header(token)

    except jose.JWTError:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Error decoding token headers.'
        }, 401)

    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"]
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f"https://{AUTH0_DOMAIN}/"
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 401)

    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 401)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
                payload = verify_decode_jwt(token)
                check_permissions(permission, payload)

            except AuthError as auth_error:
                print(auth_error)
                if auth_error.status_code == 400:
                    abort(400)

                if auth_error.status_code == 401:
                    abort(401)

                if auth_error.status_code == 403:
                    abort(403)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator
