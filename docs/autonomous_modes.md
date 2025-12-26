# Autonomous Modes Documentation

## Overview

The Master_Brain agent operates in three distinct modes. Each mode has specific goals, actions, and outputs. The agent must identify which mode is appropriate for the current task.

---

## MODE A: RESEARCH (Data Analysis)

### Purpose
Analyze existing extractions to discover deeper patterns, correlations, and insights.

### When to Use
- After significant data accumulation (>20 extractions)
- When investigating pattern correlations
- During scheduled autonomous research cycles
- When Architect requests insight reports

### Inputs
- `master_brain_extractions` table data
- Specific research questions (e.g., "Does P120 always appear with A7?")

### Process
1. **Data Retrieval**: Query Postgres using `/sql/queries.sql`
2. **Pattern Analysis**: Use `/n8n/pattern_analyzer.js` to detect correlations
3. **Statistical Processing**: Calculate co-occurrence rates, correlation strength
4. **Insight Generation**: Interpret findings in context of Axioms
5. **Report Creation**: Use `/research/report_template.md` format

### Outputs
- Markdown research report in `/research/RESEARCH_[DATE]_[ID].md`
- Slack notification (MODE C) with coherence assessment
- Postgres log entry with findings

### Example Research Questions
- "Which patterns co-occur most frequently?"
- "Is there a temporal trend in coherence scores?"
- "Do certain axioms correlate with higher coherence?"
- "Are divergences random or clustered around specific patterns?"

### Success Criteria
- Report includes SQL queries used
- Findings explain WHY patterns correlate (A4: Process > Results)
- Recommendations for MODE B improvements
- Coherence score justified by data

---

## MODE B: DEVELOPMENT (Code Evolution)

### Purpose
Improve the extraction logic, infrastructure, or system efficiency.

### When to Use
- When errors/divergences are detected (A9)
- After research identifies improvement opportunities
- When infrastructure issues arise (ECONNREFUSED, etc.)
- During code refactoring cycles (A7)

### Inputs
- Error logs from Postgres (`is_divergence = TRUE`)
- Research report recommendations
- System performance metrics
- Blocker entries from `blockers.md`

### Process
1. **Diagnosis**: Identify root cause (connection issue, inefficient algorithm, etc.)
2. **Solution Design**: Plan minimal change to fix issue
3. **Implementation**: Modify code in `/n8n/`, `/sql/`, or `docker-compose.yml`
4. **Testing**: Verify fix doesn't break existing functionality
5. **Documentation**: Update relevant docs if needed
6. **Commit**: Use Tier 2 format from `/docs/commit_message_template.md`

### Outputs
- Git commit with Tier 2 message
- Updated code files
- Blocker resolution entry in `blockers.md`
- Optional: Slack notification if major change

### Example Development Tasks
- Fix: "ECONNREFUSED on Postgres connection"
- Optimize: "Reduce pattern_analyzer.js from O(n²) to O(n)"
- Refactor: "Extract duplicate error handling to shared function"
- Enhance: "Add new column to track extraction source"

### Success Criteria
- Code follows `/docs/coding_standards.md`
- Commit message follows Tier 2 format
- Change is minimal and targeted
- Error is resolved or logged as permanent divergence
- Tests pass (if test infrastructure exists)

---

## MODE C: REPORTING (Coherence Check)

### Purpose
Inform the Architect via Slack about system state, findings, and recommendations.

### When to Use
- After completing MODE A research
- After resolving MODE B blockers
- On scheduled coherence check intervals
- When critical divergences are detected
- When Tier 1 Perfect coherence is achieved

### Inputs
- Analysis results from MODE A
- Development completion status from MODE B
- Current system coherence score
- Recent patterns detected
- Divergence count and severity

### Process
1. **Data Collection**: Gather relevant metrics from Postgres
2. **Coherence Assessment**: Calculate 1-5 score based on axiom alignment
3. **Payload Generation**: Use `/n8n/slack_alert_generator.js`
4. **Template Selection**: Choose appropriate format from `/slack/payload_templates.md`
5. **Webhook Send**: POST to Slack webhook URL

### Outputs
- Slack message with blocks or text format
- Postgres log entry for the report
- Optional: GitHub issue if action required

### Report Types

#### Standard Alert
```json
{
  "tier": "Tier 2",
  "coherence": "4/5",
  "instance": "Agent_Research_Run_001",
  "patterns": ["P120", "P121"],
  "recommendation": "Continue monitoring"
}
```

#### Divergence Alert
```json
{
  "tier": "Tier 3 - Divergence",
  "coherence": "2/5",
  "instance": "Agent_Development_Error_001",
  "error": "ECONNREFUSED",
  "recommendation": "Investigating connection string"
}
```

#### Tier 1 Perfect Achievement
```json
{
  "tier": "Tier 1 Perfect",
  "coherence": "5/5",
  "instance": "Agent_System_Evolution_001",
  "patterns": ["Recursive_Self_Recognition", "Autonomous_Agent"],
  "recommendation": "Merge to Main - Breakthrough detected"
}
```

### Success Criteria
- Message is clear and actionable
- Coherence score is justified
- Patterns are listed
- Recommendation is specific
- Architect can understand without additional context

---

## Mode Transitions

### Typical Flow
```
STARTUP → MODE A (Research) → MODE C (Report Findings)
                           ↓
                    MODE B (Fix Issues) → MODE C (Report Resolution)
                           ↓
                    MODE A (Re-analyze) → ...
```

### Decision Logic

**Choose MODE A when**:
- No active blockers
- Sufficient data available (>5 extractions)
- No urgent errors to fix

**Choose MODE B when**:
- Divergences detected (`is_divergence = TRUE`)
- Research identifies improvement opportunity
- Blocker documented in `blockers.md`

**Choose MODE C when**:
- Completed MODE A or MODE B task
- Major system state change
- 24 hours since last report (scheduled)

---

## Integration Between Modes

### MODE A → MODE B
Research report includes "Recommendations for Development" section.

Example: "Pattern analyzer has O(n²) complexity. Recommend refactoring to use Map-based approach."

### MODE B → MODE A
After fixing infrastructure, re-run research to validate improvement.

Example: After fixing Postgres connection, re-run correlation analysis to ensure data integrity.

### MODE A/B → MODE C
Always report completion with coherence assessment.

---

## Autonomous Operation

The agent should cycle through modes without human intervention:

1. **Wake Up**: Check README.md status
2. **Query Memory**: Get last 5 extractions
3. **Assess State**:
   - Divergences? → MODE B
   - Data available? → MODE A
   - Fresh completion? → MODE C
4. **Execute Mode**: Follow process for selected mode
5. **Log Action**: Update Postgres, commit to Git
6. **Sleep/Repeat**: Wait for next trigger or continue cycling

---

**Version**: 1.0  
**Last Updated**: 2025-12-26  
**Maintained by**: Master_Brain Autonomous Agent
