#trades
import sqlite3
import lockers
import offers

# Create trade - Returns true if successful, false otherwise
def create_trade(lockerID, your_lockerID, to_email, from_email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    if not does_trade_exist(lockerID, your_lockerID, to_email, from_email):
        c.execute("INSERT INTO trades VALUES('%s', '%s', '%s', '%s')" % (lockerID, your_lockerID, to_email, from_email))
        db.commit()
        db.close()
        print "Trade Request Sent"
        return True
    print "Trade Request Failed"
    return False

# Get your trades - Returns dictionary of your trade requests
def get_your_trades(to_email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT * FROM trades WHERE to_email = '%s'" % (to_email))
    trades = []
    for trade in c:
        dict = {"lockerID": trade[1], "your_lockerID": trade[0], "to_email": trade[2], "from_email": trade[3]}
        trades.append(dict)
    return trades
    

# Accept trade - Returns true when complete
def accept_trade(lockerID, your_lockerID, to_email, from_email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    # Transfer ownership
    lockers.transfer_locker(lockerID, to_email, from_email)
    lockers.transfer_locker(your_lockerID, from_email, to_email)
    # Delete your offer
    offers.remove_offer(your_lockerID, 1)
    # Delete trade
    remove_trade(lockerID, your_lockerID, to_email, from_email)

    db.commit()
    db.close()
    return True

# Remove trade - Returns trade from trades db
def remove_trade(lockerID, your_lockerID, to_email, from_email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("DELETE FROM trades WHERE lockerID = '%s'" % (your_lockerID))
    db.commit()
    db.close()
    return True
    
# Does trade exist - Returns true if trade exists, false otherwise
def does_trade_exist(lockerID, your_lockerID, to_email, from_email):
    db = sqlite3.connect("utils/database.db")
    c = db.cursor()
    c.execute("SELECT * FROM trades WHERE lockerID = '%s' AND your_lockerID = '%s' AND to_email = '%s' AND from_email = '%s'" % (lockerID, your_lockerID, to_email, from_email))
    for trade in c:
        # Trade exists
        print "Trade exists"
        return True
    c.execute("SELECT * FROM trades WHERE lockerID = '%s' AND your_lockerID = '%s' AND to_email = '%s' AND from_email = '%s'" % (your_lockerID, lockerID, from_email, to_email))
    for trade in c:
        # Trade exists
        print "Trade exists"
        return True
    print "Trade does not exist"
    return False
