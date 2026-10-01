# Civic Science Contribution OS

A provenance-first logger for human citizen-science participation. The current released software line is v0.2.x; v0.2.1 is the provenance-integrity patch.

## Safety / research boundary

This tool does **not** inspect citizen-science subjects, recommend classifications, automate clicks, or submit decisions. For the Planet Hunters TESS pilot, classification is HUMAN_ONLY and external generative-AI assistance during classification is prohibited unless explicit project permission is recorded.

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

From PowerShell in the repository folder:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\INSTALL-WINDOWS.ps1
.\VERIFY-WINDOWS.ps1
```

The bootstrap creates a local `.venv`; it does not configure browser automation, API submission, or classification assistance.

## v0.2 hardening

v0.2 adds:
- strict rejection of unknown session fields;
- timezone validation for all recorded timestamps;
- coupled explanation requirements for `OTHER` ambiguity;
- Jinja2 weekly rendering;
- `NOT_APPLICABLE` zero-session AI-boundary status;
- derived ambiguity and evidence indexes;
- richer post-session CLI capture;
- expanded invariant coverage.

## Verification

GitHub Actions tests Python 3.10–3.13, package installation, pytest, and the CLI smoke path. See `docs/RELEASE_PROVENANCE.md` for exact evidence and claim ceilings, and `docs/WINDOWS_DEPLOYMENT.md` for the bounded local-install procedure.

## Manifest provenance

`TRANSFER_MANIFEST.sha256.json` preserves the original v0.1 transfer/archive hashes as historical provenance. `MANIFEST.sha256.json` is the canonical current-source manifest for the explicitly covered executable/test/deployment payload. CI runs `tools/verify_manifest.py` and fails closed on hash or byte-count drift.
