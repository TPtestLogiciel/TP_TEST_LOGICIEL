import sqlite3
import os

conn = sqlite3.connect('data.db')
cur = conn.cursor()


def CheckUsername(username):

	return False

def CheckPassword(password):

	return False

def CheckKey(key):

	return False

def CheckUserLogin(username, password):
    return False

def CheckDbHealth():
    return False


def bdd_creation():

    sql = "DROP TABLE IF EXISTS BDD"
    cur.execute(sql)
    conn.commit()

    sql = '''CREATE TABLE BDD (
                  username TEXT NOT NULL,
                  password TEXT NOT NULL,
				  ip TEXT NOT NULL,
				  clef_pub TEXT NOT NULL,
				  clef_priv TEXT NOT NULL
           );'''
	
    cur.execute(sql)
    conn.commit()
    print("Base de données crée et correctement connectée à SQLite")
    return True

def bdd_ajout(username, password, ip, clef_pub, clef_priv):
    sql = "INSERT INTO bdd (username, password, ip, clef_pub, clef_priv) VALUES (?, ?, ?, ?, ?)"
    value = (username, password, ip, clef_pub, clef_priv)
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