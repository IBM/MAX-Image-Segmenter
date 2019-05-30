FROM codait/max-base:v1.1.3

ARG model_bucket=http://max-assets.s3.us.cloud-object-storage.appdomain.cloud/image-segmenter/1.0
ARG model_file=assets.tar.gz

ARG use_pre_trained_model=true

WORKDIR /workspace
RUN if [ "$use_pre_trained_model" = "true" ] ; then\
  wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
  tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

# check file integrity
# RUN md5sum -c md5sums.txt


RUN if [ "$use_pre_trained_model" = "false" ] ; then \
      # rename the directory that contains the custom-trained model artifacts
      mv /workspace/custom_assets/* /workspace/assets; \
    fi
RUN ls -Ral /workspace/assets/

EXPOSE 5000

CMD python /workspace/app.py
