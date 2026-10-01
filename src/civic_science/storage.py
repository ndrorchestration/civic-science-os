from __future__ import annotations
import csv
from pathlib import Path
import yaml
from .models import SessionRecord

ROOT = Path("participation")
SESSIONS = ROOT / "sessions"

def save_session(record: SessionRecord, root: Path = ROOT) -> Path:
    sessions = root / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    path = sessions / f"{record.session_id}.yaml"
    data = record.model_dump(mode="json")
    data["duration_minutes"] = record.duration_minutes
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    rebuild_index(root)
    return path

def load_sessions(root: Path = ROOT) -> list[SessionRecord]:
    sessions = root / "sessions"
    if not sessions.exists():
        return []
    records = []
    for path in sorted(sessions.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        data.pop("duration_minutes", None)
        records.append(SessionRecord.model_validate(data))
    return records

def rebuild_index(root: Path = ROOT) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    out = root / "session-log.csv"
    rows = []
    for r in load_sessions(root):
        rows.append({
            "session_id": str(r.session_id), "started_at": r.started_at.isoformat(),
            "ended_at": r.ended_at.isoformat(), "duration_minutes": r.duration_minutes,
            "ecosystem": r.ecosystem, "project": r.project,
            "classifications_completed": r.classifications_completed,
            "classification_mode": r.classification_mode,
            "ai_assistance_during_classification": r.ai_assistance_during_classification,
            "claim_status": r.claim_status.value,
        })
    fields = ["session_id","started_at","ended_at","duration_minutes","ecosystem","project","classifications_completed","classification_mode","ai_assistance_during_classification","claim_status"]
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    return out
