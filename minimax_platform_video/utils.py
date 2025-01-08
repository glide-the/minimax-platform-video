import hashlib


def _hash(_input: str) -> str:
    """Use a deterministic hashing approach."""
    return hashlib.md5(_input.encode()).hexdigest()  # noqa S324


def create_hash_key(operation: str, parameters: dict) -> str:
    parameters_str = str(sorted((k, v) for k, v in parameters.items()))
    return f"{operation}-{_hash(parameters_str)}"
