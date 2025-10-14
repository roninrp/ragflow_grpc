"""
grpc_ext/grpc_server/crypto_utils_grpc.py

Module to encode a human generated password: str into a encryption used between gRPC server and client.

"""

# crypto_utils.py
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

# Must be the same key on client and server
SECRET_KEY = b"16byteslongkey!!"


def encrypt_password(password: str) -> dict[str, str, str]:
    """
    Password encrypter for encoding passwords to access Ragflow's HTTP endpoints.
    Encrypts a password using AES-GCM.

    Parameters
    ----------
    password : str
        Human generated password.

    Returns
    -------
    dict of str
        A dictionary containing the base64-encoded encryption components:

        - **encrypted_password** : str
          The encrypted ciphertext, encoded in base64.
        - **nonce** : str
          The random nonce used during encryption, encoded in base64.
        - **tag** : str
          The authentication tag for AES-GCM, encoded in base64.
    """
    nonce = get_random_bytes(12)
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(password.encode())

    # Base64 encode everything for transmission
    return {
        "encrypted_password": base64.b64encode(ciphertext).decode(),
        "nonce": base64.b64encode(nonce).decode(),
        "tag": base64.b64encode(tag).decode(),
    }


def decrypt_password(encrypted_password: str, nonce: str, tag: str) -> str:
    """
    Password decrypter for encoding passwords to access Ragflow's HTTP endpoints.
    Decrypts a password encrypted with AES-GCM.

    Parameters
    ----------
    encrypted_password : str
        The encrypted ciphertext, encoded in base64.
    nonce : str
        The random nonce used during encryption, encoded in base64.
    tag : str
        The authentication tag for AES-GCM, encoded in base64.

    Returns
    -------
    password : str
        Human generated password.
    """
    ciphertext = base64.b64decode(encrypted_password)
    nonce_bytes = base64.b64decode(nonce)
    tag_bytes = base64.b64decode(tag)

    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce_bytes)
    decrypted = cipher.decrypt_and_verify(ciphertext, tag_bytes)
    return decrypted.decode()
