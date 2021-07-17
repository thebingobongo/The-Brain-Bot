import os
from dotenv import load_dotenv
import pymysql

load_dotenv()
hostname = os.getenv('HOST')
passwd = os.getenv('PASSWD')

connection = None
con = pymysql.connect(host=hostname, user='admin',
                      passwd=passwd, database='thevat')
cur = con.cursor()
cur.execute("USE thevat")


def getLeaderBoard(limit=10):
    cur.execute(f"SELECT * FROM users ORDER BY balance DESC LIMIT {limit}")
    res = cur.fetchall()
    return res


def hasOpenTicket(memberid):
    cur.execute(f"SELECT * FROM opentickets WHERE discordid = {memberid};")
    if cur.rowcount == 0:
        return False
    else:
        return True


def createTicket(memberid):
    cur.execute(f"INSERT INTO opentickets (discordid) value({memberid})")
    con.commit()


def closeTicket(memberid):
    cur.execute(f"DELETE FROM opentickets WHERE discordid = '{memberid}';")
    con.commit()

def addWarn(target, warn, submitter):
    cur.execute(
        f"INSERT INTO warns (discordid, warnmessage, submitterid, submittime) values ({target}, '{warn}', {submitter}, now());")
    con.commit()


def getWarns(target):
    cur.execute(f"SELECT * FROM warns WHERE discordid = {target};")
    res = cur.fetchall()
    return res


def deleteWarn(memberid, warn):
    cur.execute(f"DELETE FROM warns WHERE discordid = {memberid} AND warnmessage = {warn}")
    con.commit()


def addNote(target, note, submitter):
    cur.execute(
        f"INSERT INTO notes (discordid, note, submitterid, submittime) values ({target}, '{note}', {submitter}, now());")
    con.commit()


def getNotes(target):
    cur.execute(f"SELECT * FROM notes WHERE discordid = {target};")
    res = cur.fetchall()
    return res


def deleteNote(memberid, note):
    cur.execute(f"DELETE FROM notes WHERE discordid = {memberid} AND note = {note}")
    con.commit()


def getUserBal(memberID):
    cur.execute(f"SELECT * FROM users WHERE discordid = {memberID};")
    userbal = cur.fetchone()
    return userbal[1]


def updateUserBal(memberid, ammount):
    cur.execute(f"UPDATE users SET balance = {ammount} WHERE discordid = {memberid};")
    con.commit()


def addBal(memberid, ammount):
    bal = getUserBal(memberid)
    bal = int(bal) + int(ammount)
    updateUserBal(memberid, bal)


def subBal(memberid, ammount):
    bal = getUserBal(memberid)
    bal = int(bal) - int(ammount)
    updateUserBal(memberid, bal)


def hasEnough(memberid, ammount):
    bal = getUserBal(memberid)
    if bal >= ammount:
        return True
    else:
        return False


def getUserRole(discordid):
    cur.execute(f"SELECT * FROM users WHERE discordid = {discordid};")
    userrole = cur.fetchone()
    return userrole[2]


def updateUserRole(discordid, roleid):
    cur.execute(f"UPDATE users SET roleid = {roleid} WHERE discordid = {discordid};")
    con.commit()


def createUser(discordid):
    cur.execute(f"INSERT INTO users (discordid, balance, roleid) values ({discordid}, 200, 831213206155952179);")
    con.commit()


def deleteUser(discordid):
    cur.execute(f"delete from users where discordid = '{discordid}';")


def getInventory(discordid):
    cur.execute(f"SELECT * FROM inventory WHERE discordid = '{discordid}';")
    res = cur.fetchall()
    return res


def hasItem(discordid, itemname):
    cur.execute(f"SELECT * FROM inventory WHERE discordid = '{discordid}' AND item_name = '{itemname}';")
    return cur.rowcount != 0


def addItem(discordid, itemname):
    cur.execute(f"INSERT INTO inventory (discordid, item_name) values ('{discordid}', '{itemname}');")
    con.commit()


def removeItem(discordid, itemname):
    cur.execute(f"DELETE FROM inventory WHERE discordid = '{discordid}' AND item_name = '{itemname}';")
    con.commit()