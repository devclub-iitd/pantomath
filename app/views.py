from flask import request, jsonify
import json
import csv
from .ldap_scrap import get_departmental_records, get_student_info
from .grades import get_gradesheet, AuthenticationError


# List of statuses
ok = 200
badrequest = 400
unauthorized = 401
forbidden = 403
notfound = 404
invalid = 403
internalServerError = 500
badGateway = 502
serviceUnavailable = 503


def index():
    return 'Welcome to Pantomath!'


## Grades API
def getGrades():
    return res(404, 'Grades API Not Available Yet..')
    
def getGradesheet():
    if not ('username' in request.form):
        return res(400, 'No Username Provided')
    if not ('password' in request.form):
        return res(400, 'No Password Provided')

    username = request.form['username']
    password = request.form['password']

    try:
        gradesheet = get_gradesheet(username, password)
    except AuthenticationError as e:
        return res(403, 'Invalid Login Credentials')
    except Exception as e:
        print (e)
        return res(500, 'Internal Server Error')

    # success
    return res(200, 'Gradesheet successfully retrieved', gradesheet)
    

## LDAP API
def getDepartmentStudentRecords():
    if not ('category' in request.form):
        return res(400, 'No category provided.')

    category = request.form['category']

    # Query LDAP
    try:
        records = get_departmental_records(category)
    except Exception as e:
        # Some error occurred
        return res(500, 'Internal Server Error')

    if (len(records) == 0):
        # No such category was found
        return res(400, 'No students of this category found')

    # Success
    return res(200, 'Successfully retrieved departmental records', records)


def getStudentInfo():
    if not ('uid' in request.form):
        return res(400, 'No uid provided.')

    uid = request.form['uid']
    searchAttributes=["department", "category", "username", "altEmail"]

    # Extract extra search attributes
    if ("entry" in request.form):
        searchAttributes.append("uniqueIITDid")
    if ("dateOfBirth" in request.form):
        searchAttributes.append("dateOfBirth")
    if ("gender" in request.form):
        searchAttributes.append("gender")
    if ("bloodGroup" in request.form):
        searchAttributes.append("bloodGroup")
    if ("suspended" in request.form):
        searchAttributes.append("suspended")
    if ("emailalias" in request.form):
        searchAttributes.append("emailalias")

    # Get the results from LDAP
    try:
        results = get_student_info(uid, searchAttributes)
    except Exception as e:
        # Some error occurred
        return res(500, 'Internal Server Error')

    if (len(results) == 0):
        # Invalid UID
        return res(400, 'Invalid UID Provided')
        
    # Change relevant keys
    if ("uniqueIITDid" in results):
        results["entry"] = results["uniqueIITDid"]
        results.pop("uniqueIITDid")

    if ("username" in results):
        results["name"] = results["username"]
        results.pop("username")

    # Return
    return res(200, 'Successfully Retrieved Student Info', results)


# Helper functions
def res(code, msg, data=None):
    # Returns the appropriate response
    response = {
        'error': False if code == 200 else True,
        'message': msg,
        'data': data 
    }
    return jsonify(response), code
