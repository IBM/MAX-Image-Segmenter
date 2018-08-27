FROM codait/max-base

ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab
ARG model_file=full.pb.tar.gz

RUN pip install numpy && \
    pip install tensorflow && \
    pip install pillow

RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}
RUN tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}


ENV MODEL_TYPE="full"

COPY . /workspace

EXPOSE 5000

CMD python /workspace/app.py
