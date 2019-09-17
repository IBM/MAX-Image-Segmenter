## Train the Model with Your Own Data

- [Prepare Data for Training](#prepare-your-data-for-training)
- [Train the Model](#train-the-model)


## Prepare Data for Training

To prepare your data for training complete the steps listed in [data_preparation/README.md](data_preparation/README.md).


## Train the Model

In this document `$MODEL_REPO_HOME_DIR` refers to the cloned MAX model repository directory, e.g.
`/users/hi_there/MAX-Image-Segmenter`. 


### Install Local Prerequisites

Open a terminal window, change dir into `$MODEL_REPO_HOME_DIR/training` and install the Python prerequisites. (Model training requires Python 3.6 or above.)

   ```
   $ cd training/

   $ pip install -r requirements.txt
    ... 
   ```

### Use Pre Trained Weights

If you wish to perform transfer learning or resume from a previous checkpoint, place the checkpoint files in the `$MODEL_REPO_HOME_DIR/training/sample_training_data/initial_model/` folder. The checkpoint files usually consist one `model.ckpt-<iteration_number>.data*` file, one corresponding `model.ckpt-<iteration_number>.index` file and a `checkpoint` file which has the name of the checkpoint. For example if you wish to resume from a previous training run of 30000 iterations, your files would ideally be called `model.ckpt-30000.data.0000-of-0001`, `model.ckpt-30000.index` and `checkpoint` with the checkpoint file having one entry `model_checkpoint_path: "model.ckpt-30000"`.

### Customize Model Specific Parameters

If you wish to change training hyper-parameters like `num_iterations`, `learning_rate`, `stride_size` etc, pass the corresponding arguments to `$MODEL_REPO_HOME_DIR/training/training_code/training_command.sh`. You can also change the backbone/model type to either `full` (which uses the `xception_65` architecture) or the faster `mobile`(which uses a `mobilenet_v2` architecture).

### Run the Setup Script

The `wml_setup.py` script prepares your local environment and your IBM Cloud resources for model training.

1. Locate the training configuration file. It is named `max-image-segmenter-training-config.yaml`.

   ```

   $ ls *.yaml
     max-image-segmenter-training-config.yaml
   ```

1. Configure your environment for model training. Run `wml_setup.py` and follow the prompts.

   ```
    $ python wml_setup.py max-image-segmenter-training-config.yaml 
     ...
   ```
   
1. After setup has completed, define the displayed environment variables. These variables provide the model training script with access credentials for your Watson Machine Learning service and Cloud Object Storage service. 

   MacOS example:

   ```
   $ export ML_INSTANCE=...
   $ export ML_APIKEY=...
   $ export ML_ENV=...
   $ export AWS_ACCESS_KEY_ID=...
   $ export AWS_SECRET_ACCESS_KEY=...
   ```
   
   > The training script `wml_train.py` requires these environment variables. If they are not set, model training cannot be started.

### Train the Model Using Watson Machine Learning

1. Verify that the training preparation steps complete successfully. Replace `<model-name.yaml>` with your configuration file.

   ```
    $ python wml_train.py max-image-segmenter-training-config.yaml prepare
     ...
     # --------------------------------------------------------
     # Checking environment variables ...
     # --------------------------------------------------------
     ...
   ```

   If preparation completed successfully:

    - The required environment variables are defined.
    - Training data is present in the Cloud Object Storage bucket that Watson Machine Learning will access to train the model.
    - The model training code is packaged in a ZIP file named `max-image-segmenter-model-building-code.zip` that Watson Machine Learning uses to train the model.

1. Start model training.

   ```
   $ python wml_train.py <...-training-config.yaml> package
    ...
    # --------------------------------------------------------
    # Starting model training ...
    # --------------------------------------------------------
    Training configuration summary:
    Training run name     : train-max-image-segmenter
    Training data bucket  : ...
    Results bucket        : ...
    Model-building archive: max-image-segmenter-model-building-code.zip
    Model training was started. Training id: model-...
    ...
   ```
   
    > Take note of the training id.

1. Monitor the model training progress.

   ```
   ...
   Training status is updated every 15 seconds - (p)ending (r)unning (e)rror (c)ompleted: 
   ppppprrrrrrr...
   ```

   > Training continues should your training script get disconnected (e.g. because you terminated the script or lost network connectivity). You can resume monitoring by running `python wml_train.py max-image-segmenter-training-config.yaml package <training-id>`.

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

### Re-build the Docker Image

Once the training run is complete, there should be an updated `frozen_inference_graph.pb` file in `$MODEL_REPO_HOME_DIR/custom_assets` folder. At this point the Docker container can be rebuilt using the command below from the root directory of the repo ie `$MODEL_REPO_HOME_DIR`.

```shell

$ docker build -t max-image-segmenter --build_arg use_pre_trained_model=false .

```
Once the container is built, run the following command to run the container as mentioned in the main readme section.

```shell

$ docker run -it -p 5000:5000 max-image-segmenter

```

