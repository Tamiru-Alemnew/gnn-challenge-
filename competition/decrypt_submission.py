"""
The Cold Start Citation Challenge 2026
--------------------------------------
Script: Submission Decryption (Hybrid RSA + AES-256-CBC)
Description: Decrypts predictions.enc into predictions.csv inside CI using
             the RSA private key supplied via environment variable.
Author: Competition Organizers

Usage:
    SUBMISSION_PRIVATE_KEY=[PEM] python decrypt_submission.py \\
        --input submissions/inbox/team/run_001/predictions.enc \\
        --output submissions/inbox/team/run_001/predictions.csv
"""

import argparse
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


ENV_PRIVATE_KEY = "SUBMISSION_PRIVATE_KEY"


def load_private_key_from_env():
    pem_str = os.environ.get(ENV_PRIVATE_KEY)
    if not pem_str:
        raise RuntimeError(
            f"Environment variable {ENV_PRIVATE_KEY} is not set. "
            "Configure it from GitHub Secrets with the RSA private key."
        )
    pem_bytes = pem_str.encode("utf-8")
    return serialization.load_pem_private_key(pem_bytes, password=None)


def decrypt_aes_cbc(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    # Remove PKCS7 padding
    unpadder = sym_padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Path to encrypted predictions.enc file.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Path to decrypted predictions.csv output.",
    )
    args = parser.parse_args()

    enc_path = Path(args.input)
    out_path = Path(args.output)

    if not enc_path.exists():
        raise FileNotFoundError(f"Encrypted submission not found: {enc_path}")

    private_key = load_private_key_from_env()
    data = enc_path.read_bytes()

    if len(data) < 4 + 16:
        raise ValueError("Encrypted file is too short or malformed.")

    # First 4 bytes: length of encrypted AES key
    key_len = int.from_bytes(data[:4], byteorder="big")
    offset = 4

    enc_key = data[offset:offset + key_len]
    offset += key_len
    iv = data[offset:offset + 16]
    ciphertext = data[offset + 16:]

    if len(enc_key) != key_len or len(iv) != 16 or len(ciphertext) == 0:
        raise ValueError("Encrypted submission format is invalid.")

    # Decrypt AES key with RSA OAEP(SHA256)
    aes_key = private_key.decrypt(
        enc_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Decrypt CSV with AES-256-CBC
    plaintext = decrypt_aes_cbc(ciphertext, aes_key, iv)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(plaintext)

    print(f"✓ Decrypted predictions written to: {out_path}")


if __name__ == "__main__":
    main()



