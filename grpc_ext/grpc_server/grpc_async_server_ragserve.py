"""
grpc_ext/grpc_server/grpc_async_server_ragserve.py

Asynchronus gRPC server serving the registration, login and new_token HTTP endpoints of RAGFlow's server.
This is launched within the docker environment same as other ragflow servers.
"""

import os
import sys
import grpc
import httpx
from dotenv import load_dotenv


import ragflow_register_login_getapi_pb2 as pb2
import ragflow_register_login_getapi_pb2_grpc as pb2_grpc

from crypto_utils_grpc import decrypt_password
from crypto_utils_ragflow import encrypt_password

import asyncio
import logging

# ---------------------------------------------------------------------
# Load environment
# ---------------------------------------------------------------------
load_dotenv()

# Ragflow's server port, set in ragflow/docker/.env file
SVR_HTTP_PORT = os.getenv("SVR_HTTP_PORT")

# gRPC's server port, set in ragflow/docker/.env file
GRPC_PORT = os.getenv("GRPC_PORT", "50051")

# Internal reference address for Ragflow's server
RAGFLOW_HOST = os.getenv("RAGFLOW_HOST", "ragflow")  # not defined in .env

# Internal reference url for Ragflow's server
RAGFLOW_API_URL = f"http://{RAGFLOW_HOST}:{SVR_HTTP_PORT}"

# File path for the public key meant for passing encrypted password to Ragflow endpoints relative to ragflow/docker
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), "../conf/public.pem")


# ---------------------------------------------------------------------
# gRPC Service Implementation
# ---------------------------------------------------------------------


class RagServices(pb2_grpc.RagServicesServicer):  # type: ignore  # proto generated class
    """gRPC RagServices class with methods defined in ragflow_register_login_getapi.proto file."""

    async def Registration(self, request, context):  # type: ignore  # proto generated class
        """
        Registers users by accessing "/v1/user/register" HTTP endpoint.
        Accessed indirectly via the equivalent grpc client

        Parameters
        ----------
        request : pb2.RegistrationCredentials
            Class defined in ragflow_register_login_getapi.proto

        Returns
        -------
        pb2.ResponseString
            Class defined in ragflow_register_login_getapi.proto
        """
        print("Serverside Registration triggered")
        url = RAGFLOW_API_URL + "/v1/user/register"
        email = request.email
        name = request.name
        # password = request.password
        try:
            password = decrypt_password(request.encrypted_password, request.nonce, request.tag)
            print("Decrypted password:", password)  # to be muted
        except Exception as e:
            print("Decryption error", str(e))

        enc_password = encrypt_password(password)
        register_payload = {"email": email, "nickname": name, "password": enc_password}

        try:
            # res = requests.post(url=url, json=register_payload) # to change
            # res = res.json()
            async with httpx.AsyncClient() as client:
                res = await client.post(url, json=register_payload)
                res = res.json()
            print("\n", res)
            if res["code"] == 0:
                reply = res.get("message", "No answer returned.")
            else:
                reply = f"Error {res['code']}: {res['message']}"
        except Exception as e:
            reply = f"Request failed: {str(e)}"

        return pb2.ResponseString(reply=reply)

    async def Login(self, request, context):  # type: ignore  # proto generated class
        """
        Logs registered users in by accessing "/v1/user/login" HTTP endpoint.
        Accessed indirectly via the equivalent grpc client

        Parameters
        ----------
        request : pb2.LoginCredentials
            Class defined in ragflow_register_login_getapi.proto

        Returns
        -------
        pb2.ResponseString
            Class defined in ragflow_register_login_getapi.proto
        """
        print("Serverside Login triggered")
        url = RAGFLOW_API_URL + "/v1/user/login"
        email = request.email

        try:
            password = decrypt_password(request.encrypted_password, request.nonce, request.tag)
            print("Decrypted password:", password)  # to be muted
        except Exception as e:
            print("Decryption error", str(e))

        enc_password = encrypt_password(password)
        login_payload = {"email": email, "password": enc_password}

        try:
            # response = requests.post(url=url, json=login_payload)  # response.headers["Authorization"] can be used to generate new tokens
            # res = response.json()
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=login_payload)
                res = response.json()
            print("\n", res)
            if res["code"] == 0:
                reply = res.get("message", "No answer returned.")
            else:
                reply = f"Error {res['code']}: {res['message']}"
        except Exception as e:
            reply = f"Request failed: {str(e)}"

        return pb2.ResponseString(reply=reply)

    async def GetApiKey(self, request, context):  # type: ignore  # proto generated class
        """
        Obtains new api token for logged in users by accessing "/v1/system/new_token" HTTP endpoint.
        Accessed indirectly via the equivalent grpc client

        Parameters
        ----------
        request : pb2.LoginCredentials
            Class defined in ragflow_register_login_getapi.proto

        Returns
        -------
        pb2.ResponseString
            Class defined in ragflow_register_login_getapi.proto
        """
        print("Serverside GetApiKey triggered")

        url = RAGFLOW_API_URL + "/v1/system/new_token"

        url_login = RAGFLOW_API_URL + "/v1/user/login"

        email = request.email
        # name = request.name
        # password = request.password

        try:
            password = decrypt_password(request.encrypted_password, request.nonce, request.tag)
            print("Decrypted password:", password)  # to be muted
        except Exception as e:
            print("Decryption error", str(e))

        enc_password = encrypt_password(password)
        login_payload = {"email": email, "password": enc_password}

        try:
            # login_response = requests.post(url=url_login, json=login_payload)
            # login_res = login_response.json()
            async with httpx.AsyncClient() as client:
                login_response = await client.post(url_login, json=login_payload)
                login_res = login_response.json()
            if login_res["code"] == 0:
                auth = login_response.headers["Authorization"]
                auth = {"Authorization": auth}

                try:
                    # response = requests.post(url=url, headers=auth)
                    # res = response.json()
                    async with httpx.AsyncClient() as client:
                        response = await client.post(url, headers=auth)
                        res = response.json()
                    if res.get("code") == 0:
                        reply = res["data"].get("token")
                    else:
                        reply = f"Error getting new token {res['code']}: {res['message']}"
                except Exception as e:
                    reply = f"Request getting new token failed: {str(e)}"

            else:
                reply = f"Error logging in {login_res['code']}: {login_res['message']}"
        except Exception as e:
            reply = f"Request login failed: {str(e)}"

        return pb2.ResponseString(reply=reply)


# ---------------------------------------------------------------------
# gRPC Server Startup
# ---------------------------------------------------------------------
async def serve_grpc():
    """Starts the async gRPC server on GRPC_PORT with default value 50051"""
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    server = grpc.aio.server()
    pb2_grpc.add_RagServicesServicer_to_server(RagServices(), server)
    lsttn_addr = f"[::]:{GRPC_PORT}"
    server.add_insecure_port(lsttn_addr)
    logging.info("Starting server on %s", lsttn_addr)
    print(f"[gRPC] Server started on port {GRPC_PORT}, forwarding to {RAGFLOW_API_URL}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # or DEBUG
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],  # important: send logs to stdout
    )

    logger = logging.getLogger(__name__)

    logger.info("gRPC Server starting...")

    asyncio.run(serve_grpc())
