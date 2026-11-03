# Roadmap

- [x] Fixed-size chunking with SHA-256
- [x] Block store with deduplication
- [x] Snapshots as JSON manifests
- [x] CLI: init, backup, list, restore
- [ ] `verify` command to check block integrity
- [ ] Compression of stored blocks (zlib / zstd)
- [ ] Content-defined chunking (rolling hash)
- [ ] `prune` command to delete old snapshots and unused blocks
- [ ] `.snapignore` and `--dry-run`
- [ ] Space-savings statistics per snapshot
- [ ] More tests (edge cases, empty files, large files)
- [ ] CI with GitHub Actions
