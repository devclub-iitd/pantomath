from flask import request, jsonify
import json, os
from .ldap_scrap import get_departmental_records, get_student_info
from .grades import get_gradesheet, AuthenticationError
from .utils import get_student_data

PATH = os.path.dirname(os.path.abspath(__file__))

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
    return """
    <h2> Welcome to Pantomath </h2>
    <h4> Please find the documentation at <a href="https://pantomath.docs.apiary.io/">https://pantomath.docs.apiary.io/ </a></h4>
    """

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
    return res(200, gradesheet)
    

## Courses API ##
def getAllCourses():
    # Get information about all courses floated
    try:
        file = open(PATH + "/../DB/courses.json", 'rb')
        data = json.load(file)
    except Exception as e:
        print (e)
        return res(500, 'Internal Server Error')

    result = {}
    for courseCode, courseInfo in data.items():
        result[courseCode] = formatCourseInfo(courseInfo)

    # Success
    return res(200, result)


def getCourseInfo():
    # Get the infomation about a particular course
    if (not 'course_code' in request.form):
        return res(400, 'No course code provided.')
    
    courseCode = request.form['course_code'].upper()
    try:
        file = open(PATH + "/../DB/courses.json", 'rb')
        data = json.load(file)
    except Exception as e:
        print (e)
        return res(500, 'Internal Server Error')

    courseData = data.get(courseCode, None)
    if courseData is None:
        return res(404, 'Course is not present in the database')

    # Success
    return res(200, formatCourseInfo(courseData))


def updateCoursesDB():
    # Update the courses DB i.e. the courses offered this semester
    return res(404, 'API not available yet...')

def deleteCoursesDB():
    # Delete the courses DB i.e. the courses offered this semester
    return res(404, 'API not available yet...')


def getRegisteredCourses():
    # Get the registered courses of the given user
    if (not 'username' in request.form):
        return res(400, 'No username provided.')
    
    username = request.form['username']
    try:
        file = open(PATH + "/../DB/student.json", 'rb')
        data = json.load(file)
    except Exception as e:
        print (e)
        return res(500, 'Internal Server Error')
    
    entrynum = username_to_entrynum(username)
    userdata = data.get(entrynum, None)
    if userdata is None:
        return res(404, 'Username is not present in the database')

    # Success
    return res(200, userdata)


def updateRegisteredCourses():
    # Scrap the academics website for course info and store as json files
    try:
        get_student_data()
    except Exception as e:
        # Some error occured
        print (e)
        return res(500, 'Internal Server Error')

    # Success
    return res(200, {'status': 'DB updated Successfully'})


def deleteRegisteredCourses():
    return res(404, 'API not available yet...')

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
    return res(200, records)


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
    return res(200, results)


# Helper functions
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


def username_to_entrynum(u):
    return "20" + u[3:5] + u[:3].upper() + u[5:]

def formatCourseInfo(courseInfo):
    # put the course slot inside course info
    result = {}
    for slot, info in courseInfo.items():
        result = info
        result['slot'] = slot

    return result