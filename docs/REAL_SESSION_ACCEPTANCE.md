# Real-session acceptance gate

The software publication gate is already satisfied separately. This gate concerns functional exercise against real human participation.

## Session 1 acceptance checks

- [ ] Human classification session actually occurred.
- [ ] Start/end timestamps are timezone-aware.
- [ ] Planet Hunters TESS remains recorded as HUMAN_ONLY.
- [ ] AI assistance during classification is false.
- [ ] At least one current instruction source is retained.
- [ ] Classification count is null or a non-negative platform-visible value.
- [ ] Any ambiguity codes are drawn from the controlled vocabulary.
- [ ] The saved YAML validates through `civic-science session validate`.
- [ ] The derived CSV index rebuilds successfully.
- [ ] `civic-science review weekly` generates the first real process review.
- [ ] Review contains the bounded-impact disclaimer.

## Promotion

When all checks pass, state may advance from:

`SOFTWARE PUBLICATION VERIFIED / REAL-PARTICIPATION VALIDATION PENDING`

to:

`SOFTWARE PUBLICATION VERIFIED / ONE REAL SESSION FUNCTIONALLY EXERCISED`

Do not promote beyond one-session functional exercise until the three-session pilot gate is complete.
