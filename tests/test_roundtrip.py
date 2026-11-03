from SnapVault.snapshot import create_snapshot, restore_snapshot
from SnapVault.store import BlockStore


def test_backup_dedup_and_restore(tmp_path):
    src = tmp_path / "src"
    src.mkdir()
    (src / "a.txt").write_bytes(b"hello world" * 10000)
    (src / "b.txt").write_bytes(b"hello world" * 10000)

    store = BlockStore(str(tmp_path / "vault"))
    store.init()

    snap_id, new, total = create_snapshot(store, str(src))
    assert new < total

    out = tmp_path / "out"
    assert restore_snapshot(store, snap_id, str(out)) == 2
    assert (out / "a.txt").read_bytes() == (src / "a.txt").read_bytes()
    assert (out / "b.txt").read_bytes() == (src / "b.txt").read_bytes()
