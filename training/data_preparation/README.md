## How to prepare your data for training

Follow the instructions in this document to prepare your data for model training.
- [Prerequisites](#prerequisites)
- [Preparing your data](#preparing-your-data)

## Prerequisites

The training data consists of images and their corresponding segmentation labels. Each training image and the corresponding label should have the same name, however the image formats can be different. 

Example:
Training image -> 1.jpg
Training label -> 1.png

The labels need to be `.png` or `.jpg` images of the same size as the input image but each pixel should contain the corresponding label_id. If the data is not in this format already follow the [Image annotation tool guide](www.google.com) to create the label files.

## Preparing your data
An example dataset prepration is shown in the `sample/datasets/` directory. Here the training image files we want to convert are under `sample/JPEGImages/` and the labels are under `sample/SegmentationClass`.

### Preparing train, trainval and val data split
Create 3 text files called `train.txt`, `val.txt` and `trainval.txt`. These files will contain the names of the files which are for training and validation from the dataset. The example dataset has this split at `sample/ImageSets/`

### Converting dataset to .tfrecord files
Once you have the image and label files, we will use the script `datasets/convert_data.py` to convert images and labels to the required `.tfrecords` format.

In convert_data.py, change the following flags defined to contain the path to the appropriate directories. The default paths are noted below the flag name. All paths in the below are relative to the `convert_data.py` file.

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
python convert_data.py jpg png
```

Once you have the output `.tfrecord` files (will be in `sample/tfrecords` by default), move them to the `training/sample_training_data` directory in the root folder of this repo.

