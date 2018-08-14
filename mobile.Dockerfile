FROM codait/max-base

RUN mkdir -p /workspace/assets

RUN pip install numpy && \
    pip install tensorflow && \
    pip install pillow

RUN wget -nv --show-progress --progress=bar:force:noscroll http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz && \
  mv deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz /workspace/assets/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz

RUN tar -x -C /workspace/assets -f /workspace/assets/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz -v && rm /workspace/assets/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz

ENV MODEL_TYPE="mobile"

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
