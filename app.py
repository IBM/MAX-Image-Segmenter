from __future__ import print_function
import os
import sys
from flask import Flask
from api import api
from flask_cors import CORS

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
    print('\033[92m' + \
    'NOTE: MAX model server is currently allowing cross-origin requests - ' + \
    '\033[1m' + '(CORS ENABLED)' + '\033[0m' + \
    '\033[0m', file=sys.stderr)    

if __name__ == '__main__':
    app.run(host='0.0.0.0')
