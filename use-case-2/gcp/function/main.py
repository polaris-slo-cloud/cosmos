import functions_framework
from googleapiclient.discovery import build
from google.oauth2 import service_account
import logging


# Google Cloud Project and Job details
PROJECT_ID = "total-fiber-439913-f1"
JOB_ID = "2024-11-03_05_31_59-17617496085829078179"
REGION = "europe-west10"

@functions_framework.http
def trigger_dataflow_job(request):
    try:
        # Initialize Dataflow API client
        dataflow_service = build("dataflow", "v1b3")
        logging.info("Dataflow API client initialized successfully.")

        # Construct the Dataflow job request
        job_response = dataflow_service.projects().locations().jobs().get(
            projectId=PROJECT_ID,
            location=REGION,
            jobId=JOB_ID
        ).execute()
        logging.info(f"Job status retrieved successfully: {job_response}")

        # Return the job status
        return {"status": "success", "job_state": job_response.get("currentState")}, 200

    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return {"status": "error", "message": str(e)}, 500

