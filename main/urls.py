from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('api/getDepartmentStudentRecords', views.getDepartmentStudentRecords, name='getDepartmentStudentRecords'),
    path('api/getAllDepartmentRecords', views.getAllDepartmentRecords, name='getAllDepartmentRecords')

]