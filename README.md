# pantomath
One Stop platform for all our scraping needs

## Running
```
$ pip install -r requirements.txt
$ export FLASK_APP=server.py
$ flask run --host=<IP> --port=<PORT>
```

Note: In case of [error installing python-ldap](https://stackoverflow.com/a/4768467/7116413), on a Debian/Ubuntu system:
`sudo apt-get install libsasl2-dev python-dev libldap2-dev libssl-dev
`