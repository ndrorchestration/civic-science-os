from __future__ import annotations
from datetime import datetime
from pathlib import Path
import typer, yaml
from .models import SessionRecord
from .storage import load_sessions, save_session
from .review import render_weekly

app = typer.Typer(help="Civic Science Contribution OS logger")
session_app = typer.Typer(); review_app = typer.Typer()
app.add_typer(session_app, name="session"); app.add_typer(review_app, name="review")

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
    for r in load_sessions(): typer.echo(f"{r.session_id}\t{r.started_at.isoformat()}\t{r.project}\t{r.duration_minutes}m")

@session_app.command("add")
def add_session(started_at: str, ended_at: str, classifications_completed: int | None = None, uncertainty_notes: str = "", learning_notes: str = ""):
    record = SessionRecord(
        started_at=datetime.fromisoformat(started_at), ended_at=datetime.fromisoformat(ended_at),
        ecosystem="zooniverse", project="Planet Hunters TESS",
        project_url="https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess",
        workflow="Do you see a Transit?",
        instruction_sources=["https://www.zooniverse.org/projects/nora-dot-eisner/planet-hunters-tess"],
        classifications_completed=classifications_completed, uncertainty_notes=uncertainty_notes,
        learning_notes=learning_notes,
    )
    typer.echo(str(save_session(record)))

@review_app.command("weekly")
def weekly(output: Path = Path("reports/weekly-review.md")):
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_weekly(load_sessions()), encoding="utf-8")
    typer.echo(str(output))
