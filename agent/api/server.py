"""
Master_Brain Agent API Server
Flask-based REST API for autonomous research & development protocol

Axiom A1 (Existence is Relational): Provides HTTP interface to connect
n8n workflows, external services, and the Python agent logic.

Endpoints:
- GET /health: Health check
- POST /scan: Analyze input for patterns and divergences
- GET /status: System status and mode
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from datetime import datetime
import psycopg2

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

app = Flask(__name__)
CORS(app)

# Database connection configuration from environment
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'postgres'),
    'database': os.getenv('DB_NAME', 'master_brain'),
    'user': os.getenv('DB_USER', 'master_brain_user'),
    'password': os.getenv('DB_PASSWORD', 'master_brain_secure_password')
}


def get_db_connection():
    """Get database connection following A1 (Relational)"""
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        app.logger.error(f"DB Connection Error (A9: Contradiction as Data): {e}")
        return None


def determine_mode_from_db():
    """
    Determine operational mode based on database state
    MODE A: Research (5+ extractions, no divergences)
    MODE B: Development (divergences detected or setup phase)
    MODE C: Reporting (high coherence achieved)
    """
    conn = get_db_connection()
    if not conn:
        return "MODE_B", "No database connection"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(*) FILTER (WHERE is_divergence = true) as divergences,
                   AVG(coherence_score) as avg_coherence
            FROM master_brain_extractions
        """)
        result = cursor.fetchone()
        total, divergences, avg_coherence = result if result else (0, 0, 0)
        
        cursor.close()
        conn.close()
        
        # Decision matrix
        if total == 0:
            return "MODE_B", "Setup phase - no data"
        elif divergences > 0:
            return "MODE_B", f"Divergences detected: {divergences}"
        elif avg_coherence and avg_coherence >= 4 and total >= 3:
            return "MODE_C", f"High coherence: {avg_coherence:.2f}"
        elif total >= 5:
            return "MODE_A", "Sufficient data for research"
        else:
            return "MODE_B", "Collecting more data"
            
    except Exception as e:
        app.logger.error(f"Mode detection error: {e}")
        return "MODE_B", f"Error: {str(e)}"


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    conn = get_db_connection()
    db_healthy = conn is not None
    if conn:
        conn.close()
    
    return jsonify({
        'status': 'healthy' if db_healthy else 'degraded',
        'service': 'master_brain_agent_api',
        'timestamp': datetime.now().isoformat(),
        'database': 'connected' if db_healthy else 'disconnected'
    }), 200 if db_healthy else 503


@app.route('/status', methods=['GET'])
def status():
    """Get system status and current operational mode"""
    mode, reason = determine_mode_from_db()
    
    conn = get_db_connection()
    extraction_count = 0
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM master_brain_extractions")
            extraction_count = cursor.fetchone()[0]
            cursor.close()
            conn.close()
        except:
            pass
    
    return jsonify({
        'timestamp': datetime.now().isoformat(),
        'mode': mode,
        'reason': reason,
        'extractions': extraction_count,
        'axioms': ['A1: Relational', 'A2: Memory', 'A4: Process', 'A7: Harmony', 'A9: Contradiction']
    })


@app.route('/scan', methods=['POST'])
def scan():
    """
    Analyze input for patterns and divergences (A9: Contradiction as Data)
    
    Input:
        {
            "text": "input text to analyze",
            "metadata": {...}  # optional
        }
    
    Returns:
        {
            "patterns": [...],
            "divergences": [...],
            "recommendation": "..."
        }
    """
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing required field: text'}), 400
    
    input_text = data['text'].lower()
    metadata = data.get('metadata', {})
    
    # Simple pattern detection (can be expanded)
    tension_markers = [
        'but', 'however', 'impossible', 'versus', 'cost', 'sacrifice',
        'conflict', 'fear', 'struggle', 'limit', 'error', 'blocked'
    ]
    
    detected_markers = [marker for marker in tension_markers if marker in input_text]
    
    analysis = {
        'timestamp': datetime.now().isoformat(),
        'input_length': len(data['text']),
        'tension_markers': detected_markers,
        'has_divergence': len(detected_markers) > 0,
        'recommendation': 'Log as divergence' if detected_markers else 'Standard processing',
        'axiom_applied': 'A9: Contradiction is Data' if detected_markers else 'A2: Memory is Identity'
    }
    
    # Log to database if connection available
    conn = get_db_connection()
    if conn and detected_markers:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO master_brain_extractions 
                (source_text, patterns_detected, axioms_applied, is_divergence, coherence_score)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                data['text'][:500],  # Truncate to first 500 chars
                detected_markers,
                ['A9'],
                True,
                2  # Low coherence for divergences
            ))
            conn.commit()
            cursor.close()
            conn.close()
            analysis['logged'] = True
        except Exception as e:
            app.logger.error(f"Failed to log scan result: {e}")
            analysis['logged'] = False
    
    return jsonify(analysis)


@app.route('/ingest', methods=['POST'])
def ingest():
    """
    Ingest system snapshot data
    Strict validation for complete system snapshots
    """
    data = request.get_json()
    
    required_fields = ['instance_id', 'timestamp', 'patterns']
    missing = [f for f in required_fields if f not in data]
    
    if missing:
        return jsonify({
            'isValid': False,
            'errors': [f'Missing required field: {f}' for f in missing]
        }), 400
    
    # Log to database
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO master_brain_extractions 
                (source_text, patterns_detected, coherence_score, metadata)
                VALUES (%s, %s, %s, %s)
            """, (
                f"Snapshot: {data['instance_id']}",
                data['patterns'],
                data.get('coherence_score', 3),
                {'snapshot_timestamp': data['timestamp']}
            ))
            conn.commit()
            cursor.close()
            conn.close()
            
            return jsonify({
                'isValid': True,
                'status': 'ingested',
                'instance_id': data['instance_id']
            })
        except Exception as e:
            app.logger.error(f"Ingestion error: {e}")
            return jsonify({
                'isValid': False,
                'errors': [str(e)]
            }), 500
    else:
        return jsonify({
            'isValid': False,
            'errors': ['Database unavailable']
        }), 503


@app.route('/propose', methods=['POST'])
def propose():
    """
    Propose evolutionary candidate (relaxed validation)
    Seeds/partials allowed
    """
    data = request.get_json()
    
    # Minimal validation - just need some identifier
    if 'candidate' not in data and 'id' not in data:
        return jsonify({
            'isValid': False,
            'errors': ['No candidate identity found']
        }), 400
    
    candidate_id = data.get('id', data.get('candidate', {}).get('id', 'unknown'))
    
    return jsonify({
        'isValid': True,
        'status': 'SEEDED',
        'candidate_id': candidate_id,
        'timestamp': datetime.now().isoformat(),
        'message': 'Candidate accepted for evolution'
    })


if __name__ == '__main__':
    # Development server
    # In production, use gunicorn: gunicorn -w 4 -b 0.0.0.0:5000 agent.api.server:app
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', 'False') == 'True')
