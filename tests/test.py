import pytest
import pycurl
import io
import json


def test_response():
    c = pycurl.Curl()
    b = io.BytesIO()
    c.setopt(pycurl.URL, 'http://localhost:5000/model/predict')
    c.setopt(pycurl.HTTPHEADER, ['Accept:application/json', 'Content-Type: multipart/form-data'])
    c.setopt(pycurl.HTTPPOST, [('image', (pycurl.FORM_FILE, "assets/stc.jpg"))])
    c.setopt(pycurl.WRITEFUNCTION, b.write)
    c.perform()
    assert c.getinfo(pycurl.RESPONSE_CODE) == 200
    c.close()

    response = b.getvalue()
    response = json.loads(response)

    assert response['status'] == 'ok'
    assert response['image_size'] == [513, 256]
    assert len(response['seg_map']) == response['image_size'][1]

    assert response['seg_map'][0][0] == 0  # there are no objects in the top left corner
    assert response['seg_map'][128][128] == 15  # there is a person here
    assert response['seg_map'][200][500] == 20  # computer monitor (labeled as "TV") in bottom right corner


if __name__ == '__main__':
    pytest.main([__file__])
