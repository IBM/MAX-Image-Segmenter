from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from config import MODEL_META_DATA
from core.backend import ModelWrapper, read_image

api = Namespace('model', description='Model information and inference operations')

model_meta = api.model('ModelMetadata', {
    'id': fields.String(required=True, description='deeplab'),
    'name': fields.String(required=True, description='mobilenetv2_coco_voc_trainval / xception_coco_voc_trainval'),
    'description': fields.String(required=True, description='Models trained on VOCO 2012. See https://github.com/tensorflow/models/blob/master/research/deeplab/g3doc/model_zoo.md'),
    'license': fields.String(required=False, description='Apache v2')
})


@api.route('/metadata')
class Model(Resource):
    @api.doc('get_metadata')
    @api.marshal_with(model_meta)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA


label_prediction = api.model('LabelPrediction', {
    'label_id': fields.String(required=False, description='Label identifier'),
    'label': fields.String(required=True, description='Class label'),
    'probability': fields.Float(required=True)
})


predict_response = api.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'image_size': fields.List(fields.Integer),
    'seg_map': fields.List(fields.List(fields.Integer))
})

# set up parser for image input data
image_parser = api.parser()
image_parser.add_argument('image', type=FileStorage, location='files', required=True)


@api.route('/predict')
class Predict(Resource):
    model_wrapper = ModelWrapper()

    @api.doc('predict')
    @api.expect(image_parser)
    @api.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = image_parser.parse_args()
        image_data = args['image'].read()
        image = read_image(image_data)

        resized_im, seg_map = self.model_wrapper.predict(image)

        result['image_size'] = resized_im.size

        result['seg_map'] = seg_map
        result['status'] = 'ok'

        return result
