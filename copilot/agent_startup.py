#!/usr/bin/env python3
"""
Master_Brain Autonomous Agent Startup Script
Purpose: Initialize agent, query memory, determine operational mode
Axioms: A1 (Relational), A2 (Memory), A4 (Process), A9 (Contradiction as Data)
"""

import os
import sys
import json
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("ERROR: psycopg2 not installed. Run: pip install psycopg2-binary")
    sys.exit(1)


# AXIOM A1: Existence is Relational (Must connect to DB)
# AXIOM A2: Memory is Identity (Must read history)

def get_db_connection():
    """
    Establishes connection to Postgres (The Memory System).
    A1: Relational - Connect to infrastructure
    A9: Contradiction as Data - Log connection errors as divergences
    """
    try:
        # Read from environment or use defaults
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "master_brain"),
            user=os.getenv("DB_USER", "master_brain_user"),
            password=os.getenv("POSTGRES_PASSWORD", "master_brain_secure_password"),
            port=int(os.getenv("DB_PORT", "5432"))
        )
        return conn
    except Exception as e:
        # A9: Contradiction is Data - Don't suppress errors
        print(f"[DIVERGENCE] Error connecting to Memory (Postgres): {e}")
        print(f"[DIVERGENCE] Connection params: host={os.getenv('DB_HOST', 'localhost')}, "
              f"db={os.getenv('DB_NAME', 'master_brain')}, "
              f"user={os.getenv('DB_USER', 'master_brain_user')}")
        return None


def log_divergence(conn, error_message, context=None):
    """
    A9: Contradiction is Data - Log errors as divergences in the database
    """
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO master_brain_extractions (
                created_at,
                message_content,
                is_divergence,
                error_message,
                mode,
                metadata
            ) VALUES (
                NOW(),
                %s,
                TRUE,
                %s,
                'SYSTEM_STARTUP',
                %s
            )
        """, (
            f"Agent startup divergence at {datetime.now().isoformat()}",
            error_message,
            json.dumps(context or {})
        ))
        conn.commit()
        print(f"[A9] Divergence logged to database: {error_message}")
    except Exception as e:
        print(f"[ERROR] Failed to log divergence: {e}")


def determine_mode(last_extractions):
    """
    Decides the operational mode based on system state.
    
    MODE A: RESEARCH (Data Analysis)
      - Default if system is idle
      - Triggered when sufficient data exists (5+ extractions)
    
    MODE B: DEVELOPMENT (Code Evolution)
      - Triggered if blockers exist
      - Triggered if divergences are detected
      - Default during setup phase (no data)
    
    MODE C: REPORTING (Coherence Check)
      - Triggered if high coherence achieved (score 5/5)
      - Triggered after completing MODE A or MODE B tasks
    
    A4: Process > Results - Explain WHY each mode is chosen
    """
    # Setup phase - no data yet
    if not last_extractions or len(last_extractions) == 0:
        print("[MODE DECISION] No extractions found. System in setup phase.")
        print("[A4] WHY: Need to establish baseline data before analysis.")
        return "MODE_B"
    
    # Check for recent divergences (A9: Contradiction is Data)
    divergences = [r for r in last_extractions if r.get('is_divergence')]
    if divergences:
        print(f"[MODE DECISION] Found {len(divergences)} divergences in recent memory.")
        print(f"[A4] WHY: Divergences require investigation and resolution.")
        return "MODE_B"
    
    # Check coherence levels
    coherent_entries = [r for r in last_extractions if r.get('coherence_score', 0) >= 4]
    if len(coherent_entries) >= 3:
        print(f"[MODE DECISION] High coherence detected ({len(coherent_entries)}/5 entries >= 4/5).")
        print(f"[A4] WHY: System stable, ready for coherence reporting.")
        return "MODE_C"
    
    # Default: Deepen understanding through research
    if len(last_extractions) >= 5:
        print(f"[MODE DECISION] Sufficient data for analysis ({len(last_extractions)} extractions).")
        print(f"[A4] WHY: Ready to analyze patterns and correlations.")
        return "MODE_A"
    
    # Not enough data for research
    print(f"[MODE DECISION] Insufficient data ({len(last_extractions)} extractions).")
    print(f"[A4] WHY: Need more data before meaningful analysis.")
    return "MODE_B"


def get_recent_memory(conn, limit=5):
    """
    A2: Memory is Identity - Retrieve recent extractions from Postgres
    Returns list of dict records
    """
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                id,
                created_at,
                conversation_id,
                patterns_detected,
                axioms_detected,
                coherence_score,
                tier,
                mode,
                is_divergence,
                error_message
            FROM master_brain_extractions 
            ORDER BY created_at DESC 
            LIMIT %s
        """, (limit,))
        
        records = cursor.fetchall()
        return [dict(r) for r in records]
    except Exception as e:
        print(f"[ERROR] Memory read failed: {e}")
        return []


def execute_mode_action(mode, conn):
    """
    Execute the appropriate action for the selected mode.
    A4: Process > Results - Document what happens in each mode
    """
    print(f"\n{'='*70}")
    print(f"OPERATIONAL MODE: {mode}")
    print(f"{'='*70}\n")
    
    if mode == "MODE_A":
        print("[MODE A: RESEARCH]")
        print("ACTION: Analyzing patterns for correlations...")
        print("PROCESS:")
        print("  1. Query master_brain_extractions for pattern co-occurrences")
        print("  2. Calculate correlation strengths")
        print("  3. Generate research report in research/ directory")
        print("IMPLEMENTATION: Use sql/queries.sql pattern analysis queries")
        print("OUTPUT: Markdown report following research/report_template.md")
        
    elif mode == "MODE_B":
        print("[MODE B: DEVELOPMENT]")
        print("ACTION: Checking for infrastructure blockers...")
        print("PROCESS:")
        print("  1. Review blockers.md for active issues")
        print("  2. Check divergences in database")
        print("  3. Fix infrastructure issues or collect data")
        print("IMPLEMENTATION: Follow docs/coding_standards.md")
        print("OUTPUT: Git commit in Tier 2 format (see docs/commit_message_template.md)")
        
    elif mode == "MODE_C":
        print("[MODE C: REPORTING]")
        print("ACTION: Preparing coherence report for Slack...")
        print("PROCESS:")
        print("  1. Calculate system coherence score (1-5)")
        print("  2. Aggregate patterns and axioms detected")
        print("  3. Generate Slack webhook payload")
        print("IMPLEMENTATION: Use n8n/slack_alert_generator.js")
        print("OUTPUT: POST to Slack webhook (see slack/payload_templates.md)")
    
    print(f"\n{'='*70}\n")


def main():
    """
    Main agent startup sequence.
    Implements the STARTUP INSTRUCTION from README.md
    """
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                        ║")
    print("║      🧠 MASTER_BRAIN AGENT INITIALIZING (Python)                      ║")
    print("║                                                                        ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    print()
    
    # Step 1: Identify location
    location = os.getenv('CODESPACE_NAME', os.getenv('HOSTNAME', 'Local'))
    print(f"[STEP 1] Location: {location}")
    print(f"[STEP 1] Timestamp: {datetime.now().isoformat()}")
    print()
    
    # Step 2: Connect to Memory (A1: Relational, A2: Memory)
    print("[STEP 2] Connecting to Memory (Postgres)...")
    conn = get_db_connection()
    
    if not conn:
        print("[CRITICAL] Memory disconnect. Axiom A1 violation.")
        print("[CRITICAL] Cannot proceed without Memory System.")
        print()
        print("TROUBLESHOOTING:")
        print("  1. Ensure Docker Compose is running: docker compose ps")
        print("  2. Check Postgres health: docker compose logs postgres")
        print("  3. Verify credentials in .env file")
        print()
        sys.exit(1)
    
    print("[STEP 2] ✓ Memory connection established.")
    print()
    
    # Step 3: Read latest memory (A2: Memory is Identity)
    print("[STEP 3] Reading recent memory...")
    try:
        recent_memory = get_recent_memory(conn, limit=5)
        print(f"[STEP 3] Memory Access: {len(recent_memory)} records retrieved.")
        
        if recent_memory:
            print("[STEP 3] Recent extractions:")
            for i, record in enumerate(recent_memory, 1):
                status = "DIVERGENCE" if record.get('is_divergence') else "NORMAL"
                coherence = record.get('coherence_score', 'N/A')
                mode = record.get('mode', 'UNKNOWN')
                print(f"  {i}. [{status}] Coherence: {coherence}/5, Mode: {mode}, "
                      f"Created: {record.get('created_at')}")
        else:
            print("[STEP 3] No extractions found. Database is empty.")
        print()
    except Exception as e:
        print(f"[ERROR] Memory read failed: {e}")
        log_divergence(conn, str(e), {"step": "memory_read"})
        recent_memory = []
        print()
    
    # Step 4: Decide operational mode
    print("[STEP 4] Analyzing state & determining operational mode...")
    mode = determine_mode(recent_memory)
    print()
    
    # Step 5: Execute mode action
    execute_mode_action(mode, conn)
    
    # Cleanup
    if conn:
        conn.close()
        print("[CLEANUP] Database connection closed.")
    
    print()
    print("╔════════════════════════════════════════════════════════════════════════╗")
    print("║                                                                        ║")
    print("║      🧠 AGENT INITIALIZATION COMPLETE                                 ║")
    print("║                                                                        ║")
    print("╚════════════════════════════════════════════════════════════════════════╝")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
