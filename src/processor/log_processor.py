from typing import Dict, Any
from datetime import datetime

class LogProcessor:
    def __init__(self):
        pass

    def process_log(self, error_log: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process the error log and extract relevant information.
        """
        try:
            # Extract key information from the error log
            processed_log = {
                "original_log": error_log,
                "processed_timestamp": datetime.utcnow().isoformat(),
                "log_type": self._determine_log_type(error_log),
                "severity": self._determine_severity(error_log),
                "context": {
                    "application": error_log["contextualMetadata"]["applicationName"],
                    "environment": error_log["contextualMetadata"]["environment"],
                    "host": error_log["contextualMetadata"]["affectedHost"],
                    "source_agent": f"{error_log['sourceAgent']['name']} v{error_log['sourceAgent']['version']}"
                },
                "anomaly_details": {
                    "reason": error_log["anomalyDetectionResults"]["reason"],
                    "score": error_log["anomalyDetectionResults"]["score"],
                    "notes": error_log["anomalyDetectionResults"]["notes"],
                    "matched_patterns": error_log["anomalyDetectionResults"].get("matchedPatterns", [])
                },
                "log_details": {
                    "original_line": error_log["logEntry"]["originalLine"],
                    "timestamp": error_log["logEntry"]["timestamp"],
                    "level": error_log["logEntry"]["level"],
                    "message": error_log["logEntry"].get("message", "")
                }
            }
            return processed_log
        except Exception as e:
            raise Exception(f"Error processing log: {str(e)}")

    def _determine_log_type(self, error_log: Dict[str, Any]) -> str:
        """
        Determine the type of log based on its content.
        """
        # Use the log level as the primary type indicator
        log_level = error_log["logEntry"]["level"].upper()
        if log_level in ["ERROR", "CRITICAL"]:
            return "error"
        elif log_level == "WARNING":
            return "warning"
        elif log_level == "INFO":
            return "info"
        return "unknown"

    def _determine_severity(self, error_log: Dict[str, Any]) -> str:
        """
        Determine the severity of the error based on anomaly score and log level.
        """
        anomaly_score = error_log["anomalyDetectionResults"]["score"]
        log_level = error_log["logEntry"]["level"].upper()
        
        if log_level in ["CRITICAL"] or anomaly_score >= 0.8:
            return "critical"
        elif log_level in ["ERROR"] or anomaly_score >= 0.6:
            return "high"
        elif log_level in ["WARNING"] or anomaly_score >= 0.4:
            return "medium"
        return "low" 