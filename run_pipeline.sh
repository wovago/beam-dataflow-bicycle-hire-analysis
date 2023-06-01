#!/bin/bash

# Wrapper script that will run the Apache Beam pipeline on GCP Dataflow

# Source and export environment variables
source ./environment.sh

# Pass parameters and run pipeline with setup.py file
python3 ./run_pipeline.py \
    --region $REGION \
    --output $OUTPUT \
    --project $PROJECT \
    --temp_location $TEMP \
    --runner DataflowRunner \
    --setup_file ./setup.py





