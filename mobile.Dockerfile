FROM codait/max-base

RUN mkdir -p /workspace/assets

RUN pip install numpy && \
    pip install tensorflow && \
    pip install pillow

RUN wget -nv --show-progress --progress=bar:force:noscroll http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/mobile/frozen_inference_graph.pb && \
  mv frozen_inference_graph.pb /workspace/assets/mobile.pb

ENV MODEL_TYPE="mobile"

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
