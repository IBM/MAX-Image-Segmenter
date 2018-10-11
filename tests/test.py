import pytest
import requests


def test_swagger():

    model_endpoint = 'http://localhost:5000/swagger.json'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200
    assert r.headers['Content-Type'] == 'application/json'

    json = r.json()
    assert 'swagger' in json
    assert json.get('info') and json.get('info').get('title') == 'Model Asset Exchange Server'


def test_metadata():

    model_endpoint = 'http://localhost:5000/model/metadata'

    r = requests.get(url=model_endpoint)
    assert r.status_code == 200

    metadata = r.json()
    assert metadata['id'] == 'deeplab-tf'
    assert metadata['name'] == 'deeplab TensorFlow Model'
    assert metadata['description'] == 'deeplab TensorFlow model trained on VOCO 2012'
    assert metadata['license'] == 'Apache v2'


def test_predict():
    model_endpoint = 'http://localhost:5000/model/predict'
    file_path = 'assets/stc.jpg'

    with open(file_path, 'rb') as file:
        file_form = {'image': (file_path, file, 'image/jpeg')}
        r = requests.post(url=model_endpoint, files=file_form)
    assert r.status_code == 200
    response = r.json()

    assert response['status'] == 'ok'
    assert response['image_size'] == [513, 256]
    assert len(response['seg_map']) == response['image_size'][1]

    assert response['seg_map'][0][0] == 0  # there are no objects in the top left corner
    assert response['seg_map'][128][128] == 15  # there is a person here
    assert response['seg_map'][200][500] == 20  # computer monitor (labeled as "TV") in bottom right corner


if __name__ == '__main__':
    pytest.main([__file__])
