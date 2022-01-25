import sqlite3
import os

conn = sqlite3.connect('data.db')
cur = conn.cursor()

def CheckUsername(username):
    if len(username) <= 3 :
        return False
    for ch in username :
        if not ch.isalnum() :
            return False
    return True

def CheckPassword(password):
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

def CheckKey(key):
    if len(key) != 64:
        return False
    return True

def CheckUserLogin(username, password):
	cur = conn.cursor()

	cur.execute("SELECT password FROM BDD WHERE username=:username",{"username":username})
	ret = cur.fetchall()
	if len(ret) != 1 or password != ret[0][0] :
		return False
	return True

def CheckIP(ip):
    
    List_elem=ip.split('.')
    is_in_limit=True
    number_only=True
    is_size_limit=True

    if len(List_elem) != 4:
        is_size_limit = False
        return is_size_limit

    for elem in List_elem:
        if elem.isdecimal()==False:
            number_only = False
            return number_only
        
        if (int(elem) < 0 or int(elem) > 255):
            is_in_limit=False
            return is_in_limit
    return True

def bdd_creation():

    sql = "DROP TABLE IF EXISTS BDD"
    cur.execute(sql)
    conn.commit()

    sql = '''CREATE TABLE BDD (
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
				  ip TEXT NOT NULL,
				  clef_pub TEXT NOT NULL
           );'''
	
    cur.execute(sql)
    conn.commit()
    print("Base de données crée et correctement connectée à SQLite")
    return True

def bdd_ajout(username, password, ip, clef_pub):
    test_username = CheckUsername(username)
    test_password = CheckPassword(password)
    test_ip = CheckIP(ip)
    test_clef = CheckKey(clef_pub)
    test_user_login = CheckUserLogin(username,password)

    if test_user_login == True :
        return False
    if (test_clef and test_ip and test_password and test_username) == False:
        return False
    
    sql = "INSERT INTO bdd (username, password, ip, clef_pub) VALUES (?, ?, ?, ?)"
    value = (username, password, ip, clef_pub)
    cur.execute(sql, value)
    conn.commit()
    print("Ajout d'infos")
    bdd_affich()
    return True

def bdd_affich():
	cur.execute("SELECT * FROM bdd")
	result = cur.fetchall()
	for row in result:
		print(row)
		print("\n")

def bdd_fermer():
	cur.close()
	conn.close()
	print("Connexion SQLite est fermée")