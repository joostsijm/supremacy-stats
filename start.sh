#!/bin/sh

#
# Run Flask application
#

export FLASK_APP=app/flaskr.py
export FLASK_DEBUG=1
flask run
