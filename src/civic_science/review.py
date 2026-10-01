from __future__ import annotations
from collections import Counter
from datetime import date
from pathlib import Path
from .models import SessionRecord

DISCLAIMER = "This report summarizes contribution-process records. It does not estimate classification accuracy, scientific impact, or project outcomes."

def render_weekly(records: list[SessionRecord], start: date | None = None, end: date | None = None) -> str:
    start = start or (min((r.started_at.date() for r in records), default=date.today()))
    end = end or (max((r.ended_at.date() for r in records), default=start))
    selected = [r for r in records if start <= r.started_at.date() <= end]
    mins = sum(r.duration_minutes for r in selected)
    counts = [r.classifications_completed for r in selected if r.classifications_completed is not None]
    ambiguities = Counter(code.value for r in selected for code in r.ambiguity_codes)
    compliant = all(r.classification_mode == "HUMAN_ONLY" and not r.ai_assistance_during_classification for r in selected if r.project.lower() == "planet hunters tess")
    lines = [f"# Civic Science Weekly Review — {start} to {end}", "", DISCLAIMER, "",
             f"- Sessions: {len(selected)}", f"- Logged minutes: {round(mins,2)}",
             f"- Recorded classifications: {sum(counts) if counts else 'not recorded'}",
             f"- AI-boundary compliance: {'PASS' if compliant else 'FAIL'}", "", "## Ambiguity codes"]
    lines += [f"- {k}: {v}" for k,v in sorted(ambiguities.items())] or ["- None recorded"]
    lines += ["", "## Procedural friction"]
    friction = [x for r in selected for x in r.procedural_friction]
    lines += [f"- {x}" for x in friction] or ["- None recorded"]
    lines += ["", "## Learning notes"]
    notes = [r.learning_notes for r in selected if r.learning_notes.strip()]
    lines += [f"- {x}" for x in notes] or ["- None recorded"]
    return "\n".join(lines) + "\n"
