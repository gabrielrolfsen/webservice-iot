import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, flash, Response

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
    name = request.form['name']
    username = request.form['username']
    password = request.form['password']
    cur = db.execute("INSERT INTO users (name, username, pass, access) VALUES (?, ?, ?, ?)",
        (name, username, password, "1"))
    db.commit()
    return "Ok", STATUS_CREATED

@app.route('/login', methods=['POST'])
def login():
    db = get_db()
    username = request.form['username']
    password = request.form['password']
    cursor = db.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    # TODO: get user from database
    if (cursor.fetchone() > 0):
        session['logged_in'] = True
        return Response("", STATUS_OK)

    return Response("{\n\"error:\": \"Login not valid\"\n}", STATUS_FORBIDDEN)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return "OK"
