# pantomath
One Stop platform for all our scraping needs

## Setting Up
### Installation
```
$ git clone https://github.com/devclub-iitd/pantomath.git
$ pip install -r requirements.txt
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

### Generating Admin Keys
1. Decide an `admin_secret` and a `db_secret` for your application.
2. Generate the corresponding keys:
`$ python utility/genkey.py <admin_secret> <db_secret>`
3. Copy the `ADMIN_SECRET` and `DB_SECRET` spit out by the app
4. Export these two keys and add to `env.sh` for future setup
`$ export ADMIN_SECRET=<ADMIN_SECRET> && export DB_SECRET=<DB_SECRET>`
5. Decide a `SECRET_KEY` for signing the JWT API keys
`$ export SECRET_KEY=<SECRET_KEY>`

### Updating Database and Generating API Keys
1. Start the app as described in next section.
2. Head over to http://pantomath/admin
3. Update all the databases from http://pantomath/admin/db
3. Generate API key for your app from http://pantomath/admin/keys by entering the `<admin_secret>`, selecting the APIs needed, and a name for your application.

## Running 
```
$ export FLASK_APP=server.py
$ flask run --host=<IP> --port=<PORT>
```

## Documentation

Documentation is available at https://pantomath.docs.apiary.io/  

## APIs Provided
* Gradesheet and Grades
* Student Profile and Department Info
* Courses list and information
* Student registered courses
* Student Daily Schedule
* Student Exam Schedule
* Facebook _(@Siddhant)_