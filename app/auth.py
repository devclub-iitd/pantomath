"""
Contains API authentication functions and helper functions
"""

import bcrypt
import jwt
import datetime
import os, json
from flask import current_app as app
# from helper import res
# import .helper

PATH = os.path.dirname(os.path.abspath(__file__))

## List of APIS available
API_LIST = {
    'GRADES': True,
    'LDAP': True,
    'COURSES': True,
    'STUCOURSES': True,
    'SCHEDULE': True,
    'EXAMSCHEDULE': True,
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


def update_api_access(info):
    """
    Updates the API access of the given app
    """
    try:
        file = open(PATH + "/../DB/access.json", 'r')
        accessData = json.load(file)
    except:
        raise

    try:
        accessData[info['application_name']] = {
            'api_list': info['api_list'],
            'timestamp': info['timestamp']
        }
    except Exception as e:
        print (e)
        raise

    try:
        with open(PATH + '/../DB/access.json', 'w') as f:
            f.write(json.dumps(accessData, indent=4, sort_keys=True))
    except:
        raise


def check_api_access(info):
    """
    Checks whether the payload is valid depending on latest timestamp
    """

    try:
        file = open(PATH + '/../DB/access.json', 'r')
        accessData = json.load(file)
    except:
        return False

    try:
        application = info['application_name']
        applicationData = accessData.get(application)

        if applicationData is None:
            return False

        timestamp = applicationData["timestamp"]
        if info['timestamp'] == timestamp:
            return True 
        return False
    except:
        return False

    
def list_api_access():
    """
    List all apps with their API access
    """
    try:
        file = open(PATH + '/../DB/access.json', 'r')
        accessData = json.load(file)
    except:
        raise

    try:
        return accessData
    except:
        raise


def revoke_api_access(application):
    """
    Revoke the API access of this application
    """
    try:
        file = open(PATH + '/../DB/access.json', 'r')
        accessData = json.load(file)
        if (application in accessData):
            accessData.pop(application, None)

        with open(PATH + '/../DB/access.json', 'w') as f:
            f.write(json.dumps(accessData, indent=4, sort_keys=True))        
    except:
        raise