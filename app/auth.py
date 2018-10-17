"""
Contains API authentication functions and helper functions
"""

import bcrypt
import jwt
import datetime
from flask import current_app as app
# from helper import res
# import .helper

## List of APIS available
API_LIST = {
    'GRADES': True,
    'LDAP': True,
    'COURSES': True,
    'STU_COURSES': True,
    'SCHEDULE': True,
    'EXAM_SCHEDULE': True,
    'FACEBOOK': True
}

def validate_admin (admin_secret):
    """
    Validate if the given admin_secret is the correct one
    """

    try:
        admin_secret = admin_secret.encode()
        hashed = app.config['ADMIN_SECRET'].encode()
        return bcrypt.checkpw(admin_secret, hashed)

    except Exception as e:
        return False


def validate_db_admin (db_secret):
    """
    Validate if the given db_secret is the correct one
    """

    try:
        db_secret = db_secret.encode()
        hashed = app.config['DB_SECRET'].encode()
        return bcrypt.checkpw(db_secret, hashed)
    except Exception as e:
        return False


def bad_api(api):
    """
    Validate if the given API is valid or not
    """
    return (not api.isalpha()) or (not api.isupper()) or (API_LIST.get(api) is None)

    
def encode_payload(payload):
    """
    Sign the payload with jwt using secret key
    Return as API key
    Expiry = 100 days
    """
    jwt_secret = app.config['SECRET_KEY']
    # expiry = 60 * 60 * 24 * 100 # 100 days
    # payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expiry)
    encoded_jwt = jwt.encode(payload, jwt_secret, algorithm='HS256')

    return (encoded_jwt).decode()


def decode_payload(encoded_payload):
    """
    Decode the payload with jwt using secret key
    Return the payload if valid
    """
    jwt_secret = app.config['SECRET_KEY']
    payload = jwt.decode(encoded_payload, jwt_secret, algorithms='HS256')

    return payload
