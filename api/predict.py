from core.model import ModelWrapper
from flask_restplus import fields
from werkzeug.datastructures import FileStorage
from maxfw.core import MAX_API, PredictAPI, CustomMAXAPI

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


class ModelLabelsAPI(CustomMAXAPI):

    @MAX_API.doc('labels')
    def get(self):
        """Return the list of labels that can be predicted by the model"""

        labels = [{"id": 0, "name": 'background'},
                  {"id": 1, "name": 'aeroplane'},
                  {"id": 2, "name": 'bicycle'},
                  {"id": 3, "name": 'bird'},
                  {"id": 4, "name": 'boat'},
                  {"id": 5, "name": 'bottle'},
                  {"id": 6, "name": 'bus'},
                  {"id": 7, "name": 'car'},
                  {"id": 8, "name": 'cat'},
                  {"id": 9, "name": 'chair'},
                  {"id": 10, "name": 'cow'},
                  {"id": 11, "name": 'diningtable'},
                  {"id": 12, "name": 'dog'},
                  {"id": 13, "name": 'horse'},
                  {"id": 14, "name": 'motorbike'},
                  {"id": 15, "name": 'person'},
                  {"id": 16, "name": 'pottedplant'},
                  {"id": 17, "name": 'sheep'},
                  {"id": 18, "name": 'sofa'},
                  {"id": 19, "name": 'train'},
                  {"id": 20, "name": 'tv'}]

        return labels


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
