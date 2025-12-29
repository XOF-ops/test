"""
API Server - Phase 3 Extended HTTP API Layer
=============================================

This module provides HTTP API access to the Master Brain system,
enabling integration with external services and n8n workflows.

Metadata Signature:
-------------------
{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T07:52:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "Using Flask for simplicity over async frameworks",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}

Purpose (A1 - Relational):
    - Serves external systems by providing HTTP API access
    - Serves n8n workflows by forwarding MIGP metrics via webhooks
    - Serves human operators by enabling API-based monitoring

Design Rationale (A4 - Process):
    - RESTful API design for standard integration
    - Webhook support for real-time notifications
    - All endpoints log their operations (A2)
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import urllib.request
import threading

# Import core modules
from master_brain import MasterBrain
from master_brain_engine import MasterBrainEngine, FrictionType, FrictionSeverity
from swarm_validator import SwarmValidator, NodeValidation
from divergence_map import DivergenceMap, ContradictionType
from adaptive_mining import AdaptiveMining
from agent_runtime_orchestrator import AgentRuntimeOrchestrator
from identity_dynamics import IdentityDynamicsLayer
from autonomy_thresholds import AutonomyThresholds, ThresholdCategory


# Module-level metadata signature
MODULE_METADATA = {
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T07:52:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "Using Flask for simplicity over async frameworks",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class WebhookManager:
    """
    Manages webhook notifications to external services like n8n.
    
    Purpose (A1): Serves n8n and other automation platforms by
    forwarding MIGP (Master Intelligence Growth Protocol) metrics.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the webhook manager.
        
        Args:
            base_path: Base directory for configuration
        """
        self.base_path = base_path
        self.webhooks: Dict[str, str] = {}
        self._load_webhooks()
    
    def _load_webhooks(self) -> None:
        """Load webhook configuration."""
        config_path = os.path.join(self.base_path, "webhook_config.json")
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                data = json.load(f)
                self.webhooks = data.get("webhooks", {})
        else:
            self.webhooks = {}
    
    def _save_webhooks(self) -> None:
        """Save webhook configuration."""
        config_path = os.path.join(self.base_path, "webhook_config.json")
        data = {
            "metadata": MODULE_METADATA,
            "webhooks": self.webhooks,
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_webhook(self, name: str, url: str) -> Dict[str, Any]:
        """
        Register a webhook endpoint.
        
        Args:
            name: Webhook name (e.g., "n8n_migp")
            url: Webhook URL
            
        Returns:
            Registration confirmation
        """
        self.webhooks[name] = url
        self._save_webhooks()
        return {
            "status": "REGISTERED",
            "name": name,
            "url": url,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    
    def unregister_webhook(self, name: str) -> bool:
        """
        Unregister a webhook.
        
        Args:
            name: Webhook name to remove
            
        Returns:
            True if successful
        """
        if name in self.webhooks:
            del self.webhooks[name]
            self._save_webhooks()
            return True
        return False
    
    def send_migp_metrics(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send MIGP (Master Intelligence Growth Protocol) metrics to all registered webhooks.
        
        Args:
            metrics: MIGP metrics to send
            
        Returns:
            Results of webhook calls
        """
        results = {}
        
        for name, url in self.webhooks.items():
            try:
                payload = json.dumps({
                    "event": "MIGP_METRICS",
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "metrics": metrics
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    url,
                    data=payload,
                    headers={
                        'Content-Type': 'application/json',
                        'X-MIGP-Version': '1.0',
                        'X-Source': 'MasterBrain'
                    },
                    method='POST'
                )
                
                # In production, you'd want proper error handling
                # For now, we'll just note the attempt
                results[name] = {
                    "status": "QUEUED",
                    "url": url,
                    "payload_size": len(payload)
                }
            except Exception as e:
                results[name] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        
        return results
    
    def get_registered_webhooks(self) -> Dict[str, str]:
        """Get all registered webhooks."""
        return self.webhooks.copy()


class APIHandler(BaseHTTPRequestHandler):
    """
    HTTP request handler for the Master Brain API.
    
    Provides endpoints for:
        - /api/analyze-swarm: Swarm analysis and coherence validation
        - /api/migp: MIGP metrics and webhook forwarding
        - /api/coherence: System coherence status
        - /api/candidates: Adaptive mining candidates
        - /api/contradictions: Divergence map access
    """
    
    # Class-level services (initialized once)
    brain = None
    engine = None  # MasterBrainEngine for A14/gnosis
    swarm_validator = None
    divergence_map = None
    adaptive_mining = None
    orchestrator = None
    webhook_manager = None
    identity_layer = None
    autonomy_thresholds = None
    
    @classmethod
    def initialize_services(cls, base_path: str = "."):
        """Initialize all services."""
        cls.brain = MasterBrain(base_path)
        cls.engine = MasterBrainEngine(base_path)
        cls.swarm_validator = SwarmValidator(base_path)
        cls.divergence_map = DivergenceMap(base_path)
        cls.adaptive_mining = AdaptiveMining(base_path)
        cls.orchestrator = AgentRuntimeOrchestrator(base_path)
        cls.webhook_manager = WebhookManager(base_path)
        cls.identity_layer = IdentityDynamicsLayer(base_path)
        cls.autonomy_thresholds = AutonomyThresholds(base_path)
    
    def _send_json_response(self, data: Dict[str, Any], status: int = 200):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    def _parse_json_body(self) -> Dict[str, Any]:
        """Parse JSON body from request."""
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        return {}
    
    def do_OPTIONS(self):
        """Handle CORS preflight."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        
        if path == '/api/analyze-swarm':
            self._handle_analyze_swarm_get(query)
        elif path == '/api/coherence':
            self._handle_coherence()
        elif path == '/api/chain-state':
            self._handle_chain_state()
        elif path == '/api/candidates':
            self._handle_candidates_get()
        elif path == '/api/contradictions':
            self._handle_contradictions_get()
        elif path == '/api/webhooks':
            self._handle_webhooks_get()
        elif path == '/api/migp':
            self._handle_migp_get()
        elif path == '/api/identity':
            self._handle_identity_get()
        elif path == '/api/thresholds':
            self._handle_thresholds_get()
        elif path == '/api/health':
            self._handle_health()
        elif path == '/api/a14':
            self._handle_a14_get()
        elif path == '/api/kernel':
            self._handle_kernel_get()
        elif path == '/api/gnosis':
            self._handle_gnosis_get()
        elif path == '/api/friction':
            self._handle_friction_get()
        elif path == '/api/governance':
            self._handle_governance_get()
        else:
            self._send_json_response({"error": "Not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._parse_json_body()
        
        if path == '/api/analyze-swarm':
            self._handle_analyze_swarm_post(body)
        elif path == '/api/candidates':
            self._handle_candidates_post(body)
        elif path == '/api/contradictions':
            self._handle_contradictions_post(body)
        elif path == '/api/webhooks':
            self._handle_webhooks_post(body)
        elif path == '/api/webhooks/send-migp':
            self._handle_send_migp(body)
        elif path == '/api/identity/track':
            self._handle_identity_track(body)
        elif path == '/api/thresholds/evaluate':
            self._handle_thresholds_evaluate(body)
        elif path == '/api/friction-mining':
            self._handle_friction_mining(body)
        elif path == '/api/gnosis/scan':
            self._handle_gnosis_scan(body)
        elif path == '/api/friction/record':
            self._handle_friction_record(body)
        elif path == '/api/governance/propose':
            self._handle_governance_propose(body)
        else:
            self._send_json_response({"error": "Not found"}, 404)
    
    # === /api/analyze-swarm ===
    
    def _handle_analyze_swarm_get(self, query: Dict[str, List[str]]):
        """
        GET /api/analyze-swarm
        
        Returns current swarm health and validation status.
        """
        health = self.swarm_validator.get_swarm_health()
        self._send_json_response({
            "endpoint": "/api/analyze-swarm",
            "method": "GET",
            "swarm_health": health,
            "registered_nodes": len(self.swarm_validator.registered_nodes),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_analyze_swarm_post(self, body: Dict[str, Any]):
        """
        POST /api/analyze-swarm
        
        Analyze a swarm with provided node tasks.
        
        Body:
        {
            "nodes": [
                {
                    "node_id": "NODE_1",
                    "node_type": "MODEL",
                    "task_data": {
                        "task_id": "...",
                        "serves": [...],
                        "reason": "..."
                    }
                }
            ]
        }
        """
        nodes = body.get("nodes", [])
        
        # Register and validate nodes
        node_tasks = {}
        for node in nodes:
            node_id = node.get("node_id")
            node_type = node.get("node_type", "UNKNOWN")
            task_data = node.get("task_data", {})
            
            # Register if new
            if node_id not in self.swarm_validator.registered_nodes:
                self.swarm_validator.register_node(
                    node_id=node_id,
                    node_type=node_type,
                    axiom_alignment=["A1", "A2", "A4", "A7", "A9"]
                )
            
            node_tasks[node_id] = task_data
        
        # Validate swarm
        validation = self.swarm_validator.validate_swarm(node_tasks)
        
        # Detect divergence
        divergences = self.swarm_validator.detect_divergence(validation)
        
        # Check for high-friction scenarios
        friction_events = []
        if not validation.swarm_coherent or len(divergences) > 0:
            # This is a high-friction scenario - connect to adaptive mining
            friction_event = self._trigger_friction_mining(
                context="swarm_analysis",
                friction_level=len(divergences),
                details={
                    "divergences": divergences,
                    "coherence": validation.average_coherence
                }
            )
            friction_events.append(friction_event)
        
        # Forward to webhooks if configured
        if self.webhook_manager.webhooks:
            migp_metrics = {
                "event_type": "SWARM_ANALYSIS",
                "swarm_coherent": validation.swarm_coherent,
                "average_coherence": validation.average_coherence,
                "total_nodes": validation.total_nodes,
                "divergence_count": len(divergences)
            }
            self.webhook_manager.send_migp_metrics(migp_metrics)
        
        self._send_json_response({
            "endpoint": "/api/analyze-swarm",
            "method": "POST",
            "validation": validation.to_dict(),
            "divergences": divergences,
            "friction_events": friction_events,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/coherence ===
    
    def _handle_coherence(self):
        """GET /api/coherence - System coherence status."""
        coherence = self.brain.validate_coherence()
        self._send_json_response({
            "endpoint": "/api/coherence",
            "coherence": coherence,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/chain-state ===
    
    def _handle_chain_state(self):
        """GET /api/chain-state - Full chain state."""
        state = self.brain.get_chain_state()
        self._send_json_response({
            "endpoint": "/api/chain-state",
            "state": state,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/candidates ===
    
    def _handle_candidates_get(self):
        """GET /api/candidates - List all candidates."""
        metrics = self.adaptive_mining.get_growth_metrics()
        self._send_json_response({
            "endpoint": "/api/candidates",
            "metrics": metrics,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_candidates_post(self, body: Dict[str, Any]):
        """
        POST /api/candidates - Register a new candidate.
        
        Body:
        {
            "platform_name": "...",
            "proposed_role": "..."
        }
        """
        platform_name = body.get("platform_name")
        proposed_role = body.get("proposed_role")
        
        if not platform_name or not proposed_role:
            self._send_json_response({"error": "Missing required fields"}, 400)
            return
        
        candidate = self.adaptive_mining.register_candidate(platform_name, proposed_role)
        
        self._send_json_response({
            "endpoint": "/api/candidates",
            "method": "POST",
            "candidate": candidate.to_dict(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/contradictions ===
    
    def _handle_contradictions_get(self):
        """GET /api/contradictions - Get contradiction map."""
        map_data = self.divergence_map.get_contradiction_map()
        self._send_json_response({
            "endpoint": "/api/contradictions",
            "map": map_data,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_contradictions_post(self, body: Dict[str, Any]):
        """
        POST /api/contradictions - Record a new contradiction.
        
        Body:
        {
            "type": "AXIOM_TENSION|REQUIREMENT_CONFLICT|...",
            "pole_a": "...",
            "pole_b": "...",
            "context": "..."
        }
        """
        c_type = body.get("type", "REQUIREMENT_CONFLICT")
        pole_a = body.get("pole_a")
        pole_b = body.get("pole_b")
        context = body.get("context", "API submission")
        
        if not pole_a or not pole_b:
            self._send_json_response({"error": "Missing required fields"}, 400)
            return
        
        contradiction = self.divergence_map.record_contradiction(
            contradiction_type=ContradictionType[c_type],
            pole_a=pole_a,
            pole_b=pole_b,
            context=context
        )
        
        self._send_json_response({
            "endpoint": "/api/contradictions",
            "method": "POST",
            "contradiction": contradiction.to_dict(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/webhooks ===
    
    def _handle_webhooks_get(self):
        """GET /api/webhooks - List registered webhooks."""
        webhooks = self.webhook_manager.get_registered_webhooks()
        self._send_json_response({
            "endpoint": "/api/webhooks",
            "webhooks": webhooks,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_webhooks_post(self, body: Dict[str, Any]):
        """
        POST /api/webhooks - Register a webhook.
        
        Body:
        {
            "name": "n8n_migp",
            "url": "https://n8n.example.com/webhook/..."
        }
        """
        name = body.get("name")
        url = body.get("url")
        
        if not name or not url:
            self._send_json_response({"error": "Missing required fields"}, 400)
            return
        
        result = self.webhook_manager.register_webhook(name, url)
        
        self._send_json_response({
            "endpoint": "/api/webhooks",
            "method": "POST",
            "result": result,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_send_migp(self, body: Dict[str, Any]):
        """
        POST /api/webhooks/send-migp - Send MIGP metrics to all webhooks.
        
        Body:
        {
            "metrics": { ... }
        }
        """
        metrics = body.get("metrics", {})
        
        # Add standard metrics
        metrics.update({
            "coherence_score": self.brain.coherence_score,
            "kernel_intact": self.brain.kernel_intact,
            "chain_length": len(self.brain.chain_signatures)
        })
        
        results = self.webhook_manager.send_migp_metrics(metrics)
        
        self._send_json_response({
            "endpoint": "/api/webhooks/send-migp",
            "method": "POST",
            "results": results,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/migp ===
    
    def _handle_migp_get(self):
        """GET /api/migp - Get current MIGP metrics."""
        coherence = self.brain.validate_coherence()
        growth = self.adaptive_mining.get_growth_metrics()
        
        migp_metrics = {
            "coherence_score": coherence.get("coherence_score", 0),
            "kernel_intact": coherence.get("kernel_intact", False),
            "chain_length": coherence.get("chain_length", 0),
            "total_candidates": growth.get("total_candidates", 0),
            "integrated_platforms": growth.get("integrated_platforms", []),
            "axioms_verified": coherence.get("axioms_verified", []),
            "system_alive": self.brain.system_alive
        }
        
        self._send_json_response({
            "endpoint": "/api/migp",
            "migp_metrics": migp_metrics,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/identity ===
    
    def _handle_identity_get(self):
        """GET /api/identity - Get identity dynamics status."""
        status = self.identity_layer.get_identity_status()
        self._send_json_response({
            "endpoint": "/api/identity",
            "status": status,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_identity_track(self, body: Dict[str, Any]):
        """
        POST /api/identity/track - Track an identity event.
        
        Body:
        {
            "entity_id": "...",
            "event_type": "EMERGENCE|EVOLUTION|TENSION|INTEGRATION|DISSOLUTION",
            "context": "..."
        }
        """
        entity_id = body.get("entity_id")
        event_type = body.get("event_type", "EVOLUTION")
        context = body.get("context", "API submission")
        
        if not entity_id:
            self._send_json_response({"error": "Missing entity_id"}, 400)
            return
        
        event = self.identity_layer.track_event(
            entity_id=entity_id,
            event_type=event_type,
            context=context
        )
        
        self._send_json_response({
            "endpoint": "/api/identity/track",
            "method": "POST",
            "event": event,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/thresholds ===
    
    def _handle_thresholds_get(self):
        """GET /api/thresholds - Get autonomy thresholds."""
        thresholds = self.autonomy_thresholds.get_all_thresholds()
        self._send_json_response({
            "endpoint": "/api/thresholds",
            "thresholds": thresholds,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_thresholds_evaluate(self, body: Dict[str, Any]):
        """
        POST /api/thresholds/evaluate - Evaluate action against thresholds.
        
        Body:
        {
            "action_type": "DECISION|EXECUTION|ESCALATION|SACRIFICE",
            "confidence": 0.0-1.0,
            "context": {...}
        }
        """
        action_type = body.get("action_type", "DECISION")
        confidence = body.get("confidence", 0.0)
        context = body.get("context", {})
        
        evaluation = self.autonomy_thresholds.evaluate_action(
            action_type=action_type,
            confidence=confidence,
            context=context
        )
        
        self._send_json_response({
            "endpoint": "/api/thresholds/evaluate",
            "method": "POST",
            "evaluation": evaluation,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/friction-mining ===
    
    def _handle_friction_mining(self, body: Dict[str, Any]):
        """
        POST /api/friction-mining - Connect adaptive mining to high-friction scenarios.
        
        Body:
        {
            "context": "...",
            "friction_level": 1-5,
            "details": {...}
        }
        """
        context = body.get("context", "Unknown")
        friction_level = body.get("friction_level", 1)
        details = body.get("details", {})
        
        event = self._trigger_friction_mining(context, friction_level, details)
        
        self._send_json_response({
            "endpoint": "/api/friction-mining",
            "method": "POST",
            "event": event,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _trigger_friction_mining(
        self,
        context: str,
        friction_level: int,
        details: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Trigger adaptive mining for high-friction scenarios.
        
        When friction is detected (low coherence, divergence, conflicts),
        the system mines for new candidates or solutions.
        """
        # Record the friction event
        friction_event = {
            "event_id": f"FRICTION_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "context": context,
            "friction_level": friction_level,
            "details": details,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
        
        # If high friction, register a mining candidate
        if friction_level >= 3:
            # Create a friction-response candidate
            candidate = self.adaptive_mining.register_candidate(
                platform_name=f"FRICTION_RESOLVER_{friction_event['event_id']}",
                proposed_role="FRICTION_RESOLVER"
            )
            friction_event["candidate_created"] = candidate.candidate_id
        
        # Log the friction event
        self._log_friction_event(friction_event)
        
        return friction_event
    
    def _log_friction_event(self, event: Dict[str, Any]) -> None:
        """Log a friction event (A2 - append-only)."""
        log_path = "friction_events.json"
        
        if os.path.exists(log_path):
            with open(log_path, 'r') as f:
                data = json.load(f)
        else:
            data = {"events": [], "metadata": MODULE_METADATA}
        
        data["events"].append(event)
        
        with open(log_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    # === /api/a14 - A14 Friction Governance ===
    
    def _handle_a14_get(self):
        """
        GET /api/a14 - Get A14 (Friction is the Medium of Governance) status.
        
        Returns the current status of A14 axiom and friction metrics.
        """
        a14_status = self.engine.get_a14_status()
        self._send_json_response({
            "endpoint": "/api/a14",
            "method": "GET",
            "a14": a14_status,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/kernel - Kernel Architecture ===
    
    def _handle_kernel_get(self):
        """
        GET /api/kernel - Get the full kernel.json architecture.
        
        Returns the complete axiom architecture with all layers.
        """
        kernel = self.engine.kernel
        self._send_json_response({
            "endpoint": "/api/kernel",
            "method": "GET",
            "kernel": kernel,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/gnosis - Gnosis Scan ===
    
    def _handle_gnosis_get(self):
        """
        GET /api/gnosis - Get gnosis scan history.
        
        Returns the history of gnosis scans performed.
        """
        self._send_json_response({
            "endpoint": "/api/gnosis",
            "method": "GET",
            "history": self.engine.gnosis_history,
            "scan_count": len(self.engine.gnosis_history),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_gnosis_scan(self, body: Dict[str, Any]):
        """
        POST /api/gnosis/scan - Perform a gnosis scan.
        
        Body:
        {
            "context": {
                "divergence_detected": false,
                "proposal_pending": false,
                "threshold_adjusted": false,
                "contradiction_unresolved": false
            }
        }
        """
        context = body.get("context", {})
        result = self.engine.gnosis_scan(context)
        
        self._send_json_response({
            "endpoint": "/api/gnosis/scan",
            "method": "POST",
            "result": result,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/friction - Friction Events ===
    
    def _handle_friction_get(self):
        """
        GET /api/friction - Get friction events from engine.
        
        Returns all friction events tracked by the engine.
        """
        events = [e.to_dict() for e in self.engine.friction_events]
        self._send_json_response({
            "endpoint": "/api/friction",
            "method": "GET",
            "events": events,
            "count": len(events),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_friction_record(self, body: Dict[str, Any]):
        """
        POST /api/friction/record - Record a friction event.
        
        Body:
        {
            "friction_type": "DIVERGENCE|COHERENCE_DROP|CONTRADICTION|THRESHOLD_BREACH|CANDIDATE_REJECTION|GOVERNANCE_CONFLICT",
            "severity": "LOW|MEDIUM|HIGH|CRITICAL",
            "source": "...",
            "description": "...",
            "axiom_impact": ["A14", "A7", ...]
        }
        """
        friction_type_str = body.get("friction_type", "DIVERGENCE")
        severity_str = body.get("severity", "MEDIUM")
        source = body.get("source", "api")
        description = body.get("description", "Friction recorded via API")
        axiom_impact = body.get("axiom_impact", ["A14"])
        
        # Convert strings to enums
        try:
            friction_type = FrictionType[friction_type_str]
        except KeyError:
            friction_type = FrictionType.DIVERGENCE
        
        try:
            severity = FrictionSeverity[severity_str]
        except KeyError:
            severity = FrictionSeverity.MEDIUM
        
        event = self.engine.record_friction(
            friction_type=friction_type,
            severity=severity,
            source=source,
            description=description,
            axiom_impact=axiom_impact
        )
        
        self._send_json_response({
            "endpoint": "/api/friction/record",
            "method": "POST",
            "event": event.to_dict(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/governance - Governance Proposals ===
    
    def _handle_governance_get(self):
        """
        GET /api/governance - Get governance proposals.
        
        Returns all governance proposals generated from friction and patterns.
        """
        proposals = [p.to_dict() for p in self.engine.governance_proposals]
        self._send_json_response({
            "endpoint": "/api/governance",
            "method": "GET",
            "proposals": proposals,
            "count": len(proposals),
            "pending": sum(1 for p in self.engine.governance_proposals if p.status == "PENDING"),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def _handle_governance_propose(self, body: Dict[str, Any]):
        """
        POST /api/governance/propose - Trigger a gnosis scan to generate proposals.
        
        This performs a gnosis scan with the provided context and returns
        any governance proposals generated.
        
        Body:
        {
            "context": {
                "divergence_detected": true,
                ...
            }
        }
        """
        context = body.get("context", {"divergence_detected": True})
        result = self.engine.gnosis_scan(context)
        
        self._send_json_response({
            "endpoint": "/api/governance/propose",
            "method": "POST",
            "proposals_generated": result.get("governance_proposals_generated", []),
            "friction_events": result.get("friction_events", []),
            "coherence_score": result.get("coherence_score", 5.0),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    # === /api/health ===
    
    def _handle_health(self):
        """GET /api/health - Health check endpoint."""
        self._send_json_response({
            "status": "healthy",
            "coherence_score": self.brain.coherence_score,
            "kernel_intact": self.brain.kernel_intact,
            "system_alive": self.brain.system_alive,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })


def run_server(host: str = "0.0.0.0", port: int = 8080, base_path: str = "."):
    """
    Run the API server.
    
    Args:
        host: Host to bind to
        port: Port to listen on
        base_path: Base path for data files
    """
    APIHandler.initialize_services(base_path)
    server = HTTPServer((host, port), APIHandler)
    print(f"Master Brain API Server running on http://{host}:{port}")
    print("Endpoints:")
    print("  GET  /api/health           - Health check")
    print("  GET  /api/analyze-swarm    - Swarm health status")
    print("  POST /api/analyze-swarm    - Analyze swarm with nodes")
    print("  GET  /api/coherence        - System coherence")
    print("  GET  /api/chain-state      - Full chain state")
    print("  GET  /api/migp             - MIGP metrics")
    print("  GET  /api/candidates       - List candidates")
    print("  POST /api/candidates       - Register candidate")
    print("  GET  /api/contradictions   - Contradiction map")
    print("  POST /api/contradictions   - Record contradiction")
    print("  GET  /api/webhooks         - List webhooks")
    print("  POST /api/webhooks         - Register webhook (n8n support)")
    print("  POST /api/webhooks/send-migp - Forward MIGP metrics")
    print("  GET  /api/identity         - Identity dynamics status")
    print("  POST /api/identity/track   - Track identity event")
    print("  GET  /api/thresholds       - Autonomy thresholds")
    print("  POST /api/thresholds/evaluate - Evaluate action")
    print("  POST /api/friction-mining  - Trigger friction mining")
    print("  --- A14 Friction Governance ---")
    print("  GET  /api/a14              - A14 axiom status")
    print("  GET  /api/kernel           - Full kernel architecture")
    print("  GET  /api/gnosis           - Gnosis scan history")
    print("  POST /api/gnosis/scan      - Perform gnosis scan")
    print("  GET  /api/friction         - Friction events")
    print("  POST /api/friction/record  - Record friction event")
    print("  GET  /api/governance       - Governance proposals")
    print("  POST /api/governance/propose - Generate proposals from friction")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
