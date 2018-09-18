from flask import Flask
from app import views

app = Flask(__name__)

app.add_url_rule('/', view_func=views.index)

## Grades API ##
app.add_url_rule('/api/gradesheet', view_func=views.getGradesheet, methods=['POST'])
app.add_url_rule('/api/grades', view_func=views.getGrades, methods=['POST'])

## Courses API ##
app.add_url_rule('/api/updateCoursesDB', view_func=views.updateCoursesDB, methods=['POST'])
app.add_url_rule('/api/registeredCourses', view_func=views.getRegisteredCourses, methods=['GET', 'POST'])
app.add_url_rule('/api/allCourses', view_func=views.getAllCourses, methods=['GET', 'POST'])
app.add_url_rule('/api/courseInfo', view_func=views.getCourseInfo, methods=['GET', 'POST'])

## LDAP API ##
app.add_url_rule('/api/deptStudentRecords', view_func=views.getDepartmentStudentRecords, methods=['POST'])
app.add_url_rule('/api/getStudentInfo', view_func=views.getStudentInfo, methods=['POST'])