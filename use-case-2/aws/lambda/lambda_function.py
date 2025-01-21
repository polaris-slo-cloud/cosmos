import json
import boto3

# Initialize the Glue client
glue_client = boto3.client('glue')

# Glue job details
GLUE_JOB_NAME = 'UseCase2GlueJob'

def lambda_handler(event, context):
    try:

        # Start the Glue ETL job
        response = start_glue_job()

        return {
            'statusCode': 200,
            'body': json.dumps('ETL process triggered successfully. Glue Job ID: ' + response['JobRunId'])
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error triggering ETL: {str(e)}')
        }

def start_glue_job():
    # Trigger the Glue job
    response = glue_client.start_job_run(JobName=GLUE_JOB_NAME)
    return response
