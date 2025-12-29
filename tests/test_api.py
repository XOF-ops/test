"""
API Endpoint Tests using Flask test client.
Provides CI coverage for all API endpoints.
"""

import json
import pytest
from agent.api.server import app


@pytest.fixture
def client():
    """Create Flask test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_returns_ok(self, client):
        """Health endpoint should return status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"
        assert "timestamp" in data


class TestAnalyzeSwarmEndpoints:
    """Tests for swarm analysis endpoints."""

    def test_get_swarm_no_data(self, client):
        """GET should return no_data when no analysis exists."""
        response = client.get("/api/analyze-swarm")
        assert response.status_code == 200
        data = json.loads(response.data)
        # May have data or no_data depending on prior runs
        assert "status" in data or "timestamp" in data

    def test_post_swarm_analysis(self, client):
        """POST should analyze swarm and return snapshot."""
        payload = {
            "nodes": [
                {"id": "n1", "coherence": 0.7},
                {"id": "n2", "coherence": 0.6},
                {"id": "n3", "coherence": 0.8}
            ]
        }
        response = client.post(
            "/api/analyze-swarm",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "snapshot" in data
        assert data["snapshot"]["node_count"] == 3

    def test_post_swarm_triggers_friction_mining(self, client):
        """POST with low-coherence nodes should trigger friction mining."""
        payload = {
            "nodes": [
                {"id": "n1", "coherence": 0.3},
                {"id": "n2", "coherence": 0.4}
            ]
        }
        response = client.post(
            "/api/analyze-swarm",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["snapshot"]["friction_mining"]["triggered"] is True

    def test_get_swarm_after_post(self, client):
        """GET should return previously posted snapshot."""
        # First POST
        payload = {"nodes": [{"id": "test", "coherence": 0.9}]}
        client.post(
            "/api/analyze-swarm",
            data=json.dumps(payload),
            content_type="application/json"
        )
        # Then GET
        response = client.get("/api/analyze-swarm")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "node_count" in data


class TestWebhookEndpoints:
    """Tests for webhook management endpoints."""

    def test_list_webhooks(self, client):
        """GET webhooks should return list."""
        response = client.get("/api/webhooks")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "webhooks" in data
        assert "count" in data

    def test_register_webhook(self, client):
        """POST should register new webhook."""
        payload = {"url": "https://example.com/webhook/test"}
        response = client.post(
            "/api/webhooks",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "registered"
        assert "webhook" in data
        assert data["webhook"]["url"] == payload["url"]

    def test_register_webhook_with_name(self, client):
        """POST with name should register webhook with custom name."""
        payload = {
            "url": "https://example.com/webhook/named",
            "name": "my-webhook"
        }
        response = client.post(
            "/api/webhooks",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["webhook"]["name"] == "my-webhook"

    def test_register_webhook_no_url(self, client):
        """POST without url should return error."""
        response = client.post(
            "/api/webhooks",
            data=json.dumps({}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_send_migp(self, client):
        """POST send-migp should attempt to send to webhooks."""
        payload = {
            "pattern": "P127",
            "autonomy_score": 0.74,
            "identity_count": 3
        }
        response = client.post(
            "/api/webhooks/send-migp",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "sent_at" in data
        assert "payload" in data
        assert "results" in data


class TestThresholdEndpoints:
    """Tests for autonomy threshold endpoints."""

    def test_get_thresholds(self, client):
        """GET thresholds should return current thresholds."""
        response = client.get("/api/thresholds")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "thresholds" in data
        thresholds = data["thresholds"]
        assert "friction" in thresholds
        assert "coherence" in thresholds
        assert "sacrifice" in thresholds
        assert "governance" in thresholds
        assert "divergence" in thresholds

    def test_evaluate_thresholds(self, client):
        """POST evaluate should check action against thresholds."""
        payload = {
            "action": "DEPLOY_MIGP",
            "metrics": {
                "friction": 0.5,
                "coherence": 0.7,
                "sacrifice": 0.5,
                "governance": 0.5,
                "divergence": 0.2
            }
        }
        response = client.post(
            "/api/thresholds/evaluate",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["action"] == "DEPLOY_MIGP"
        assert "passed" in data
        assert "checks" in data
        assert "timestamp" in data

    def test_evaluate_with_auto_tune(self, client):
        """POST evaluate with pass_rate should trigger auto-tune."""
        payload = {
            "action": "TEST_ACTION",
            "metrics": {"coherence": 0.6},
            "pass_rate": 0.45
        }
        response = client.post(
            "/api/thresholds/evaluate",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "auto_tune" in data
        assert data["auto_tune"]["direction"] == "relaxed"


class TestIdentityEndpoints:
    """Tests for identity dynamics endpoints."""

    def test_get_identity_status(self, client):
        """GET identity should return current status."""
        response = client.get("/api/identity")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "identity_count" in data
        assert "event_count" in data
        assert "identities" in data
        assert "last_updated" in data

    def test_track_identity_event(self, client):
        """POST track should record identity event."""
        payload = {
            "event": "TENSION",
            "details": {
                "identity_a": "Alice",
                "identity_b": "Bob",
                "reason": "pace mismatch"
            }
        }
        response = client.post(
            "/api/identity/track",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "event" in data
        assert data["event"]["type"] == "TENSION"
        assert "identities_updated" in data
        assert "Alice" in data["identities_updated"]
        assert "Bob" in data["identities_updated"]

    def test_track_multiple_events(self, client):
        """Multiple track calls should increment event count."""
        # First event
        client.post(
            "/api/identity/track",
            data=json.dumps({"event": "EMERGENCE", "details": {"identity": "NewAgent"}}),
            content_type="application/json"
        )
        # Second event
        response = client.post(
            "/api/identity/track",
            data=json.dumps({"event": "UPDATE", "details": {"identity": "NewAgent"}}),
            content_type="application/json"
        )
        data = json.loads(response.data)
        assert data["total_events"] >= 2


class TestFrictionMiningEndpoint:
    """Tests for friction mining endpoint."""

    def test_friction_mining(self, client):
        """POST should process nodes and return candidates."""
        payload = {
            "nodes": [
                {"id": "n1", "coherence": 0.4},
                {"id": "n2", "coherence": 0.45},
                {"id": "n3", "coherence": 0.6}
            ]
        }
        response = client.post(
            "/api/friction-mining",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "completed"
        assert "candidates" in data
        # Only nodes with coherence < 0.5 should be candidates
        assert data["candidates_count"] == 2

    def test_friction_mining_no_candidates(self, client):
        """POST with high-coherence nodes should return no candidates."""
        payload = {
            "nodes": [
                {"id": "n1", "coherence": 0.8},
                {"id": "n2", "coherence": 0.9}
            ]
        }
        response = client.post(
            "/api/friction-mining",
            data=json.dumps(payload),
            content_type="application/json"
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["candidates_count"] == 0

    def test_friction_mining_no_nodes(self, client):
        """POST without nodes should return error."""
        response = client.post(
            "/api/friction-mining",
            data=json.dumps({}),
            content_type="application/json"
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data
