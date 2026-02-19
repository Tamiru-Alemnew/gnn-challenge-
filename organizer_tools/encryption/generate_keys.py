"""
The Cold Start Citation Challenge 2026
--------------------------------------
Script: RSA Key Generation
Description: Generates an RSA-2048 key pair for secure submission encryption.
Author: Competition Organizers

Usage:
    python generate_keys.py

Output:
    - private_key.pem              (DO NOT COMMIT; upload to GitHub Secrets)
    - competition_public_key.pem   (commit this to competition/ folder)
"""

from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def main() -> None:
    repo_root = Path(__file__).parent.parent.parent  # repo root (goes up: encryption -> organizer_tools -> repo)
    enc_dir = Path(__file__).parent          # organizer_tools/encryption
    enc_dir.mkdir(parents=True, exist_ok=True)

    # Generate RSA-2048 private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    # Serialize private key (PEM, PKCS8, no password)
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    private_key_path = enc_dir / "private_key.pem"
    with open(private_key_path, "wb") as f:
        f.write(private_pem)

    # Serialize public key (PEM, SubjectPublicKeyInfo)
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    competition_dir = repo_root / "competition"
    competition_dir.mkdir(parents=True, exist_ok=True)
    public_key_path = competition_dir / "competition_public_key.pem"
    with open(public_key_path, "wb") as f:
        f.write(public_pem)

    print("=" * 70)
    print("RSA-2048 key pair generated.")
    print(f"Private key (KEEP SECRET, DO NOT COMMIT): {private_key_path}")
    print(f"Public key (commit this file):           {public_key_path}")
    print()
    print("Next steps for organizers:")
    print("  1. Open private_key.pem and copy its full contents.")
    print("  2. In GitHub → Settings → Secrets → Actions, create:")
    print("       Name: SUBMISSION_PRIVATE_KEY")
    print("       Value: [paste entire PEM, including BEGIN/END lines]")
    print("  3. Commit competition_public_key.pem to the repo.")
    print("=" * 70)


if __name__ == "__main__":
    main()


