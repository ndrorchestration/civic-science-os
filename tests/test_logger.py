from datetime import datetime, timedelta
from pathlib import Path
import csv
import pytest
from pydantic import ValidationError
from civic_science.models import AmbiguityCode, SessionRecord
from civic_science.storage import save_session, load_sessions, rebuild_indexes
from civic_science.review import render_weekly, DISCLAIMER

BASE = dict(
    ecosystem="zooniverse",
    project="Planet Hunters TESS",
    project_url="https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess",
    instruction_sources=[
        "https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess",
        "https://www.zooniverse.org/about/ai-ethics",
    ],
)

def make(**kw):
    start = datetime.now().astimezone()
    end = start + timedelta(minutes=20)
    return SessionRecord(started_at=start, ended_at=end, **BASE, **kw)

def test_valid_human_only():
    r = make(classifications_completed=3)
    assert r.duration_minutes == 20

def test_ai_rejected():
    with pytest.raises(ValueError):
        make(ai_assistance_during_classification=True)

def test_bad_time_rejected():
    start = datetime.now().astimezone()
    with pytest.raises(ValueError):
        SessionRecord(started_at=start, ended_at=start - timedelta(minutes=1), **BASE)

def test_negative_count_rejected():
    with pytest.raises(ValueError):
        make(classifications_completed=-1)

def test_missing_instruction_source_rejected():
    data = BASE | {"instruction_sources": []}
    with pytest.raises(ValueError):
        SessionRecord(started_at=datetime.now().astimezone(), ended_at=datetime.now().astimezone(), **data)

def test_naive_timestamps_rejected():
    with pytest.raises(ValueError, match="timezone-aware"):
        SessionRecord(
            started_at="2026-10-01T14:00:00",
            ended_at="2026-10-01T14:10:00",
            **BASE,
        )

def test_unknown_extra_field_rejected():
    payload = make().model_dump(mode="json")
    payload["classification_recommendation"] = "transit"
    with pytest.raises(ValidationError):
        SessionRecord.model_validate(payload)

def test_other_requires_note():
    with pytest.raises(ValueError, match="OTHER ambiguity code requires"):
        make(ambiguity_codes=[AmbiguityCode.OTHER])

def test_other_note_requires_other_code():
    with pytest.raises(ValueError, match="requires ambiguity code OTHER"):
        make(other_ambiguity_note="unusual pattern")

def test_roundtrip_and_all_indexes(tmp_path: Path):
    save_session(
        make(
            classifications_completed=2,
            ambiguity_codes=[AmbiguityCode.LOW_SIGNAL, AmbiguityCode.OTHER],
            other_ambiguity_note="unclear artifact",
        ),
        tmp_path,
    )
    records = load_sessions(tmp_path)
    assert len(records) == 1
    paths = rebuild_indexes(tmp_path)
    assert all(path.exists() for path in paths.values())
    with paths["ambiguity_log"].open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 2
    assert any(row["code"] == "OTHER" and row["note"] == "unclear artifact" for row in rows)
    with paths["evidence_register"].open(encoding="utf-8") as f:
        evidence = list(csv.DictReader(f))
    assert len(evidence) == 2

def test_review_uses_bounded_disclaimer():
    report = render_weekly([make(classifications_completed=2)])
    assert DISCLAIMER in report
    assert "AI-boundary compliance: PASS" in report
    assert "Missing/invalid provenance fields: none detected" in report

def test_zero_session_review_is_not_applicable():
    report = render_weekly([])
    assert "Sessions: 0" in report
    assert "AI-boundary compliance: NOT_APPLICABLE" in report
    assert "does not estimate classification accuracy" in report

def test_unknown_claim_status_rejected():
    payload = make().model_dump(mode="json")
    payload["claim_status"] = "CERTAIN"
    with pytest.raises(ValidationError):
        SessionRecord.model_validate(payload)

def test_unknown_ambiguity_rejected():
    payload = make().model_dump(mode="json")
    payload["ambiguity_codes"] = ["NOT_A_REAL_CODE"]
    with pytest.raises(ValidationError):
        SessionRecord.model_validate(payload)
