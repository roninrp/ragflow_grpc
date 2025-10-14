# grpc_ext/grpc_server/grpc_async_ragclient_ext.py
from grpc_async_ragclient import registration, login, getapikey

import asyncio
import logging

import time
import random


def test_client_methods():
    """
    Test fucntion to test the methods in the client service defined in grpc_async_ragcleint.py.

    As HTTP endpoint for deleting a user is not implemented, this fucntion generates a new user everytime for testing purposes.

    It tests login getapikey mdethods for a new user and the registers the same user and tests them again.
    """

    num = random.randint(0, 99)  # inclusive of both 0 and 99
    timestamp = time.strftime("%Y%m%d%H%M%S")

    email = f"rag_flow_{timestamp}_{num}@mymailxyz.com"
    name = f"rag_{timestamp}_{num}"
    password = "infini_rag_flow"

    # asyncio.run(registration(email= email, name=name, password=password))
    print("\n\n")
    reply = login_user(email=email, password=password)
    print(reply)
    assert reply == f"Error 109: Email: {email} is not registered!"

    print("\n\n")
    reply = getapikey_user(email=email, password=password)
    print(reply)
    assert reply == f"Error logging in 109: Email: {email} is not registered!"

    reply = register_user(email=email, name=name, password=password)
    print(reply)
    assert reply == f"{name}, welcome aboard!"

    print("\n\n")
    reply = login_user(email=email, password=password)
    print(reply)
    assert reply == "Welcome back!"

    print("\n\n")
    reply = getapikey_user(email=email, password=password)
    print(reply)
    assert reply[:7] == "ragflow"


def register_user(email: str, name: str, password: str) -> str:
    return asyncio.run(registration(email=email, name=name, password=password))


def login_user(email: str, password: str) -> str:
    return asyncio.run(login(email=email, password=password))


def getapikey_user(email: str, password: str) -> str:
    return asyncio.run(getapikey(email=email, password=password))


if __name__ == "__main__":
    logging.basicConfig()
    # Example usage
    email = "rag_flow_101@gmail.com"
    name = "rag_101"
    password = "infini_rag_flow"

    reply = asyncio.run(registration(email=email, name=name, password=password))
    print(reply)
    print("\n\n")
    reply = asyncio.run(login(email=email, password=password))
    print(reply)

    print("\n\n")
    reply = asyncio.run(getapikey(email=email, password=password))
    print(reply)
