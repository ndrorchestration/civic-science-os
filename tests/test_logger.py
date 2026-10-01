from datetime import datetime, timedelta
from pathlib import Path
import pytest
from civic_science.models import SessionRecord
from civic_science.storage import save_session, load_sessions
from civic_science.review import render_weekly, DISCLAIMER

BASE = dict(ecosystem="zooniverse", project="Planet Hunters TESS",
            project_url="https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess",
            instruction_sources=["https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess"])

def make(**kw):
    start = datetime.now().astimezone(); end = start + timedelta(minutes=20)
    return SessionRecord(started_at=start, ended_at=end, **BASE, **kw)

def test_valid_human_only():
    r = make(classifications_completed=3); assert r.duration_minutes == 20

def test_ai_rejected():
    with pytest.raises(ValueError): make(ai_assistance_during_classification=True)

def test_bad_time_rejected():
    start = datetime.now().astimezone()
    with pytest.raises(ValueError): SessionRecord(started_at=start, ended_at=start-timedelta(minutes=1), **BASE)

def test_negative_count_rejected():
    with pytest.raises(ValueError): make(classifications_completed=-1)

def test_missing_instruction_source_rejected():
    data = BASE | {"instruction_sources": []}
    with pytest.raises(ValueError): SessionRecord(started_at=datetime.now().astimezone(), ended_at=datetime.now().astimezone(), **data)

def test_roundtrip_and_review(tmp_path: Path):
    save_session(make(classifications_completed=2), tmp_path)
    records = load_sessions(tmp_path)
    assert len(records) == 1
    report = render_weekly(records)
    assert DISCLAIMER in report and "AI-boundary compliance: PASS" in report

def test_zero_session_review_is_bounded():
    report = render_weekly([])
    assert "Sessions: 0" in report and "does not estimate classification accuracy" in report

def test_naive_timestamps_rejected(tmp_path, monkeypatch):
    with pytest.raises(ValueError, match="timezone-aware"):
        SessionRecord(
            started_at="2026-10-01T14:00:00",
            ended_at="2026-10-01T14:10:00",
            ecosystem="zooniverse",
            project="Planet Hunters TESS",
            project_url="https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess",
            instruction_sources=["https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess"],
        )
