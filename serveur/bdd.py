import sqlite3


def connect_db():
    conn = sqlite3.connect('data.db')
    cur = conn.cursor()
    return conn,cur

def check_username(username):
    if len(username) <= 3 :
        return False
    for ch in username:
        if not ch.isalnum():
            return False
    return True

def check_password(password):
    if len(password) < 8:
        return False

    if any(not char.isalnum() for char in password) == False:
        return False
    if any(char.isnumeric() for char in password) == False:
        return False
    if any(char.isupper() for char in password) == False:
        return False
    if any(char.islower() for char in password) == False:
        return False
    return True


def check_key(key):
    if len(key) != 64:
        return False
    return True

def check_user_login(username, password):

    conn,cur=connect_db()

    cur.execute("SELECT password FROM BDD WHERE username=:username",{"username":username})
    ret = cur.fetchall()

    bdd_close(conn,cur)
    if len(ret) != 1 or password != ret[0][0] :
        return False
    return True


def check_ip(ip):
    List_elem_port = ip.split(":")
    List_elem_ip = List_elem_port[0].split(".")

    is_in_limit_ip = True
    number_only_ip = True
    is_size_limit_ip = True

    # Test IP
    if len(List_elem_ip) != 4:
        is_size_limit_ip = False
        return is_size_limit_ip

    for elem in List_elem_ip:
        if elem.isdecimal() == False:
            number_only_ip = False
            return number_only_ip

        if int(elem) < 0 or int(elem) > 255:
            is_in_limit_ip = False
            return is_in_limit_ip

    is_empty_port = True
    number_only_port = True
    is_size_limit_port = True
    is_positif_port = True

    # Test Port
    if len(List_elem_port) != 2:
        is_size_limit_port = False
        return is_size_limit_port

    if len(List_elem_port[1]) < 1:
        is_empty_port = False
        return is_empty_port

    for elem_port in List_elem_port[1]:
        if elem_port.isnumeric() == False:
            number_only_port = False
            return number_only_port

    if int(List_elem_port[1]) < 0:
        is_positif_port = False
        return is_positif_port

    return True


def bdd_creation():
    conn,cur=connect_db()

    sql = "DROP TABLE IF EXISTS BDD"
    cur.execute(sql)
    conn.commit()

    sql = """CREATE TABLE BDD (
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
                  ip TEXT NOT NULL,
                  clef_pub TEXT NOT NULL
           );"""
    
    cur.execute(sql)
    conn.commit()
    bdd_close(conn,cur)
    print("Data base correctly launched")
    return True

def bdd_add(username, password, ip, clef_pub):
    conn,cur=connect_db()

    test_username = check_username(username)
    test_password = check_password(password)
    test_ip = check_ip(ip)
    test_clef = check_key(clef_pub)
    test_user_login = check_user_login(username,password)

    if test_username==False:
        return 455
    elif test_ip==False:
        return 456
    elif test_password==False:
        return 457

    elif test_clef==False:
        return 458
    elif test_user_login==True:
        return 459

    sql = "INSERT INTO bdd (username, password, ip, clef_pub) VALUES (?, ?, ?, ?)"
    value = (username, password, ip, clef_pub)
    cur.execute(sql, value)
    conn.commit()
    bdd_close(conn,cur)
    print("Ajout d'infos")
    bdd_show()
    return 1

def bdd_get_ip_port(username):
    conn,cur=connect_db()

    cur.execute("SELECT ip FROM BDD WHERE username=:username",{"username":username})
    ret = cur.fetchall()

    bdd_close(conn,cur)
    if len(ret) != 1:
        return False, False
    List_elem_port = ret[0][0].split(":")
    return List_elem_port[0],List_elem_port[1]

def bdd_show():
    conn,cur=connect_db()
    cur.execute("SELECT * FROM bdd")
    result = cur.fetchall()
    for row in result:
        print(row)
        print("\n")
    bdd_close(conn,cur)

def bdd_close(conn,cur):
    cur.close()
    conn.close()
    print("SQLite connection is closed")

