# The Watchtower - Navigation System Setup Guide

**System Status**: AUTONOMOUS  
**Phase**: 12.1 (The Sensorium)  
**Objective**: Navigation

## Overview

The Watchtower is a perpetual autonomous system that scans the world stream, processes information through the Master Brain API, and archives Gnosis Blocks while discarding noise.

## Architecture

The system operates as a Perpetual Loop with four core components:

1. **The Senses (n8n)**: Scans external feeds (RSS, News, Markets) every 30 minutes
2. **The Mind (API)**: Processes headlines for Contradiction, Fear, or Glitch
3. **The Memory (Postgres)**: Archives only the Gnosis Blocks. Noise is discarded
4. **The Compass (Divergence)**: Alerts when patterns are detected (e.g., P126 Kinetic Vein)

## Prerequisites

Before setting up The Watchtower, ensure you have:

- **n8n** instance running (self-hosted or cloud)
- **Master Brain API** accessible at `http://master_brain_agent_api:5000`
- **PostgreSQL database** with the `master_brain_extractions` table
- Database credentials configured in n8n

## Database Setup

Ensure your PostgreSQL database has the required table:

```sql
CREATE TABLE IF NOT EXISTS master_brain_extractions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    message_content TEXT NOT NULL,
    patterns_detected JSONB DEFAULT '[]',
    axioms_detected TEXT
);
```

## Installation Instructions

### Step 1: Import the n8n Workflow

1. Open your n8n instance
2. Go to **Workflows** → **Import from File** (or use the menu option)
3. Select the `watchtower_workflow.json` file from this repository
4. The workflow will be imported with all nodes configured

### Step 2: Configure PostgreSQL Credentials

1. In n8n, go to **Credentials**
2. Create a new **Postgres** credential with ID `master-brain-db`
3. Enter your database connection details:
   - Host: Your PostgreSQL host
   - Database: Your database name
   - User: Your database user
   - Password: Your database password
   - Port: 5432 (or your custom port)

### Step 3: Verify Master Brain API Endpoint

1. Open the workflow in n8n
2. Click on the **"Gnosis Scan (The Mind)"** node
3. Verify the URL points to your Master Brain API:
   - Default: `http://master_brain_agent_api:5000/scan`
   - Update if your API is hosted elsewhere

### Step 4: Activate the Workflow

1. In the workflow editor, click the **"Active"** toggle in the top-right
2. The workflow will now run every 30 minutes automatically
3. You can also click **"Execute Workflow"** to test it immediately

## Customizing the Data Source

The default configuration pulls from TheHackersNews RSS feed. You can customize this:

### Available RSS Feeds

Edit the **"World Stream (RSS)"** node and change the URL to:

- **Technology/Security**: `https://feeds.feedburner.com/TheHackersNews`
- **Hacker News**: `https://hnrss.org/frontpage`
- **Geopolitics**: Any geopolitical news RSS feed
- **Financial Markets**: Bloomberg, Reuters, or similar RSS feeds
- **Custom**: Any valid RSS feed URL

### Adjusting Scan Frequency

Edit the **"The Pulse (30m)"** node to change the interval:

- Every 15 minutes: Set `minutesInterval` to `15`
- Every hour: Set `minutesInterval` to `60`
- Every 6 hours: Set `minutesInterval` to `360`

## Monitoring the System

### Navigation Dashboard

Run the Navigation View query to see what the system has discovered:

```bash
psql -U your_user -d your_database -f navigation_view.sql
```

Or directly in your SQL client:

```sql
SELECT 
    id,
    timestamp,
    message_content as "The Territory (Raw Input)",
    patterns_detected as "The Map (Pattern)",
    axioms_detected as "The Compass (Status)"
FROM 
    master_brain_extractions
WHERE 
    jsonb_array_length(patterns_detected) > 0
ORDER BY 
    timestamp DESC
LIMIT 50;
```

### Understanding the Output

- **The Territory**: The raw headline/content that was scanned
- **The Map**: Detected patterns (e.g., `P126`, `P135`)
- **The Compass**: Status codes indicating what was found

### Pattern Interpretation

- **P126 (Kinetic Vein)**: Tech world hitting limits, kinetic energy building
- **P135 (Awareness Glitch)**: Narrative fracturing, awareness gaps detected
- Other patterns: See Master Brain API documentation

## n8n Workflow Details

### Node Flow

```
The Pulse (30m)
    ↓
World Stream (RSS)
    ↓
Gnosis Scan (The Mind)
    ↓
Filter: Is it Gnosis?
    ↓
Archive (The Memory)
```

### Node Descriptions

1. **The Pulse (30m)** - Schedule Trigger
   - Triggers the workflow every 30 minutes
   - Ensures continuous autonomous operation

2. **World Stream (RSS)** - RSS Feed Reader
   - Fetches latest entries from the configured feed
   - Extracts title and content snippet

3. **Gnosis Scan (The Mind)** - HTTP Request
   - POSTs to Master Brain API `/scan` endpoint
   - Sends combined title and content snippet
   - Returns analysis with detected patterns

4. **Filter: Is it Gnosis?** - Conditional (IF)
   - Checks if status contains `GNOSIS_BLOCK_DETECTED`
   - Only passes through meaningful signals

5. **Archive (The Memory)** - Postgres Insert
   - Stores detected Gnosis Blocks in database
   - Records message content, patterns, and axioms

## Evolution Mandate

### For the Operator

1. **Activate the Watchtower**: Import and activate the workflow
2. **Observe the Drift**: Check the logs after 24 hours
3. **Interpret Patterns**:
   - P126 (Kinetic Vein) = Tech limits being reached
   - P135 (Awareness Glitch) = Narrative fracturing
4. **Steer**: If the system archives surprising patterns, that's your heading

### System Behavior

The system is now:
- ✓ Looking at the Horizon
- ✓ Filtering noise autonomously  
- ✓ Extracting Gnosis without manual intervention
- ✓ Building a navigational memory

## Troubleshooting

### Workflow Not Triggering

- Check that the workflow is **Active** (toggle in top-right)
- Verify the Schedule Trigger settings
- Check n8n execution logs

### No Data in Database

- Verify PostgreSQL credentials are correct
- Check that the `master_brain_extractions` table exists
- Ensure the Master Brain API is returning `GNOSIS_BLOCK_DETECTED` status

### API Connection Errors

- Verify Master Brain API is running and accessible
- Check the URL in the "Gnosis Scan" node
- Ensure network connectivity between n8n and the API

### RSS Feed Errors

- Test the RSS feed URL in a browser
- Try alternative feed URLs
- Check n8n logs for specific error messages

## Advanced Configuration

### Multiple Feed Sources

You can duplicate the workflow and configure different RSS feeds:

1. Duplicate the workflow in n8n
2. Change the RSS feed URL
3. Rename the workflow (e.g., "Watchtower - Geopolitics")
4. Activate both workflows

### Custom Filtering Logic

Modify the **"Filter: Is it Gnosis?"** node to add additional conditions:

- Filter by specific pattern types
- Set minimum confidence thresholds
- Add pattern-specific routing

### Alert Integration

Add notification nodes after the filter:

- Email notifications
- Slack/Discord webhooks
- SMS alerts via Twilio
- Custom webhooks

## Files in This Repository

- `watchtower_workflow.json` - n8n workflow configuration
- `navigation_view.sql` - SQL query for viewing navigation log
- `WATCHTOWER_SETUP.md` - This setup guide

## Support

For issues or questions:
1. Check the n8n execution logs
2. Review Master Brain API logs
3. Verify database connectivity
4. Check PostgreSQL logs for insertion errors

---

**The System is now looking at the Horizon.**

*Ἐλπίδα.* (Hope)
