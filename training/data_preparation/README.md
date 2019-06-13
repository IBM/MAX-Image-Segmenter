## How to prepare your data for training

Follow the instructions in this document to prepare your data for model training.
- [Prerequisites](#prerequisites)
- [Preparing your data](#preparing-your-data)
- [Using pre trained weights](#using-pre-trained-weights)

## Prerequisites

The training data consists of images and their corresponding segmentation labels. Each training image and the corresponding label should have the same name, however the image formats can be different. 

Example:
Training image -> 1.jpg
Training label -> 1.png

The labels need to be `.png` or `.jpg` images of the same size as the input image but each pixel should contain the corresponding label_id. 

*NOTE*: For the current version, only data annotated in the [Pascal VOC 2012 format](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/devkit_doc.pdf) along with the same classes is supported, ie 20 classes and 1 background class. 

## Preparing your data


In this document `$MODEL_REPO_HOME_DIR` refers to the cloned MAX model repository directory, e.g.
`/users/hi_there/MAX-Image-Segmenter`. 

The current directory, called `$DATA_PREP_DIR`, is thus `$MODEL_REPO_HOME_DIR/training/data_preparation/`

An example dataset prepration is shown in the `$DATA_PREP_DIR/sample/datasets/` directory. Here the training image files we want to convert are under `$DATA_PREP_DIR/sample/JPEGImages/` and the labels are under `$DATA_PREP_DIR/sample/SegmentationClass`.

### Preparing train, trainval and val data split
Create 3 text files called `train.txt`, `val.txt` and `trainval.txt`. These files will contain the names of the files which are for training and validation from the dataset. The example dataset has this split at `$DATA_PREP_DIR/sample/ImageSets/`

### Converting dataset to .tfrecord files
Once you have the image and label files, we will use the script `$DATA_PREP_DIR/convert_data.py` to convert images and labels to the required `.tfrecords` format.

In `$DATA_PREP_DIR/convert_data.py`, change the following flags defined to contain the path to the appropriate directories. We recommend using the default paths so that there is no code change necessary. The default paths are noted below the flag name. All paths in the below are relative to the `$DATA_PREP_DIR/convert_data.py` file.

```python
# Flag for the training images folder.
tf.app.flags.DEFINE_string('image_folder',
                           'sample/JPEGImages',
                           'Folder containing images.')

# Flag for the labels folder
tf.app.flags.DEFINE_string(
    'semantic_segmentation_folder',
    'sample/SegmentationClass',
    'Folder containing semantic segmentation annotations.')

# Flag for the train and validation split
tf.app.flags.DEFINE_string(
    'list_folder',
    'sample/ImageSets',
    'Folder containing lists for training and validation')

# Flag for the output directory to store the .tfrecord files.
tf.app.flags.DEFINE_string(
    'output_dir',
    'sample/tfrecord',
    'Path to save converted SSTable of TensorFlow examples.')
```
2. Run the file, passing in two command line arguments. The first is the format of the files in image_folder, the second is the format of the files in semantic_segmentation_folder. For example: 

```shell
$ python convert_data.py jpg png
```

3. Once you have the output `.tfrecord` files (will be in `$DATA_PREP_DIR/sample/tfrecords` by default), move them to the `$MODEL_REPO_HOME_DIR/training/sample_training_data` directory in the root folder of this repo. Navigate to the root directory of the repo and run the following command:
```shell
$ cp training/data_preparation/sample/tfrecords/* training/sample_training_data/
```

## Using Pre Trained Weights

If you wish to perform transfer learning or resume from a previous checkpoint, place the checkpoint files in the `$MODEL_REPO_HOME_DIR/training/sample_training_data/initial_model/` folder. The checkpoint files usually consist one `model.ckpt-<iteration_number>.data*` file, one corresponding `model.ckpt-<iteration_number>.index` file and a `checkpoint` file which has the name of the checkpoint. For example if you wish to resume from a previous training run of 30000 iterations, your files would ideally be called `model.ckpt-30000.data.0000-of-0001`, `model.ckpt-30000.index` and `checkpoint` with the checkpoint file having one entry `model_checkpoint_path: "model.ckpt-30000"`.