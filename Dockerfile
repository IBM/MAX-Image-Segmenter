FROM continuumio/miniconda3

RUN mkdir -p /workspace/assets

RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/deeplabv3_pascal_trainval_2018_01_04.tar.gz && \
  mv deeplabv3_pascal_trainval_2018_01_04.tar.gz /workspace/assets/deeplabv3_pascal_trainval_2018_01_04.tar.gz

# Mobile net version
RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz && \
  mv deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz /workspace/assets/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz


RUN pip install --upgrade pip && \
	pip install numpy && \
    pip install tensorflow && \
    pip install pillow && \
    pip install flask-restplus

COPY . /workspace

EXPOSE 5000

CMD python workspace/app.py
