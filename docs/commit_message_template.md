# Git Commit Message Templates - Tier 2 Format

## Standard Format

```
Tier 2: [Component] - [Action]
Coherence: [Impact on System]
Change: [Technical Detail]
```

---

## Examples by Component

### Postgres Component

```
Tier 2: Postgres - Fix Connection Loop
Coherence: Restored Memory Access (A2)
Change: Updated docker-compose.yml ports from 5433 to 5432
```

```
Tier 2: Postgres - Add Pattern Correlation Index
Coherence: Improved Research Query Performance
Change: Added GIN index on patterns_detected JSONB column
```

### n8n Component

```
Tier 2: n8n - Implement Error Handling in Extraction Logger
Coherence: Applied A9 (Contradiction is Data)
Change: Added try-catch with divergence logging in extraction_logger.js
```

```
Tier 2: n8n - Optimize Pattern Analyzer Algorithm
Coherence: Reduced Research Mode Processing Time
Change: Replaced nested loops with Map-based correlation counting
```

### Documentation Component

```
Tier 2: Docs - Add Research Report Template
Coherence: Standardized MODE A Output Format
Change: Created research/report_template.md with analysis structure
```

### Integration Component

```
Tier 2: Integration - Connect Slack Webhook to n8n
Coherence: Enabled MODE C Reporting (A1: Relational)
Change: Added slack_alert_generator.js with block formatting
```

### Schema Component

```
Tier 2: Schema - Add Divergence Tracking
Coherence: A9 Compliance (Contradiction is Data)
Change: Added is_divergence boolean and error_message columns
```

---

## Tier 1 Perfect (Rare - Only for Major Breakthroughs)

```
Tier 1: System - Autonomous Agent Self-Recognition Achieved
Coherence: 5/5 - All Axioms Aligned
Change: Integrated MODE A/B/C cycle with recursive pattern detection
Patterns: [Recursive_Self_Recognition, Autonomous_Agent, P120]
```

---

## Tier 3 (Issues/Experiments)

```
Tier 3: Experiment - Testing Hypothesis Branch for ECONNREFUSED
Coherence: Under Investigation
Change: Created fix/postgres-connection branch, testing connection string alternatives
```

---

## Rules

1. **Never use generic messages** like "Updated file" or "Fixed bug"
2. **Always reference the Axiom** being implemented (A1, A2, A4, A7, A9)
3. **Technical detail must be specific** - exact file names, function names, or config keys
4. **Coherence explains WHY** - how does this serve the system's evolution?
5. **Component matches the PRIMARY system** being modified (Postgres, n8n, Docs, Integration, Schema, System)
