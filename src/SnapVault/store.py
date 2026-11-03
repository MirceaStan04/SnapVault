import os


class BlockStore:
    def __init__(self, root: str):
        self.root = root
        self.blocks_dir = os.path.join(root, "blocks")
        self.snapshots_dir = os.path.join(root, "snapshots")

    def init(self) -> None:
        os.makedirs(self.blocks_dir, exist_ok=True)
        os.makedirs(self.snapshots_dir, exist_ok=True)

    def _block_path(self, block_hash: str) -> str:
        return os.path.join(self.blocks_dir, block_hash[:2], block_hash)

    def has(self, block_hash: str) -> bool:
        return os.path.exists(self._block_path(block_hash))

    def put(self, block_hash: str, data: bytes) -> bool:
        """Store a block. Return True if it was new, False if deduplicated."""
        path = self._block_path(block_hash)
        if os.path.exists(path):
            return False
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "wb") as f:
            f.write(data)
        os.replace(tmp, path)
        return True

    def get(self, block_hash: str) -> bytes:
        with open(self._block_path(block_hash), "rb") as f:
            return f.read()
