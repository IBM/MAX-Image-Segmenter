# Set up the working environment.
CURRENT_DIR=$(pwd)
WORK_DIR="${CURRENT_DIR}/deeplab"
DATASET_DIR=$DATA_DIR

export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim

# Set up the working directories.
TRAIN_LOGDIR="${RESULT_DIR}/model/checkpoint"
DATASET="${DATASET_DIR}"
SUMMARY_LOGDIR="${LOG_DIR}/logs/tb/test"

NUM_ITERATIONS=100
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
