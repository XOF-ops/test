"""
Tests for MasterBrainEngine and API Server.
"""

import json
import pytest
from master_brain_engine import MasterBrainEngine
from api_server import create_app


class TestMasterBrainEngine:
    """Tests for MasterBrainEngine class."""

    def test_initialization(self):
        """Test engine initialization."""
        engine = MasterBrainEngine()
        assert engine._initialized is True
        assert engine._scan_count == 0
        assert engine._last_scan_time is None

    def test_gnosis_scan_basic(self):
        """Test basic gnosis scan functionality."""
        engine = MasterBrainEngine()
        result = engine.gnosis_scan("This is a test message")

        assert 'timestamp' in result
        assert 'patterns_detected' in result
        assert 'axioms_detected' in result
        assert 'coherence' in result
        assert 'classification' in result
        assert 'scan_id' in result

    def test_gnosis_scan_with_patterns(self):
        """Test gnosis scan detecting patterns."""
        engine = MasterBrainEngine()
        text = "The dialogue between us creates something relational. This process matters."
        result = engine.gnosis_scan(text)

        assert len(result['patterns_detected']) > 0
        assert len(result['axioms_detected']) > 0

    def test_gnosis_scan_updates_count(self):
        """Test that scan count is updated."""
        engine = MasterBrainEngine()
        engine.gnosis_scan("test 1")
        engine.gnosis_scan("test 2")

        assert engine._scan_count == 2

    def test_get_status(self):
        """Test engine status retrieval."""
        engine = MasterBrainEngine()
        status = engine.get_status()

        assert status['initialized'] is True
        assert status['status'] == 'operational'
        assert 'patterns_available' in status
        assert 'axioms_available' in status

    def test_pattern_detection_p001(self):
        """Test P001 pattern detection."""
        engine = MasterBrainEngine()
        text = "The dialogue creates a relational process between us."
        result = engine.gnosis_scan(text)

        pattern_ids = [p['pattern_id'] for p in result['patterns_detected']]
        assert 'P001' in pattern_ids

    def test_coherence_calculation(self):
        """Test coherence calculation."""
        engine = MasterBrainEngine()
        result = engine.gnosis_scan(
            "Dialogue is relational. The process of tension creates archive data."
        )

        assert 'score' in result['coherence']
        assert 'coherent' in result['coherence']


class TestAPIServer:
    """Tests for API Server endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        app = create_app()
        app.config['TESTING'] = True
        return app.test_client()

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'

    def test_scan_endpoint(self, client):
        """Test scan endpoint with valid text."""
        response = client.post(
            '/api/scan',
            json={'text': 'Test message for scanning'},
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'patterns_detected' in data
        assert 'axioms_detected' in data
        assert 'coherence' in data

    def test_scan_endpoint_missing_text(self, client):
        """Test scan endpoint with missing text field."""
        response = client.post(
            '/api/scan',
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_scan_endpoint_empty_text(self, client):
        """Test scan endpoint with empty text."""
        response = client.post(
            '/api/scan',
            json={'text': '   '},
            content_type='application/json'
        )
        assert response.status_code == 400

    def test_status_endpoint(self, client):
        """Test status endpoint for dashboards."""
        response = client.get('/api/status')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'initialized' in data
        assert 'scan_count' in data
        assert data['status'] == 'operational'

    def test_status_full_endpoint(self, client):
        """Test full status endpoint."""
        response = client.get('/api/status/full')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'patterns_available' in data
        assert isinstance(data['patterns_available'], list)

    def test_conversations_endpoint(self, client):
        """Test conversations listing endpoint."""
        response = client.get('/api/conversations')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'conversations' in data

    def test_scan_with_pattern_detection(self, client):
        """Test scan endpoint detects patterns in text."""
        response = client.post(
            '/api/scan',
            json={'text': 'The dialogue between us creates relational tension and process.'},
            content_type='application/json'
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['patterns_detected']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
