import logging
import signal
import sys
import threading
from flask import Flask, render_template, jsonify
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('burnout_monitor.log')
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__)

# Global state for monitoring
should_run = True
shared_metrics = {
    'mouse_clicks': 0,
    'key_presses': 0,
    'screen_time': 0,
    'current_app': '',
    'last_updated': None,
    'risk_level': 'low',
    'recommendations': []
}

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully"""
    global should_run
    logger.info("Shutdown signal received. Cleaning up...")
    should_run = False
    sys.exit(0)

@app.route('/')
def index():
    """Render the dashboard page"""
    return render_template('index.html')

@app.route('/history')
def history():
    """Render the history page"""
    return render_template('history.html')

@app.route('/api/current_metrics')
def get_current_metrics():
    """API endpoint for current monitoring metrics"""
    global shared_metrics
    return jsonify(shared_metrics)

def main():
    """Main application entry point"""
    try:
        # Register signal handlers
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        logger.info("Starting Burnout Monitor...")

        # Initialize monitoring components (will be implemented later)
        # monitor = InteractionMonitor(shared_metrics)
        # analyzer = BurnoutAnalyzer(shared_metrics)
        # data_storage = DataStorage()

        # Start the Flask server
        app.run(host='0.0.0.0', port=8000, debug=False, use_reloader=False)

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
