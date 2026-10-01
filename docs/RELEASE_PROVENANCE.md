# Release provenance — v0.1.0

Status: CODED_AND_TESTED / READY_TO_TRANSFER / NOT FUNCTIONALLY EXERCISED ON REAL PARTICIPATION.

## Intended scope

Civic Science Contribution OS v0.1.0 records and validates human citizen-science participation sessions, derives a CSV index, and generates bounded weekly process reviews.

It does not inspect project subjects, recommend classifications, automate classification controls, submit classifications, estimate scientific accuracy, or claim scientific impact.

## First pilot

The first planned pilot is Planet Hunters TESS on Zooniverse. The local pilot contract requires `HUMAN_ONLY` classification and `ai_assistance_during_classification=false` unless explicit project authorization is later recorded.

## Verification expectations

- Python 3.10+ package installation succeeds.
- The invariant test suite passes.
- `civic-science --help` succeeds.
- Windows bootstrap and verification scripts are provided for local deployment.
- Real-participation status must not advance until a human session is actually completed and logged.

## Claim ceiling

Passing CI establishes only software-level conformance to this bounded logger contract. It does not establish classification skill, citizen-science contribution impact, project endorsement, scientific validity, independent validation, or authorization to automate classifications.
