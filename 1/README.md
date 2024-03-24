## Description

Simple inference server. 
Users can send images in .jpg or .png format to identify objects, drawn on them.

## Architecture

- Inference server (Flask). 
- Key-value cache (Redis). Used to store image hashes to optimize dublicate requests.

## Run

    `docker-compose up`

Tested only in Linux environment

## Usage

1. Open demo.html
2. Upload file
