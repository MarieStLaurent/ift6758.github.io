#!/bin/bash

pip install --quiet orion

# TODO: change this to the maximum number of desired trials.
MAX_TRIALS=50
EXPERIMENT_NAME="one-model-each-marie"

latest_tag=`git --git-dir=ift6758.github.io/.git --work-tree=ift6758.github.io describe --tags`
echo "latest tag is '$latest_tag'"
echo "experiment name is '$EXPERIMENT_NAME'"

if [[ $latest_tag == $EXPERIMENT_NAME ]]; then
        echo "Starting experiment '$EXPERIMENT_NAME'."
else
        echo "WARNING: experiment name '$EXPERIMENT_NAME' is not the same as the latest tag '$latest_tag'!"
        echo "this will make it hard to reproduce the results, as the code used at train and test-time might be different!"
fi

mkdir -p logs

MAX_EPOCHS_PER_EXPERIMENT=500
orion -v --debug hunt --max-trials $MAX_TRIALS -n $EXPERIMENT_NAME ./ift6758.github.io/project/train.py \
        --experiment_name $EXPERIMENT_NAME \
        --epochs $MAX_EPOCHS_PER_EXPERIMENT \
        --batch_size~"choices(64, 128, 256)" \
        --activation tanh \
        --learning_rate~"choices(0.01, 0.005, 0.001)" \
        --optimizer~"choices('ADAM', 'SGD')" \
        --num_like_pages~"choices(5000, 10000)" \
        --use_dropout~"choices('True', 'False')" \
        --use_batchnorm False \
        --l1_reg~"choices(0, 0.005)" \
        --l2_reg~"choices(0, 0.005)" \
        >> "logs/$EXPERIMENT_NAME.txt"
