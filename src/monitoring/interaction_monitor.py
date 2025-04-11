import logging
import threading
import time
from datetime import datetime
from pynput import mouse, keyboard
import psutil

logger = logging.getLogger(__name__)

class InteractionMonitor:
    """Monitors user interactions including mouse, keyboard, and application usage"""
    
    def __init__(self, shared_metrics):
        """Initialize the interaction monitor"""
        self.shared_metrics = shared_metrics
        self.mouse_listener = None
        self.keyboard_listener = None
        self.monitor_thread = None
        self.running = False
        
        # Counters for current interval
        self._mouse_clicks = 0
        self._key_presses = 0
        self._start_time = datetime.now()
        
        logger.info("Interaction monitor initialized")
    
    def start(self):
        """Start all monitoring activities"""
        try:
            self.running = True
            
            # Start mouse monitoring
            self.mouse_listener = mouse.Listener(
                on_click=self._on_mouse_click,
                on_move=self._on_mouse_move
            )
            self.mouse_listener.start()
            
            # Start keyboard monitoring
            self.keyboard_listener = keyboard.Listener(
                on_press=self._on_key_press
            )
            self.keyboard_listener.start()
            
            # Start the monitoring thread
            self.monitor_thread = threading.Thread(target=self._monitor_loop)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            
            logger.info("All monitoring systems started successfully")
            
        except Exception as e:
            logger.error(f"Failed to start monitoring: {str(e)}")
            self.stop()
            raise
    
    def stop(self):
        """Stop all monitoring activities"""
        self.running = False
        
        if self.mouse_listener:
            self.mouse_listener.stop()
        
        if self.keyboard_listener:
            self.keyboard_listener.stop()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        
        logger.info("Monitoring stopped")
    
    def _on_mouse_click(self, x, y, button, pressed):
        """Handle mouse click events"""
        if pressed:
            self._mouse_clicks += 1
    
    def _on_mouse_move(self, x, y):
        """Handle mouse movement events"""
        pass  # We might track this later for movement patterns
    
    def _on_key_press(self, key):
        """Handle keyboard press events"""
        self._key_presses += 1
    
    def _get_active_window_title(self):
        """Get the currently active window title"""
        try:
            # This is a simplified version - in practice we'd use platform-specific code
            # or a cross-platform library to get the active window title
            return "Active Window"  # Placeholder
        except Exception as e:
            logger.error(f"Failed to get active window: {str(e)}")
            return "Unknown"
    
    def _calculate_screen_time(self):
        """Calculate total screen time in minutes"""
        return (datetime.now() - self._start_time).total_seconds() / 60
    
    def _monitor_loop(self):
        """Main monitoring loop that updates shared metrics"""
        update_interval = 5  # Update every 5 seconds
        
        while self.running:
            try:
                # Update shared metrics
                self.shared_metrics.update({
                    'mouse_clicks': self._mouse_clicks,
                    'key_presses': self._key_presses,
                    'screen_time': self._calculate_screen_time(),
                    'current_app': self._get_active_window_title(),
                    'last_updated': datetime.now().isoformat()
                })
                
                # Sleep for the update interval
                time.sleep(update_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {str(e)}")
                time.sleep(1)  # Sleep briefly before retrying
    
    def get_current_metrics(self):
        """Get the current metrics"""
        return {
            'mouse_clicks': self._mouse_clicks,
            'key_presses': self._key_presses,
            'screen_time': self._calculate_screen_time(),
            'current_app': self._get_active_window_title()
        }
