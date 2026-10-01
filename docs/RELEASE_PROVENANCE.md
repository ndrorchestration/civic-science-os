# Release provenance — v0.2.0

Status: SOFTWARE VERIFIED / RELEASE CANDIDATE / NOT FUNCTIONALLY EXERCISED ON REAL PARTICIPATION.

## Exact verified source

Verified source head before release-documentation update:
`6378ced0b34ecd77b47cf656ed2439baa2446d80`

GitHub Actions run:
`36926696579`

Verification result:
- Python 3.10: SUCCESS
- Python 3.11: SUCCESS
- Python 3.12: SUCCESS
- Python 3.13: SUCCESS
- package install: SUCCESS
- pytest: SUCCESS
- CLI smoke: SUCCESS

A later release-documentation commit must receive its own exact-head CI result before becoming the tagged release target.

## Intended scope

Civic Science Contribution OS v0.2.0 records and validates human citizen-science participation sessions, derives process indexes, and generates bounded weekly process reviews.

It does not inspect project subjects, recommend classifications, automate classification controls, submit classifications, estimate scientific accuracy, or claim scientific impact.

## v0.2.0 hardening

- Extra/unknown fields are forbidden in canonical session records.
- `started_at`, `ended_at`, and `recorded_at` must be timezone-aware.
- `OTHER` ambiguity requires an explanatory note; orphaned OTHER notes are rejected.
- Weekly reports render via Jinja2.
- Zero-session AI-boundary status is `NOT_APPLICABLE`.
- `session-log.csv`, `ambiguity-log.csv`, and `evidence-register.csv` are derived from canonical YAML.
- Post-session CLI capture supports ambiguity, friction, learning, and follow-up fields.
- Tests cover invalid claim status, invalid ambiguity code, extra-field rejection, and ambiguity-note coupling.

## First pilot

Planet Hunters TESS remains the first planned pilot. The controlling local contract requires `HUMAN_ONLY` and `ai_assistance_during_classification=false` unless explicit project authorization is later recorded.

## Claim ceiling

Passing software CI establishes only software-level conformance to this bounded logger contract. It does not establish:
- classification skill;
- scientific accuracy;
- citizen-science contribution impact;
- project endorsement;
- scientific validity;
- independent validation;
- exoplanet discovery;
- authorization to automate classifications.

## Real-participation promotion gate

State may advance to `ONE REAL SESSION FUNCTIONALLY EXERCISED` only after:
1. a real human-only session occurs;
2. no external generative AI aids classification;
3. the process record validates;
4. derived indexes rebuild;
5. the first real process review is generated.
