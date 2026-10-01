from __future__ import annotations
import csv
from pathlib import Path
import yaml
from .models import AmbiguityCode, SessionRecord

ROOT = Path("participation")

def save_session(record: SessionRecord, root: Path = ROOT) -> Path:
    sessions = root / "sessions"
    sessions.mkdir(parents=True, exist_ok=True)
    path = sessions / f"{record.session_id}.yaml"
    data = record.model_dump(mode="json")
    data["duration_minutes"] = record.duration_minutes
    path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
    rebuild_indexes(root)
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

def _write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

def rebuild_indexes(root: Path = ROOT) -> dict[str, Path]:
    root.mkdir(parents=True, exist_ok=True)
    records = load_sessions(root)

    session_rows = [{
        "session_id": str(r.session_id),
        "started_at": r.started_at.isoformat(),
        "ended_at": r.ended_at.isoformat(),
        "duration_minutes": r.duration_minutes,
        "ecosystem": r.ecosystem,
        "project": r.project,
        "classifications_completed": r.classifications_completed,
        "classification_mode": r.classification_mode,
        "ai_assistance_during_classification": r.ai_assistance_during_classification,
        "claim_status": r.claim_status.value,
    } for r in records]
    session_path = root / "session-log.csv"
    _write_csv(session_path, list(session_rows[0].keys()) if session_rows else [
        "session_id","started_at","ended_at","duration_minutes","ecosystem","project",
        "classifications_completed","classification_mode","ai_assistance_during_classification","claim_status"
    ], session_rows)

    ambiguity_rows = []
    for r in records:
        for code in r.ambiguity_codes:
            ambiguity_rows.append({
                "session_id": str(r.session_id),
                "code": code.value,
                "note": r.other_ambiguity_note if code == AmbiguityCode.OTHER else "",
            })
    ambiguity_path = root / "ambiguity-log.csv"
    _write_csv(ambiguity_path, ["session_id","code","note"], ambiguity_rows)

    evidence_rows = []
    for r in records:
        for source in r.instruction_sources:
            evidence_rows.append({
                "session_id": str(r.session_id),
                "source_url": str(source),
                "claim_status": r.claim_status.value,
                "recorded_at": r.recorded_at.isoformat(),
            })
    evidence_path = root / "evidence-register.csv"
    _write_csv(evidence_path, ["session_id","source_url","claim_status","recorded_at"], evidence_rows)
    return {"session_log": session_path, "ambiguity_log": ambiguity_path, "evidence_register": evidence_path}

def rebuild_index(root: Path = ROOT) -> Path:
    return rebuild_indexes(root)["session_log"]
