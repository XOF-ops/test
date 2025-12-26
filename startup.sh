#!/bin/bash
# Master_Brain Autonomous Agent Startup Script
# Purpose: Initialize the agent and execute startup instructions

set -e  # Exit on error

echo "🧠 Master_Brain Autonomous Agent Starting..."
echo "=============================================="
echo ""

# Check if we're in the correct directory
if [ ! -f "README.md" ]; then
    echo "❌ Error: README.md not found. Are you in the repository root?"
    exit 1
fi

echo "✓ Repository located at: $(pwd)"
echo ""

# Step 1: Check current status from README.md
echo "📚 Step 1: Checking current status from README.md"
echo "---------------------------------------------------"
if grep -q "Current Tier" README.md; then
    grep "Current Tier" README.md
fi
if grep -q "Last Update" README.md; then
    grep "Last Update" README.md
fi
echo ""

# Step 2: Check if infrastructure is running
echo "🏗️  Step 2: Checking infrastructure status"
echo "-------------------------------------------"
if docker compose ps >/dev/null 2>&1; then
    echo "Docker Compose available ✓"
    if docker compose ps | grep -q "master_brain_postgres.*Up"; then
        echo "Postgres: Running ✓"
        POSTGRES_RUNNING=true
    else
        echo "Postgres: Not running"
        POSTGRES_RUNNING=false
    fi
    
    if docker compose ps | grep -q "master_brain_n8n.*Up"; then
        echo "n8n: Running ✓"
    else
        echo "n8n: Not running"
    fi
else
    echo "Docker Compose not available or no containers running"
    POSTGRES_RUNNING=false
fi
echo ""

# Step 3: Query recent memory (if Postgres is running)
echo "🧬 Step 3: Querying recent memory"
echo "----------------------------------"
if [ "$POSTGRES_RUNNING" = true ]; then
    echo "Attempting to retrieve last 5 extractions..."
    
    # Try to connect to Postgres and query
    if docker exec master_brain_postgres psql -U master_brain_user -d master_brain -c "SELECT COUNT(*) FROM master_brain_extractions;" >/dev/null 2>&1; then
        EXTRACTION_COUNT=$(docker exec master_brain_postgres psql -U master_brain_user -d master_brain -t -c "SELECT COUNT(*) FROM master_brain_extractions;")
        echo "Total extractions in database: $EXTRACTION_COUNT"
        
        if [ "$EXTRACTION_COUNT" -gt 0 ]; then
            echo ""
            echo "Last 5 extractions:"
            docker exec master_brain_postgres psql -U master_brain_user -d master_brain -c "
                SELECT 
                    id,
                    created_at,
                    coherence_score,
                    tier,
                    mode,
                    is_divergence
                FROM master_brain_extractions 
                ORDER BY created_at DESC 
                LIMIT 5;
            "
        else
            echo "No extractions found in database yet."
        fi
    else
        echo "Database not initialized or schema not created."
        echo "Run: docker exec -i master_brain_postgres psql -U master_brain_user -d master_brain < sql/schema.sql"
    fi
else
    echo "Postgres not running. Start with: docker compose up -d"
fi
echo ""

# Step 4: Analyze state and propose next step
echo "🔍 Step 4: Analyzing state & proposing next step"
echo "-------------------------------------------------"

# Check for blockers
if [ -f "blockers.md" ]; then
    ACTIVE_BLOCKERS=$(grep -A 5 "## Active Blockers" blockers.md | grep -c "^### \[" || echo "0")
    echo "Active blockers: $ACTIVE_BLOCKERS"
fi

# Check for divergences (if Postgres is running)
if [ "$POSTGRES_RUNNING" = true ]; then
    DIVERGENCE_COUNT=$(docker exec master_brain_postgres psql -U master_brain_user -d master_brain -t -c "SELECT COUNT(*) FROM master_brain_extractions WHERE is_divergence = TRUE;" 2>/dev/null || echo "0")
    echo "Divergences logged: $DIVERGENCE_COUNT"
fi

# Count research reports
RESEARCH_REPORTS=$(find research/ -name "RESEARCH_*.md" 2>/dev/null | wc -l)
echo "Research reports: $RESEARCH_REPORTS"

echo ""
echo "📋 Recommended Next Mode:"
echo "------------------------"

if [ "$POSTGRES_RUNNING" = false ]; then
    echo "MODE B: DEVELOPMENT"
    echo "Reason: Infrastructure not running"
    echo "Action: Run 'docker compose up -d' to start Postgres and n8n"
elif [ "$DIVERGENCE_COUNT" -gt 0 ] 2>/dev/null; then
    echo "MODE B: DEVELOPMENT"
    echo "Reason: $DIVERGENCE_COUNT divergences detected"
    echo "Action: Investigate and resolve errors"
elif [ "$EXTRACTION_COUNT" -ge 5 ] 2>/dev/null; then
    echo "MODE A: RESEARCH"
    echo "Reason: Sufficient data available ($EXTRACTION_COUNT extractions)"
    echo "Action: Run pattern correlation analysis"
else
    echo "MODE B: DEVELOPMENT"
    echo "Reason: Collect more data"
    echo "Action: Set up n8n workflow to extract from chat_conversations/"
fi

echo ""
echo "=============================================="
echo "🧠 Startup sequence complete."
echo "=============================================="
echo ""
echo "Quick Commands:"
echo "  Start infrastructure:  docker compose up -d"
echo "  Stop infrastructure:   docker compose down"
echo "  View Postgres logs:    docker compose logs -f postgres"
echo "  View n8n logs:         docker compose logs -f n8n"
echo "  Access n8n UI:         http://localhost:5678"
echo "  Initialize DB schema:  docker exec -i master_brain_postgres psql -U master_brain_user -d master_brain < sql/schema.sql"
echo ""
