from typing import Dict, Any
import os
from google.cloud import aiplatform
from vertexai.generative_models import GenerativeModel

class GenAIAgent:
    def __init__(self):
        # Load the Vertex AI API key from the JSON file
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/anish/RemediationAgent/orbit-460719-c8e358a7f170.json"
        # Initialize Vertex AI with the correct project ID and location
        aiplatform.init(project="orbit-460719", location="us-central1")
        # Use the Gemini model
        self.model = GenerativeModel("gemini-2.0-flash-lite-001")

    def get_remediation(self, processed_log: Dict[str, Any]) -> str:
        """
        Generate remediation steps based on the processed error log.
        """
        try:
            prompt = self._construct_prompt(processed_log)
            response = self.model.generate_content(prompt)
            remediation = response.text.strip()
            print(f"Generated Remediation:\n{remediation}")
            return remediation
        except Exception as e:
            error_msg = str(e)
            print(f"Full error: {error_msg}")  # Print full error for debugging
            raise Exception(f"Error generating remediation: {error_msg}")

    def _construct_prompt(self, processed_log: Dict[str, Any]) -> str:
        """
        Construct a detailed prompt for the AI based on the processed log.
        """
        context = processed_log["context"]
        anomaly = processed_log["anomaly_details"]
        log = processed_log["log_details"]
        
        return f"""You are an expert system administrator and developer. Your task is to provide a concise, actionable remediation plan for the following error message:

ERROR MESSAGE:
"{log['message']}"

Context:
- Application: {context['application']}
- Environment: {context['environment']}
- Affected Host: {context['host']}
- Source Agent: {context['source_agent']}

Anomaly Detection:
- Reason: {anomaly['reason']}
- Anomaly Score: {anomaly['score']}
- Additional Notes: {anomaly['notes']}
- Matched Patterns: {', '.join(anomaly['matched_patterns']) if anomaly['matched_patterns'] else 'None'}

Please provide:
1. Step-by-step remediation instructions (max 3 steps)
2. Preventive measures (max 2 points)
3. How to verify that the issue is resolved (max 2 points)

Be concise, direct, and practical. Only include information relevant to the error message above.""" 