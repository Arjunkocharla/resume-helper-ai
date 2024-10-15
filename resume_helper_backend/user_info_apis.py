import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import firebase_admin
from firebase_admin import credentials, auth, firestore
from b2sdk.v2 import InMemoryAccountInfo, B2Api
import boto3
from botocore.client import Config
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate(json.loads(os.getenv('FIREBASE_CONFIG')))
firebase_admin.initialize_app(cred)

db = firestore.client()

# Initialize B2 API
info = InMemoryAccountInfo()
b2_api = B2Api(info)
b2_api.authorize_account("production", os.getenv('B2_KEY_ID'), os.getenv('B2_APPLICATION_KEY'))
bucket = b2_api.get_bucket_by_name(os.getenv('B2_BUCKET_NAME'))

# S3 client for generating pre-signed URLs
s3_client = boto3.client(
    's3',
    endpoint_url=os.getenv('B2_ENDPOINT'),
    aws_access_key_id=os.getenv('B2_KEY_ID'),
    aws_secret_access_key=os.getenv('B2_APPLICATION_KEY'),
    config=Config(signature_version='s3v4')
)

# Middleware to verify Firebase ID token
def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        id_token = request.headers.get('Authorization')
        if not id_token:
            return jsonify({"error": "No token provided"}), 401
        try:
            id_token = id_token.split('Bearer ')[1]
            decoded_token = auth.verify_id_token(id_token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({"error": str(e)}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/user/profile', methods=['GET'])
@verify_token
def get_user_profile():
    uid = request.user['uid']
    user_doc = db.collection('user_info').document(uid).get()
    if user_doc.exists:
        return jsonify(user_doc.to_dict()), 200
    else:
        return jsonify({"error": "User profile not found"}), 404

@app.route('/api/user/profile', methods=['PUT'])
@verify_token
def update_user_profile():
    uid = request.user['uid']
    user_data = request.json
    db.collection('user_info').document(uid).set(user_data, merge=True)
    return jsonify({"message": "Profile updated successfully"}), 200

@app.route('/api/user/resume', methods=['POST'])
@verify_token
def upload_resume():
    uid = request.user['uid']
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        try:
            file_data = file.read()
            file_name = f"{uid}/{file.filename}"
            file_info = bucket.upload_bytes(file_data, file_name)
            
            resume_data = {
                "fileId": file_info.id_,
                "fileName": file.filename,
                "uploadDate": firestore.SERVER_TIMESTAMP,
                "fileSize": len(file_data),
                "fileType": os.path.splitext(file.filename)[1][1:]
            }
            
            # Update the resume_info document
            db.collection('user_info').document(uid).set({
                'resume_info': firestore.ArrayUnion([resume_data])
            }, merge=True)
            
            return jsonify({"message": "Resume uploaded successfully", "resumeId": file_info.id_}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.route('/api/user/resumes', methods=['GET'])
@verify_token
def get_user_resumes():
    uid = request.user['uid']
    user_doc = db.collection('user_info').document(uid).get()
    if user_doc.exists:
        user_data = user_doc.to_dict()
        resumes = user_data.get('resume_info', [])
        return jsonify(resumes), 200
    else:
        return jsonify({"error": "User profile not found"}), 404

@app.route('/api/user/resume/<resume_id>', methods=['GET'])
@verify_token
def get_resume_download_url(resume_id):
    uid = request.user['uid']
    user_doc = db.collection('user_info').document(uid).get()
    if not user_doc.exists:
        return jsonify({"error": "User profile not found"}), 404
    
    user_data = user_doc.to_dict()
    resumes = user_data.get('resume_info', [])
    resume_data = next((resume for resume in resumes if resume['fileId'] == resume_id), None)
    
    if not resume_data:
        return jsonify({"error": "Resume not found"}), 404
    
    try:
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': os.getenv('B2_BUCKET_NAME'),
                'Key': f"{uid}/{resume_data['fileName']}"
            },
            ExpiresIn=3600  # URL expires in 1 hour
        )
        return jsonify({
            "download_url": presigned_url,
            "file_name": resume_data['fileName'],
            "expires_in": 3600
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/resume/<resume_id>', methods=['DELETE'])
@verify_token
def delete_resume(resume_id):
    uid = request.user['uid']
    try:
        user_doc = db.collection('user_info').document(uid).get()
        if not user_doc.exists:
            return jsonify({"error": "User profile not found"}), 404
        
        user_data = user_doc.to_dict()
        resumes = user_data.get('resume_info', [])
        resume_to_delete = next((resume for resume in resumes if resume['fileId'] == resume_id), None)
        
        if not resume_to_delete:
            return jsonify({"error": "Resume not found"}), 404
        
        # Delete from B2
        bucket.delete_file_version(resume_id)
        
        # Remove from Firestore
        updated_resumes = [resume for resume in resumes if resume['fileId'] != resume_id]
        db.collection('user_info').document(uid).update({
            'resume_info': updated_resumes
        })
        
        return jsonify({"message": "Resume deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
