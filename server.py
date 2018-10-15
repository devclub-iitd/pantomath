from flask import Flask
from app import views

app = Flask(__name__)

## Configuration
app.config.from_object('config.Development')

## Views and API
## Static
app.add_url_rule('/', view_func=views.index)

## Grades API ##
app.add_url_rule('/api/gradesheet', view_func=views.getGradesheet, methods=['POST'])
app.add_url_rule('/api/grades', view_func=views.getGrades, methods=['POST'])

## Courses API ##
app.add_url_rule('/api/courseInfo', view_func=views.getAllCourses, methods=['GET'])
app.add_url_rule('/api/courseInfo', view_func=views.getCourseInfo, methods=['POST'])
app.add_url_rule('/api/courseInfo', view_func=views.updateCoursesDB, methods=['PUT'])
app.add_url_rule('/api/courseInfo', view_func=views.deleteCoursesDB, methods=['DELETE'])

app.add_url_rule('/api/registeredCourses', view_func=views.getRegisteredCourses, methods=['POST'])
app.add_url_rule('/api/registeredCourses', view_func=views.updateRegisteredCourses, methods=['PUT'])
app.add_url_rule('/api/registeredCourses', view_func=views.deleteRegisteredCourses, methods=['DELETE'])

## LDAP API ##
app.add_url_rule('/api/deptStudentRecords', view_func=views.getDepartmentStudentRecords, methods=['POST'])
app.add_url_rule('/api/getStudentInfo', view_func=views.getStudentInfo, methods=['POST'])

## Timetable API ##
app.add_url_rule('/api/schedule', view_func=views.getSchedule, methods=['POST', 'GET'])
app.add_url_rule('/api/schedule', view_func=views.updateSchedule, methods=['PUT'])
app.add_url_rule('/api/schedule', view_func=views.deleteSchedule, methods=['DELETE'])

## Exam Schedule API ##
app.add_url_rule('/api/examSchedule', view_func=views.updateExamSchedule, methods=['PUT', 'GET'])
app.add_url_rule('/api/examSchedule', view_func=views.deleteExamSchedule, methods=['DELETE'])
app.add_url_rule('/api/examSchedule', view_func=views.getExamSchedule, methods=['POST'])


## Admin API ##
