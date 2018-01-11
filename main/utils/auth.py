#auth
import sqlite3, hashlib

# Login - Returns true if successful, false otherwise
def login(email, password):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT email, password FROM accounts WHERE email = '%s'" % (email));
    for account in c:
        print account
        uemail = account[0]
        passw = account[1]
        # Check if email and encrypted password match
        if email == uemail and encrypt_password(password) == passw:
            print "Successful Login"
            return True
    print "Login Failed"
    return False

# Encrypt password - Returns SHA256
def encrypt_password(password):
    encrypted = hashlib.sha256(password).hexdigest()
    return encrypted

# Create account - Returns true if successful, false otherwise
def create_account(email, password):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    if not does_email_exist(email) and is_valid_email(email):
        # Add user to accounts table
        c.execute("INSERT INTO accounts VALUES('%s', '%s', '%s', '%s')" % (email, encrypt_password(password), "[]", "false"))
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
    if (email.find("@stuy.edu") != -1) and (email.split("@")[1] == "stuy.edu"):
        print "Valid Email"
        return True
    print "Invalid Email"
    return False
