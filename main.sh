#!/bin/bash

IMAGE_NAME="hmm:latest"

function build_docker_image() {
  echo "Building docker image..."
  docker build -t $IMAGE_NAME .
}

function run_docker_image() {
  echo "Running docker image $IMAGE_NAME"
  docker run -it --rm $IMAGE_NAME
}

function main() {
  build_docker_image
  run_docker_image
}

main
