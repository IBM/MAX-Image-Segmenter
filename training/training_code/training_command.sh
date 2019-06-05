set -x
# Set up the working environment.
CURRENT_DIR=$(pwd)
WORK_DIR="${CURRENT_DIR}/deeplab"
DATASET_DIR=$DATA_DIR
MODEL_TYPE=mobile
MODEL_VARIANT=mobilenet_v2
export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

if [ "${MODEL_TYPE}" == "full" ]; then 
  MODEL_VARIANT=xception_65;
fi

# Set up the working directories.
TRAIN_LOGDIR="${RESULT_DIR}/model/checkpoint"
DATASET="${DATASET_DIR}"
SUMMARY_LOGDIR="${LOG_DIR}/logs/tb/test"
EXPORT_DIR="${RESULT_DIR}/model/frozen_graph_def"

NUM_ITERATIONS=10
python "${WORK_DIR}"/train.py \
--logtostderr \
--train_split="train" \
--model_variant="${MODEL_VARIANT}" \
--atrous_rates=6 \
--atrous_rates=12 \
--atrous_rates=18 \
--output_stride=16 \
--decoder_output_stride=4 \
--train_crop_size=513 \
--train_crop_size=513 \
--train_batch_size=4 \
--training_number_of_steps="${NUM_ITERATIONS}" \
--train_logdir="${TRAIN_LOGDIR}" \
--summary_logdir="${SUMMARY_LOGDIR}" \
--dataset="pqr" \
--dataset_dir="${DATASET}"

RETURN_CODE_TRAIN=$?
if [ $RETURN_CODE_TRAIN -gt 0 ]; then
  # the training script returned an error; exit with TRAINING_FAILED_RETURN_CODE
  echo "Error: Training run exited with status code $RETURN_CODE_TRAIN"
  exit $RETURN_CODE_TRAIN
fi

CKPT_PATH="${TRAIN_LOGDIR}/model.ckpt-${NUM_ITERATIONS}"
CHECKPOINT_FINAL_LOGDIR="${RESULT_DIR}/model/checkpoint/final"
mkdir -p $CHECKPOINT_FINAL_LOGDIR
cp ${CKPT_PATH}* ${CHECKPOINT_FINAL_LOGDIR}

echo "Exporting model as a frozen graph"
cp "${TRAIN_LOGDIR}/model.ckpt-${NUM_ITERATIONS}" CHECKPOINT_FINAL_LOGDIR
EXPORT_PATH="${EXPORT_DIR}/frozen_inference_graph_${MODEL_TYPE}.pb"

python "${WORK_DIR}"/export_model.py \
  --logtostderr \
  --checkpoint_path="${CKPT_PATH}" \
  --export_path="${EXPORT_PATH}" \
  --model_variant="${MODEL_VARIANT}" \
  --atrous_rates=6 \
  --atrous_rates=12 \
  --atrous_rates=18 \
  --output_stride=16 \
  --decoder_output_stride=4 \
  --num_classes=59 \
  --crop_size=513 \
  --crop_size=513 \
  --inference_scales=1.0

RETURN_CODE_EXPORT=$?
echo "Export process complete with return code.. $RETURN_CODE_EXPORT"

if [ $RETURN_CODE_EXPORT -gt 0 ]; then
  # the training script returned an error; exit with TRAINING_FAILED_RETURN_CODE
  echo "Error: Model conversion run exited with status code $RETURN_CODE_EXPORT"
  exit $RETURN_CODE_EXPORT
fi
