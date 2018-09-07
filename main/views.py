from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from bs4 import BeautifulSoup


# Create your views here.
def index(request):
    response = JsonResponse({'foo': 'bar'})
    return response



@api_view(['GET'])
def getAllDepartmentRecords(request):
    listOfUrls=[
        "http://ldap1.iitd.ernet.in/LDAP/chemical/ch114.shtml"
    ]
    code2dept = {
        "ce":"civil",
        "ch":"chemical",
        "cs":"cse",
        "bb":"dbeb",
        "ee":"ee",
        "mt":"maths",
        "me":"mech",
        "ph":"physics",
        "tt":"textile"
    }
    totalDic=[]
    Dept = ""
    ind=0

    for url in listOfUrls:
        response = requests.get(url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")

        table_body = soup.find('table')

        rows = table_body.find_all('tr')
        print(url)
            
        for row in rows:
            cols = row.find_all('td')
            if(len(cols) > 1):
                cols = [ele.text.strip() for ele in cols]
                cols.append(Dept)
                totalDic.append([ele for ele in cols if ele]) # Get rid of empty values
                totalDic[ind][0] = kerberos_to_entry_number(totalDic[ind][0])
                ind = ind+1
            else:
                cols = [ele.text.strip() for ele in cols]
                Dept = code2dept[str(cols[0][0:2])]
    print(totalDic)
    return 4

@api_view(['GET'])
def getDepartmentStudentRecords(request):
    # print ('hey')
    # print (request.name)
    response = JsonResponse({'foo': 'bar'})
    return response
