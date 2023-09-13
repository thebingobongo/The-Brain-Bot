import os

import pymysql
from dotenv import load_dotenv

load_dotenv()
hostname = os.getenv('HOST')
passwd = os.getenv('PASSWD')

connection = None
con = pymysql.connect(host=hostname, user='admin',
                      passwd=passwd, database='thevat')



def getLeaderBoard(limit=10):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM users ORDER BY balance DESC LIMIT {limit}")
    res = cur.fetchall()
    cur.close()
    return res


def hasOpenTicket(memberid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM opentickets WHERE discordid = {memberid};")
    cur.close()
    if cur.rowcount == 0:
        return False
    else:
        return True


def createTicket(memberid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"INSERT INTO opentickets (discordid) value({memberid})")
    con.commit()
    cur.close()


def closeTicket(memberid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"DELETE FROM opentickets WHERE discordid = '{memberid}';")
    con.commit()
    cur.close()

def openTickets():
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM opentickets;")
    res = cur.fetchall()
    cur.close()
    return res


def addWarn(target, warn, submitter):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"INSERT INTO warns (discordid, warnmessage, submitterid, submittime) values ({target}, '{warn}', {submitter}, now());")
    con.commit()
    cur.close()


def getWarns(target):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM warns WHERE discordid = {target};")
    res = cur.fetchall()
    cur.close()
    return res


def deleteWarn(memberid, warn):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"DELETE FROM warns WHERE discordid = {memberid} AND warnmessage = '{warn}'")
    con.commit()
    cur.close()


def addNote(target, note, submitter):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(
        f"INSERT INTO notes (discordid, note, submitterid, submittime) values ({target}, '{note}', {submitter}, now());")
    con.commit()
    cur.close()


def getNotes(target):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM notes WHERE discordid = {target};")
    res = cur.fetchall()
    cur.close()
    return res


def deleteNote(memberid, note):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"DELETE FROM notes WHERE discordid = {memberid} AND note = '{note}'")
    con.commit()
    cur.close()


def getTodo():
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute("SELECT * FROM todo;")
    res = cur.fetchall()
    cur.close()
    return res

def deleteTodo(todo_item):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"DELETE FROM todo WHERE todo_item = '{todo_item}';")
    con.commit()
    cur.close()


def addTodo(todo_item):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"INSERT INTO todo (todo_item) values ('{todo_item}');")
    con.commit()
    cur.close()


def getUserBal(memberID):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM users WHERE discordid = {memberID};")
    userbal = cur.fetchone()
    cur.close()
    return userbal[1]


def updateUserBal(memberid, amount):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"UPDATE users SET balance = {amount} WHERE discordid = {memberid};")
    con.commit()
    cur.close()


def resetBalance():
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f'UPDATE users SET balance = {0};')
    con.commit()
    cur.close()


def addBal(memberid, amount):
    bal = getUserBal(memberid)
    bal = int(bal) + int(amount)
    updateUserBal(memberid, bal)


def subBal(memberid, amount):
    bal = getUserBal(memberid)
    bal = int(bal) - int(amount)
    updateUserBal(memberid, bal)


def hasEnough(memberid, amount):
    bal = getUserBal(memberid)
    if bal >= amount:
        return True
    else:
        return False


def getUserRole(discordid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM users WHERE discordid = {discordid};")
    userrole = cur.fetchone()
    cur.close()
    return userrole[2]


def updateUserRole(discordid, roleid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"UPDATE users SET roleid = {roleid} WHERE discordid = {discordid};")
    con.commit()
    cur.close()


def createUser(discordid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"INSERT INTO users (discordid, balance, roleid) values ({discordid}, 200, 831213206155952179);")
    con.commit()
    cur.close()


def deleteUser(discordid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"delete from users where discordid = '{discordid}';")
    cur.close()


def getInventory(discordid):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM inventory WHERE discordid = '{discordid}';")
    res = cur.fetchall()
    cur.close()
    return res


def hasItem(discordid, itemname):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"SELECT * FROM inventory WHERE discordid = '{discordid}' AND item_name = '{itemname}';")
    cur.close()
    return cur.rowcount != 0


def addItem(discordid, itemname):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"INSERT INTO inventory (discordid, item_name) values ('{discordid}', '{itemname}');")
    con.commit()
    cur.close()


def removeItem(discordid, itemname):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute(f"DELETE FROM inventory WHERE discordid = '{discordid}' AND item_name = '{itemname}';")
    con.commit()
    cur.close()


def addBounty(user_id, challenge, amount):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute("INSERT INTO bounties (user_id, challenge, amount) VALUES (?,?,?);", (user_id, challenge, amount))
    con.commit()
    cur.close()


def removeBounty(bounty_id):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute("DELETE FROM bounties WHERE bounty_id=? ", (bounty_id,))
    con.commit()
    cur.close()


def showBounties(user_id):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute("SELECT * FROM bounties WHERE user_id=?", (user_id,))
    res = cur.fetchall()
    cur.close()
    return res


def getBountyAmount(bounty_id):
    cur = con.cursor()
    cur.execute("USE thevat")
    cur.execute("SELECT amount FROM bounties WHERE bounty_id=?", (bounty_id,))
    res = cur.fetchall()
    amount = res[0]
    cur.close()
    return amount


def completeBounty(bounty_id):
    amount = getBountyAmount(bounty_id)
    removeBounty(bounty_id)
    return amount

