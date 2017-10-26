import os
import sqlite3
import time
from .servo import Servo
from .light_bulb import Light_bulb
from flask import Flask, request, session, g, redirect, url_for, abort, flash, Response, json,jsonify

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'main.db'),
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('WEBSERVER_SETTINGS', silent=True)

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_FORBIDDEN = 401

motor = Servo()
bulb = Light_bulb()

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/sign-up', methods=['POST'])
def sign_up():
    db = get_db()

    # Gets the JSON content received 
    content = request.get_json()

    # if: pin code is valid, register! / else: invalid pin code
    if (content['pin_code'] == "123"):
        # Gets actual time
        time_now = time.strftime("%c")

        # Inserts the new user into the database
        cursor = db.execute("INSERT INTO users (name, username, password, access_level, creation_date) VALUES (?, ?, ?, ?, ?)",
            (content['name'], content['username'], content['password'], "1", time_now))
        db.commit()
        return "User created", STATUS_CREATED

    else:
        data = {'error': 'Pin code invalid'}
        return jsonify(data), STATUS_FORBIDDEN


@app.route('/login', methods=['POST'])
def login():
    db = get_db()

    # Gets the JSON content received 
    content = request.get_json()

    # Search the database for a row with the username and password received in JSON file
    cursor = db.execute('SELECT * FROM users WHERE username=? AND password=?', (content['username'], content['password']))
    row = cursor.fetchone()

    # if: username and/or password don't exist / else: Login!!
    if row is None:
        data = {'error': 'Username and/or password not valid'}
        return jsonify(data), STATUS_FORBIDDEN
    else:
        session['logged_in'] = True
        data = {'name': row[1], 'username': row[2], 'password': row[3]}
        return jsonify(data), STATUS_OK

@app.route('/logout', methods=['POST'])
def logout():
    # Logout even if the user is not logged in
    session.pop('logged_in', None)
    return "LOGOUT SUCCESSFUL"

#@app.route('/devices')
#def list_devices():
#    db = get_db()
#    cursor = db.execute('SELECT * FROM devices')
#    # Descobrir com pega todos os resultados do banco
#    return cursor.fetchAll()

@app.route('/devices', methods=['POST'])
def action_device():
    db = get_db()
    device_id = request.form['id']
    action = request.form['action']
    cursor = db.execute('SELECT type FROM devices WHERE id=?', device_id)
    # TODO: verify if this is the best way to do it
    fetched = cursor.fetchone()
    if (fetched):
        type = fetched['type']
        if type == 1: # tipo 1: fechadura
            if action == 'OPEN':
                motor.open()
            else:
                motor.close()
        elif type == 2: #tipo2: lampada
            if action == 'ON':
                bulb.light_on()
            else:
                bulb.light_off()

    # retorna se deu certo ou nao e um payload que vcs decidem
    return "", STATUS_OK
