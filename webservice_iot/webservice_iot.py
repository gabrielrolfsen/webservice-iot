##############################################################################################
#                                                                                            #
# Caso executar fora de um raspberry pi, comentar a linha 6 (import RPi.GPIO as GPIO) e as   #
# rotinas de interrupcao ao fim do codigo. Comentar tambem todas mencoes GPIO nos arquivos   #
# light_bulb e servo.                                                                        #
#                                                                                            #
##############################################################################################

import os
import sqlite3
import time
import threading
import RPi.GPIO as GPIO
from .servo import Servo
from .light_bulb import Light_bulb
from flask import Flask, request, session, g, redirect, url_for, abort, flash, Response, json, jsonify

app = Flask(__name__)
app.config.from_object(__name__)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'main.db'),
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('WEBSERVER_SETTINGS', silent=True)
app.config["JSON_SORT_KEYS"] = False

STATUS_OK = 200
STATUS_CREATED = 201
STATUS_FORBIDDEN = 401
STATUS_NOT_FOUND = 404

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


# Sign-up attempt and callback
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


# Login attempt and callback
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


# Logout attempt and callback
@app.route('/logout', methods=['POST'])
def logout():

    # Logout even if the user is not logged in
    session.pop('logged_in', None)
    return Response("",STATUS_OK)


# Returns the list of available devices
@app.route('/devices', methods=['GET'])
def list_devices():
    db = get_db()
    
    # Search the database for all devices
    cursor = db.execute('SELECT * FROM devices')
    row = cursor.fetchone()

    # if: One device available at least / else: no devices available
    if row is not None:
        dic = {'query': []}

        while row is not None:
            data = {'id': str(row[0]), 'name': row[1], 'type': str(row[2]), 'status': row[3], 'last_active_time': row[4]}
            dic['query'].append(data)
            row = cursor.fetchone()

        return jsonify(dic['query']), STATUS_OK

    else:
        data = {'error': 'No available devices'}
        return jsonify(data), STATUS_NOT_FOUND

#To Do @brunohideki
#@app.route('/door_lock/<id>', methods=['GET'])
#def door_lock_details(id):

# Returns the data of the lamp with id = <id>
@app.route('/light_bulb/<id>', methods=['GET'])
def light_bulb_details(id):
    db = get_db()

    # Search the database for a row with id received in parameter of the endpoint and parameter = 2 (light_bulb)
    cursor = db.execute('SELECT * FROM devices WHERE id=? AND type=2', id)
    row = cursor.fetchone()

    # if: Device is valid, return your data / else: unespected error
    if row is not None:
        data = {'id': str(row[0]), "name": row[1], 'type': str(row[2]), 'status': row[3], 'dimmer_value': str(bulb.dimmer_value),
            'last_activate_time': row[4]}
        return jsonify(data), STATUS_OK

    else:
        data = {'error': 'Unspected error'}
        return jsonify(data), STATUS_FORBIDDEN


@app.route('/devices/action', methods=['POST'])
def action_device():
    db = get_db()

    # Gets the JSON content received 
    content = request.get_json()

    # Search the database for a row with id received in parameter of the endpoint
    cursor = db.execute('SELECT * FROM devices WHERE id=?', content['id'])
    row = cursor.fetchone()

    if row is not None:

        # fechadura
        if (content['type'] == "1"):
            print("Acao no motor") 
            #To Do @brunohideki

        # Lighting Behaviors
        elif (content['type'] == "2"): 
            if (content['action'] == "CHANGE_STATUS"):
                if(content['value'] == "ON"):
                    bulb.light_on()

                elif(content['value'] == "OFF"):
                    bulb.light_off()

                else:
                    data = {'error': 'Value field is wrong'}
                    return jsonify(data), STATUS_FORBIDDEN

            elif (content['action'] == "DIMMER"):
                value = int(content['value'])
                bulb.set_dimmer_value(value)

            else:
                data = {'error': 'Action field is wrong'}
                return jsonify(data), STATUS_FORBIDDEN

            # Updates the database with the new status and last action time
            time_now = time.strftime("%c")
            cursor = db.execute("UPDATE devices SET status=?, last_active_time=? WHERE id=?", 
                (bulb.light_status, time_now, content['id']))
            db.commit()

            data = {"id": content['id'], "type": content['type'], "status": bulb.light_status, "dimmer": str(bulb.dimmer_value)}
            return jsonify(data), STATUS_OK

        else:
            data = {'error': 'Type field is wrong'}
            return jsonify(data), STATUS_FORBIDDEN
    else:
        data = {'error': 'Unspected error'}
        return jsonify(data), STATUS_FORBIDDEN

    # Comportamento default, lembrar de retirar quando o metodo estiver completo    
    return "", STATUS_OK

###################################### Interrupt ######################################################

# When the power button is pressed the code calls this routine
def button_press(channel):
    with app.app_context():

        db = get_db()

        if (bulb.light_status == "OFF"):
            bulb.light_on()

        else:
            bulb.light_off()

        # Updates the database with the new status and last action time
        time_now = time.strftime("%c")
        cursor = db.execute("UPDATE devices SET status=?, last_active_time=? WHERE type=2", 
            (bulb.light_status, time_now))
        db.commit()

# When the alternating current goes through zero the code calls this routine
def zero_cross_detected(channel):

        if(bulb.dimmer_value == 0):
            if (bulb.light_status == "ON"):
                GPIO.output(15, GPIO.LOW)

        elif(bulb.dimmer_value == 10):
            if (bulb.light_status == "OFF"):
                GPIO.output(15, GPIO.HIGH)

        else:
            time.sleep(bulb.timer_dimmer)
            GPIO.output(15, GPIO.HIGH)
            time.sleep(0.000006)
            GPIO.output(15, GPIO.LOW)

# Interrupt when the power button is pressed
GPIO.add_event_detect(19, GPIO.FALLING, callback=button_press, bouncetime = 1000)
# Interrupt when alternating current goes through zero volts
GPIO.add_event_detect(16, GPIO.RISING, callback=zero_cross_detected, bouncetime = 8)
