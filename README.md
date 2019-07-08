[![Build Status](https://travis-ci.org/IBM/MAX-Image-Segmenter.svg?branch=master)](https://travis-ci.org/IBM/MAX-Image-Segmenter) [![Website Status](https://img.shields.io/website/http/max-image-segmenter.max.us-south.containers.appdomain.cloud/swagger.json.svg?label=api+demo)](http://max-image-segmenter.max.us-south.containers.appdomain.cloud/)  
[<img src="docs/deploy-max-to-ibm-cloud-with-kubernetes-button.png" width="400px">](http://ibm.biz/max-to-ibm-cloud-tutorial) 

# IBM Developer Model Asset Exchange: Image Segmentation

This repository contains code to instantiate and deploy an image segmentation model. This model takes an image file as
an input and returns a segmentation map containing a predicted class for each pixel in the input image.

This repository contains 2 models trained on PASCAL VOC 2012. One model is trained using the xception architecture and
produces very accurate results but takes a few seconds to run and the other model is trained on MobileNetV2 and is
faster but less accurate. You can specify which model you wish to use when you start the Docker image. See below for
more details.

The segmentation map returns an integer between 0 and 20 that corresponds to one of the labels below for each pixel in
the input image. The first nested array corresponds to the top row of pixels in the image and the first element in that
array corresponds to the pixel at the top left hand corner of the image. NOTE: the image will be resized and the
segmentation map refers to pixels in the resized image, not the original input image.

| Id | Label       | Id | Label       | Id | Label       |
|----|-------------|----|-------------|----|-------------|
| 0  | background  | 7  | car         | 14 | motorbike   |
| 1  | aeroplane   | 8  | cat         | 15 | person      |
| 2  | bicycle     | 9  | chair       | 16 | pottedplant |
| 3  | bird        | 10 | cow         | 17 | sheep       |
| 4  | boat        | 11 | diningtable | 18 | sofa        |
| 5  | bottle      | 12 | dog         | 19 | train       |
| 6  | bus         | 13 | horse       | 20 | tv          |

The model files are hosted on IBM Cloud Object Storage. The code in this repository deploys the model as a web service
in a Docker container. This repository was developed as part of the [IBM Code Model Asset Exchange](https://developer.ibm.com/code/exchanges/models/) and the public API is powered by [IBM Cloud](https://ibm.biz/Bdz2XM).

## Model Metadata

| Domain        | Application                 | Industry | Framework  | Training Data                                                   | Input Data Format |
|---------------|-----------------------------|----------|------------|-----------------------------------------------------------------|-------------------|
| Image & Video | Object Detection | General    | Tensorflow | VOC2012 ~10k images | Image (PNG/JPG) |


## References

* _Haozhi Qi, Zheng Zhang, Bin Xiao, Han Hu, Bowen Cheng, Yichen Wei, Jifeng Dai_, [Deformable Convolutional Networks -- COCO Detection and Segmentation Challenge 2017 Entry](http://presentations.cocodataset.org/COCO17-Detect-MSRA.pdf). ICCV COCO Challenge
    Workshop, 2017.

* _Mark Everingham, S. M. Ali Eslami, Luc Van Gool, Christopher K. I. Williams, John M. Winn, Andrew Zisserman_, [The Pascal Visual Object Classes Challenge: A Retrospective](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/). IJCV, 2014.

* _Tsung-Yi Lin, Michael Maire, Serge Belongie, Lubomir Bourdev, Ross Girshick, James Hays, Pietro Perona, Deva Ramanan, C. Lawrence Zitnick, Piotr Dollar_, [Microsoft COCO: Common Objects in Context](http://cocodataset.org/). In the Proc. of ECCV, 2014.


## Licenses

| Component | License | Link  |
| ------------- | --------  | -------- |
| This repository | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [LICENSE](LICENSE) |
| Model Code (3rd party) | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [TensorFlow Models Repository](https://github.com/tensorflow/models/blob/master/LICENSE) |
| Model Weights | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [TensorFlow Models Repository](https://github.com/tensorflow/models/blob/master/LICENSE) |
| Test Samples | [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) | [Sample README](samples/README.md)


## Prerequisites

* `docker`: The [Docker](https://www.docker.com/) command-line interface. Follow the [installation instructions](https://docs.docker.com/install/) for your system.
* The minimum recommended resources for this model is 2GB Memory and 2 CPUs.


# Steps

1. [Deploy from Docker Hub](#deploy-from-docker-hub)
2. [Deploy on Kubernetes](#deploy-on-kubernetes)
3. [Run Locally](#run-locally)
4. [Retrain the Model on Watson Machine Learning](#retrain-the-model-on-watson-machine-learning)

## Deploy from Docker Hub

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 codait/max-image-segmenter
```

This will pull a pre-built image from Docker Hub (or use an existing image if already cached locally) and run it.
If you'd rather checkout and build the model locally you can follow the [run locally](#run-locally) steps below.

## Deploy on Kubernetes

You can also deploy the model on Kubernetes using the latest docker image on Docker Hub.

On your Kubernetes cluster, run the following commands:

```
$ kubectl apply -f https://raw.githubusercontent.com/IBM/MAX-Image-Segmenter/master/max-image-segmenter.yaml
```

The model will be available internally at port `5000`, but can also be accessed externally through the `NodePort`.

A more elaborate tutorial on how to deploy this MAX model to production on [IBM Cloud](https://ibm.biz/Bdz2XM) can be found [here](http://ibm.biz/max-to-ibm-cloud-tutorial).

## Run Locally

To build and deploy the model to a REST API using Docker, follow these steps:

1. [Build the Model](#1-build-the-model)
2. [Deploy the Model](#2-deploy-the-model)
3. [Use the Model](#3-use-the-model)
4. [Run the Notebook](#4-run-the-notebook)
5. [Development](#5-development)
6. [Cleanup](#6-cleanup)


### 1. Build the Model

Clone the `MAX-Image-Segmenter` repository locally. In a terminal, run the following command:

```
$ git clone https://github.com/IBM/MAX-Image-Segmenter.git
```

Change directory into the repository base folder: 

```
$ cd MAX-Image-Segmenter
```

To build the docker image locally, run:

```
$ docker build -t max-image-segmenter .
```

All required model assets will be downloaded during the build process. _Note_ that currently this docker image is CPU only (we will add support for GPU images later).


### 2. Deploy the Model

To run the docker image, which automatically starts the model serving API, run:

```
$ docker run -it -p 5000:5000 max-image-segmenter
```

If you would like to specify what model or image size to load into the model, use -e flags to pass the API environmental variables:

```
$ docker run -it -e MODEL_TYPE='mobile' -e IMAGE_SIZE=333 -p 5000:5000 max-image-segmenter
```

By default, Cross-Origin Resource Sharing (CORS) is disabled. To _enable_ CORS support, include the following -e flag with your run command:

```
$ docker run -it -e CORS_ENABLE='true' -p 5000:5000 max-image-segmenter
```

_Note_ extra parameter info:
* Model types available: 'mobile', 'full' (default: mobile)
* Image size range: 16 to 1024 pixels (default: 513)
* CORS_ENABLE accepts either 'true' or 'false' (default: 'false')

_Note_ that the image size parameter controls to what size the image will be resized to before it is processed by the model. Smaller images run faster but generate less accurate segmentation maps. 


### 3. Use the Model

The API server automatically generates an interactive Swagger documentation page. Go to `http://localhost:5000` to load
it. From there you can explore the API and also create test requests.

Use the `model/predict` endpoint to load a test image (you can use one of the test images from the `samples` folder) and
get predicted segmentation map for the image from the API.

![pic](/docs/swagger-screenshot.png "Swagger Screenshot")

You can also test it on the command line, for example:

```
$ curl -F "image=@samples/stc.jpg" -XPOST http://localhost:5000/model/predict
```

You should see a JSON response like that below:

```
{
  "status": "ok",
  "image_size": [
    256,
    128
  ],
  "seg_map": [
    [
      0,
      0,
      0,
      ...,
      15,
      15,
      15,
      ...,
      0,
      0,
      0
    ],
    ...,
    ...,
    ...,
    [
      0,
      0,
      0,
      ...,
      15,
      15,
      15,
      ...,
      0,
      0,
      0
    ]
  ]
}
```
### 4. Run the Notebook

Once the model server is running, you can see how to use it by walking through [the demo notebook](demo.ipynb). _Note_ the demo requires `jupyter`, `numpy`, `Pillow`, `matplotlib` and `pycurl`.

Run the following command from the model repo base folder, in a new terminal window (leaving the model server running in the other terminal window):

```
jupyter notebook
```

This will start the notebook server. You can open the demo notebook by clicking on `demo.ipynb`.

### 5. Development

To run the Flask API app in debug mode, edit `config.py` to set `DEBUG = True` under the application settings. You will
then need to rebuild the Docker image (see [step 1](#1-build-the-model)).

### 6. Cleanup

To stop the Docker container, type `CTRL` + `C` in your terminal.

## Train this Model on Watson Machine Learning

This model supports both fine-tuning with transfer learning and training from scratch on a custom model. Please follow the steps listed under the [training readme](training/README.md) to retrain the model on [Watson Machine Learning](https://www.ibm.com/cloud/machine-learning), a deep-learning as a service (DLaaS) offering of [IBM Cloud](https://ibm.biz/Bdz2XM).