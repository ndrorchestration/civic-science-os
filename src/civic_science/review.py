from __future__ import annotations
from collections import Counter
from datetime import date
from jinja2 import Template
from .models import SessionRecord

DISCLAIMER = "This report summarizes contribution-process records. It does not estimate classification accuracy, scientific impact, or project outcomes."

_TEMPLATE = Template("""# Civic Science Weekly Review — {{ start }} to {{ end }}

{{ disclaimer }}

- Sessions: {{ session_count }}
- Logged minutes: {{ minutes }}
- Recorded classifications: {{ classification_count }}
- AI-boundary compliance: {{ ai_compliance }}

## Ambiguity codes
{% if ambiguities %}{% for code, count in ambiguities %}- {{ code }}: {{ count }}
{% endfor %}{% else %}- None recorded
{% endif %}
## Procedural friction
{% if friction %}{% for item in friction %}- {{ item }}
{% endfor %}{% else %}- None recorded
{% endif %}
## Learning notes
{% if notes %}{% for item in notes %}- {{ item }}
{% endfor %}{% else %}- None recorded
{% endif %}
## Provenance check
- Missing/invalid provenance fields: none detected among validated records.

## Next operational improvement candidates
{% if session_count == 0 %}- Complete the first real HUMAN_ONLY session before drawing workflow conclusions.
{% else %}- Review recurring ambiguity and friction patterns after the three-session pilot gate.
{% endif %}""")

def render_weekly(records: list[SessionRecord], start: date | None = None, end: date | None = None) -> str:
    start = start or min((r.started_at.date() for r in records), default=date.today())
    end = end or max((r.ended_at.date() for r in records), default=start)
    selected = [r for r in records if start <= r.started_at.date() <= end]
    mins = round(sum(r.duration_minutes for r in selected), 2)
    counts = [r.classifications_completed for r in selected if r.classifications_completed is not None]
    ambiguities = Counter(code.value for r in selected for code in r.ambiguity_codes)
    pht = [r for r in selected if r.project.strip().lower() == "planet hunters tess"]
    if not selected:
        ai_compliance = "NOT_APPLICABLE"
    elif all(r.classification_mode == "HUMAN_ONLY" and not r.ai_assistance_during_classification for r in pht):
        ai_compliance = "PASS"
    else:
        ai_compliance = "FAIL"
    return _TEMPLATE.render(
        start=start,
        end=end,
        disclaimer=DISCLAIMER,
        session_count=len(selected),
        minutes=mins,
        classification_count=sum(counts) if counts else "not recorded",
        ai_compliance=ai_compliance,
        ambiguities=sorted(ambiguities.items()),
        friction=[x for r in selected for x in r.procedural_friction],
        notes=[r.learning_notes for r in selected if r.learning_notes.strip()],
    ).rstrip() + "\n"
