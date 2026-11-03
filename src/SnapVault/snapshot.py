import json
import os
import time

from .chunker import chunk_file
from .store import BlockStore


def create_snapshot(store: BlockStore, source: str):
    source = os.path.abspath(source)
    files = {}
    new_blocks = 0
    total_blocks = 0
    for dirpath, _, names in os.walk(source):
        for name in sorted(names):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, source).replace(os.sep, "/")
            hashes = []
            for block_hash, data in chunk_file(full):
                total_blocks += 1
                if store.put(block_hash, data):
                    new_blocks += 1
                hashes.append(block_hash)
            files[rel] = hashes
    snap_id = time.strftime("%Y%m%d-%H%M%S")
    manifest = {"id": snap_id, "source": source, "files": files}
    path = os.path.join(store.snapshots_dir, snap_id + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    return snap_id, new_blocks, total_blocks


def list_snapshots(store: BlockStore):
    names = sorted(os.listdir(store.snapshots_dir))
    return [n[:-5] for n in names if n.endswith(".json")]


def load_snapshot(store: BlockStore, snap_id: str):
    path = os.path.join(store.snapshots_dir, snap_id + ".json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def restore_snapshot(store: BlockStore, snap_id: str, dest: str) -> int:
    manifest = load_snapshot(store, snap_id)
    dest = os.path.abspath(dest)
    count = 0
    for rel, hashes in manifest["files"].items():
        target = os.path.abspath(os.path.join(dest, rel))
        if not target.startswith(dest + os.sep):
            raise ValueError("Unsafe path in snapshot: " + rel)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            for block_hash in hashes:
                f.write(store.get(block_hash))
        count += 1
    return count
