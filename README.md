# pantomath
One Stop platform for all our scraping needs

## Running
```
$ pip install -r requirements.txt
$ export FLASK_APP=server.py
$ flask run --host=<IP> --port=<PORT>
```

Note: In case of Installation errors -
1. [error installing python-ldap](https://stackoverflow.com/a/4768467/7116413), on a Debian/Ubuntu system:
`sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev`
2. [error with tkinter](https://stackoverflow.com/a/43616757/7116413), on a Debian/Ubuntu system:
 `sudo apt-get install python3-tk`
3. [error with cv2](https://stackoverflow.com/a/48533185/7116413), on Debian/Ubuntu system: 
`pip3 install opencv-python`
4. [error with bcrypt](https://pypi.org/project/bcrypt/), on Debian/Ubuntu system:
`sudo apt-get install build-essential libffi-dev python-dev`


## Documentation

Documentation is available at https://pantomath.docs.apiary.io/  

## APIs Provided
* Gradesheet and Grades
* Student Profile and Department Info
* Courses list and information
* Student registered courses
* Student Daily Schedule
* Student Exam Schedule