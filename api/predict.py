from core.model import ModelWrapper
from flask_restplus import fields
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI

# set up parser for image input data
input_parser = MAX_API.parser()
input_parser.add_argument('image', type=FileStorage, location='files', required=True,
                          help='An image file (encoded as PNG or JPG/JPEG)')


predict_response = MAX_API.model('ModelPredictResponse', {
    'status': fields.String(required=True, description='Response status message'),
    'image_size': fields.List(fields.Integer,
                              description="The size of the output image segmentation map (may differ from input image)"),
    'seg_map': fields.List(fields.List(fields.Integer,
                                       description="Segmentation map containing a predicted class for each pixel"))
})


class ModelPredictAPI(PredictAPI):

    model_wrapper = ModelWrapper()

    @MAX_API.doc('predict')
    @MAX_API.expect(input_parser)
    @MAX_API.marshal_with(predict_response)
    def post(self):
        """Make a prediction given input data"""
        result = {'status': 'error'}

        args = input_parser.parse_args()
        image_data = args['image'].read()
        image = self.model_wrapper._read_image(image_data)

        resized_im, seg_map = self.model_wrapper.predict(image)

        result['image_size'] = resized_im.size

        result['seg_map'] = seg_map
        result['status'] = 'ok'

        return result
