## Description

Simple inference server. 
Users can send images in .jpg or .png format to identify objects, drawn on them.

## Architecture

- Inference server (Flask). 
- Key-value cache (Redis). Used to store image hashes to optimize dublicate requests.

## Run

    kubectl apply -f web-service.yaml,web-deployment.yaml,redis-service.yaml,redis-deployment.yaml,redis-volume.yaml
    
Tested only in Linux environment

## Usage

1. Expose service

    kubectl port-forward service/web 50000:50000

2. Open demo.html
3. Upload file
