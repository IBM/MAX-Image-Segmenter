FROM quay.io/codait/max-base:v1.4.0

ARG model_bucket=https://codait-cos-max.s3.us.cloud-object-storage.appdomain.cloud/max-image-segmenter/1.1.0

ARG model_file=assets.tar.gz

ARG use_pre_trained_model=true

RUN if [ "$use_pre_trained_model" = "true" ] ; then\
      wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
      tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}; \
    fi

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN if [ "$use_pre_trained_model" = "true" ] ; then \
      # validate downloaded pre-trained model assets
      sha512sum -c sha512sums.txt ; \
    else \
      # rename the directory that contains the custom-trained model artifacts
      if [ -d "./custom_assets/" ] ; then \
        rm -rf ./assets && ln -s ./custom_assets ./assets ; \
      fi \
    fi

EXPOSE 5000

CMD python app.py
