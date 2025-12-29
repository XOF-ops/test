"""
Flask API Server for MIGP Agent.
Provides endpoints for swarm analysis, webhooks, thresholds, identity, and friction mining.
"""

import json
import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify

from agent.integrations.webhook_manager import WebhookManager
from agent.core.autonomy_thresholds import AutonomyThresholds
from agent.core.identity_dynamics import IdentityDynamics


app = Flask(__name__)

# Initialize managers
webhook_manager = WebhookManager()
thresholds_manager = AutonomyThresholds()
identity_dynamics = IdentityDynamics()

# Storage paths
SWARM_SNAPSHOT_PATH = "logs/last_swarm_analysis.json"
CANDIDATES_PATH = "candidates"


def _load_swarm_snapshot():
    """Load the last swarm analysis snapshot."""
    if os.path.exists(SWARM_SNAPSHOT_PATH):
        try:
            with open(SWARM_SNAPSHOT_PATH, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return None


def _save_swarm_snapshot(snapshot):
    """Save swarm analysis snapshot."""
    os.makedirs(os.path.dirname(SWARM_SNAPSHOT_PATH), exist_ok=True)
    with open(SWARM_SNAPSHOT_PATH, "w") as f:
        json.dump(snapshot, f, indent=2)


def _trigger_friction_mining(nodes):
    """
    Trigger friction mining on nodes with low coherence.
    Returns candidates for mining.
    """
    candidates = []
    threshold = 0.5

    for node in nodes:
        coherence = node.get("coherence", 1.0)
        if coherence < threshold:
            candidate = {
                "node_id": node.get("id"),
                "coherence": coherence,
                "friction_score": 1.0 - coherence,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "pending"
            }
            candidates.append(candidate)

    if candidates:
        os.makedirs(CANDIDATES_PATH, exist_ok=True)
        filename = f"{CANDIDATES_PATH}/friction_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, "w") as f:
            json.dump(candidates, f, indent=2)

    return candidates


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()})


@app.route("/api/analyze-swarm", methods=["GET"])
def get_swarm_analysis():
    """Get the last swarm analysis snapshot."""
    snapshot = _load_swarm_snapshot()
    if snapshot:
        return jsonify(snapshot)
    return jsonify({
        "status": "no_data",
        "message": "No swarm analysis available. POST to create one."
    })


@app.route("/api/analyze-swarm", methods=["POST"])
def post_swarm_analysis():
    """
    Analyze swarm data and persist snapshot.
    Automatically triggers friction mining if low-coherence nodes detected.
    """
    data = request.get_json() or {}
    nodes = data.get("nodes", [])

    # Calculate aggregate metrics
    total_coherence = sum(n.get("coherence", 0) for n in nodes)
    avg_coherence = total_coherence / len(nodes) if nodes else 0

    snapshot = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "node_count": len(nodes),
        "average_coherence": round(avg_coherence, 4),
        "nodes": nodes
    }

    # Trigger friction mining for low-coherence nodes
    friction_candidates = _trigger_friction_mining(nodes)
    if friction_candidates:
        snapshot["friction_mining"] = {
            "triggered": True,
            "candidates_count": len(friction_candidates)
        }
    else:
        snapshot["friction_mining"] = {"triggered": False}

    _save_swarm_snapshot(snapshot)

    return jsonify({
        "status": "success",
        "snapshot": snapshot
    })


@app.route("/api/webhooks", methods=["GET"])
def list_webhooks():
    """List all registered webhooks."""
    webhooks = webhook_manager.list_webhooks()
    return jsonify({
        "webhooks": webhooks,
        "count": len(webhooks)
    })


@app.route("/api/webhooks", methods=["POST"])
def register_webhook():
    """Register a new webhook URL."""
    data = request.get_json() or {}
    url = data.get("url")

    if not url:
        return jsonify({"error": "url is required"}), 400

    webhook = webhook_manager.register(url, data.get("name"))
    return jsonify({
        "status": "registered",
        "webhook": webhook
    })


@app.route("/api/webhooks/send-migp", methods=["POST"])
def send_migp():
    """Send MIGP payload to all registered webhooks."""
    data = request.get_json() or {}

    if not data:
        return jsonify({"error": "payload is required"}), 400

    result = webhook_manager.send_migp(data)
    return jsonify(result)


@app.route("/api/thresholds", methods=["GET"])
def get_thresholds():
    """Get current autonomy thresholds."""
    return jsonify({
        "thresholds": thresholds_manager.get_thresholds()
    })


@app.route("/api/thresholds/evaluate", methods=["POST"])
def evaluate_thresholds():
    """Evaluate an action against current thresholds."""
    data = request.get_json() or {}

    action = data.get("action", "UNKNOWN")
    metrics = data.get("metrics", {})
    pass_rate = data.get("pass_rate")

    result = thresholds_manager.evaluate(action, metrics, pass_rate)
    return jsonify(result)


@app.route("/api/identity", methods=["GET"])
def get_identity_status():
    """Get current identity dynamics status."""
    return jsonify(identity_dynamics.get_status())


@app.route("/api/identity/track", methods=["POST"])
def track_identity_event():
    """Track an identity-related event."""
    data = request.get_json() or {}

    event_type = data.get("event", "UPDATE")
    details = data.get("details", {})

    result = identity_dynamics.track_event(event_type, details)
    return jsonify(result)


@app.route("/api/friction-mining", methods=["POST"])
def manual_friction_mining():
    """Manually trigger friction mining on provided nodes."""
    data = request.get_json() or {}
    nodes = data.get("nodes", [])

    if not nodes:
        return jsonify({"error": "nodes array is required"}), 400

    candidates = _trigger_friction_mining(nodes)

    return jsonify({
        "status": "completed",
        "candidates": candidates,
        "candidates_count": len(candidates)
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
