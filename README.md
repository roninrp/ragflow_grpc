# 🚀 Async gRPC ↔ Ragflow Integration

This repository contains an **asynchronous gRPC server-client system** integrated with 3 **Ragflow’s HTTP endpoints**.

It provides a structured approach for connecting backend services to Ragflow’s AI-based retrieval and reasoning capabilities through fast, concurrent gRPC communication. These can be readily extended to the HTTP endpoints mentioned in [Ragflow docs](https://ragflow.io/docs/dev/http_api_reference)

The system is containerized with **Docker Compose**, enabling quick local setup and deployment.

---

## 🧭 Overview

The project bridges **gRPC-based microservices** and **Ragflow’s REST API**.
This project demonstrates the barebones of how to have an asnchronous gRPC server and client commincate with 3 of Ragflow's endpoints- namely:
- register a new user,
- login,
- generate a new api token for a given user.

Given this implementation, it can be seemlessly developed to incorporate more of Ragflow's HTTP endpoints.

---

## 🧱 Project Structure
The project uses Ragflows modules and files and therefore the system requirements are similar to that of Ragflow's with certain additional dependencies(ref). Apart from a few changes to Ragflow's files the main files are located within `ragflow_grpc/grpc_ext`.
```
grpc_ext/
├── Dockerfile
├── docs
├── grpc_server
├── README.md
└── requirements.txt
```
---

## ⚙️ System Requirements
The hardware system requirements for running Ragflow are given in [README_RAG.html](../README_RAG.html) (Refer to the Get Started section...)
The Makefile in ragflow/ will make sure your system meets the following requirements in a uv virtual environment.

| Component | Minimum Version | Notes |
|------------|----------------|-------|
| **Python** | 3.10 | AsyncIO and grpc.aio features required |
| **Docker** | 28.5.0 | For containerization and orchestration |
| **Docker Compose** | v2.40.0| For multi-container setup |
| **grpcio / grpcio-tools** | 1.63.0| For gRPC functionality |

---
## ⚙️ Usage guide
### Setting up the System
To install, run from the projects root folder `ragflow_grpc/`:
```
make setup
```

This installs:
- uv and a virtual environment for the project
- python=3.10 and pins it to it
- dependencies from requirements-dev.txt and grpc_ext/requirements.txt
- pre-commit hooks
- turns down docker launched servers if any and removes orphans
- builds no-cache docker container images using docker-compose-grpc.yml in ragflow/docker/

### Starting the System
To startup the servers, run from the root folder ragflow/:
```
make up
```

This:
- launches the docker containers built earlier via docker compose using the same docker-compose-grpc.yml in ragflow/docker/
- runs pytest to test for HTTP endpoints of Ragflow accessed by the gRPC server and
- gRPC client methods for communicating with Ragflow.

### Stopping the System
To shutdown, run:
```
make down
```

This:
- turns down all docker launched servers any and removes orphans



## 🌐 Integration Flow

1. **gRPC Client** sends a structured or natural-language query via gRPC.
2. **gRPC Server** receives the request, processes it asynchronously, and calls relevant Ragflow’s HTTP endpoint.
3. **Ragflow Server** returns a structured or text-based response at its endpoint.
4. **gRPC Server** sends this result back to the **grpc Client** through gRPC.




---

## 🔍 Configuration Files

### `docker/docker-compose-grpc.yml`
Modified .yml lauches gRPC and Ragflow servers.
The environment variables are defined in `docker/.env` file.

#### Ports
The gRPC server uses port `50051` and connects internally to `http://ragflow:9380` to access Ragflow's ports.
Ragflow end points can be accessed via `SVR_HTTP_PORT=9380` defined in `docker/.env`.
The access to Ragflow's UI can be obtained from `http://localhost:9380`.

#### Dockerfile for gRPC
This is located in `grpc_ext/` and is accessed by `docker/docker-compose-grpc.yml` to launch a gRPC service named `ragflow-grpc-server`.


### `docker/docker-compose.yml`
Original(unchanged) Ragflow docker-compose.yml file, can be used to deploy only Ragflow services.


### `grpc_ext/requirements.txt`
Contains modules for gRPC operation.

### `requirements-dev.txt`
Contains developer related modules.

---

## 🖥️ gRPC Server
These files are located in `grpc_ext/grpc_server`

These include:
- `grpc_async_server_ragserve.py` run by the docker file and launched by `docker/docker-compose-grpc.yml`.
- `grpc_async_server_ragserve_ext.py` a copy of the above file but runs (if launched) on port `50061`.

## 🤝 gRPC Client
These files are also located in `grpc_ext/grpc_server`

These include:
- `grpc_async_ragclient.py` and can be run via `un run python grpc_async_ragclient.py` and containe gRPC client functions.
- `grpc_async_ragclient_test.py` used by pytest for testing `grpc_async_ragclient.py` functions with all servers up.

## 🧪 Testing
These can be excuted from `ragflow_grpc/`
```
make test
```

### Test files
These are located in `grpc_ext/grpc_server`
These include:
- `endpoint_test.py` which tests Ragflow's endpoints accessed by the gRPC server.
- `grpc_async_ragclient_test.py` used by pytest for testing `grpc_async_ragclient.py` functions with all servers up.


---

## 📘⚙️ Docs related to gRPC services
Sphinx like docs can be found in 📚 `grpc_ext/docs/_build/html/index.html`.

These are placed in `grpc_ext/docs` and can be generated for the documentation in `grpc_ext/` by running
```
make docs
```
from the root folder (`ragflow_grpc`) and can be found in `grpc_ext/docs/_build/html/index.html`.
