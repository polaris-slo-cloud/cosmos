import json
import boto3
import csv
import io

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('runtime.sagemaker')

def lambda_handler(event, context):
    # Parse the request body to get input parameters
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        # If no body, assume the input is directly in the event (for testing purposes)
        body = event

    # Extract the relevant parameters from the API request
    input_data = [
        body['area'],
        body['bedrooms'],
        body['bathrooms'],
        body['stories'],
        body['mainroad'],
        body['guestroom'],
        body['basement'],
        body['hotwaterheating'],
        body['airconditioning'],
        body['parking'],
        body['prefarea'],
        body['furnishingstatus']
    ]

    # Convert the input data to the format expected by SageMaker
    output = io.StringIO()
    csv_writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(input_data)

    # Get the CSV data as a string
    csv_data = output.getvalue()

    # Invoke the SageMaker endpoint
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName='useCase3SageMakerEndpoint',
        ContentType='text/csv',
        Body=csv_data
    )

    # Get the result from the SageMaker response
    result = json.loads(response['Body'].read().decode())

    # Return the predicted price in the response
    return {
        'statusCode': 200,
        'body': json.dumps({
            'predicted_price': result
        })
    }
