from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

# Create your views here.
def index(request):
    response = JsonResponse({'foo': 'bar'})
    return response
