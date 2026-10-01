from __future__ import annotations
from datetime import datetime
from pathlib import Path
import typer, yaml
from .models import AmbiguityCode, SessionRecord
from .storage import load_sessions, save_session
from .review import render_weekly

app = typer.Typer(help="Civic Science Contribution OS logger")
session_app = typer.Typer()
review_app = typer.Typer()
app.add_typer(session_app, name="session")
app.add_typer(review_app, name="review")

PROJECT_URL = "https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess"
WORKFLOW_URL = "https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess/classify"
AI_ETHICS_URL = "https://www.zooniverse.org/about/ai-ethics"

@app.command()
def init():
    Path("participation/sessions").mkdir(parents=True, exist_ok=True)
    Path("reports").mkdir(parents=True, exist_ok=True)
    typer.echo("Initialized civic-science workspace.")

@session_app.command("validate")
def validate(path: Path):
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    data.pop("duration_minutes", None)
    SessionRecord.model_validate(data)
    typer.echo("VALID")

@session_app.command("list")
def list_sessions():
    for r in load_sessions():
        typer.echo(f"{r.session_id}\t{r.started_at.isoformat()}\t{r.project}\t{r.duration_minutes}m")

@session_app.command("add")
def add_session(
    started_at: str,
    ended_at: str,
    classifications_completed: int | None = None,
    uncertainty_notes: str = "",
    ambiguity_codes: str = "",
    other_ambiguity_note: str = "",
    procedural_friction: str = "",
    learning_notes: str = "",
    follow_up: str = "",
):
    codes = [AmbiguityCode(x.strip()) for x in ambiguity_codes.split(",") if x.strip()]
    friction = [x.strip() for x in procedural_friction.split("|") if x.strip()]
    record = SessionRecord(
        started_at=datetime.fromisoformat(started_at),
        ended_at=datetime.fromisoformat(ended_at),
        ecosystem="zooniverse",
        project="Planet Hunters TESS",
        project_url=PROJECT_URL,
        workflow="Do you see a Transit?",
        instruction_sources=[PROJECT_URL, WORKFLOW_URL, AI_ETHICS_URL],
        classifications_completed=classifications_completed,
        uncertainty_notes=uncertainty_notes,
        ambiguity_codes=codes,
        other_ambiguity_note=other_ambiguity_note,
        procedural_friction=friction,
        learning_notes=learning_notes,
        follow_up=follow_up,
    )
    typer.echo(str(save_session(record)))

@review_app.command("weekly")
def weekly(output: Path = Path("reports/weekly-review.md")):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_weekly(load_sessions()), encoding="utf-8")
    typer.echo(str(output))
