import logging
import numpy as np
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler

logger = logging.getLogger(__name__)

class BurnoutAnalyzer:
    """Analyzes user interaction patterns to assess burnout risk"""
    
    def __init__(self, shared_metrics):
        """Initialize the burnout analyzer"""
        self.shared_metrics = shared_metrics
        self.scaler = MinMaxScaler()
        
        # Thresholds for risk assessment
        self.THRESHOLDS = {
            'continuous_work': 120,  # minutes
            'high_activity': {
                'mouse_clicks': 100,  # clicks per hour
                'key_presses': 1000   # keypresses per hour
            }
        }
        
        # Initialize historical data storage
        self.hourly_metrics = []
        self.last_break = datetime.now()
        
        logger.info("Burnout analyzer initialized")
    
    def analyze_metrics(self, current_metrics):
        """
        Analyze current metrics and return risk assessment
        Returns: dict with risk_level and recommendations
        """
        try:
            # Store hourly metrics for pattern analysis
            self._update_hourly_metrics(current_metrics)
            
            # Calculate various risk factors
            continuous_work_risk = self._assess_continuous_work()
            activity_risk = self._assess_activity_levels(current_metrics)
            pattern_risk = self._analyze_patterns()
            
            # Combine risk factors to determine overall risk
            overall_risk = self._calculate_overall_risk([
                continuous_work_risk,
                activity_risk,
                pattern_risk
            ])
            
            # Generate recommendations based on risk factors
            recommendations = self._generate_recommendations(
                continuous_work_risk,
                activity_risk,
                pattern_risk
            )
            
            return {
                'risk_level': overall_risk,
                'recommendations': recommendations
            }
            
        except Exception as e:
            logger.error(f"Error in burnout analysis: {str(e)}")
            return {
                'risk_level': 'unknown',
                'recommendations': ['Unable to assess burnout risk at this time.']
            }
    
    def _update_hourly_metrics(self, metrics):
        """Store metrics for historical analysis"""
        self.hourly_metrics.append({
            'timestamp': datetime.now(),
            'metrics': metrics.copy()
        })
        
        # Keep only last 24 hours of data
        cutoff = datetime.now() - timedelta(hours=24)
        self.hourly_metrics = [
            m for m in self.hourly_metrics
            if m['timestamp'] > cutoff
        ]
    
    def _assess_continuous_work(self):
        """Assess risk based on time since last break"""
        minutes_since_break = (
            datetime.now() - self.last_break
        ).total_seconds() / 60
        
        if minutes_since_break > self.THRESHOLDS['continuous_work']:
            return 'high'
        elif minutes_since_break > self.THRESHOLDS['continuous_work'] / 2:
            return 'medium'
        return 'low'
    
    def _assess_activity_levels(self, metrics):
        """Assess risk based on current activity levels"""
        # Calculate hourly rates
        hours = metrics['screen_time'] / 60
        if hours == 0:
            return 'low'
        
        hourly_clicks = metrics['mouse_clicks'] / hours
        hourly_keys = metrics['key_presses'] / hours
        
        if (hourly_clicks > self.THRESHOLDS['high_activity']['mouse_clicks'] or
            hourly_keys > self.THRESHOLDS['high_activity']['key_presses']):
            return 'high'
        elif (hourly_clicks > self.THRESHOLDS['high_activity']['mouse_clicks'] / 2 or
              hourly_keys > self.THRESHOLDS['high_activity']['key_presses'] / 2):
            return 'medium'
        return 'low'
    
    def _analyze_patterns(self):
        """Analyze patterns in historical data"""
        if len(self.hourly_metrics) < 2:
            return 'low'
        
        try:
            # Look for increasing trends in activity
            recent_clicks = [m['metrics']['mouse_clicks'] for m in self.hourly_metrics[-3:]]
            recent_keys = [m['metrics']['key_presses'] for m in self.hourly_metrics[-3:]]
            
            clicks_trend = np.polyfit(range(len(recent_clicks)), recent_clicks, 1)[0]
            keys_trend = np.polyfit(range(len(recent_keys)), recent_keys, 1)[0]
            
            if clicks_trend > 0 and keys_trend > 0:
                return 'high'
            elif clicks_trend > 0 or keys_trend > 0:
                return 'medium'
            return 'low'
            
        except Exception as e:
            logger.warning(f"Error analyzing patterns: {str(e)}")
            return 'low'
    
    def _calculate_overall_risk(self, risk_factors):
        """Calculate overall risk level from individual factors"""
        risk_levels = {
            'high': 3,
            'medium': 2,
            'low': 1,
            'unknown': 0
        }
        
        # Convert risk factors to numerical values
        risk_values = [risk_levels[r] for r in risk_factors]
        avg_risk = np.mean(risk_values)
        
        if avg_risk >= 2.5:
            return 'high'
        elif avg_risk >= 1.5:
            return 'medium'
        return 'low'
    
    def _generate_recommendations(self, continuous_risk, activity_risk, pattern_risk):
        """Generate personalized recommendations based on risk factors"""
        recommendations = []
        
        if continuous_risk == 'high':
            recommendations.append(
                "Take a break! You've been working continuously for too long."
            )
        elif continuous_risk == 'medium':
            recommendations.append(
                "Consider taking a short break in the next 30 minutes."
            )
        
        if activity_risk == 'high':
            recommendations.append(
                "Your activity level is very high. Try to pace yourself and take regular breaks."
            )
        elif activity_risk == 'medium':
            recommendations.append(
                "Your activity level is increasing. Remember to maintain a sustainable pace."
            )
        
        if pattern_risk == 'high':
            recommendations.append(
                "Your work intensity has been increasing. Consider adjusting your workload."
            )
        
        # Add general recommendations if no specific ones were generated
        if not recommendations:
            recommendations.append(
                "Maintain regular breaks and monitor your energy levels."
            )
        
        return recommendations
