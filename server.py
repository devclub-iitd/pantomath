from flask import Flask
from app import views

app = Flask(__name__)

app.add_url_rule('/', view_func=views.index)

## LDAP API ##
app.add_url_rule('/api/deptStudentRecords', view_func=views.getDepartmentStudentRecords, methods=['POST'])
app.add_url_rule('/api/getStudentInfo', view_func=views.getStudentInfo, methods=['POST'])