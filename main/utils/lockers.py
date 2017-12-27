#lockers
import sqlite3, hashlib

# Create locker - Adds locker information to the database
def create_locker(lockerID, email, floor, coords):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    if not does_locker_exist(lockerID):
        # Add locker to lockers table
        c.execute("INSERT INTO lockers VALUES('%s', '%s', %d, '%s')" % (lockerID, email, floor, coords))
        db.commit()
        db.close()
        print "Locker Creation Successful"
        return True
    print "Locker Creation Failed"
    return False

# Get lockers - Return string array of lockers associated with email
def get_lockers(email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    lockers = []
    # Query for lockers with email
    c.execute("SELECT lockerID FROM lockers WHERE email = '%s'" % (email))
    for locker_id in c:
        lockers.append(locker_id[0])
    return lockers

# Get email - Return the email associated with the locker
def get_email(lockerID):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for email with lockerID
    c.execute("SELECT email FROM lockers WHERE lockerID = '%s'" % (lockerID))
    for email in c:
        return email[0]
    
# Get floor - Return the locker's floor
def get_floor(lockerID):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for floor with lockerID
    c.execute("SELECT floor FROM lockers WHERE lockerID = '%s'" % (lockerID))
    for floor in c:
        return floor[0]

# Get coords - Return the coordinates of the locker
def get_coords(lockerID):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for coords with lockerID
    c.execute("SELECT coords FROM lockers WHERE lockerID = '%s'" % (lockerID))
    for coords in c:
        return coords[0]

# Set floor
def set_floor(lockerID, new_floor):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Update floor to new_floor
    c.execute("UPDATE lockers SET floor = %d WHERE lockerID = '%s'" % (new_floor, lockerID))
    db.commit()
    db.close()
    
# Set coords
def set_coords(lockerID, new_coords):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Update coords to new_coords
    c.execute("UPDATE lockers SET coords = '%s' WHERE lockerID = '%s'" % (new_coords, lockerID))
    db.commit()
    db.close()
    
# Remove locker - Return true when complete
def remove_locker(lockerID):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Delete row with lockerID from lockers table
    c.execute("DELETE FROM lockers WHERE lockerID = '%s'" % (lockerID))
    db.commit()
    db.close()
    return True

# Does locker exist - Return true if locker exists, false otherwise
def does_locker_exist(lockerID):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for locker with lockerID
    c.execute("SELECT lockerID FROM lockers WHERE lockerID = '%s'" % (lockerID))
    for locker in c:
        print "Locker exists"
        return True
    print "Locker does not exist"
    return False
    
    
# Transfer locker - Return true when complete
def transfer_locker(lockerID, fromEmail, toEmail):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Update locker email to new email
    c.execute("UPDATE lockers SET email = '%s' WHERE lockerID = '%s' AND email = '%s'" % (toEmail, lockerID, fromEmail))
    db.commit()
    db.close()
    return True

