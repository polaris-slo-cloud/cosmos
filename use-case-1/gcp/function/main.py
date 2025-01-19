import functions_framework
from google.cloud import firestore, storage
from flask import jsonify

# Initialize Firestore and Storage clients
db = firestore.Client()
storage_client = storage.Client()

firestore_table = "users"
cloud_storage_bucket = "usecase1cloudstorage"


@functions_framework.http
def useCase1(request):
    """HTTP Cloud Function to retrieve a Firestore document and include an image URL from Cloud Storage."""
    try:
        # Parse the user ID from the HTTP request parameters
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({"error": "User ID not provided"}), 400

        # Specify the user_id as the name of the picture (from Firestore)
        doc_ref = db.collection(firestore_table).document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()

            # Use the user_id as the filename in Cloud Storage
            file_name = f"{user_id}.png"  # Assuming files are stored as <userId>.jpg

            # Get the bucket and blob reference
            bucket = storage_client.bucket(cloud_storage_bucket)
            blob = bucket.blob(file_name)
            image_url = blob.public_url

            # Add the image URL to the response data
            data['image_url'] = image_url

            return jsonify(data), 200
        else:
            return jsonify({"error": "Document not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
