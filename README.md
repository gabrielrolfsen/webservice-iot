# Debaisu's Webservice

This project is a python webserver designed to respond to Debaisu Conn Application requests.

## Supported Requests

* Login and Logout
* List connected devices
* Get light bulb specific information
* Action on Light Bulb (On-Off)

## Dependencies

```
- Python v3.0 or higher
- Python [Virtual Environment](http://flask.pocoo.org/docs/0.12/installation/#virtualenv)
- SQLite database
```

## Installation
### On OS X:

1. Install python [virtual environment](http://flask.pocoo.org/docs/0.12/installation/#virtualenv)

    ```sudo pip install virtualenv```
2. Setup virtual environment on project

    ```python3 -m venv flask```
3. Activate virtual environment

    ```. flask/bin/activate```
4. Setup environment variables

    ```export FLASK_APP=webservice_iot/webservice_iot.py```
5. (Fresh Start) Re-initialize database

    ```flask initdb```
6. Run application

    ```flask run```

