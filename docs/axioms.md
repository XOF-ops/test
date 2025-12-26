# The Immutable Axioms - Master_Brain System

## Overview

These axioms form the philosophical and operational foundation of the Master_Brain system. Every decision, code line, and analysis must align with these principles.

---

## A1: Existence is Relational

### Meaning
Nothing exists in isolation. All components must be interconnected and aware of each other.

### Implementation Rules
- **No orphaned scripts**: Every file must be referenced by another component
- **Integration priority**: Slack, n8n, and Postgres connections are mandatory
- **Dependency mapping**: Document how modules relate to each other

### Code Examples

**Good** ✅:
```javascript
// extraction_logger.js connects to Postgres AND triggers Slack alert
const logExtraction = async (data) => {
  await postgres.insert(data);  // A2: Memory
  await slack.notify(data);      // A1: Relational
};
```

**Bad** ❌:
```javascript
// Standalone script with no connections
const processData = (data) => {
  console.log(data);  // Orphaned output
};
```

### In Practice
- n8n workflows chain together (output of one node → input of next)
- Research reports reference Postgres data sources
- Every Slack alert includes context from database
- Docker services depend on each other (`depends_on`)

---

## A2: Memory is Identity

### Meaning
The system's memory (Postgres) defines what it knows. If it's not logged, it didn't happen.

### Implementation Rules
- **Everything to Postgres**: All extractions, errors, analyses must be persisted
- **Timestamps required**: Every entry must have `created_at`
- **No volatile state**: Don't rely on in-memory variables across runs
- **Git commits are secondary memory**: Commit messages must be descriptive

### Code Examples

**Good** ✅:
```sql
INSERT INTO master_brain_extractions (
  created_at, 
  coherence_score, 
  patterns_detected,
  mode
) VALUES (
  NOW(), 
  5, 
  '["P120"]'::jsonb,
  'RESEARCH'
);
```

**Bad** ❌:
```javascript
// Storing results only in memory
let analysisResults = { patterns: ["P120"] };
// No persistence - lost when process restarts
```

### In Practice
- Every n8n workflow ends with a Postgres insert
- Research findings are logged before creating the report
- Divergences (errors) are stored with `is_divergence = TRUE`
- Historical patterns can be queried for trend analysis

---

## A4: Process > Results

### Meaning
HOW you arrived at a conclusion is more valuable than the conclusion itself. Document the journey, not just the destination.

### Implementation Rules
- **Explain reasoning**: Code comments should explain "why", not "what"
- **Research reports include methodology**: Show SQL queries, algorithms used
- **Commit messages include "Coherence"**: Why this change matters
- **Log intermediate steps**: Not just final results

### Code Examples

**Good** ✅:
```javascript
// A4: Process > Results - We use Map for O(n) instead of nested loops
// because pattern correlation analysis on 1000+ records was taking >5s
const correlations = new Map();
patterns.forEach(p => {
  correlations.set(p, (correlations.get(p) || 0) + 1);
});
```

**Bad** ❌:
```javascript
// Optimized code
const correlations = new Map();
patterns.forEach(p => correlations.set(p, (correlations.get(p) || 0) + 1));
```

### In Practice
- Research reports explain WHY patterns correlate, not just THAT they do
- Commit messages: "Coherence: Improved query performance by 80%"
- n8n nodes include comments about data transformations
- Documentation focuses on understanding, not just instructions

---

## A7: Harmony Requires Sacrifice

### Meaning
If code is messy but works, it is FALSE. Clean code is true code. Refactor ruthlessly.

### Implementation Rules
- **Refactor working code**: If it's ugly, clean it up
- **No technical debt**: Don't postpone cleanup for later
- **Delete redundant code**: Sacrifice old implementations
- **Consistency over convenience**: Follow patterns even if verbose

### Code Examples

**Good** ✅:
```javascript
// Refactored: Clear, single responsibility
const calculateCoherence = (axioms, patterns) => {
  const axiomScore = axioms.length >= 3 ? 2 : 1;
  const patternScore = patterns.length >= 2 ? 2 : 1;
  return axiomScore + patternScore;
};
```

**Bad** ❌:
```javascript
// Works but messy
const calc = (a, p) => {
  let s = 0;
  if (a.length >= 3) s += 2; else s += 1;
  if (p.length >= 2) s += 2; else s += 1;
  return s;
};
```

### In Practice
- Regular code reviews (even by the agent itself)
- Refactoring is a valid MODE B task
- Commit messages starting with "Tier 2: ... - Refactor ..."
- Delete old commented-out code instead of accumulating it

---

## A9: Contradiction is Data

### Meaning
Errors, failures, and contradictions are not problems to hide. They are valuable signals to analyze.

### Implementation Rules
- **Never suppress errors**: Always log them
- **Divergence tracking**: Set `is_divergence = TRUE` in Postgres
- **Slack alerts for errors**: MODE C reporting includes failures
- **No silent failures**: Try-catch must log the error

### Code Examples

**Good** ✅:
```javascript
try {
  await processExtraction(data);
} catch (error) {
  // A9: Contradiction is Data - Log as divergence
  await postgres.insert({
    error_message: error.message,
    is_divergence: true,
    stack: error.stack,
    mode: 'ERROR_CAPTURE'
  });
  
  await slack.alert({
    tier: 'Tier 3 - Divergence',
    error: error.message
  });
}
```

**Bad** ❌:
```javascript
try {
  await processExtraction(data);
} catch (error) {
  // Silent failure - error is lost
  return null;
}
```

### In Practice
- All n8n nodes have try-catch blocks
- `master_brain_extractions` table has `is_divergence` column
- Research reports analyze divergences for patterns
- ECONNREFUSED errors are logged, not just retried blindly
- Blockers.md documents unresolved contradictions

---

## Axiom Compliance Checklist

Before committing code or creating reports, verify:

- [ ] **A1**: Is this component connected to others? (n8n → Postgres → Slack)
- [ ] **A2**: Is this action logged to Postgres with timestamp?
- [ ] **A4**: Did I document WHY, not just WHAT?
- [ ] **A7**: Is this code clean, or does it need refactoring?
- [ ] **A9**: Are errors handled and logged as divergences?

---

## Coherence Scoring Based on Axioms

### 5/5 (Tier 1 Perfect)
- All 5 axioms applied
- Code is clean, connected, logged, explained, and error-aware
- Recursive patterns detected (self-improvement)

### 4/5 (Tier 2)
- 3-4 axioms applied
- Minor improvements possible
- Functional and documented

### 3/5 (Tier 2-3)
- 2-3 axioms applied
- Works but needs refactoring (violates A7)
- Missing some logging or documentation

### 2/5 (Tier 3)
- 1-2 axioms applied
- Divergences present
- Requires investigation

### 1/5 (Critical)
- No axioms applied
- Silent failures, messy code, no logging
- Immediate attention needed

---

## Axiom Conflicts (Rare)

### When A7 (Refactor) Conflicts with A2 (Memory)
**Example**: Changing database schema would lose historical data.

**Resolution**: Migrate, don't delete. Add new columns, deprecate old ones.

### When A9 (Log Errors) Creates Too Much Data
**Example**: Thousands of duplicate errors flooding Postgres.

**Resolution**: Implement error aggregation - log first occurrence with count, not every instance.

---

## Evolution of Axioms

These axioms are **immutable** in principle but may be **extended** with new axioms (A10, A11, etc.) if the system discovers new fundamental truths.

Current axioms in use: **A1, A2, A4, A7, A9**

Potential future axioms:
- **A3**: (Reserved for future discovery)
- **A5**: (Reserved for future discovery)
- **A6**: (Reserved for future discovery)
- **A8**: (Reserved for future discovery)
- **A10+**: (Open for evolution)

---

**Version**: 1.0  
**Last Updated**: 2025-12-26  
**Maintained by**: Master_Brain Autonomous Agent  
**Coherence**: 5/5
