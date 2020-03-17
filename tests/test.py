# Copyright 2018-2019 IBM Corp. All Rights Reserved.
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
#

import os

import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'MAX Image Segmenter'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'max-image-segmenter'
    assert metadata['name'] == 'MAX Image Segmenter'
    assert metadata['description'] == 'DeepLab TensorFlow model for semantic image segmentation, trained on VOCO 2012'
    assert metadata['license'] == 'Apache v2'
    assert metadata['type'] == 'Object Detection'
    assert 'max-image-segmenter' in metadata['source']


def test_labels():

    label_endpoint = 'http://localhost:5000/model/labels'

    r = requests.get(url=label_endpoint)
    assert r.status_code == 200

    labels = r.json()
    assert len(labels) == 21
    assert labels[3]['id'] == 3
    assert labels[3]['name'] == 'bird'


def _get_image_size():

    DEFAULT_IMAGE_SIZE = 513

    image_size = os.environ.get('IMAGE_SIZE', default=str(DEFAULT_IMAGE_SIZE))
    if not image_size.isdigit():
        image_size = str(DEFAULT_IMAGE_SIZE)
    image_size = int(image_size)
    if not 16 <= image_size <= 1024:
        image_size = DEFAULT_IMAGE_SIZE

    return image_size


def _check_response(r):
    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    image_size = _get_image_size()
    assert response['image_size'] == [image_size, image_size // 2]
    assert len(response['seg_map']) == response['image_size'][1]

    assert response['seg_map'][0][0] == 0  # there are no objects in the top left corner
    if image_size == 513:
        assert response['seg_map'][130][170] == 15  # there is a person here
        assert response['seg_map'][200][500] == 20  # computer monitor (labeled as "TV") in bottom right corner
    elif image_size == 333:
        assert response['seg_map'][65][93] == 15  # there is a person here
        # computer monitor won't be detected here


def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    formats = ['jpg', 'png']
    file_path = 'tests/stc.{}'

    for f in formats:
        p = file_path.format(f)
        with open(p, 'rb') as file:
            file_form = {'image': (p, file, 'image/{}'.format(f))}
            r = requests.post(url=model_endpoint, files=file_form)
        _check_response(r)


if __name__ == '__main__':
    pytest.main([__file__])
