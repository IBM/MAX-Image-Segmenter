# Flask settings
DEBUG = False

# Flask-restplus settings
RESTPLUS_MASK_SWAGGER = False
SWAGGER_UI_DOC_EXPANSION = 'none'

# Application settings

# API metadata
API_TITLE = 'MAX Image Segmenter'
API_DESC = 'Identify objects in an image, additionally assigning each pixel of the image to a particular object'
API_VERSION = '1.1.0'

# default model
MODEL_NAME = 'deeplab'
DEFAULT_MODEL_PATH = 'assets/{}'.format(MODEL_NAME)
MODEL_LICENSE = 'Apache v2'

MODEL_META_DATA = {
    'id': API_TITLE.lower().replace(' ', '-'),
    'name': API_TITLE,
    'description': 'DeepLab TensorFlow model for semantic image segmentation, trained on VOCO 2012',
    'type': 'Object Detection',
    'license': MODEL_LICENSE,
    'source': 'https://developer.ibm.com/exchanges/models/all/max-image-segmenter'
}

_FULL_MODEL_PATH = "assets/frozen_inference_graph_full.pb"
_MOBILE_MODEL_PATH = "assets/frozen_inference_graph_mobile.pb" 