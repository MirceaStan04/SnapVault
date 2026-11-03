import hashlib
from typing import Iterator, Tuple

CHUNK_SIZE = 64 * 1024


def chunk_file(path: str, chunk_size: int = CHUNK_SIZE) -> Iterator[Tuple[str, bytes]]:
    """Yield (sha256_hex, data) for each fixed-size block of a file."""
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield hashlib.sha256(data).hexdigest(), data
