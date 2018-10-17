from bs4 import BeautifulSoup,NavigableString
import html2text
import socket
import ssl
import robobrowser
import http
import requests
from requests import Session
import json

requests.packages.urllib3.disable_warnings()

session = Session()
session.verify = False # Skip SSL verification
session.proxies = {'http': 'http://proxy22.iitd.ac.in/'} # Set default proxies

ACADEMICS_URL = 'https://academics1.iitd.ac.in/Academics/'

class AuthenticationError(Exception):
    pass

def get_course_list(username,password):

    # Browser
    br = robobrowser.RoboBrowser(session=session, parser='lxml')

    # The site we will navigate into, handling it's session
    br.open(ACADEMICS_URL)


    # Select the second (index one) form (the first form is a search query box)
    form = br.get_form(action='index.php?page=tryLogin')

    br.session.headers['Referer'] = ACADEMICS_URL

    # User credentials
    form['username'] = username
    form['password'] = password

    # Login
    br.submit_form(form)
    soup = BeautifulSoup(str(br.select),"lxml")
    link=None
    for i in soup.find_all('a'):
        if 'repoOffered' in str(i.get('href')):
            link=i.get('href')
  

    if (link is None):
        # Invalid Credentials
        raise AuthenticationError("Invalid Login Credentials")

    def remove_attrs(soup):
        for tag in soup.findAll(True):
            tag.attrs = None
        return soup

    courses_str = '' 
    if not(link is None):

        br.open(ACADEMICS_URL+link)

        soup = BeautifulSoup(str(br.select),"html5lib")

        soup_without_attributes=remove_attrs(soup)
        final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')
        for div in final_soup:
            for x in div.find_all():
                if len(x.text) == 0:
                    x.extract()

    final_soup = final_soup[1].findAll('table')[0].findAll('tr')
    data = {}
    idx = 1
    # print(final_soup)
    while idx < len(final_soup):
        td = final_soup[idx].findAll('td')
        course = {}
        course_slot = td[1].string
        course_code = td[2].string
        course["name"] = td[3].string
        course["credit"] = td[4].string
        course["structure"] = td[5].string
        course["coordinator"] = td[6].string
        course["limit"] = td[7].string
        idx = idx + 1
        slot = {}
        slot[course_slot] = course
        if course_code in data:
            data[course_code][course_slot] = course
        else:
            data[course_code] = slot
    with open('../DB/courses.json', 'w') as fp:
        json.dump(data, fp)

    return "list of courses saved at DB/courses.json"


# if __name__ == "__main__":
#     print(get_course_list("xxx", "xxx"))