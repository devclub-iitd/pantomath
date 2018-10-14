from flask import request, jsonify
import json, os
from .ldap_scrap import get_departmental_records, get_student_info
from .grades import get_gradesheet, AuthenticationError
from .courses import get_student_data
from .schedule import update_course_schedule, delete_course_schedule
from .exam import update_exam_timetable, delete_exam_schedule, download_and_segment_pdf, split_pdf, parse_pdfs, extract_schedule

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


## Schedule APIs
def updateSchedule():
    """
    Updates the schedule corresponding to all the courses
    """

    try:
        update_course_schedule()
    except Exception as e:
        print (e)
        return res(500, 'Problem updating Course Schedule Information')

    # Return
    return res(200, {'status': 'DB updated Successfully'})


def deleteSchedule():
    """
    Deletes the schedule corresponding to all the courses
    """

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
    if not ('entry' in request.form):
        return res(400, 'Entry number not provided.')

    # Read the courses taken up by the student
    entry = request.form['entry']
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

        if (code in course_venue) and (slot in course_venue[code]):
            venue = course_venue[code][slot]
        else:
            venue = "NA"

        if slot in slot_data:
            schedule = slot_data[slot]
        else:
            schedule = {}

        student_schedule.append({
            'course_code': code,
            'slot': slot,
            'room': venue,
            'schedule': schedule
        })

    # Success 
    return res(200, student_schedule)
    

## Exam Schedule APIs ##
def updateExamSchedule():
    """
    Updates the exam schedule corresponding to all the courses
    """

    exam_type = request.form.get('exam_type')
    if (exam_type is None or not (exam_type == 'minor' or exam_type == 'major')):
        return res(400, 'Valid exam type not provided')

    pdf_link = request.form.get('pdf_link')
    if (pdf_link is None):
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

    if not ('entry' in request.form):
        return res(400, 'Entry number not provided.')

    exam_type = request.form.get('exam_type')
    if (exam_type is None or not (exam_type == 'M1' or exam_type == 'M2' or exam_type == 'MJ')):
        return res(400, 'Valid exam type not provided')

    # Read the courses taken up by the student
    entry = request.form['entry']
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