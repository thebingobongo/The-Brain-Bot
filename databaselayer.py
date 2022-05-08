import os

import pymysql
from dotenv import load_dotenv

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

def openTickets():
    cur.execute(f"SELECT * FROM opentickets;")
    res = cur.fetchall()
    return res


def addWarn(target, warn, submitter):
    cur.execute(f"INSERT INTO warns (discordid, warnmessage, submitterid, submittime) values ({target}, '{warn}', {submitter}, now());")
    con.commit()


def getWarns(target):
    cur.execute(f"SELECT * FROM warns WHERE discordid = {target};")
    res = cur.fetchall()
    return res


def deleteWarn(memberid, warn):
    cur.execute(f"DELETE FROM warns WHERE discordid = {memberid} AND warnmessage = '{warn}'")
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
    cur.execute(f"DELETE FROM notes WHERE discordid = {memberid} AND note = '{note}'")
    con.commit()


def getTodo():
    cur.execute("SELECT * FROM todo;")
    res = cur.fetchall()
    print(res)
    return res

def deleteTodo(todo_item):
    cur.execute(f"DELETE FROM todo WHERE todo_item = '{todo_item}';")
    con.commit()


def addTodo(todo_item):
    cur.execute(f"INSERT INTO todo (todo_item) values ('{todo_item}');")
    con.commit()


def getUserBal(memberID):
    cur.execute(f"SELECT * FROM users WHERE discordid = {memberID};")
    userbal = cur.fetchone()
    return userbal[1]


def updateUserBal(memberid, amount):
    cur.execute(f"UPDATE users SET balance = {amount} WHERE discordid = {memberid};")
    con.commit()


def resetBalance():
    cur.execute(f'UPDATE users SET balance = {0};')
    con.commit()


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


def addBounty(user_id, challenge, amount):
    cur.execute("INSERT INTO bounties (user_id, challenge, amount) VALUES (?,?,?);", (user_id, challenge, amount))
    con.commit()


def removeBounty(bounty_id):
    cur.execute("DELETE FROM bounties WHERE bounty_id=? ", (bounty_id,))
    con.commit()


def showBounties(user_id):
    cur.execute("SELECT * FROM bounties WHERE user_id=?", (user_id,))
    res = cur.fetchall()
    return res


def getBountyAmount(bounty_id):
    cur.execute("SELECT amount FROM bounties WHERE bounty_id=?", (bounty_id,))
    res = cur.fetchall()
    amount = res[0]
    return amount


def completeBounty(bounty_id):
    amount = getBountyAmount(bounty_id)
    removeBounty(bounty_id)
    return amount


# def addStock(user_id, stock_name, stock_price, quantity:int):
#     cur.execute(f"INSERT INTO stocks (discordid, stock_name, stockprice, quantity) values ('{user_id}', '{stock_name}', '{stock_price}', {quantity});")
#     con.commit()


# def getStocks(user_id, stock_name):
#     cur.execute(f"SELECT * FROM stocks WHERE user_id= ({user_id},) AND stock_name= {stock_name};")
#     res = cur.fetchall()
#     return res


# def getPortfolio(user_id):
#     cur.execute(f"SELECT * FROM stocks WHERE user_id= '{user_id}';")
#     res = cur.fetchall()
#     return res


# def getStocksbyPrice(user_id, stock_name, stock_price):
#     cur.execute(f"SELECT * FROM stocks WHERE user_id= ({user_id},) AND stock_name= {stock_name} AND stockprice= {stock_price};")
#     res = cur.fetchall()
#     return res


# def getQuantitybyPrice(user_id, stock_name, stock_price):
#     cur.execute(
#         f"SELECT quantity FROM stocks WHERE user_id= ({user_id},) AND stock_name= {stock_name} AND stockprice= {stock_price};")
#     res = cur.fetchall()
#     return res[0]


# def addQuantity(user_id, stock_name, stock_price, quantity_to_add:int):
#     quantity = getQuantitybyPrice(user_id,stock_name,stock_price)
#     quantity += quantity_to_add
#     deleteStock(user_id,stock_name, stock_price)
#     addStock(user_id, stock_name, stock_price, quantity)


# def delQuantity(user_id, stock_name, stock_price, quantity_to_add:int):
#     quantity_to_add =  -abs(quantity_to_add)
#     addQuantity(user_id, stock_name, stock_price, quantity_to_add)


# def deleteStock(user_id,stock_name, stock_price):
#     cur.execute(f"DELETE FROM stocks WHERE discordid=? ({user_id},) AND stock_name=? ({stock_name},) AND stockprice=? ({stock_price},);")
#     con.commit()

def getStocks(memberid, stock=None):
    if type(stock) == str:
        keywords = ["SELECT ", "DROP ", "WHERE "]
        for keyword in keywords:
            if keyword in stock:
                return []  # Malicious query, fuck off

    cur.execute(
        f"SELECT * FROM stocks WHERE discordid = {memberid}"
        + (f" AND stockname = '{stock.upper()}'" if stock != None else "")
        + " ORDER BY timestamp DESC;"
    )
    stocks = cur.fetchall()
    return list(stocks)


def hasStocks(memberid, stock, amount):
    shares = sum([x[3] for x in getStocks(memberid, stock)])
    return shares >= amount


def addStocks(memberid, stock, amount, price):
    cur.execute(
        f"INSERT INTO stocks (discordid, stockname, stockprice, quantitybought, timestamp) values ({memberid}, '{stock.upper()}', {price}, {amount}, NOW());"
    )
    con.commit()


def removeStocks(memberid, stock, amount):
    if not hasStocks(memberid, stock, amount):
        return

    stocks = getStocks(memberid, stock)

    i = 0
    num_to_remove = amount
    queries = []
    while num_to_remove > 0:
        print(queries)
        _, _, price, shares, timestamp = stocks[i]

        if shares > num_to_remove:
            num = num_to_remove
            query = f"UPDATE stocks SET quantitybought={shares - num}"
        else:
            num = shares
            query = "DELETE FROM stocks"

        query += f" WHERE discordid={memberid} AND stockname='{stock.upper()}' AND timestamp='{timestamp}';"
        queries.append(query)

        num_to_remove -= num
        i += 1

    for query in queries:
        print(query)
        cur.execute(query)

    con.commit()
