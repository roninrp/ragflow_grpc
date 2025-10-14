"""
Asynchronous gRPC client communicating with a similar gRPC server
serving the registration, login and new_token HTTP endpoints of RAGFlow's server
"""

import os
import grpc  # type: ignore
from dotenv import load_dotenv

import ragflow_register_login_getapi_pb2 as pb2
import ragflow_register_login_getapi_pb2_grpc as pb2_grpc

from crypto_utils_grpc import encrypt_password

import asyncio
import logging

# For more channel options, please see https://grpc.io/grpc/core/group__grpc__arg__keys.html
CHANNEL_OPTIONS = [
    ("grpc.lb_policy_name", "pick_first"),
    ("grpc.enable_retries", 0),
    ("grpc.keepalive_timeout_ms", 10000),
]


# ---------------------------------------------------------------------
# Load environment
# ---------------------------------------------------------------------
load_dotenv()

GRPC_PORT = os.getenv("GRPC_PORT", "50051")

# ---------------------------------------------------------------------
# gRPC Client Implementation
# ---------------------------------------------------------------------


async def registration(email: str, name: str, password: str) -> str:
    """
    Registers users by accessing "/v1/user/register" HTTP endpoint.
    Accessed indirectly via the equivalent grpc server method.

    Parameters
    ----------
    email : str
        Email, enter a valid str with @ in it
    name : str
        User's nickname on the ragflow server
    password : str
        Human readable password

    Returns
    -------
    reply : str
        Reply from the Ragflow server

    """
    print("""Send a query via gRPC to the RagServices server.""")
    print(f"localhost:{GRPC_PORT}")

    en_pass = encrypt_password(password)
    encrypted_password = en_pass["encrypted_password"]
    nonce = en_pass["nonce"]
    tag = en_pass["tag"]

    async with grpc.aio.insecure_channel(target=f"localhost:{GRPC_PORT}", options=CHANNEL_OPTIONS) as channel:
        # channel = grpc.insecure_channel(f"localhost:{GRPC_PORT}")
        stub = pb2_grpc.RagServicesStub(channel)

        request = pb2.RegistrationCredentials(email=email, name=name, encrypted_password=encrypted_password, nonce=nonce, tag=tag)  # type: ignore
        print(request)
        response = await stub.Registration(request)

        print(f"🔹 Registration Details: {email}, {name}, {encrypted_password}")
        print(f"🔸 RagFlow Reply: {response.reply}")
        return response.reply


async def login(email: str, password: str) -> str:
    """
    Logs registerd users in by accessing "/v1/user/login" HTTP endpoint.
    Accessed indirectly via the equivalent grpc server method.

    Parameters
    ----------
    email : str
        Email, enter a valid str with @ in it
    password : str
        Human readable password

    Returns
    -------
    reply : str
        Reply from the Ragflow server
    """
    print("""Send a query via gRPC to the RagServices server.""")
    print(f"localhost:{GRPC_PORT}")

    en_pass = encrypt_password(password)
    encrypted_password = en_pass["encrypted_password"]
    nonce = en_pass["nonce"]
    tag = en_pass["tag"]

    async with grpc.aio.insecure_channel(target=f"localhost:{GRPC_PORT}", options=CHANNEL_OPTIONS) as channel:
        # channel = grpc.insecure_channel(f"localhost:{GRPC_PORT}")
        stub = pb2_grpc.RagServicesStub(channel)

        request = pb2.LoginCredentials(email=email, encrypted_password=encrypted_password, nonce=nonce, tag=tag)  # type: ignore
        print(request)
        response = await stub.Login(request)

        print(f"🔹 Login Details: {email}, {encrypted_password}")
        print(f"🔸 RagFlow Reply: {response.reply}")
        return response.reply


async def getapikey(email: str, password: str) -> str:
    """
    Obtains a new api token for registerd users by accessing "/v1/user/login" HTTP endpoint.
    Accessed indirectly via the equivalent grpc server method.

    Parameters
    ----------
    email : str
        Email, enter a valid str with @ in it
    password : str
        Human readable password

    Returns
    -------
    reply : str
        Reply from the Ragflow server
    """
    print("""Send a query via gRPC to the RagServices server.""")
    print(f"localhost:{GRPC_PORT}")

    en_pass = encrypt_password(password)
    encrypted_password = en_pass["encrypted_password"]
    nonce = en_pass["nonce"]
    tag = en_pass["tag"]

    async with grpc.aio.insecure_channel(target=f"localhost:{GRPC_PORT}", options=CHANNEL_OPTIONS) as channel:
        # channel = grpc.insecure_channel(f"localhost:{GRPC_PORT}")
        stub = pb2_grpc.RagServicesStub(channel)

        request = pb2.LoginCredentials(email=email, encrypted_password=encrypted_password, nonce=nonce, tag=tag)  # type: ignore
        print(request)
        response = await stub.GetApiKey(request)

        print(f"🔹 Login Details: {email}, {encrypted_password}")
        print(f"🔸 RagFlow Reply: {response.reply}")
        return response.reply


if __name__ == "__main__":
    logging.basicConfig()
    # Example usage
    email = "rag_flow_101@gmail.com"
    name = "rag_101"
    password = "infini_rag_flow"

    # asyncio.run(registration(email= email, name=name, password=password))
    print("\n\n")
    reply = asyncio.run(login(email=email, password=password))
    print(reply)

    print("\n\n")
    reply = asyncio.run(getapikey(email=email, password=password))
    print(reply)
