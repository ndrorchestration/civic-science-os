# Windows deployment — v0.2.1

Status: PROCEDURE READY / LOCAL EXECUTION PENDING.

This procedure verifies the logger on a Windows host. It does not perform or validate scientific classification.

## Preconditions

- Windows host is available.
- Git and Python 3.10+ are installed.
- Repository source is checked out at the intended verified release tag or exact commit.
- No Planet Hunters TESS subject needs to be open during installation or verification.

## Clean deployment

```powershell
git clone https://github.com/ndrorchestration/civic-science-os.git
cd civic-science-os
git fetch --tags
git checkout v0.2.1
Set-ExecutionPolicy -Scope Process Bypass
.\INSTALL-WINDOWS.ps1
.\VERIFY-WINDOWS.ps1
```

If the tag has not yet been published, use the exact release commit SHA recorded in `docs/RELEASE_PROVENANCE.md`.

## Required verification evidence

Record:
- machine identifier;
- checked-out commit SHA;
- Python version;
- pytest result;
- CLI smoke result;
- installation timestamp with timezone.

## Acceptance

Windows-local deployment is verified only if:
- the checked-out source matches the intended release commit;
- `VERIFY-WINDOWS.ps1` exits successfully;
- pytest passes;
- `civic-science --help` succeeds.

## Non-effects

Windows-local PASS does not establish:
- that a citizen-science session occurred;
- classification quality or skill;
- scientific impact;
- project endorsement;
- independent validation;
- permission to automate classifications.

Human scientific judgment remains separate from software deployment.
