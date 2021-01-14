import json
import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector

port = 80

def format_Content(db_content, db_desc):
    dictionnary = dict()
    for value in db_content:
        dictionnary[str(value[0])] = dict()
        for i in range(1, len(db_desc)):
            dictionnary[str(value[0])][str(db_desc[i][0])] = str(value[i])

    return dictionnary

def database_connection(table : str):
    simulation_db = mysql.connector.connect(
        host = "172.17.0.2",
        user = "api_rest",
        password = "f83FFLssPzpamV0g",
        database = "Simulateur-db"
    )

    simulation_db_requester = simulation_db.cursor()
    simulation_db_requester.execute("SELECT * FROM " + table)
    db_content = simulation_db_requester.fetchall()
    db_desc = simulation_db_requester.description

    simulation_db_requester.close()
    simulation_db.close()

    print(db_desc)
    return format_Content(db_content, db_desc)

def get_200(self, content):
    self.send_response(200)
    self.send_header('Content-type','application/json')
    self.end_headers()
    self.wfile.write(json.dumps(content, indent=4, sort_keys=True).encode())

def get_404(self):
    self.send_response(404)
    self.send_header('Content-type','application/json')
    self.end_headers()
    self.wfile.write("Error 404 - Content not found".encode())

def get_HistorySimuDB(self):
    db_content = database_connection("History")
    get_200(self, db_content)

def get_CasernesSimuDB(self):
    db_content = database_connection("Casernes")
    get_200(self, db_content)

def get_CamionsSimuDB(self):
    db_content = database_connection("Camions")
    get_200(self, db_content)

def get_PompierSimuDB(self):
    db_content = database_connection("Pompier")
    get_200(self, db_content)

def get_FeuxSimuDB(self):
    db_content = database_connection("Feux")
    get_200(self, db_content)

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == '/Simulateur-db/history':
            get_HistorySimuDB(self)
        elif self.path == '/Simulateur-db/casernes':
            get_CasernesSimuDB(self)
        elif self.path == '/Simulateur-db/camions':
            get_CamionsSimuDB(self)
        elif self.path == '/Simulateur-db/pompier':
            get_PompierSimuDB(self)
        elif self.path == '/Simulateur-db/feux':
            get_FeuxSimuDB(self)
        else:
            get_404(self)

api_rest = HTTPServer(('', port), myHandler)
print("Api-Rest started on port: " + str(port))

api_rest.serve_forever()