import os
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
if app.config['CORS_ENABLE'] == True:
    CORS(app, origins='*')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
