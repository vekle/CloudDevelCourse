FROM ubuntu

RUN apt-get update && apt-get install -y --no-install-recommends \
	    python3 \
	    python3-pip \
	    python3-setuptools

RUN python3 -m pip install -U pip
RUN python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN python3 -m pip install redis
RUN python3 -m pip install flask

COPY ./pytorch_infer_srv.py /app/pytorch_infer_srv.py

ENV REDIS_HOST="localhost"
ENV REDIS_PORT="6379"

ENTRYPOINT python3 /app/pytorch_infer_srv.py