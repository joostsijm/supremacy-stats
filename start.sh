#!/bin/sh

"""
Run flask application
"""

export FLASK_APP=app/flaskr.py
export FLASK_DEBUG=1
flask run
