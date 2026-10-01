# Civic Science Contribution OS

A provenance-first logger for human citizen-science participation. The v0 implementation records sessions, validates the human/AI boundary, rebuilds a derived CSV index, and generates bounded weekly process reviews.

## Safety / research boundary

This tool does **not** inspect citizen-science subjects, recommend classifications, automate clicks, or submit decisions. For the Planet Hunters TESS pilot, classification is HUMAN_ONLY and external generative-AI assistance during classification is forbidden by the local pilot contract.

## Install

```bash
python -m pip install -e .
```

## Use

```bash
civic-science init
civic-science session add --started-at "2026-10-01T14:00:00-04:00" --ended-at "2026-10-01T14:20:00-04:00" --classifications-completed 5
civic-science session list
civic-science review weekly
```

The generated weekly report is process evidence only; it does not estimate classification accuracy, scientific impact, or project outcomes.


## Windows bootstrap

From PowerShell in the extracted folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\INSTALL-WINDOWS.ps1
.\VERIFY-WINDOWS.ps1
```

The bootstrap creates a local `.venv`; it does not configure browser automation, API submission, or classification assistance.

## Repository verification

The repository-ready scaffold includes a GitHub Actions matrix for Python 3.10–3.13, running the invariant suite and a CLI smoke test. See `docs/RELEASE_PROVENANCE.md` for the exact evidence and claim ceiling for v0.1.0.
