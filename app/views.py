from flask import request, jsonify
from flask import current_app as app
import json, os
from .ldap_scrap import get_departmental_records, get_student_info
from .grades import get_gradesheet, AuthenticationError
from .courses import get_student_data
from .schedule import delete_course_schedule, download_venue_pdf, split_venue_pdf, parse_venue_pdfs, extract_venue_info
from .exam import update_exam_timetable, delete_exam_schedule, download_and_segment_pdf, split_pdf, parse_pdfs, extract_schedule
from .courses_list import get_course_list
from .helper import *
from .auth import *

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


## Grades API ##
def getGrades():
    # Check API access
    status = api_authenticated('GRADES', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    username = request.form.get('username')
    password = request.form.get('password')

    if bad_name(username):
        return res(400, 'No Valid Username Provided')
    if bad_password(password):
        return res(400, 'No Valid Password Provided')

    return res(404, 'Grades API Not Available Yet..')


def getGradesheet():
    """
    Retrieve the gradesheet of the user
    """
    # Check API access
    status = api_authenticated('GRADES', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    username = request.form.get('username')
    password = request.form.get('password')

    if bad_name(username):
        return res(400, 'No Valid Username Provided')
    if bad_password(password):
        return res(400, 'No Valid Password Provided')

    try:
        gradesheet = get_gradesheet(username, password)
    except AuthenticationError as e:
        return res(401, 'Invalid Login Credentials')
    except Exception as e:
        print (e)
        return res(500, 'Internal Server Error')

    # success
    return res(200, gradesheet)
    
## End Grades API ##

## Courses API ##
def getAllCourses():
    """
    Get information about all courses floated
    """
    # Check API access
    status = api_authenticated('COURSES', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

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
    
    # Check API access
    status = api_authenticated('COURSES', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    # Get the infomation about a particular course
    courseCode = request.form.get('course_code')
    if bad_name(courseCode):
        return res(400, 'No valid course code provided.')
    courseCode = courseCode.upper()

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
    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    # Update the courses DB i.e. the courses offered this semester
    username = request.form.get('username')
    password = request.form.get('password')

    if bad_name(username):
        return res(400, 'No Valid Username Provided')
    if bad_password(password):
        return res(400, 'No Valid Password Provided')

    try:
        msg = get_course_list(username, password)
    except AuthenticationError as e:
        return res(403, 'Invalid Login Credentials')
    except Exception as e:
        print (e)
        return res(500, 'Internal Server Error')

    # success
    return res(200, msg)


def deleteCoursesDB():
    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    # Delete the courses DB i.e. the courses offered this semester
    return res(404, 'API not available yet...')

## End Courses API ##

## STU Courses API ##
def getRegisteredCourses():
    # Check API access
    status = api_authenticated('STUCOURSES', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    # Get the registered courses of the given user
    username = request.args.get('username')
    if bad_name(username):
        return res(400, 'No username provided.')
    
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
    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    username = request.form.get('username')
    password = request.form.get('password')

    if bad_name(username):
        return res(400, 'No Valid Username Provided')
    if bad_password(password):
        return res(400, 'No Valid Password Provided')

    # Scrap the academics website for course info and store as json files
    try:
        get_student_data(username, password)
    except Exception as e:
        # Some error occured
        print (e)
        return res(500, 'Internal Server Error')

    # Success
    return res(200, {'status': 'DB updated Successfully'})


def deleteRegisteredCourses():
    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    return res(404, 'API not available yet...')

## End STU Courses API ##

## LDAP API ##
def getDepartmentStudentRecords():
    # Check API access
    status = api_authenticated('LDAP', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    category = request.args.get('category')
    if bad_name(category):
        return res(400, 'No category provided.')

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
    # Check API access
    status = api_authenticated('LDAP', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    uid = request.form.get('uid')
    if bad_name(uid):
        return res(400, 'No uid provided.')

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

## End LDAP API ##

## Schedule APIs ##
def updateSchedule():
    """
    Updates the schedule corresponding to all the courses
    """

    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    pdf_link = request.form.get('pdf_link')
    if bad_url(pdf_link):
        return res(400, 'Valid PDF link not provided')

    # Fetch the PDF file
    try:
        download_venue_pdf(pdf_link)
    except Exception as e:
        print (e)
        return res(400, 'PDF can\'t be downloaded')

    # Segment the PDF file
    try:
        split_venue_pdf()
    except Exception as e:
        print (e)
        return res(500, 'PDF split has a problem')

    # Parse the PDF files
    try:
        parse_venue_pdfs()
    except Exception as e:
        print (e)
        return res(500, 'Problem parsing the PDF')
    
    # Extract the venue information and store in venue.json
    try:
        extract_venue_info()
    except Exception as e:
        print (e)
        return res(500, 'Problem extracting venue info')

    # Return
    return res(200, {'status': 'DB updated Successfully'})


def deleteSchedule():
    """
    Deletes the schedule corresponding to all the courses
    """

    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    try:
        delete_course_schedule()
    except Exception as e:
        return res(500, 'Problem deleting schedule Database')

    # Success
    return res(200, {'status': 'DB deleted Successfully'})


def getSchedule ():
    """
    Fetches the schedule of the given entry number
    """
    # Check API access
    status = api_authenticated('SCHEDULE', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    entry = request.args.get('entry')
    if bad_name(entry):
        return res(400, 'Entry number not provided.')
    entry = entry.upper()

    # Read the courses taken up by the student
    try:
        file = open(PATH + "/../DB/student.json", 'rb')
        student_course_data = json.load(file)
    except Exception as e:
        print (e)
        return res(500, 'Student Database not present')

    try:
        student_course_data = student_course_data[entry]["courses"]
    except Exception as e:
        print (e)
        return res(404, 'Student record not available')

    # Slot info
    try:
        with open(os.path.join(PATH, '../DB/slot.json')) as f:
            slot_data = json.load(f)
    except Exception as e:
        print (e)
        return res(500, 'Slot Info not available')

    # For each course get it's corresponding schedule
    try:
        file = open(PATH + "/../DB/venue.json")
        course_venue = json.load(file)
    except Exception as e:
        return res(500, 'Schedule Database not present')

    student_schedule = []
    for course in student_course_data:
        code = course['code']
        slot = course['slot']

        if (code in course_venue):
            venue = course_venue[code]['room']
            room_capacity = course_venue[code]['capacity']
        else:
            venue = "NA"
            room_capacity = "NA"

        if slot in slot_data:
            schedule = slot_data[slot]
        else:
            schedule = {}

        student_schedule.append({
            'course_code': code,
            'slot': slot,
            'room': venue,
            'room_capacity': room_capacity,
            'schedule': schedule
        })

    # Success 
    return res(200, student_schedule)
    
## End Schedule APIs ##

## Exam Schedule APIs ##
def updateExamSchedule():
    """
    Updates the exam schedule corresponding to all the courses
    """

    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    exam_type = request.form.get('exam_type')
    if (bad_name(exam_type) or not (exam_type == 'minor' or exam_type == 'major')):
        return res(400, 'Valid exam type not provided')

    pdf_link = request.form.get('pdf_link')
    if bad_url(pdf_link):
        return res(400, 'PDF link not provided')
    
    # Fetch the PDF file
    try:
        download_and_segment_pdf(exam_type, pdf_link)
    except Exception as e:
        print (e)
        return res(400, 'PDF can\'t be downloaded')
    
    # Segment the PDF File
    try:
        split_pdf(exam_type)
    except Exception as e:
        print (e)
        return res(500, 'PDF split has a problem')

    # Parse the PDF files
    try:
        parse_pdfs(exam_type)
    except Exception as e:
        print (e)
        return res(500, 'Problem parsing the PDF')
    
    # Update exam venue and timings
    try:
        extract_schedule(exam_type)
    except Exception as e:
        print (e)
        return res(500, 'Problem extracting schedule')

    try:
        update_exam_timetable()
    except Exception as e:
        print (e)
        return res(500, 'Problem updating Exam Schedule Information')

    # Return
    return res(200, {'status': 'DB updated Successfully'})


def deleteExamSchedule():
    """
    Deletes the exam schedule
    """

    status = has_db_rights(request.form)
    if status == 400:
        return res(400, 'admin_secret or db_secret not provided')
    elif status == 401:
        return res(401, 'Incorrect admin_secret or db_secret')

    try:
        delete_exam_schedule()
    except Exception as e:
        return res(500, 'Problem deleting schedule Database')

    # Success
    return res(200, {'status': 'DB deleted Successfully'})


def getExamSchedule ():
    """
    Fetches the schedule of the given entry number
    """
    status = api_authenticated('EXAMSCHEDULE', request.headers)
    if (status == 400):
        return res(400, 'API key or application name not provided')
    elif (status == 401):
        return res(401, 'Invalid API key')

    entry = request.args.get('entry')
    if bad_name(entry):
        return res(400, 'Entry number not provided.')
    entry = entry.upper()

    exam_type = request.args.get('exam_type')
    if (bad_name(exam_type) or not (exam_type == 'M1' or exam_type == 'M2' or exam_type == 'MJ')):
        return res(400, 'Valid exam type not provided')

    # Read the courses taken up by the student
    try:
        file = open(PATH + "/../DB/student.json", 'rb')
        student_course_data = json.load(file)
    except Exception as e:
        print (e)
        return res(500, 'Student Database not present')

    try:
        student_course_data = student_course_data[entry]["courses"]
    except Exception as e:
        print (e)
        return res(404, 'Student record not available')

    # Exam info
    try:
        with open(os.path.join(PATH, '../DB/exam.json')) as f:
            exam_data = json.load(f)
    except Exception as e:
        print (e)
        return res(500, 'Exam Info not available')

    # Exam room info
    try:
        if (exam_type == 'MJ'):
            with open(os.path.join(PATH, '../DB/major.json')) as f:
                exam_room_info = json.load(f)
        else:
            with open(os.path.join(PATH, '../DB/minor.json')) as f:
                exam_room_info = json.load(f)
    except Exception as e:
        print (e)
        exam_room_info = {}

    # For each course get it's corresponding schedule
    exam_schedule = []
    for course in student_course_data:
        code = course['code']
        slot = course['slot']

        if slot in exam_data:
            slot_date = exam_data[slot]
        else:
            slot_date = {}

        if exam_type in slot_date:
            date = slot_date[exam_type]
        else:
            date = "NA"

        if code in exam_room_info:
            schedule = exam_room_info[code]
        else:
            schedule = {}

        exam_schedule.append({
            'course_code': code,
            'slot': slot,
            'date': date,
            'schedule': schedule
        })

    # Success 
    return res(200, exam_schedule)
   
## End Exam Schedule APIs ##

## Admin API ##
def generateAPIkeys():
    """
    Generate the API key for the given application with access rights to the given apps
    """
    if request.json is None:
        return res(400, "Request Content-Type should be of type application/json")
    if type(request.json) is not dict:
        return res(400, "Request should be a JSON object")

    admin_secret = request.json.get('admin_secret')
    if (bad_password(admin_secret)):
        return res(400, 'Please provide a valid Admin Secret')

    # Check the password
    if (not validate_admin(admin_secret)):
        return res(401, 'Incorrect Admin Secret')

    application_name = request.json.get('application_name')
    if (bad_name(application_name)):
        return res(400, 'Please provide an Alpha-numeric application name')

    requested_apis = request.json.get('requested_apis')
    if (bad_api_list(requested_apis)):
        return res(400, 'Please provide valid set of requested APIs')

    try:
        timestamp = get_timestamp()
        payload = {
            'application_name': application_name,
            'api_list': requested_apis,
            'timestamp': timestamp
        }

        update_api_access(payload)
        key = encode_payload (payload)
        return res(200, {
            'access_key': key
        })

    except Exception as e:
        print (e)
        return res(500, 'Failed to generate API key')


def listAPIkeys():
    """
    List which apps have access to which APIs
    """
    if request.form is None:
        return res(400, 'Please submit form data')

    admin_secret = request.form.get('admin_secret')
    if bad_password(admin_secret):
        return res(400, 'Please provide valid Admin Secret')

    if not validate_admin(admin_secret):
        return res(401, 'Incorrect Admin Secret')

    try:
        api_list = list_api_access()
        return res(200, api_list)
    except:
        return res(500, 'Error fetching API List')

## End Admin API ##
