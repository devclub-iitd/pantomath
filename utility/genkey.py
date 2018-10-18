"""
Generates an Admin-key and DB-key for you
Call using
`python genkey.py your-password`
"""

import sys
import re
import bcrypt

def bad_password(password):
    """
    checks for valid password
    """
    return len(password) < 8 or re.match('^[A-Za-z0-9@#$%^&\*\.+=]+$', password) is None

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ('Please provide 2 passwords for admin and DB key')
        exit(1)

    admin_password = (sys.argv[1]).encode()
    if bad_password(admin_password.decode()):
        print ('Password should be of minimum length 8 and should contain only A-Za-z0-9@#$%^&*.+=')
        exit(1)
    admin_key = bcrypt.hashpw(admin_password, bcrypt.gensalt())

    db_password = (sys.argv[2]).encode()
    if bad_password(db_password.decode()):
        print ('Password should be of minimum length 8 and should contain only A-Za-z0-9@#$%^&*.+=')
        exit(1)
    db_key = bcrypt.hashpw(db_password, bcrypt.gensalt())

    print ("ADMIN_SECRET:", admin_key.decode())
    print ("DB_SECRET:", db_key.decode())
