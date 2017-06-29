import sqlite3 as sql
from passlib.hash import sha256_crypt


db = 'database.db'


def connect(db):
    con = sql.connect(db)
    cur = con.cursor()
    return con, cur


def retrieveUsers():
    con, cur = connect(db)
    cur.execute("SELECT username, password FROM Users")
    users = cur.fetchall()
    con.close()
    users_list = [i[0] for i in users]
    return users_list


def registerUser(name, password):
    con, cur = connect(db)
    try:
        cur.execute("INSERT INTO Users (username, password) VALUES (?,?)",
                    (name, password))
    except sql.IntegrityError:
        return "Username already taken"
    con.commit()
    con.close()
    addUsers("Global", name)
    joinRoom(name, "Global")


def validateUser(name, password):
    con, cur = connect(db)
    cur.execute(
        "SELECT username, password FROM Users WHERE username = ?", (name,))
    user_details = cur.fetchone()
    con.close()
    if user_details and sha256_crypt.verify(password, user_details[1]):
        return True
    return False


def retrieveRooms():
    con, cur = connect(db)
    cur.execute("SELECT roomname FROM Rooms")
    rooms = cur.fetchall()
    rooms_list = []
    for i in rooms:
        rooms_list.append(i[0])
    return rooms_list


def storeMessage(msg, room):
    con, cur = connect(db)
    cur.execute("INSERT INTO History (message, room) VALUES (?,?)",
                (msg, room))
    con.commit()
    con.close()


def retrieveHistory(room):
    con, cur = connect(db)
    cur.execute("SELECT message FROM History WHERE room = ?", (room, ))
    msgs = cur.fetchall()
    con.close()
    msgs_list = []
    for i in msgs:
        msgs_list.append(i[0])
    return msgs_list


def usersRooms(name):
    con, cur = connect(db)
    cur.execute("SELECT rooms FROM Users WHERE username =?", (name,))
    rooms = cur.fetchone()
    con.close()
    if rooms[0]:
        rooms_list = []
        rooms_list.append(rooms[0].split(', '))
        rooms_list[0].pop()
        return rooms_list[0]
    return []


def joinRoom(name, room):
    con, cur = connect(db)
    rooms = usersRooms(name)
    rooms.append(room)
    r = ""
    for i in rooms:
        r += i + ", "
    cur.execute("UPDATE Users SET rooms = ? WHERE username = ? ", (r, name,))
    con.commit()
    con.close()


def leaveRoom(name, room):
    con, cur = connect(db)
    rooms = usersRooms(name)
    rooms.remove(room)
    r = ""
    for i in rooms:
        r += i + ", "
    cur.execute("UPDATE Users SET rooms = ? WHERE username = ? ", (r, name,))
    con.commit()
    con.close()


def createRoom(room):
    con, cur = connect(db)
    cur.execute("INSERT INTO Rooms (roomname, admin) VALUES (?,?)",
                (room, admin,))
    cur.execute(
        """CREATE TABLE IF NOT EXISTS room_{}
         (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL) """.format(room))
    con.commit()
    con.close()


def deleteRoom(room):
    users = roomsUsers(room)
    con, cur = connect(db)
    cur.execute("DELETE FROM Rooms WHERE roomname = ?", (room,))
    cur.execute("DROP TABLE room_{}".format(room))
    con.commit()
    con.close()
    for user in users:
        leaveRoom(user, room)
    deleteRoomHistory(room)


def deleteRoomHistory(room):
    con, cur = connect(db)
    cur.execute("DELETE FROM History WHERE room = ?", (room,))
    con.commit()
    con.close()


def addUsers(room, users):
    con, cur = connect(db)
    if type(users) is list:
        for user in users:
            cur.execute(
                "INSERT INTO room_{} (username) VALUES (?)".format(room,),
                (user,))
    else:
        cur.execute(
            "INSERT INTO room_{} (username) VALUES (?)".format(room,),
            (users,))
    con.commit()
    con.close()


def removeUsers(room, users):
    con, cur = connect(db)
    if type(users) is list:
        for user in users:
            cur.execute(
                "DELETE FROM room_{} WHERE username = ?".format(room, ),
                (user,))
    else:
        cur.execute(
            "INSERT INTO room_{} (username) VALUES (?)".format(room,),
            (users,))
    con.commit()
    con.close()


def getAdmin(room):
    con, cur = connect(db)
    cur.execute("SELECT admin from rooms WHERE roomname = ?", (room,))
    admin = cur.fetchone()
    con.close()
    if admin:
        return admin[0]
    return admin


def roomsUsers(room):
    con, cur = connect(db)
    cur.execute("SELECT username FROM room_{}".format(room))
    users = cur.fetchall()
    con.close()
    users_list = []
    for user in users:
        users_list.append(user[0])
    return users_list
