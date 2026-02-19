"""
The Cold Start Citation Challenge 2026
--------------------------------------
Script: Submission Encryption (Hybrid RSA + AES-256-CBC)
Description: Encrypts predictions.csv into predictions.enc using the
             competition public key for secure submission.
Author: Competition Organizers

Usage:
    python encrypt_submission.py \
        --predictions submissions/inbox/team/run_001/predictions.csv \
        --public-key competition/competition_public_key.pem \
        --output submissions/inbox/team/run_001/predictions.enc

Output format (binary):
    [4-byte big-endian len(enc_key)] +
    [encrypted_aes_key] +
    [16-byte IV] +
    [encrypted_data]
"""

import argparse
import os
from pathlib import Path

from cryptography.hazmat.primitives import hashes, padding as sym_padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def load_public_key(public_key_path: Path):
    with open(public_key_path, "rb") as f:
        data = f.read()
    return serialization.load_pem_public_key(data)


def encrypt_aes_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    # PKCS7 padding to AES block size (128 bits)
    padder = sym_padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--predictions",
        type=str,
        required=True,
        help="Path to predictions.csv to encrypt.",
    )
    parser.add_argument(
        "--public-key",
        type=str,
        required=True,
        help="Path to competition_public_key.pem.",
    )
    parser.add_argument(
        "--output",
        type=str,
        required=False,
        help="Output encrypted file path (default: predictions.enc next to CSV).",
    )
    args = parser.parse_args()

    predictions_path = Path(args.predictions)
    public_key_path = Path(args.public_key)

    if not predictions_path.exists():
        raise FileNotFoundError(f"predictions.csv not found: {predictions_path}")
    if not public_key_path.exists():
        raise FileNotFoundError(f"Public key not found: {public_key_path}")

    if args.output:
        output_path = Path(args.output)
    else:
        output_path = predictions_path.with_suffix(".enc")

    # Read plaintext CSV
    plaintext = predictions_path.read_bytes()

    # Generate random AES-256 key and IV
    aes_key = os.urandom(32)  # 32 bytes = 256 bits
    iv = os.urandom(16)       # 16 bytes IV for AES-CBC

    # Encrypt CSV with AES-256-CBC
    ciphertext = encrypt_aes_cbc(plaintext, aes_key, iv)

    # Load RSA public key and encrypt AES key with OAEP(SHA256)
    public_key = load_public_key(public_key_path)
    enc_key = public_key.encrypt(
        aes_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Write envelope: [len(enc_key)][enc_key][iv][ciphertext]
    key_len_bytes = len(enc_key).to_bytes(4, byteorder="big")
    with open(output_path, "wb") as f:
        f.write(key_len_bytes)
        f.write(enc_key)
        f.write(iv)
        f.write(ciphertext)

    print(f"✓ Encrypted submission written to: {output_path}")
    print("Participants should keep predictions.csv private in their fork "
          "and submit only predictions.enc + metadata.json.")


if __name__ == "__main__":
    main()



