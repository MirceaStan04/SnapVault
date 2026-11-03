from SnapVault.chunker import chunk_file


def test_chunk_file_splits_and_hashes(tmp_path):
    p = tmp_path / "a.bin"
    p.write_bytes(b"x" * 150)
    chunks = list(chunk_file(str(p), chunk_size=64))
    assert len(chunks) == 3
    assert chunks[0][0] == chunks[1][0]
    assert chunks[2][1] == b"x" * 22
