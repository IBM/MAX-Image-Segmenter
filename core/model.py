# This file contains code from https://github.com/tensorflow/models/blob/master/research/deeplab/deeplab_demo.ipynb
# and was released under an Apache 2 license
import os
import tarfile
import numpy as np
import tensorflow as tf
import warnings
from config import _FULL_MODEL_PATH
from config import _MOBILE_MODEL_PATH
from PIL import Image
import io
import logging
from config import MODEL_META_DATA as model_meta
from maxfw.model import MAXModelWrapper

logger = logging.getLogger()


# Import model parameters as environmental variables if they were passed to docker run
model_type = os.environ.get('MODEL_TYPE', default='mobile')
image_size = int(os.environ.get('IMAGE_SIZE', default=513))

if (image_size < 16) or (image_size > 1024):
    image_size = 513
    warnings.warn('image size not in range 16 to 1024, reverted to default image size of 513')

if (model_type != 'full') and (model_type != 'mobile'):
    model_type = 'mobile'
    warnings.warn('model type not mobile or full, reverted to default model type mobile')


class DeepLabModel(object):
    """Class to load deeplab model and run inference."""

    INPUT_TENSOR_NAME = 'ImageTensor:0'
    OUTPUT_TENSOR_NAME = 'SemanticPredictions:0'
    FROZEN_GRAPH_NAME = 'frozen_inference_graph'

    def __init__(self, tarball_path):
        """Creates and loads pre-trained deeplab model."""
        self.graph = tf.Graph()

        graph_def = None
        # Extract frozen graph from tar archive.
        tar_file = tarfile.open(tarball_path)
        for tar_info in tar_file.getmembers():
            if self.FROZEN_GRAPH_NAME in os.path.basename(tar_info.name):
                file_handle = tar_file.extractfile(tar_info)
                graph_def = tf.GraphDef.FromString(file_handle.read())
                break

        tar_file.close()

        if graph_def is None:
            raise RuntimeError('Cannot find inference graph in tar archive.')

        with self.graph.as_default():
            tf.import_graph_def(graph_def, name='')

        self.sess = tf.Session(graph=self.graph)

    def run(self, image):
        """Runs inference on a single image.

        Args:
          image: A PIL.Image object, raw input image.

        Returns:
          resized_image: RGB image resized from original input image.
          seg_map: Segmentation map of `resized_image`.
        """
        width, height = image.size
        resize_ratio = 1.0 * image_size / max(width, height)
        target_size = (int(resize_ratio * width), int(resize_ratio * height))
        resized_image = image.convert('RGB').resize(target_size, Image.ANTIALIAS)
        batch_seg_map = self.sess.run(
            self.OUTPUT_TENSOR_NAME,
            feed_dict={self.INPUT_TENSOR_NAME: [np.asarray(resized_image)]})
        seg_map = batch_seg_map[0]
        return resized_image, seg_map


class ModelWrapper(MAXModelWrapper):
    """Model wrapper for TensorFlow models in SavedModel format"""
    MODEL_META_DATA = model_meta

    def __init__(self):
        # Set model path based on environmental variable
        if model_type == 'full':
            self.model = DeepLabModel(_FULL_MODEL_PATH)
        if model_type == 'mobile':
            self.model = DeepLabModel(_MOBILE_MODEL_PATH)

    def _read_image(self, image_data):
        try:
            image = Image.open(io.BytesIO(image_data))
        except Exception as excptn:
            print(str(excptn))
            from flask import abort
            abort(400, "The provided input is not a valid image.")

        return image

    def _predict(self, x):
        resized_im, seg_map = self.model.run(x)

        return resized_im, seg_map
