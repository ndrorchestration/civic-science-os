from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.sha256.json"

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def main() -> int:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    failures = []
    for entry in data["files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            failures.append(f"missing: {entry['path']}")
            continue
        actual_hash = sha256(path)
        actual_bytes = path.stat().st_size
        if actual_hash != entry["sha256"]:
            failures.append(f"sha256 mismatch: {entry['path']} expected={entry['sha256']} actual={actual_hash}")
        if actual_bytes != entry["bytes"]:
            failures.append(f"byte-count mismatch: {entry['path']} expected={entry['bytes']} actual={actual_bytes}")
    if failures:
        print("MANIFEST VERIFICATION FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print(f"MANIFEST VERIFIED: {len(data['files'])} covered files")
    return 0

if __name__ == "__main__":
    sys.exit(main())
