# Converting dataset to .tfrecord files

1. In convert_data.py, change flags defined to contain the path to the appropriate directories. For example:

```python
tf.app.flags.DEFINE_string('image_folder',
                           'sample/dataset/JPEGImages',
                           'Folder containing images.')

tf.app.flags.DEFINE_string(
    'semantic_segmentation_folder',
    'sample/dataset/SegmentationClass',
    'Folder containing semantic segmentation annotations.')

tf.app.flags.DEFINE_string(
    'list_folder',
    'sample/dataset/ImageSets',
    'Folder containing lists for training and validation')

tf.app.flags.DEFINE_string(
    'output_dir',
    'sample/tfrecord',
    'Path to save converted SSTable of TensorFlow examples.')
```
2. Run the file, passing in two command line arguments. The first is the format of the files in image_folder, the second is the format of the files in semantic_segmentation_folder. For example: python convert_data.py jpg png

