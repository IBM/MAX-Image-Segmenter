import pytest
import requests


def test_response():
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
