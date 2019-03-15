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

_FULL_MODEL_PATH = "/workspace/assets/deeplabv3_pascal_trainval_2018_01_04.tar.gz"
_MOBILE_MODEL_PATH = "/workspace/assets/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz"  # Mobile net version
