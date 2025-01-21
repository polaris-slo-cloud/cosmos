import json
import boto3
from boto3.dynamodb.conditions import Key

# Initialize the DynamoDB resource and S3 client
dynamodb = boto3.resource('dynamodb')
s3_client = boto3.client('s3')

# Define the DynamoDB table name and S3 bucket name
TABLE_NAME = 'useCase2DynamoDbUserData'
BUCKET_NAME = 'usecase1s3bucket'

def lambda_handler(event, context):
    # Extract UserID from the event
    user_id = event['queryStringParameters']['userID']

    # Fetch user data from DynamoDB
    user_data = get_user_data(user_id)

    if not user_data:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found (data)')
        }

    # Fetch media URLs from S3 (assuming media files are public)
    media_urls = get_media_urls(user_id)

    if not media_urls:
        return {
            'statusCode': 404,
            'body': json.dumps('User not found (profile picture)')
        }

    # Construct the response
    response = {
        'userID': user_id,
        'userData': user_data,
        'mediaURLs': media_urls
    }

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }

def get_user_data(user_id):
    table = dynamodb.Table(TABLE_NAME)

    try:
        # Query DynamoDB to get the user data by UserID
        response = table.get_item(Key={'UserID': user_id})
        return response.get('Item', None)
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None

def get_media_urls(user_id):
    try:
        # List objects in the S3 bucket
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME, Prefix=f"{user_id}.png")
        if 'Contents' not in response:
            return []

        # Construct the URLs for each media file
        media_urls = [
            f"https://{BUCKET_NAME}.s3.amazonaws.com/{item['Key']}"
            for item in response['Contents']
        ]
        return media_urls
    except Exception as e:
        print(f"Error fetching media URLs: {e}")
        return []
