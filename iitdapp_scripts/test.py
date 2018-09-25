import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import urllib.request
import json
from bs4 import BeautifulSoup
from time import strptime
import datetime 



# Scrape from BSP

fp = urllib.request.urlopen("http://bsp.iitd.ac.in")
BSPMagzine = fp.read()
BSPMagzine = BSPMagzine.decode("utf8")
fp.close()

soup = BeautifulSoup(BSPMagzine, 'html.parser')

divs = soup.findAll("div", {"class": "td_module_6 td_module_wrap td-animation-stack td-meta-info-hide"})
# data = []
# dict = {}

cred = credentials.Certificate("iitdapp-firebase-adminsdk-asjla-822cf5c20a.json")



# fire base Upload
firebase_admin = firebase_admin.initialize_app(cred, {'databaseURL': 'https://iitdapp.firebaseio.com'})
ref = db.reference("")
users_ref = ref.child('blogs')



	

i = 1
for div in divs:
	
	blogURL = div.h3.a['href']
	fp = urllib.request.urlopen(blogURL)
	BSPMagzine = fp.read()
	BSPMagzine = BSPMagzine.decode("utf8")
	fp.close()

	soup = BeautifulSoup(BSPMagzine, 'html.parser')
	contents = soup.findAll("p")
	author = soup.find("div", {"class": "td-post-author-name"})
	time = soup.find("time", {"class" : "entry-date updated td-module-date"}).getText()
	c = ""
	for content in contents:
		c = c + content.getText() + "\n"		

	tim = time.split(" ")
	
	dd = tim[1]
	dd = dd[0:len(dd)-1]
	yy = tim[2]
	mm = tim[0][0:3]
	mm = strptime(mm,'%b').tm_mon
	name = tim[0]
	time = datetime.date(int(yy), int(mm), int(dd))
	time = yy + "-" + str(mm) + "-" + dd;


	divcat = div.find('div',attrs={'class': 'td-module-meta-info'})
	temp = ref.child('blogs/' + time)	
	
	users_ref.update({time :{str(i):{"uid" : str(i),"image": div.img['src'], "title": div.h3.a['title'] , "category" : divcat.a.getText(), "body" : c, "website" : "BSP" , "author" : author.a.getText(), "time" : time , "postURL" : blogURL}} })
	i = i+1
	# print(i)




	# <time class="entry-date updated td-module-date" datetime="2018-09-03T11:51:51+00:00">September 3, 2018</time>
