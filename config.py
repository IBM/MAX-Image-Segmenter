# Flask settings
DEBUG = True

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# Application settings

# API metadata
API_TITLE = 'Model Asset Exchange Server'
API_DESC = 'An API for serving models'
API_VERSION = '0.1'

# default model
MODEL_NAME = 'deeplab'
DEFAULT_MODEL_PATH = 'assets/{}'.format(MODEL_NAME)
MODEL_LICENSE = 'Apache v2'

MODEL_META_DATA = {
    'id': '{}-tf'.format(MODEL_NAME.lower()),
    'name': '{} TensorFlow Model'.format(MODEL_NAME),
    'description': '{} TensorFlow model trained on VOCO 2012'.format(MODEL_NAME),
    'type': 'image_classification',
    'license': '{}'.format(MODEL_LICENSE)
}

_FULL_MODEL_PATH = "/workspace/assets/full.pb"
_MOBILE_MODEL_PATH = "/workspace/assets/mobile.pb"  # Mobile net version
