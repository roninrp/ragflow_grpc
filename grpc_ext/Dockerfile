FROM python:3.10-slim

WORKDIR /app

# Copy everything into /app
COPY . .


# # Copy the public.pem file from ragflow/conf. Do this if /conf/public.pem isn't mounted as volume in the grpc section of the .yml file
# COPY ../conf/public.pem /app/conf/public.pem

# Create virtual environment and install dependencies
# RUN python -m venv /app/venv && \
#    /app/venv/bin/pip install --upgrade pip setuptools wheel && \
#    /app/venv/bin/pip install grpcio==1.66.1 grpcio-tools==1.66.1 protobuf==5.27.2 requests python-dotenv pycryptodomex

COPY requirements.txt /app/requirements.txt

RUN python -m venv /app/venv && \
   /app/venv/bin/pip install --upgrade pip setuptools wheel && \
   /app/venv/bin/pip install -r /app/requirements.txt

# Upgrade pip, setuptools, wheel
# Ensure pip is installed
#RUN /app/venv/bin/python -m ensurepip --upgrade
#RUN /app/venv/bin/pip install --upgrade pip setuptools wheel

# Install from requirements.txt
#COPY requirements.txt /app/requirements.txt
#RUN /app/venv/bin/pip install -r /app/requirements.txt


ENV PATH="/app/venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"

# Generate gRPC Python code if not already present
RUN python -m grpc_tools.protoc \
    -I./grpc_server \
    --python_out=./grpc_server \
    --grpc_python_out=./grpc_server \
    ./grpc_server/ragflow_register_login_getapi.proto

# Set working directory to gRPC server
WORKDIR /app/grpc_server

# Start the gRPC server
CMD ["python", "-u", "grpc_async_server_ragserve.py"]
