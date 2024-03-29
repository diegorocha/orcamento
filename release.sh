#!/bin/bash

VERSION=$(git rev-parse --short HEAD)
echo "Building and pushing $VERSION"
IMAGE="us.gcr.io/diegor-infra/orcamento"
IMAGE_VERSION="$IMAGE:$VERSION"
docker build -t $IMAGE_VERSION --build-arg VERSION_CODE=$VERSION .
docker push $IMAGE_VERSION
echo "Sending static to storage"
VERSION_CODE=$VERSION python manage.py collectstatic --noinput
echo "Deploying new release"
cd terraform && terraform apply -var "app_image=$IMAGE" -var "app_version=$VERSION"
