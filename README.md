# SnapVault

Incremental backup tool with block-level deduplication, written in Python.

SnapVault splits files into fixed-size blocks, hashes each block with SHA-256 and
stores every unique block only once. Each backup is a small JSON manifest that
lists which blocks make up each file, so repeated backups of mostly unchanged
folders take very little extra space.

It is a command-line tool for anyone who wants a simple, transparent backup
format with no dependencies beyond the Python standard library.

## Install

```
git clone https://github.com/MirceaStan04/SnapVault
cd SnapVault
pip install -e .
```

Requires Python 3.9 or newer.

## Usage

```
snapvault init vault                  # create a repository
snapvault backup vault ./Documents    # create a snapshot
snapvault list vault                  # list snapshots
snapvault restore vault <id> ./out    # restore a snapshot
```

Running `backup` twice on an unchanged folder stores 0 new blocks.

## Tests

```
pip install pytest
pytest
```

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## License

MIT
