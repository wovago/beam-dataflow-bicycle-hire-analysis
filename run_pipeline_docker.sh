#!/bin/bash

# Wrapper script that will run the Apache Beam pipeline on GCP Dataflow

# Source and export environment variables
source ./environment.sh

# Pass parameters and run pipeline with prebuilt, custom Docker container image
# Note: Apache beam version in Docker container needs to be the same 
#       as beam version in launch environment!
python3 run_pipeline.py \
    --region $REGION \
    --output $OUTPUT \
    --project $PROJECT \
    --temp_location $TEMP \
    --runner DataflowRunner \
    --sdk_container_image=$IMAGE_URI \
    --sdk_location=container \
    --experiments=use_runner_v2





