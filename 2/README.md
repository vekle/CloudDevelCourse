## Description

Simple inference server. 
Users can send images in .jpg or .png format to identify objects, drawn on them.

## Architecture

- Inference server (Flask). 
- Key-value cache (Redis). Used to store image hashes to optimize dublicate requests.

## Run

Install minikube and run commands to build service and expose it on local machine

    docker build -t infer-app ./infer-app
    minikube image load infer-app
    kubectl apply -f web-service.yaml,web-deployment.yaml,redis-service.yaml,redis-deployment.yaml,redis-volume.yaml
    kubectl port-forward service/web 50000:50000
    
Tested only in Linux environment

## Usage

1. Open demo.html
2. Upload file
