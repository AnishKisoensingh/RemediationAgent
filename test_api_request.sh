#!/bin/bash

# Test case 1: Security breach
echo "Testing security breach remediation..."
curl -X POST http://localhost:8000/remediate \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "test-security-1",
    "eventTimestamp": "2025-05-29T05:45:24.644650+00:00",
    "sourceAgent": {
      "name": "AnomalyDetectionAgent",
      "version": "1.0.0"
    },
    "logEntry": {
      "originalLine": "2025-05-28 22:45:24 CRITICAL: Security breach detected from 172.16.0.10",
      "timestamp": "2025-05-28T22:45:24Z",
      "level": "CRITICAL",
      "message": "Security breach detected from 172.16.0.10"
    },
    "anomalyDetectionResults": {
      "reason": "Contains known anomaly pattern (keyword match)",
      "score": -1.0,
      "notes": "This log contains ERROR/CRITICAL level message",
      "matchedPatterns": []
    },
    "contextualMetadata": {
      "applicationName": "GenericApplication",
      "environment": "development",
      "affectedHost": "UnknownHost"
    }
  }'

echo -e "\n\nTest case 2: Database crash..."
curl -X POST http://localhost:8000/remediate \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "test-db-1",
    "eventTimestamp": "2025-05-29T05:45:25.644650+00:00",
    "sourceAgent": {
      "name": "AnomalyDetectionAgent",
      "version": "1.0.0"
    },
    "logEntry": {
      "originalLine": "2025-05-28 22:45:25 ERROR: Fatal: System crash detected in database",
      "timestamp": "2025-05-28T22:45:25Z",
      "level": "ERROR",
      "message": "Fatal: System crash detected in database"
    },
    "anomalyDetectionResults": {
      "reason": "Contains known anomaly pattern (keyword match)",
      "score": -1.0,
      "notes": "This log contains ERROR/CRITICAL level message",
      "matchedPatterns": []
    },
    "contextualMetadata": {
      "applicationName": "DatabaseService",
      "environment": "production",
      "affectedHost": "db-01"
    }
  }'

echo -e "\n\nTest case 3: Memory overflow..."
curl -X POST http://localhost:8000/remediate \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "test-memory-1",
    "eventTimestamp": "2025-05-29T05:45:26.644650+00:00",
    "sourceAgent": {
      "name": "AnomalyDetectionAgent",
      "version": "1.0.0"
    },
    "logEntry": {
      "originalLine": "2025-05-28 22:45:26 ERROR: Memory overflow in webserver - system unstable",
      "timestamp": "2025-05-28T22:45:26Z",
      "level": "ERROR",
      "message": "Memory overflow in webserver - system unstable"
    },
    "anomalyDetectionResults": {
      "reason": "Contains known anomaly pattern (keyword match)",
      "score": -1.0,
      "notes": "This log contains ERROR/CRITICAL level message",
      "matchedPatterns": []
    },
    "contextualMetadata": {
      "applicationName": "WebServer",
      "environment": "production",
      "affectedHost": "web-01"
    }
  }'

echo -e "\n\nTest case 4: Unknown error..."
curl -X POST http://localhost:8000/remediate \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "test-unknown-1",
    "eventTimestamp": "2025-05-29T05:45:27.644650+00:00",
    "sourceAgent": {
      "name": "AnomalyDetectionAgent",
      "version": "1.0.0"
    },
    "logEntry": {
      "originalLine": "2025-05-28 22:45:27 WARNING: Unusual pattern detected in system logs",
      "timestamp": "2025-05-28T22:45:27Z",
      "level": "WARNING",
      "message": "Unusual pattern detected in system logs"
    },
    "anomalyDetectionResults": {
      "reason": "Unknown pattern detected",
      "score": 0.5,
      "notes": "This log contains an unusual pattern",
      "matchedPatterns": []
    },
    "contextualMetadata": {
      "applicationName": "SystemMonitor",
      "environment": "production",
      "affectedHost": "monitor-01"
    }
  }' 