FROM codait/max-base:v1.1.3

ARG model_bucket=https://max.cdn.appdomain.cloud/max-image-segmenter/1.1.0

ARG model_file=assets.tar.gz

ARG use_pre_trained_model=true

WORKDIR /workspace
RUN if [ "$use_pre_trained_model" = "true" ] ; then\
      wget -nv --show-progress --progress=bar:force:noscroll ${model_bucket}/${model_file} --output-document=assets/${model_file} && \
      tar -x -C assets/ -f assets/${model_file} -v && rm assets/${model_file}; \
    fi

COPY requirements.txt /workspace
RUN pip install -r requirements.txt

COPY . /workspace

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

CMD python /workspace/app.py
