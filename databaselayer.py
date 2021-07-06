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

def getUserBal(memberID):
    cur.execute(f"SELECT * FROM users WHERE discordid = {memberID}")
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
        return False
    else:
        return True


def getUserRole(discordid):
    cur.execute(f"SELECT * FROM users WHERE discordid = {discordid}")
    userrole = cur.fetchone()
    return userrole[2]


def updateUserRole(discordid,roleid):
    cur.execute(f"UPDATE users SET roleid = {roleid} WHERE discordid = {discordid};")
    con.commit()


def createUser(discordid):
    cur.execute(f"INSERT INTO users (discordid, balance, roleid) values ({discordid}, 200, 831213206155952179)")
    con.commit()


def deleteUser(discordid):
    cur.execute(f"delete from users where discordid = {discordid}")