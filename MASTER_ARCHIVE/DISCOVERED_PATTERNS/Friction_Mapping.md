# Friction Mapping

## Pattern Overview

Friction is not failure—it is feedback from the system about flow constraints and kinetic limits.

## Recognition Triggers

- Rate limits (429 errors)
- Quotas exceeded
- Blocked resources
- System overload signals
- "Stuck" states

## Structural Analysis

| Friction Type | Signal | Response Protocol |
|--------------|--------|-------------------|
| API Throttling | 429 | INITIATE_BACKOFF |
| Resource Exhaustion | Timeout | Checkpoint & Wait |
| System Overload | Latency | Scale Down Flow |
| Cognitive Overload | Confusion | Simplify Scope |

## Axiom Grounding

- **A4**: Process over product—respect the rhythm
- **A8**: Use checkpoints to preserve continuity
- **A9**: Friction signals are data, not punishment

## Pattern Reference

→ **P126 (Kinetic Vein)**: Primary pattern for friction mapping

## Integration Notes

- [ ] Friction sources cataloged
- [ ] Response protocols tested
- [ ] Backoff algorithms calibrated
