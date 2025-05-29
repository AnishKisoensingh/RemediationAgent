from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
from typing import Dict, Any, Optional
import logging
from database.sqlite_service import SQLiteService
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
db = SQLiteService()

class ErrorLog(BaseModel):
    event_id: str = Field(alias="eventId")
    timestamp: str = Field(alias="eventTimestamp")
    source_agent: Dict[str, Any] = Field(alias="sourceAgent")
    log_entry: Dict[str, Any] = Field(alias="logEntry")
    anomaly_detection: Dict[str, Any] = Field(alias="anomalyDetectionResults")
    contextual_metadata: Dict[str, Any] = Field(alias="contextualMetadata")

    model_config = ConfigDict(populate_by_name=True)

def generate_remediation(error_log: ErrorLog) -> Dict[str, Any]:
    """Generate comprehensive, context-aware remediation based on error type."""
    message = error_log.log_entry.get("message", "").lower()
    level = error_log.log_entry.get("level", "").upper()
    app_name = error_log.contextual_metadata.get("applicationName", "unknown")
    host = error_log.contextual_metadata.get("affectedHost", "unknown")

    # Security breach remediation
    if "security breach" in message:
        ip = message.split("from")[-1].strip()
        return {
            "action": "block_ip",
            "parameters": {
                "ip_address": ip,
                "duration": 3600
            },
            "description": f"Block IP address {ip} due to security breach detection on {host}.",
            "steps": [
                f"1. Use your firewall to block the IP address {ip}.",
                "2. Review system and application logs for any other suspicious activity from this IP.",
                "3. Notify the security team and document the incident.",
                "4. Update firewall rules to prevent future access from this IP."
            ],
            "preventive_measures": [
                "Enable and regularly update intrusion detection systems.",
                "Regularly review and update firewall rules.",
                "Educate users about phishing and social engineering attacks."
            ],
            "verification": [
                f"Run 'sudo iptables -L' or equivalent to verify {ip} is blocked.",
                "Monitor logs for any further attempts from the blocked IP."
            ]
        }

    # Database issues
    elif "database" in message:
        if "connection failed" in message:
            return {
                "action": "restart_database",
                "parameters": {
                    "service_name": "database",
                    "wait_time": 60
                },
                "description": f"Restart the database service on {host} due to connection failure.",
                "steps": [
                    "1. Check the database service status using 'systemctl status <service>' or equivalent.",
                    "2. Restart the database service using 'systemctl restart <service>' or equivalent.",
                    "3. Wait 60 seconds and verify the service is running.",
                    "4. Check application connectivity to the database."
                ],
                "preventive_measures": [
                    "Monitor database resource usage and set up alerts for failures.",
                    "Ensure regular database backups are scheduled.",
                    "Test failover and recovery procedures periodically."
                ],
                "verification": [
                    "Verify the database service is active and running.",
                    "Check application logs to confirm successful reconnection."
                ]
            }
        elif "crash" in message:
            return {
                "action": "restore_database",
                "parameters": {
                    "backup_id": "latest",
                    "verify_after_restore": True
                },
                "description": f"Restore the database on {host} from the latest backup due to crash.",
                "steps": [
                    "1. Identify the latest valid backup.",
                    "2. Stop the database service.",
                    "3. Restore the database from the backup.",
                    "4. Start the database service.",
                    "5. Verify data integrity and application connectivity."
                ],
                "preventive_measures": [
                    "Schedule regular automated backups.",
                    "Test backup restoration procedures regularly.",
                    "Monitor for early signs of database corruption or instability."
                ],
                "verification": [
                    "Check that the database service is running.",
                    "Run integrity checks and verify application access."
                ]
            }

    # Memory issues
    elif "memory overflow" in message:
        service = "webserver" if "webserver" in message else "mailserver"
        return {
            "action": "scale_resources",
            "parameters": {
                "service_name": service,
                "memory_increase": "2x",
                "restart_after_scale": True
            },
            "description": f"Increase memory allocation for {service} on {host} due to overflow.",
            "steps": [
                f"1. Check current memory usage on {host} using 'free -m' or 'top'.",
                f"2. Increase memory allocation for {service} (e.g., update container or VM settings).",
                f"3. Restart the {service} service to apply changes.",
                "4. Monitor the service for stability after restart."
            ],
            "preventive_measures": [
                "Set up memory usage alerts for critical services.",
                "Optimize application code to reduce memory leaks.",
                "Regularly review and adjust resource allocations."
            ],
            "verification": [
                f"Monitor memory usage on {host} to ensure it remains within limits.",
                f"Check {service} logs for any further memory-related errors."
            ]
        }

    # Default remediation for unknown errors
    return {
        "action": "investigate_error",
        "parameters": {
            "error_level": level,
            "service_name": app_name
        },
        "description": f"Manual investigation required for unknown error type on {host}.",
        "steps": [
            "1. Review the error message and related logs.",
            "2. Check the health and status of affected services.",
            "3. Escalate to the appropriate team if necessary."
        ],
        "preventive_measures": [
            "Implement comprehensive monitoring and alerting.",
            "Document all incidents and resolutions for future reference."
        ],
        "verification": [
            "Confirm the issue is resolved and services are operational.",
            "Monitor for recurrence of the error."
        ]
    }

@app.post("/remediate")
async def remediate_error(error_log: ErrorLog):
    try:
        # Log the incoming request
        logger.info("=" * 80)
        logger.info("Incoming API Request:")
        logger.info(json.dumps(error_log.dict(), indent=2))
        logger.info("=" * 80)

        # Extract essential data for storage
        essential_data = {
            "message": error_log.log_entry.get("message"),
            "level": error_log.log_entry.get("level")
        }

        # Check if we have a stored remediation for this error
        stored_remediation = db.get_remediation(essential_data)
        
        if stored_remediation:
            logger.info("Found existing remediation in database")
            logger.info("Remediation returned to client (from database):")
            logger.info(json.dumps(stored_remediation, indent=2))
            return {
                "status": "success",
                "message": "Retrieved stored remediation",
                "source": "database",
                "remediation": stored_remediation
            }
        
        # If no stored remediation, generate a new one
        logger.info("No existing remediation found, generating new remediation")
        remediation = generate_remediation(error_log)
        logger.info("Remediation returned to client (from agent):")
        logger.info(json.dumps(remediation, indent=2))
        
        # Store only essential data and remediation
        db.store_error(essential_data, remediation)
        
        return {
            "status": "success",
            "message": "Generated new remediation",
            "source": "agent",
            "remediation": remediation
        }
        
    except Exception as e:
        logger.error(f"Error in remediation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 