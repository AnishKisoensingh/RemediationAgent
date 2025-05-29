import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/anish/RemediationAgent/orbit-460719-40dfab18b8b4.json"
from google.cloud import firestore
import logging

class FirestoreService:
    def __init__(self):
        try:
            self.db = firestore.Client(project="orbit-460719")
        except Exception as e:
            logging.error(f"Failed to initialize Firestore client: {str(e)}")
            raise

    def store_error(self, error_log, remediation):
        """Store error log and remediation in Firestore."""
        try:
            error_hash = self._hash_error_log(error_log)
            doc_ref = self.db.collection("errors").document()
            doc_ref.set({
                "error_log": error_log,
                "remediation": remediation,
                "error_hash": error_hash,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            return doc_ref.id
        except Exception as e:
            logging.error(f"Failed to store error in Firestore: {str(e)}")
            raise

    def get_remediation(self, error_log):
        """Retrieve remediation from Firestore if the error exists."""
        try:
            error_hash = self._hash_error_log(error_log)
            query = self.db.collection("errors").where(
                filter=firestore.FieldFilter("error_hash", "==", error_hash)
            ).limit(1)
            docs = query.get()
            if docs:
                return docs[0].to_dict()["remediation"]
            return None
        except Exception as e:
            logging.error(f"Failed to get remediation from Firestore: {str(e)}")
            raise

    def _hash_error_log(self, error_log):
        """Generate a unique hash for the error log."""
        import hashlib
        error_str = str(error_log)
        return hashlib.md5(error_str.encode()).hexdigest() 