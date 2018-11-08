FROM codait/max-base

ARG model_bucket=http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/image-segmenter/1.0
ARG model_file=assets.tar.gz

WORKDIR /workspace
RUN wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=/workspace/assets/${model_file}
RUN tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

# RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/deeplabv3_pascal_trainval_2018_01_04.tar.gz && \
#   mv deeplabv3_pascal_trainval_2018_01_04.tar.gz /workspace/assets/deeplabv3_pascal_trainval_2018_01_04.tar.gz

# Mobile net version
# RUN wget -nv http://max-assets.s3-api.us-geo.objectstorage.softlayer.net/deeplab/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz && \
#   mv deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz /workspace/assets/deeplabv3_mnv2_pascal_trainval_2018_01_29.tar.gz

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

RUN md5sum -c md5sums.txt  # check file integrity

EXPOSE 5000

CMD python /workspace/app.py
