import argparse

from .snapshot import create_snapshot, list_snapshots, restore_snapshot
from .store import BlockStore


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="snapvault",
        description="Incremental backup with block-level deduplication.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create a new backup repository")
    p.add_argument("repo")

    p = sub.add_parser("backup", help="back up a folder")
    p.add_argument("repo")
    p.add_argument("source")

    p = sub.add_parser("list", help="list snapshots")
    p.add_argument("repo")

    p = sub.add_parser("restore", help="restore a snapshot")
    p.add_argument("repo")
    p.add_argument("snapshot_id")
    p.add_argument("dest")

    args = parser.parse_args(argv)
    store = BlockStore(args.repo)

    if args.command == "init":
        store.init()
        print("Initialized repository at " + args.repo)
    elif args.command == "backup":
        snap_id, new, total = create_snapshot(store, args.source)
        print(f"Snapshot {snap_id}: {new} new blocks, {total - new} deduplicated")
    elif args.command == "list":
        for snap_id in list_snapshots(store):
            print(snap_id)
    elif args.command == "restore":
        n = restore_snapshot(store, args.snapshot_id, args.dest)
        print(f"Restored {n} files to {args.dest}")


if __name__ == "__main__":
    main()
