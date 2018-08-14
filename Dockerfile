FROM codait/max-base

RUN mkdir -p /workspace/assets

RUN pip install numpy && \
    pip install tensorflow && \
    pip install pillow

RUN wget -nv --show-progress --progress=bar:force:noscroll http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/deeplabv3_pascal_trainval_2018_01_04.tar.gz && \
  mv deeplabv3_pascal_trainval_2018_01_04.tar.gz /workspace/assets/deeplabv3_pascal_trainval_2018_01_04.tar.gz

RUN tar -x -C /workspace/assets -f /workspace/assets/deeplabv3_pascal_trainval_2018_01_04.tar.gz -v && rm /workspace/assets/deeplabv3_pascal_trainval_2018_01_04.tar.gz

ENV MODEL_TYPE="full"

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
