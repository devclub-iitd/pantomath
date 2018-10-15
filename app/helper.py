"""
Contains helper functions and validations
"""

from flask import request, jsonify
import re, json, os

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


def username_to_entrynum(u):
    return "20" + u[3:5] + u[:3].upper() + u[5:]

def formatCourseInfo(courseInfo):
    # put the course slot inside course info
    result = {}
    for slot, info in courseInfo.items():
        result = info
        result['slot'] = slot

    return result