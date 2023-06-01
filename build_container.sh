source ./environment.sh

# Create container repository
gcloud artifacts repositories create $REPOSITORY \
    --repository-format=docker \
    --location=$REGION \
    --async

# Add gcloud as Docker credential helper
gcloud auth configure-docker $REGION-docker.pkg.dev

# Build container image using Google cloud build and push to repository
gcloud builds submit --tag "$REGION-docker.pkg.dev/$PROJECT/$REPOSITORY/$CONTAINER:$TAG" .

