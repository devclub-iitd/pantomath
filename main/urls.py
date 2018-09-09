from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),

    # this saves a students records json file on server
    path('save_student_data/', views.save_student_data, name='index'),
    path('api/registeredCourses', views.registered_courses, name='registered'),
        
    path('api/getDepartmentStudentRecords', views.getDepartmentStudentRecords, name='getDepartmentStudentRecords'),
    path('api/getAllDepartmentRecords', views.getAllDepartmentRecords, name='getAllDepartmentRecords')

]