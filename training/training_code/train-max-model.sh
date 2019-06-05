#!/bin/bash

# uncomment to enable debug output
#set -x

# --------------------------------------------------------------------
#  Standard training wrapper script for Model Asset Exchange models
#  Complete the following IBM customization steps and remove the TODO
#  comments.
#   (1) Locate "IBM TODO 1"; specify the training command
#   (2) Locate "IBM TODO 2"; customize the packaging code
# --------------------------------------------------------------------

SUCCESS_RETURN_CODE=0
TRAINING_FAILED_RETURN_CODE=1
POST_PROCESSING_FAILED=2
PACKAGING_FAILED_RETURN_CODE=3

# ---------------------------------------------------------------
# Perform pre-training tasks
# (1) Verify that environment variables are defined
# ---------------------------------------------------------------

echo "# ************************************************************"
echo "# Training model"
echo "# ************************************************************"
echo "DATA_DIR: $DATA_DIR"
echo "RESULT_DIR: $RESULT_DIR"

# ---------------------------------------------------------------
# Perform training tasks
# ---------------------------------------------------------------

# IBM TODO 1: Specify the training command; the cwd contains the files from 
#             the training_code directory
# Example: "python3 train-dcgan.py --dataset ${DATA_DIR}/aligned --epoch 20"
# start training and capture return code

pip install -r requirements.txt

TRAINING_CMD="./training_command.sh"

# display training command
echo "Running training command \"$TRAINING_CMD\""

# run training command
$TRAINING_CMD

# capture return code
RETURN_CODE=$?
if [ $RETURN_CODE -gt 0 ]; then
  # the training script returned an error; exit with TRAINING_FAILED_RETURN_CODE
  echo "Error: Training run exited with status code $RETURN_CODE"
  exit $TRAINING_RUN_FAILED_RETURN_CODE
fi

echo "Training completed. Output is stored in $RESULT_DIR."

# ---------------------------------------------------------------
# IBM TODO 2:
# Add post processing code as necessary; for example
#  - patch the TensorFlow checkpoint file (if applicable)
#  - convert the trained model into other formats
#  - ... 
# ---------------------------------------------------------------

# according to WML coding guidelines the trained model should be 
# saved in ${RESULT_DIR}/model
cd ${RESULT_DIR}/model

#
# Post processing for serialized TensorFlow models: 
# If the output of the training run is a TensorFlow checkpoint, patch it. 
#


#
# TODO: add custom code if required; e.g. to convert the
#       trained model into other formats ...
#

# ---------------------------------------------------------------
# Prepare for packaging
# (1) create the staging directory structure
# (2) copy the training log file 
# (3) copy the trained model artifacts
# ---------------------------------------------------------------

cd ${RESULT_DIR}

BASE_STAGING_DIR=${RESULT_DIR}/output
# subdirectory where trained model artifacts will be stored
TRAINING_STAGING_DIR=${BASE_STAGING_DIR}/trained_model

#
# 1. make the directories
#
mkdir -p $TRAINING_STAGING_DIR

#
# 3. copy trained model artifacts
#
# example for tensorflow checkpoint files

if [ -d ${RESULT_DIR}/model/frozen_graph_def ]; then
 mkdir -p ${TRAINING_STAGING_DIR}/tensorflow/frozen_graph_def
 cp ${RESULT_DIR}/model/frozen_graph_def/*.pb ${TRAINING_STAGING_DIR}/tensorflow/frozen_graph_def
fi


if [ -d ${RESULT_DIR}/model/checkpoint ]; then
 mkdir -p ${TRAINING_STAGING_DIR}/tensorflow/checkpoint
 cp ${RESULT_DIR}/model/checkpoint/final/* ${TRAINING_STAGING_DIR}/tensorflow/checkpoint/
fi

# The following files should now be present in BASE_STAGING_DIR
#   trained_model/<framework-name>/file1
#   trained_model/<framework-name>/file2
#   trained_model/<framework-name>/subdirectory/file3
#   trained_model/<framework-name-2>/file4
#   ...

# ----------------------------------------------------------------------
# Create a compressed TAR archive containing files from $BASE_STAGING_DIR
# NO CODE CUSTOMIZATION SHOULD BE REQUIRED
# ----------------------------------------------------------------------

echo "# ************************************************************"
echo "# Packaging artifacts"
echo "# ************************************************************"

# standardized archive name; do not change; train.sh is configured to download this file
OUTPUT_ARCHIVE=${RESULT_DIR}/model_training_output.tar.gz

CWD=`pwd`
cd $BASE_STAGING_DIR
# Create compressed archive from $BASE_STAGING_DIR 
echo "Creating downloadable archive \"$OUTPUT_ARCHIVE\"."
tar cvfz ${OUTPUT_ARCHIVE} .
RETURN_CODE=$?
if [ $RETURN_CODE -gt 0 ]; then
  # the tar command returned an error; exit with PACKAGING_FAILED_RETURN_CODE
  echo "Error: Packaging command exited with status code $RETURN_CODE."
  exit $PACKAGING_FAILED_RETURN_CODE
fi
cd $CWD

# remove the staging directory
rm -rf $BASE_STAGING_DIR

echo "Packaging completed."
exit $SUCCESS_RETURN_CODE

#
# Expected result:
#  - $OUTPUT_ARCHIVE contains
#     /trained_model/<framework-name>/file1
#     /trained_model/<framework-name>/file2
#     /trained_model/<framework-name>/subdirectory/file3
#     /trained_model/<framework-name-2>/file4
#