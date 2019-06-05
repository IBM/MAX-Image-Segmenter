## How to train this model using your own data

- [Prepare your data for training](#prepare-your-data-for-training)
- [Train the model](#train-the-model)


## Prepare your data for training

To prepare your data for training complete the steps listed in [data_preparation/README.md](data_preparation/README.md).

## Train the model


In this document `$MODEL_REPO_HOME_DIR` refers to the cloned MAX model repository directory, e.g.
`/users/hi_there/MAX-Image-Segmenter`. 

### Install local prerequisites

Open a terminal window, change dir into `$MODEL_REPO_HOME_DIR/training` and install the Python prerequisites. (Model training requires Python 3.6 or above.)

   ```
   $ cd training/

   $ pip install -r requirements.txt
    ... 
   ```

### Run the setup script

  TODO


### Train the model using Watson Machine Learning

1. Locate the training configuration file.

   ```

   $ ls *.yaml
     ...yaml
   ```

1. Verify that the training preparation steps complete successfully. Replace `<model-name.yaml>` with your configuration file.

   ```
    $ python train.py <model-name.yaml> prepare
     ...
     # --------------------------------------------------------
     # Checking environment variables ...
     # --------------------------------------------------------
     ...
   ```

   If prepartion completed successfully:

    - Training data is present in the Cloud Object Storage bucket that WML will access during model training.
    - Model training code is packaged `<model-name>-model-building-code.zip`

1. Start model training.

   ```
   $ python train.py <model-name.yaml>
    ...
    # --------------------------------------------------------
    # Starting model training ...
    # --------------------------------------------------------
    Training configuration summary:
    Training run name     : train-max-...
    Training data bucket  : ...
    Results bucket        : ...
    Model-building archive: max-...-model-building-code.zip
    Model training was started. Training id: model-...
    ...
   ```

1. Monitor training progress

   ```
   ...
   Training status is updated every 15 seconds - (p)ending (r)unning (e)rror (c)ompleted: 
   ppppprrrrrrr...
   ```

   After training has completed the training log file `training-log.txt` is downloaded along with the trained model artifacts.

   ```
   ...
   # --------------------------------------------------------
   # Downloading training log file "training-log.txt" ...
   # --------------------------------------------------------
   Downloading "training-.../training-log.txt" from bucket "..." to "training_output/training-log.txt"
   ..
   # --------------------------------------------------------
   # Downloading trained model archive "model_training_output.tar.gz" ...
   # --------------------------------------------------------
   Downloading "training-.../model_training_output.tar.gz" from bucket "..." to "training_output/model_training_output.tar.gz"
   ....................................................................................
   ```

   > If training was terminated early due to an error only the log file is downloaded. Inspect it to identify the problem.

   ```
   $ ls training_output/
     model_training_output.tar.gz
     trained_model/
     training-log.txt 
   ```

1. Return to the parent directory

### Re-build the Docker image


