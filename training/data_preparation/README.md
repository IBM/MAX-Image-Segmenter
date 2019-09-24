## Data Preparation

Follow the instructions in this document to prepare your data for model training.
- [Prerequisites](#prerequisites)
- [Preparing your data](#preparing-your-data)

## Prerequisites

### Packages

Install the required packages to convert the data locally. 

```shell
$ pip install -r data_prep_requirements.txt
```

### Data Format

The training data consists of images and their corresponding segmentation labels. Each training image and the corresponding label should have the same name, however the image formats can be different. 

Valid Example:
Training image -> 1.jpg
Corresponding label -> 1.png

Invalid Example:
Training image -> 1.jpg
Corresponding label -> 1_label.png

The labels need to be `.png` or `.jpg` images of the same size as the input image but each pixel should contain the corresponding label_id. 

*NOTE*: For the current version, only data annotated in the [Pascal VOC 2012 format](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/devkit_doc.pdf) along with the same classes is supported, ie 20 classes and 1 background class. 

## Preparing Your Data

In this document `$MODEL_REPO_HOME_DIR` refers to the cloned MAX model repository directory, e.g.
`/users/hi_there/MAX-Image-Segmenter`. 

The current directory, called `$DATA_PREP_DIR`, is thus `$MODEL_REPO_HOME_DIR/training/data_preparation/`

An example dataset preparation script is shown in the `$DATA_PREP_DIR/sample/datasets/` directory. Here the training image files we want to convert are under `$DATA_PREP_DIR/sample/JPEGImages/` and the labels are under `$DATA_PREP_DIR/sample/SegmentationClass`.

### Preparing train, trainval and val Data Split
Create 3 text files called `train.txt`, `val.txt` and `trainval.txt`. These files will contain the names of the files which are for training and validation from the dataset. The example dataset has this split at `$DATA_PREP_DIR/sample/ImageSets/`

### Converting Dataset to .tfrecord Files
Once you have the image and label files, we will use the script `$DATA_PREP_DIR/convert_data.py` to convert images and labels to the required `.tfrecords` format.

Run `$DATA_PREP_DIR/convert_data.py` and if needed change the flags shown below. The default paths/values are noted below the flag name.
For example:
```shell
$ python convert_data.py --image_folder='/my/image/folder/' --input_image_format='jpg'
```

```shell
flags:

convert_data.py:
  --image_folder: Folder containing images.
    (default: 'sample/JPEGImages')
  --input_image_format: Format of training images.
    (default: 'jpg')
  --input_label_format: Format of training images.
    (default: 'png')
  --list_folder: Folder containing lists for training and validation
    (default: 'sample/ImageSets')
  --output_dir: Path to save converted SSTable of TensorFlow examples.
    (default: 'sample/tfrecord')
  --semantic_segmentation_folder: Folder containing semantic segmentation annotations.
    (default: 'sample/SegmentationClass')
```


2. Once you have the output `.tfrecord` files (will be in `$DATA_PREP_DIR/sample/tfrecords` by default), move them to the `$MODEL_REPO_HOME_DIR/training/sample_training_data` directory in the root folder of this repo. Navigate to the root directory of the repo and run the following command:
```shell
$ cp training/data_preparation/sample/tfrecords/* training/sample_training_data/
```
