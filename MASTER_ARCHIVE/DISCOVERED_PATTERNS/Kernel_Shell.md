# Kernel Shell

## Pattern Overview

The distinction between kernel (core, immutable) and shell (interface, adaptable) enables stable evolution.

## Structural Model

```
┌─────────────────────────────────┐
│           SHELL                 │
│  (Interfaces, Patterns, Tools)  │
│  ┌─────────────────────────┐   │
│  │        KERNEL           │   │
│  │  (Axioms, Core Logic)   │   │
│  │  ┌─────────────────┐   │   │
│  │  │   IMMUTABLE     │   │   │
│  │  │   (Layer 4)     │   │   │
│  │  └─────────────────┘   │   │
│  └─────────────────────────┘   │
└─────────────────────────────────┘
```

## Layer Mapping

| Component | Layer | Mutability |
|-----------|-------|------------|
| A1, A2, A4, A7, A9 | 4 | Immutable |
| A3, A5, A6, A8 | 3 | Revisable |
| Patterns | Shell | Extensible |
| Tools | Shell | Upgradable |

## Axiom Grounding

- **A4**: Kernel process defines shell behavior
- **A6**: Shell can self-organize around kernel
- **A9**: Kernel-shell tension is data, not error

## Governance Protocol

- Shell changes: Standard process
- Layer 3 changes: Governance amendment (Phase 11.4)
- Layer 4 changes: Not permitted

## Integration Notes

- [ ] Kernel boundaries defined
- [ ] Shell interfaces documented
- [ ] Change protocols established
