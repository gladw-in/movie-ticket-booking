"""Hashes and checks passwords safely."""

import hashlib
import hmac
import secrets

ALGORITHM = "pbkdf2_sha256"
ITERATIONS = 600_000


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{ALGORITHM}${ITERATIONS}${salt.hex()}${digest.hex()}"


def is_hashed(stored):
    return (
        isinstance(stored, str)
        and stored.startswith(f"{ALGORITHM}$")
        and stored.count("$") == 3
    )


def verify_password(password, stored):
    if not stored:
        return False
    if stored.count("$") != 3 or not stored.startswith(f"{ALGORITHM}$"):
        return hmac.compare_digest(password.encode("utf-8"), stored.encode("utf-8"))
    try:
        _, iterations, salt_hex, digest_hex = stored.split("$")
        candidate = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(candidate, bytes.fromhex(digest_hex))
    except ValueError:
        return False


def needs_rehash(stored):
    if stored is None or not is_hashed(stored):
        return True
    return int(stored.split("$")[1]) < ITERATIONS
