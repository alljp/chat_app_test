import sqlite3 as sql
from passlib.hash import sha256_crypt
# con = sql.connect("database.db")
# cur = con.cursor()


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM Users")
    users = cur.fetchall()
    con.close()
    return users


def registerUser(name, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Users (username,password) VALUES (?,?)",
                (name, password))
    con.commit()
    con.close()
    print(name, password)


def validateUser(name, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(
        "SELECT username, password FROM Users WHERE username = ?", (name,))
    user_details = cur.fetchone()
    con.close()
    print("\n\nreached")
    print(user_details)
    if user_details and sha256_crypt.verify(password, user_details[1]):
        print("\n\nsuccess")
        return True
    return False
