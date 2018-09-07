from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .utils import get_student_data
import json, os


# Create your views here.
def index(request):
    response = JsonResponse({'foo': 'bar'})
    return response

def save_student_data(request):
    get_student_data()
    path = os.getcwd()+"/main/student.json"
    with open(path, 'rb') as file:
        file = json.load(file)
    
    print(path)
    return JsonResponse(file) 