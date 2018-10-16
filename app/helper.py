"""
Contains helper functions and validations
"""

from flask import request, jsonify
import re, json, os
from .auth import bad_api, validate_admin, validate_db_admin, decode_payload

def res(code, response):
    # Returns the appropriate response
    if (code == 200):
        # Send the OK response
        return jsonify(response), 200
    else:
        # Send error
        errorMsg = {
            "error": response
        }
        return jsonify(errorMsg), code


def bad_input (input):
    """
    Validates if it's a valid input
    """
    return (input is None) or len(input) < 1


def bad_url (url):
    """
    Validate the given url
    """
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    return bad_input(url) or (re.match(regex, url) is None)


def bad_name (name):
    """
    checks for alphanumeric
    """
    return bad_input(name) or not name.isalnum()


def bad_password(password):
    """
    checks for valid password
    """
    return bad_input(password) or re.match('^[A-Za-z0-9@#$%^&\*\.+=]+$', password) is None


def bad_api_list(api_list):
    """
    checks for the validity of the list
    """
    if (api_list is None) or (type(api_list) is not list) or (len(api_list) < 1):
        return True

    for api in api_list:
        if bad_input(api) or bad_api(api):
            print ('bad api')
            return True
        
    return False


def bad_payload(payload):
    """
    Check the format of the decoded payload
    """
    return (
            (payload is None) or
            (type(payload) is not dict) or 
            (payload.get('application_name') is None) or 
            (payload.get('api_list') is None) or
            (type(payload.get('api_list')) is not list) or
            (len(payload.get('api_list')) < 1)
    )


def has_access(application_name, api_name, payload):
    """
    Check if this application has the access to this API 
    by examining the payload
    """
    if application_name != payload.get('application_name'):
        return False

    for api in payload.get('api_list'):
        if api == api_name:
            return True

    return False
    

def api_authenticated(api_name, form):
    """
    Check the API access
    """
    api_key = form.get('Api-Key')
    if bad_input(api_key):
        return 400

    application_name = form.get('Application-Name')
    if bad_name(application_name):
        return 400

    try:
        payload = decode_payload(api_key)
        if not has_access(application_name, api_name, payload):
            return 401
    except Exception as e:
        print (e)
        return 401
        return res(401, 'Invalid API key')

    return 200


def has_db_rights(form):
    """
    Checks if the caller has appropriate rights to modify DB
    """
    admin_secret = form.get('admin_secret')
    db_secret = form.get('db_secret')
    if bad_password(admin_secret) or bad_password(db_secret):
        return 400
    
    if not validate_admin(admin_secret) or not validate_db_admin(db_secret) :
        return 401

    return 200
    

def username_to_entrynum(u):
    return "20" + u[3:5] + u[:3].upper() + u[5:]

def formatCourseInfo(courseInfo):
    # put the course slot inside course info
    result = {}
    for slot, info in courseInfo.items():
        result = info
        result['slot'] = slot

    return result