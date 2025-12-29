"""
API Server for MasterBrainEngine.

This server provides REST API endpoints backed by the MasterBrainEngine.
It delegates to the engine to avoid duplicate server logic.
"""

from flask import Flask, request, jsonify
from master_brain_engine import MasterBrainEngine


def create_app(engine: MasterBrainEngine = None) -> Flask:
    """
    Create and configure the Flask application.

    Args:
        engine: Optional MasterBrainEngine instance. If not provided,
                a new instance will be created.

    Returns:
        Configured Flask application
    """
    app = Flask(__name__)

    # Use provided engine or create a new one
    if engine is None:
        engine = MasterBrainEngine()

    # Store engine in app config for access in routes
    app.config['ENGINE'] = engine

    @app.route('/api/scan', methods=['POST'])
    def scan():
        """
        Perform a gnosis scan on provided text.

        Backed by MasterBrainEngine.gnosis_scan

        Request body:
            {
                "text": "Text content to analyze"
            }

        Returns:
            JSON with scan results including patterns, axioms, and coherence
        """
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({
                'error': 'Missing required field: text',
                'usage': {'text': 'The text content to analyze'}
            }), 400

        text = data['text']
        if not isinstance(text, str) or not text.strip():
            return jsonify({
                'error': 'Field "text" must be a non-empty string'
            }), 400

        result = app.config['ENGINE'].gnosis_scan(text)
        return jsonify(result)

    @app.route('/api/status', methods=['GET'])
    def status():
        """
        Get engine status for dashboard display.

        Returns a subset of engine status information suitable
        for dashboard widgets and monitoring.

        Returns:
            JSON with engine status information
        """
        full_status = app.config['ENGINE'].get_status()

        # Return subset suitable for dashboards
        dashboard_status = {
            'status': full_status['status'],
            'initialized': full_status['initialized'],
            'scan_count': full_status['scan_count'],
            'last_scan_time': full_status['last_scan_time'],
            'patterns_available': len(full_status['patterns_available']),
            'axioms_available': len(full_status['axioms_available'])
        }

        return jsonify(dashboard_status)

    @app.route('/api/status/full', methods=['GET'])
    def status_full():
        """
        Get full engine status.

        Returns:
            JSON with complete engine status information
        """
        return jsonify(app.config['ENGINE'].get_status())

    @app.route('/api/conversations', methods=['GET'])
    def list_conversations():
        """
        List available conversations.

        Returns:
            JSON with list of conversations
        """
        conversations = app.config['ENGINE'].list_conversations()
        return jsonify({'conversations': conversations})

    @app.route('/api/health', methods=['GET'])
    def health():
        """
        Health check endpoint.

        Returns:
            JSON with health status
        """
        return jsonify({'status': 'healthy'})

    return app


# Create the default app instance
app = create_app()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='MasterBrainEngine API Server')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, debug=args.debug)
