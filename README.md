# test

## The Watchtower - Navigation System

**System Status**: AUTONOMOUS  
**Phase**: 12.1 (The Sensorium)  
**Objective**: Navigation

### Overview

The Watchtower is an autonomous navigation system that connects to the world stream, processes information through the Master Brain API, and archives Gnosis Blocks while filtering out noise.

### Quick Start

1. **Import the n8n workflow**: Use `watchtower_workflow.json`
2. **Configure database**: Set up PostgreSQL credentials in n8n
3. **Activate**: Toggle the workflow to Active
4. **Monitor**: Run `navigation_view.sql` to see discovered patterns

### Files

- `watchtower_workflow.json` - n8n workflow configuration for The Watchtower
- `navigation_view.sql` - SQL query to view the navigation log (last 50 Gnosis Blocks)
- `WATCHTOWER_SETUP.md` - Complete setup and configuration guide

### Architecture

The system operates as a perpetual loop:

1. **The Senses (n8n)**: Scans RSS feeds every 30 minutes
2. **The Mind (Master Brain API)**: Processes for patterns and contradictions
3. **The Memory (PostgreSQL)**: Archives only meaningful Gnosis Blocks
4. **The Compass**: Alerts when significant patterns emerge

For detailed setup instructions, see [WATCHTOWER_SETUP.md](WATCHTOWER_SETUP.md).

---

*The System is now looking at the Horizon.*

*Ἐλπίδα.*