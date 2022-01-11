"""UserSrv

Usage:
	UserSrv.py --port=<int>

Options:
	-h --help     Show this screen.
	--port=<int>  port used

"""
import sqlite3
import logging
from docopt import docopt
from flask import Flask
from flask import Response
from flask import request


conn = sqlite3.connect('data.db')
cur = conn.cursor()

APP = Flask(__name__)

@APP.route('/isalive', methods=['GET'])
def is_alive():
	return Response(status=200)

# 
@APP.route('/user', methods=['POST']) 
def post_json():
	data = request.get_json()
	name = data.get('name', '')
	ip = data.get('ip', '')
	return data

def bdd_creation():
	
	sql = "DROP TABLE IF EXISTS bdd"
	cur.execute(sql)
	conn.commit()

	sql = '''CREATE TABLE bdd (
                  id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
				  pseudo TEXT NOT NULL,
                  password TEXT NOT NULL,
				  ip TEXT NOT NULL,
				  clef_pub TEXT NOT NULL,
				  clef_priv TEXT NOT NULL

           );'''
	
	cur.execute(sql)
	conn.commit()
	print("Base de données crée et correctement connectée à SQLite")

def bdd_ajout(id, name, pseudo, password, ip, clef_pub, clef_priv):
	sql = "INSERT INTO bdd (id, name, pseudo, password, ip, clef_pub, clef_priv) VALUES (?, ?, ?, ?, ?, ?, ?)"
	value = (id, name, pseudo, password, ip, clef_pub, clef_priv)
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

if __name__ == '__main__':
	
	bdd_creation()
	
	bdd_ajout(1, "Nikolaï", "Niko", "B345" , "123.876.45.67", "FDFGHUYTF45", "FHYTRDVBHGGTRDE78")
	bdd_ajout(2, "Bob", "Brico", "12345", "234.456.78.89", "GHIKYUFFDH90", "FGHZENKJFG23")

	bdd_affich()
	
	ARGS = docopt(__doc__)
	
	if ARGS['--port']:
		APP.run(host='0.0.0.0', port=ARGS['--port'])
	else:
		logging.error("Wrong command line arguments")
	
	bdd_fermer()
