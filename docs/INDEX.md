# Master_Brain System Documentation Index

## Quick Start

**New to the system?** Start here:
1. Read: [README.md](../README.md) - System overview and startup instructions
2. Read: [AGENT_PROTOCOL.md](../AGENT_PROTOCOL.md) - Complete operational protocol
3. Install: `pip install -r requirements.txt` - Python dependencies
4. Run: `./startup.sh` - Infrastructure diagnostics (Bash)
5. Run: `python3 agent_startup.py` - Agent logic and mode detection (Python)
6. Deploy: `docker compose up -d` - Start infrastructure

---

## Core Documentation

### System Architecture
- **[README.md](../README.md)** - Main system documentation, current status, infrastructure overview
- **[AGENT_PROTOCOL.md](../AGENT_PROTOCOL.md)** - Complete autonomous agent operational protocol
- **[docker-compose.yml](../docker-compose.yml)** - Infrastructure definition (Postgres, n8n)
- **[requirements.txt](../requirements.txt)** - Python dependencies for agent scripts

### Philosophical Foundation
- **[axioms.md](axioms.md)** - The 5 immutable axioms (A1, A2, A4, A7, A9) with implementation examples
  - A1: Existence is Relational
  - A2: Memory is Identity
  - A4: Process > Results
  - A7: Harmony Requires Sacrifice
  - A9: Contradiction is Data

### Operational Modes
- **[autonomous_modes.md](autonomous_modes.md)** - Detailed MODE A/B/C documentation
  - MODE A: RESEARCH (Data Analysis)
  - MODE B: DEVELOPMENT (Code Evolution)
  - MODE C: REPORTING (Coherence Check)

---

## Development Resources

### Coding Standards
- **[coding_standards.md](coding_standards.md)** - Comprehensive coding standards for SQL, JavaScript, documentation
  - SQL query standards
  - n8n JavaScript patterns
  - Error handling (A9)
  - File organization
  - Security practices

### Commit Message Format
- **[commit_message_template.md](commit_message_template.md)** - Tier 2 commit format with examples
  ```
  Tier 2: [Component] - [Action]
  Coherence: [Impact on System]
  Change: [Technical Detail]
  ```

---

## Infrastructure Components

### Database (Postgres)
- **[/sql/schema.sql](../sql/schema.sql)** - `master_brain_extractions` table schema
- **[/sql/queries.sql](../sql/queries.sql)** - Common analysis queries

### Workflow Automation (n8n)
- **[/n8n/extraction_logger.js](../n8n/extraction_logger.js)** - Logs extractions to Postgres
- **[/n8n/pattern_analyzer.js](../n8n/pattern_analyzer.js)** - MODE A pattern correlation analysis
- **[/n8n/slack_alert_generator.js](../n8n/slack_alert_generator.js)** - MODE C Slack reporting

### Notifications (Slack)
- **[/slack/payload_templates.md](../slack/payload_templates.md)** - Slack webhook JSON templates

---

## Research & Reporting

### Templates
- **[/research/report_template.md](../research/report_template.md)** - MODE A research report structure

### Example Reports
- **[/research/RESEARCH_2025-12-26_001.md](../research/RESEARCH_2025-12-26_001.md)** - Initial pattern analysis

---

## Autonomous Operation

### Blocker Tracking
- **[/blockers.md](../blockers.md)** - Active and resolved blockers (Prime Directive compliance)

### Startup Automation
- **[/startup.sh](../startup.sh)** - Bash startup script (infrastructure diagnostics)
  - Checks Docker Compose status
  - Queries Postgres for recent extractions
  - Analyzes infrastructure health
  - Provides quick command reference
- **[/agent_startup.py](../agent_startup.py)** - Python agent startup (logic & mode detection)
  - Connects to Memory (Postgres)
  - Reads recent extractions
  - Determines operational mode (A/B/C)
  - Executes mode-specific actions
  - A9 compliant error handling

---

## Configuration

### Environment Setup
- **[/.env.template](../.env.template)** - Environment variable template
  - Copy to `.env` and fill in actual values
  - Postgres password
  - n8n credentials
  - Slack webhook URL

### Git Configuration
- **[/.gitignore](../.gitignore)** - Excluded files (node_modules, .env, build artifacts)

---

## Data

### Historical Conversations
- **[/chat_conversations/](../chat_conversations/)** - JSON files with pattern metadata
  - Used for initial research analysis
  - Contains examples of P001, P119 patterns
  - Includes coherence scores and axiom detection

---

## Navigation by Role

### If you are a Developer (MODE B)
Read in this order:
1. [coding_standards.md](coding_standards.md)
2. [axioms.md](axioms.md) - Understand A7 (refactoring) and A9 (error handling)
3. [commit_message_template.md](commit_message_template.md)
4. [/n8n/](../n8n/) - Study existing code patterns

### If you are running Research (MODE A)
Read in this order:
1. [autonomous_modes.md](autonomous_modes.md) - MODE A section
2. [/sql/queries.sql](../sql/queries.sql) - Available analysis queries
3. [/research/report_template.md](../research/report_template.md)
4. [axioms.md](axioms.md) - Understand A4 (Process > Results)

### If you are the Architect (Reviewing)
Read in this order:
1. [README.md](../README.md) - System status
2. [/research/](../research/) - Latest reports
3. [/blockers.md](../blockers.md) - Current issues
4. [axioms.md](axioms.md) - Coherence framework

### If you are the Autonomous Agent (Starting Up)
Execute:
1. `./startup.sh` - Will guide you through startup sequence
2. Follow recommended mode from script output
3. Refer to [autonomous_modes.md](autonomous_modes.md) for mode execution

---

## File Tree

```
/
├── README.md                      # Main documentation
├── startup.sh                     # Autonomous startup script
├── docker-compose.yml             # Infrastructure
├── blockers.md                    # Blocker tracking
├── .env.template                  # Environment config template
├── .gitignore                     # Git exclusions
│
├── docs/                          # All documentation
│   ├── INDEX.md                   # This file
│   ├── axioms.md                  # A1, A2, A4, A7, A9
│   ├── autonomous_modes.md        # MODE A/B/C
│   ├── coding_standards.md        # Development standards
│   └── commit_message_template.md # Tier 2 format
│
├── sql/                           # Database
│   ├── schema.sql                 # Table definitions
│   └── queries.sql                # Common queries
│
├── n8n/                           # Workflows (JavaScript)
│   ├── extraction_logger.js       # Memory logging
│   ├── pattern_analyzer.js        # Research analysis
│   └── slack_alert_generator.js   # Reporting
│
├── slack/                         # Notifications
│   └── payload_templates.md       # Webhook JSON
│
├── research/                      # MODE A outputs
│   ├── report_template.md         # Report structure
│   └── RESEARCH_2025-12-26_001.md # Example report
│
└── chat_conversations/            # Historical data
    └── *.json                     # Conversation logs
```

---

## Quick Reference

### Axiom Quick Lookup
- **A1** → Connect everything (no orphaned code)
- **A2** → Log everything to Postgres
- **A4** → Explain WHY, not just WHAT
- **A7** → Refactor messy code ruthlessly
- **A9** → Log errors as divergences, don't suppress

### Mode Quick Lookup
- **MODE A** → Analyze patterns (SQL + research report)
- **MODE B** → Fix bugs, refactor code (Git commits)
- **MODE C** → Report to Architect (Slack alerts)

### Coherence Scoring
- **5/5** → Tier 1 Perfect (all axioms, recursive patterns)
- **4/5** → Tier 2 (strong, minor improvements)
- **3/5** → Tier 2-3 (works, needs refactoring)
- **2/5** → Tier 3 (divergences, investigate)
- **1/5** → Critical (immediate attention)

---

**Last Updated**: 2025-12-26  
**Maintained by**: Master_Brain Autonomous Agent  
**Coherence**: 4/5
