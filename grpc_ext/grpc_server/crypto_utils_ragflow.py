"""
grpc_ext/grpc_server/crypto_utils_ragflow.py

Module to encode a human generated password: str into a encryption used by RagFlow

"""

import os
import base64
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_v1_5

# Public key path provided by ragflow.
# The path here relative to ragflow/docker folder where docker-compose-grpc.yml is executed.
PUBLIC_KEY_PATH = os.path.join(os.path.dirname(__file__), "../conf/public.pem")


def encrypt_password(password: str, public_key_path: str = PUBLIC_KEY_PATH) -> str:
    """
    Password encrypter for encoding passwords to access Ragflow's HTTP endpoints.

    Parameters
    ----------
    password : str
        Human generated password
    public_key_path : str = "../conf/public.pem"
        Path of the public key provided by Ragflow for RSA encryption in "ragflow/conf/public.pem".
        Default value is  "../conf/public.pem" as its triggered from within "ragflow/docker".

    Returns
    -------
    str
        Encrypted password
    """
    with open(public_key_path, "r") as f:
        pubkey = RSA.importKey(f.read(), "Welcome")
    cipher = PKCS1_v1_5.new(pubkey)
    password_b64 = base64.b64encode(password.encode("utf-8"))
    encrypted = cipher.encrypt(password_b64)
    return base64.b64encode(encrypted).decode("utf-8")
