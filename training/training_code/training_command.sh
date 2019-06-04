# Set up the working environment.
CURRENT_DIR=$(pwd)
WORK_DIR="${CURRENT_DIR}/deeplab"
DATASET_DIR=$DATA_DIR

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

# Set up the working directories.
TRAIN_LOGDIR="${RESULT_DIR}/model/checkpoint"
DATASET="${DATASET_DIR}"
SUMMARY_LOGDIR="${LOG_DIR}/logs/tb/test"
EXPORT_DIR="${RESULT_DIR}/model/frozen_graph_def"

NUM_ITERATIONS=10
python "${WORK_DIR}"/train.py \
--logtostderr \
--train_split="train" \
--model_variant="mobilenet_v2" \
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

# Export the trained checkpoint.
CKPT_PATH="${TRAIN_LOGDIR}/model.ckpt-${NUM_ITERATIONS}"
EXPORT_PATH="${EXPORT_DIR}/frozen_inference_graph.pb"

python "${WORK_DIR}"/export_model.py \
  --logtostderr \
  --checkpoint_path="${CKPT_PATH}" \
  --export_path="${EXPORT_PATH}" \
  --model_variant="mobilenet_v2" \
  --atrous_rates=6 \
  --atrous_rates=12 \
  --atrous_rates=18 \
  --output_stride=16 \
  --decoder_output_stride=4 \
  --num_classes=59 \
  --crop_size=513 \
  --crop_size=513 \
  --inference_scales=1.0

# Run inference with the exported checkpoint.
# Please refer to the provided deeplab_demo.ipynb for an example.