import mechanize
import cookielib
from bs4 import BeautifulSoup,NavigableString
import html2text
import string
import socket
import httplib
import ssl

ACADEMICS_URL = 'https://academics1.iitd.ac.in/Academics/'



def getGrades(username,password):

    def connect(self):      #some code to deal with certificate validation
        sock = socket.create_connection((self.host, self.port),
                                self.timeout, self.source_address)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()

        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)


    httplib.HTTPSConnection.connect = connect
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    r = br.open(ACADEMICS_URL)


    # Select the second (index one) form (the first form is a search query box)
    br.select_form(nr=0)

    # User credentials
    br.form['username'] = username
    br.form['password'] = password

    # Login
    br.submit()
    soup = BeautifulSoup(str(br.open(br.geturl()).read()),"lxml")
    current_grades_link=None
    past_grades_link=None
    for i in soup.find_all('a'):
        if 'vgrd' in str(i.get('href')):
            current_grades_link=i.get('href')
        if 'grade' in str(i.get('href')):
            past_grades_link=i.get('href')

    if (current_grades_link is None) and (past_grades_link is None):
        return (True,"Invalid Login Credentials")

    def remove_attrs(soup):
        for tag in soup.findAll(True):
            tag.attrs = None
        return soup

    grades_str = '' 
    if not(past_grades_link is None):

        gradesheet=br.open("https://academics1.iitd.ac.in/Academics/"+past_grades_link).read()

        soup = BeautifulSoup(gradesheet,"html5lib")
        soup_without_attributes=remove_attrs(soup)
        final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')
        for div in final_soup:
            for x in div.find_all():
                if len(x.text) == 0:
                    x.extract()

        limit=len(final_soup)
        for i in range(2,limit):
            grades_str += str(final_soup[i])

    return grades_str


def getGradeSheet(username,password):

    def connect(self):      #some code to deal with certificate validation
            sock = socket.create_connection((self.host, self.port),
                                self.timeout, self.source_address)
            if self._tunnel_host:
                self.sock = sock
                self._tunnel()

            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_TLSv1)


    httplib.HTTPSConnection.connect = connect
    # Browser
    br = mechanize.Browser()

    # Cookie Jar
    cj = cookielib.LWPCookieJar()
    br.set_cookiejar(cj)

    # Browser options
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

    br.addheaders = [('User-agent', 'Chrome')]

    # The site we will navigate into, handling it's session
    r = br.open(ACADEMICS_URL)


    # Select the second (index one) form (the first form is a search query box)
    br.select_form(nr=0)

    # User credentials
    br.form['username'] = username
    br.form['password'] = password

    # Login
    br.submit()
    soup = BeautifulSoup(str(br.open(br.geturl()).read()),"lxml")
    current_grades_link=None
    past_grades_link=None
    for i in soup.find_all('a'):
        if 'vgrd' in str(i.get('href')):
            current_grades_link=i.get('href')
        if 'grade' in str(i.get('href')):
            past_grades_link=i.get('href')

    if (current_grades_link is None) and (past_grades_link is None):
        return (True,"Invalid Login Credentials")

    def remove_attrs(soup):
        for tag in soup.findAll(True):
            tag.attrs = None
        return soup

    grades_str = '' 

    if not(current_grades_link is None):
        
        gradesheet=br.open("https://academics1.iitd.ac.in/Academics/"+current_grades_link).read()

        soup = BeautifulSoup(gradesheet,"html5lib")
        soup_without_attributes=remove_attrs(soup)
        final_soup =soup_without_attributes.findAll('table')[0].findAll('table')[1].findAll('table')[2]

        for x in final_soup.find_all():
            if len(x.text) == 0:
                x.extract()

        grades_str += str(final_soup)

    return grades_str


# if __name__ == "__main__":
