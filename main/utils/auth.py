#auth
import sqlite3, hashlib

# Login - Returns true if successful, false otherwise
def login(email, password):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT email, password FROM accounts WHERE email = '%s'" % (email));
    for account in c:
        uemail = account[1]
        passw = account[2]
        # Check if email and encrypted password match
        if email == uemail and encrypt_password(password) == passw:
            print "Successful Login"
            return True
    print "Login Failed"
    return False

# Encrypt password - Returns SHA256
def encrypt_password(password):
    encrypted = hashlib.ha256(password).hexdigest()
    return encrypted

# Create account - Returns true if successful, false otherwise
def create_account(name, email, password):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    if not does_email_exist(email) and is_valid_email(email):
        # Add user to accounts table
        c.execute("INSERT INTO accounts VALUES('%s', '%s', '%s', %d)" % (name, email, encrypt_password(password), 0))
        db.commit()
        db.close()
        print "Create Account Successful"
        return True
    print "Create Account Failed"
    return False

# Checks if email exists - Returns true if email exists, false otherwise
def does_email_exist(email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT email FROM accounts WHERE email = '%s'" % (email))
    for account in c:
        # Username exists
        print "Email exists"
        return True
    print "Email does not exist"
    return False

# Checks if email is stuy.edu - Returns true if it is, false otherwise
def is_valid_email(email):
    split = email.split("@")
    if split[1] == "stuy.edu":
        print "Valid Email"
        return True
    print "Invalid Email"
    return False

# Get name - Returns name associated with email
def get_name(email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for name with email
    c.execute("SELECT name FROM accounts WHERE email = '%s'" % (email))
    for name in c:
        return name[0]
