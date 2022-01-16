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
    if len(key) != 128:
        return False
    return True

def CheckUserLogin(username, password):
	cur = conn.cursor()

	cur.execute("SELECT password FROM users WHERE username=:username",{"username":username})
	ret = cur.fetchall()
	if len(ret) != 1 or password != ret[0][0] :
		conn.close()
		return False
	return True

def CheckDbHealth():
	cur = conn.cursor()
	cur.execute("SELECT * FROM BDD")
	ret = cur.fetchall()
	if len(ret) == 0 :
		return True # empty Db is healthy..?
	for usr in ret :
		if any ([not CheckUsername(usr[0]) , not CheckPassword(usr[1]),
			not CheckIP(usr[2]) , not CheckKey(usr[3])]):
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
    sql = "INSERT INTO bdd (username, password, ip, clef_pub) VALUES (?, ?, ?, ?)"
    value = (username, password, ip, clef_pub)
    cur.execute(sql, value)
    conn.commit()
    print("Ajout d'infos")

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