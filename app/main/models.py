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
    users_list = [i[0] for i in users]
    return users_list


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
    if user_details and sha256_crypt.verify(password, user_details[1]):
        return True
    return False


def retrieveRooms():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT roomname FROM Rooms")
    rooms = cur.fetchall()
    rooms_list = []
    for i in rooms:
        rooms_list.append(i[0])
    return rooms_list


def storeMessage(msg, room):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO History (message, room) VALUES (?,?)",
                (msg, room))
    con.commit()
    con.close()


def retrieveHistory(room):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT message FROM History WHERE room = ?", (room, ))
    msgs = cur.fetchall()
    msgs_list = []
    for i in msgs:
        msgs_list.append(i[0])
    return msgs_list


def usersRooms(name):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT rooms FROM Users WHERE username =?", (name,))
    rooms = cur.fetchone()
    rooms_list = []
    rooms_list.append(rooms[0].split(', '))
    rooms_list[0].pop()
    return rooms_list[0]


def joinRoom(name, room):
    con = sql.connect("database.db")
    cur = con.cursor()
    rooms = usersRooms(name)
    rooms.append(room)
    r = ""
    for i in rooms:
        r += i + ", "
    cur.execute("UPDATE Users SET rooms = ? WHERE username = ? ", (r, name,))
    con.commit()
    con.close()


def leaveRoom(name, room):
    con = sql.connect("database.db")
    cur = con.cursor()
    rooms = usersRooms(name)
    rooms.remove(room)
    r = ""
    for i in rooms:
        r += i + ", "
    cur.execute("UPDATE Users SET rooms = ? WHERE username = ? ", (r, name,))
    con.commit()
    con.close()


def createRoom(room, admin):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO Rooms (roomname, admin) VALUES (?,?)",
                (room, admin,))
    cur.execute(
        """CREATE TABLE IF NOT EXISTS room_{}
         (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL) """.format(room))
    con.commit()
    con.close()


def deleteRoom(room):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM Rooms WHERE roomname = ?", (room,))
    con.commit()
    con.close()


def addUsers(room, users):
    con = sql.connect("database.db")
    cur = con.cursor()
    for user in users:
        cur.execute(
            "INSERT INTO room_{} (username) VALUES (?)".format(room,), (user,))
        con.commit()
    con.close()


def removeUsers(room, users):
    con = sql.connect("database.db")
    cur = con.cursor()
    for user in users:
        cur.execute(
            "DELETE FROM room_{} WHERE username = ?".format(room, ), (user,))
        con.commit()
    con.close()


def getAdmin(room):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT admin from rooms WHERE roomname = ?", (room,))
    return cur.fetchone()[0]


def roomsUsers(room):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username FROM room_{}".format(room))
    users = cur.fetchall()
    users_list = []
    for user in users:
        users_list.append(user[0])
    return users_list
