import json
import logging
import os
from datetime import datetime, timedelta
from pathlib import Path

logger = logging.getLogger(__name__)

class DataStorage:
    """Handles persistent storage of monitoring data"""
    
    def __init__(self, data_dir='data'):
        """Initialize the data storage system"""
        self.data_dir = Path(data_dir)
        self._ensure_data_directory()
        logger.info(f"Data storage initialized with directory: {self.data_dir}")
    
    def _ensure_data_directory(self):
        """Create the data directory if it doesn't exist"""
        try:
            self.data_dir.mkdir(parents=True, exist_ok=True)
            logger.info("Data directory verified/created successfully")
        except Exception as e:
            logger.error(f"Failed to create data directory: {str(e)}")
            raise
    
    def save_metrics(self, metrics):
        """
        Save the current metrics to a JSON file
        Args:
            metrics (dict): The metrics to save
        """
        try:
            # Create filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = self.data_dir / f"metrics_{timestamp}.json"
            
            # Add timestamp to metrics
            metrics_with_time = {
                'timestamp': datetime.now().isoformat(),
                'metrics': metrics
            }
            
            # Write to file
            with open(filename, 'w') as f:
                json.dump(metrics_with_time, f, indent=2)
            
            logger.info(f"Metrics saved to {filename}")
            
            # Cleanup old files
            self._cleanup_old_files()
            
        except Exception as e:
            logger.error(f"Failed to save metrics: {str(e)}")
    
    def load_metrics(self, hours=24):
        """
        Load metrics from the past specified hours
        Args:
            hours (int): Number of hours of data to load
        Returns:
            list: List of metric entries
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=hours)
            metrics = []
            
            # Get all metric files
            metric_files = sorted(self.data_dir.glob("metrics_*.json"))
            
            for file_path in metric_files:
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        
                    # Parse timestamp and check if it's within our time window
                    timestamp = datetime.fromisoformat(data['timestamp'])
                    if timestamp >= cutoff_time:
                        metrics.append(data)
                    
                except Exception as e:
                    logger.warning(f"Failed to load metrics from {file_path}: {str(e)}")
                    continue
            
            logger.info(f"Loaded {len(metrics)} metric entries")
            return metrics
            
        except Exception as e:
            logger.error(f"Failed to load metrics: {str(e)}")
            return []
    
    def _cleanup_old_files(self, max_age_days=7):
        """
        Remove metric files older than specified days
        Args:
            max_age_days (int): Maximum age of files to keep
        """
        try:
            cutoff_time = datetime.now() - timedelta(days=max_age_days)
            
            for file_path in self.data_dir.glob("metrics_*.json"):
                try:
                    # Get file creation time
                    file_time = datetime.fromtimestamp(file_path.stat().st_ctime)
                    
                    # Remove if older than cutoff
                    if file_time < cutoff_time:
                        file_path.unlink()
                        logger.info(f"Removed old metric file: {file_path}")
                        
                except Exception as e:
                    logger.warning(f"Failed to process file {file_path}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Failed to cleanup old files: {str(e)}")
    
    def get_daily_summary(self, date=None):
        """
        Get a summary of metrics for a specific date
        Args:
            date (datetime): The date to summarize (defaults to today)
        Returns:
            dict: Summary metrics for the day
        """
        try:
            if date is None:
                date = datetime.now().date()
            
            # Load metrics for the day
            metrics = self.load_metrics(hours=24)
            
            # Filter metrics for the specified date
            daily_metrics = [
                m for m in metrics
                if datetime.fromisoformat(m['timestamp']).date() == date
            ]
            
            if not daily_metrics:
                return None
            
            # Calculate summary statistics
            summary = {
                'date': date.isoformat(),
                'total_mouse_clicks': sum(m['metrics']['mouse_clicks'] for m in daily_metrics),
                'total_key_presses': sum(m['metrics']['key_presses'] for m in daily_metrics),
                'total_screen_time': max(m['metrics']['screen_time'] for m in daily_metrics),
                'risk_levels': {
                    'high': sum(1 for m in daily_metrics if m['metrics'].get('risk_level') == 'high'),
                    'medium': sum(1 for m in daily_metrics if m['metrics'].get('risk_level') == 'medium'),
                    'low': sum(1 for m in daily_metrics if m['metrics'].get('risk_level') == 'low')
                }
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Failed to generate daily summary: {str(e)}")
            return None
