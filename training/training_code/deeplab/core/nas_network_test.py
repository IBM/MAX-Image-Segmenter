# Copyright 2018 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

"""Tests for resnet_v1_beta module."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import numpy as np
import tensorflow as tf

from deeplab.core import nas_genotypes
from deeplab.core import nas_network

arg_scope = tf.contrib.framework.arg_scope
slim = tf.contrib.slim


def create_test_input(batch, height, width, channels):
  """Creates test input tensor."""
  if None in [batch, height, width, channels]:
    return tf.placeholder(tf.float32, (batch, height, width, channels))
  else:
    return tf.to_float(
        np.tile(
            np.reshape(
                np.reshape(np.arange(height), [height, 1]) +
                np.reshape(np.arange(width), [1, width]),
                [1, height, width, 1]),
            [batch, 1, 1, channels]))


class NASNetworkTest(tf.test.TestCase):
  """Tests with complete small NAS networks."""

  def _pnasnet_small(self,
                     images,
                     num_classes,
                     is_training=True,
                     output_stride=16,
                     final_endpoint=None):
    """Build PNASNet model backbone."""
    hparams = tf.contrib.training.HParams(
        filter_scaling_rate=2.0,
        num_conv_filters=10,
        drop_path_keep_prob=1.0,
        total_training_steps=200000,
    )
    if not is_training:
      hparams.set_hparam('drop_path_keep_prob', 1.0)

    backbone = [1, 2, 2]
    cell = nas_genotypes.PNASCell(hparams.num_conv_filters,
                                  hparams.drop_path_keep_prob,
                                  len(backbone),
                                  hparams.total_training_steps)
    with arg_scope([slim.dropout, slim.batch_norm], is_training=is_training):
      return nas_network._build_nas_base(
          images,
          cell=cell,
          backbone=backbone,
          num_classes=num_classes,
          hparams=hparams,
          reuse=tf.AUTO_REUSE,
          scope='pnasnet_small',
          final_endpoint=final_endpoint)

  def testFullyConvolutionalEndpointShapes(self):
    num_classes = 10
    inputs = create_test_input(2, 321, 321, 3)
    with slim.arg_scope(nas_network.nas_arg_scope()):
      _, end_points = self._pnasnet_small(inputs,
                                          num_classes)
      endpoint_to_shape = {
          'Stem': [2, 81, 81, 128],
          'Cell_0': [2, 41, 41, 100],
          'Cell_1': [2, 21, 21, 200],
          'Cell_2': [2, 21, 21, 200]}
      for endpoint, shape in endpoint_to_shape.iteritems():
        self.assertListEqual(end_points[endpoint].get_shape().as_list(), shape)


if __name__ == '__main__':
  tf.test.main()
