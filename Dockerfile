FROM codait/max-base

RUN mkdir -p /workspace/assets

RUN pip install numpy && \
    pip install tensorflow && \
    pip install pillow

RUN wget -nv --show-progress --progress=bar:force:noscroll http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/full.pb && \
  mv full.pb /workspace/assets/full.pb

ENV MODEL_TYPE="full"

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
