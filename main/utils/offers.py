#offers
import sqlite3
import lockers

# Create offer - Returns true if successful, false otherwise
def create_offer(lockerID, type, price, description):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    if not does_offer_exist(lockerID, type):
        # Add offer to offers table
        c.execute("INSERT INTO offers VALUES('%s', %d, %d, '%s')" % (lockerID, type, price, description))
        db.commit()
        db.close()
        print "Offer Creation Successful"
        return True
    print "Offer Creation Failed"
    return False

# Get offer - Returns dictionary of info
def get_offer(lockerID, type):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT * FROM offers WHERE lockerID = '%s' AND type = %d" % (lockerID, type))

    for offer in c:
        price = offer[2]
        description = offer[3]
        dict = {"lockerID": lockerID, "type": type, "price": price, "description": description, "email": lockers.get_email(lockerID)}
        return dict
    
# Get price
def get_price():
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for price with lockerID and type
    c.execute("SELECT price FROM offers WHERE lockerID = '%s' AND type = %d" % (lockerID, type))
    for price in c:
        return price[0]

# Get description
def get_description():
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Query for description with lockerID and type
    c.execute("SELECT description FROM offers WHERE lockerID = '%s' AND type = %d" % (lockerID, type))
    for description in c:
        return description[0]

# Set type
def set_type(lockerID, type, new_type):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Update type to new_type
    c.execute("UPDATE offers SET type = %d WHERE lockerID = '%s' AND type = %d" % (new_type, lockerID, type))
    db.commit()
    db.close()
    
# Set price
def set_price(lockerID, type, new_price):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Update price to new_price
    c.execute("UPDATE offers SET price = %d WHERE lockerID = '%s' AND type = %d" % (new_price, lockerID, type))
    db.commit()
    db.close()

# Set description
def set_description(lockerID, type, new_description):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Update description to new_description
    c.execute("UPDATE offers SET description = %d WHERE lockerID = '%s' AND type = %d" % (new_description, lockerID, type))
    db.commit()
    db.close()


# Checks if offer exists - Returns true if offer exists, false otherwise
def does_offer_exist(lockerID, type):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT lockerID FROM offers WHERE lockerID = '%s' AND type = %d" % (lockerID, type))
    for offer in c:
        # Offer exists
        print "Offer exists"
        return True
    print "Offer does not exist"
    return False

# Remove offer - Returns true when complete
def remove_offer(lockerID, type):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Delete row with lockerID and type from offers table
    c.execute("DELETE FROM offers WHERE lockerID = '%s' AND type = %d" % (lockerID, type))
    db.commit()
    db.close()
    return True

# Get all offers - Returns array of offer dictionaries
def get_all_offers():
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    offers = []
    c.execute("SELECT * FROM offers")

    # Append each offer dictionary to offers
    for offer in c:
        offers.append(get_offer(offer[0], offer[1]))
        
    return offers

# Get latest offers - Return n latest sales or trades
def get_latest_offers(n, type):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    offers = []
    c.execute("SELECT * FROM offers WHERE type = %d ORDER BY price LIMIT %d" % (type, n))
    
    # Append each offer dictionary to offers
    for offer in c:
        offers.append(get_offer(offer[0], offer[1]))

    return offers
    
