import functions_framework
from google.cloud import aiplatform

# Set configuration variables
PROJECT_ID = "total-fiber-439913-f1"
REGION = "europe-west3"
ENDPOINT_ID = "9074388211291127808"

# Initialize the Vertex AI client once
aiplatform.init(project=PROJECT_ID, location=REGION)
endpoint = aiplatform.Endpoint(endpoint_name=ENDPOINT_ID)

@functions_framework.http
def predict_house_price(request):

    # Parse the JSON input
    data = request.get_json(silent=True)
    if not data:
        return {"error": "Invalid input: JSON data required"}, 400


    # Create instances payload
    instances = [data]

    try:
        # Make prediction
        prediction = endpoint.predict(instances=instances)
        predicted_price = prediction.predictions[0]  # Get the first prediction result
        return {"predicted_price": predicted_price}, 200
    except Exception as e:
        return {"error": str(e)}, 500
