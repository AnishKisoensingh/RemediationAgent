# Remediation Agent API

This API provides automated remediation suggestions for system errors using AI.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

## Running the FastAPI Server

1. Activate your virtual environment:
   ```bash
   source .venv/bin/activate
   ```
2. Start the server with the correct Python path:
   ```bash
   PYTHONPATH=src uvicorn api.app:app --reload
   ```

- The API will be available at http://localhost:8000
- You can test the endpoint using:
   ```bash
   ./test_api_request.sh
   ```

## API Usage

Send a POST request to `/remediate` with your error log in JSON format:

```bash
curl -X POST "http://localhost:8000/remediate" \
     -H "Content-Type: application/json" \
     -d '{"error_log": {"your": "error log data"}}'
```

The API will return a JSON response with remediation steps.

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for interactive API documentation.