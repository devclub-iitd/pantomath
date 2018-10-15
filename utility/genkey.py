"""
Generates an Admin-key and DB-key for you
Call using
`python genkey.py your-password`
"""

import sys
import bcrypt

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print ('Please provide 2 passwords for admin and DB key')
        exit(1)

    admin_password = (sys.argv[1]).encode()
    admin_key = bcrypt.hashpw(admin_password, bcrypt.gensalt())

    db_password = (sys.argv[2]).encode()
    db_key = bcrypt.hashpw(db_password, bcrypt.gensalt())

    print ("ADMIN_SECRET:", admin_key.decode())
    print ("DB_SECRET:", db_key.decode())
