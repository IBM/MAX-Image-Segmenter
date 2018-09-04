from __future__ import print_function
import os
import sys
import logging
from flask import Flask
from api import api
from flask_cors import CORS
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

# load default config
app.config.from_object('config')
# load override config if exists
if 'APP_CONFIG' in os.environ:
    app.config.from_envvar('APP_CONFIG')
api.init_app(app)
# enable CORS if flag set in config
if os.getenv('CORS_ENABLE') == 'true' and \
os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
    CORS(app, origins='*')
    app.logger.info('\033[92m' + \
    'NOTE: MAX Model Server is currently allowing ' + \
    'cross-origin requests - ' + \
    '\033[1m' + '(CORS ENABLED)' + '\033[0m' + \
    '\033[0m')    

if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    app.run(host='0.0.0.0')
