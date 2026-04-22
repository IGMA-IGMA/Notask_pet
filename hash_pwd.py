import bcrypt


def hash_password(plain_password: str) -> bytes:
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt())


def check_password(stored_hash: bytes, plain_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), stored_hash)
