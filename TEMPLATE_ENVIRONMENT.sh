#!/bin/bash

# Script to set and export GCP environment variables needed to run the Apache Beam pipeline on GCP Dataflow

# GCP project in which to run the Dataflow pipeline
export PROJECT=<PROJECT_ID>

# GCP region 
# Note: Dataflow needs to run in EU regioon to access London bicycle sharing data set from Bigquery)
export REGION='europe-west1'

# Output bucket which will contain output and staging folder
export BUCKET=<OUTPUT_BUCKET>

# Subdirectory in output bucket with filename prefix
export OUTPUT="$BUCKET/output/bikesharing-analysis"

# Subdirectory in output bucket used for staging
export TEMP="$BUCKET/temp/"

# Artifact repository name
export REPOSITORY=<REPOSITORY_NAME>

# Container name
export CONTAINER='dataflow/beam'

# Container tag
export TAG='2.47.0'

# Image URI to pull Docker container
export IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$CONTAINER:$TAG"
