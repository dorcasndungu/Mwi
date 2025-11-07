from flask import Flask, request, render_template, send_file, jsonify, Response, stream_with_context
import requests
import re
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import logging
import sys
import time
import json

# Configure logging
# Use INFO level in production, DEBUG in development
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(
    level=getattr(logging, log_level, logging.INFO),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("=" * 50)
logger.info("Starting Mwi Photo Extractor Application...")
logger.info("=" * 50)
logger.info(f"Python version: {sys.version}")
logger.info(f"Current working directory: {os.getcwd()}")
logger.info(f"Environment variables:")
logger.info(f"  - PORT: {os.environ.get('PORT', 'Not set')}")
logger.info(f"  - LOG_LEVEL: {log_level}")
logger.info(f"  - SECRET_KEY: {'Set' if os.environ.get('SECRET_KEY') else 'Using default (change in production!)'}")

# Try to import face recognition libraries, fall back to demo mode if not available
FACE_RECOGNITION_AVAILABLE = False
FACE_RECOGNITION_ERROR = None

try:
    import face_recognition
    import cv2
    import numpy as np
    FACE_RECOGNITION_AVAILABLE = True
    logger.info("✅ Real face recognition libraries loaded successfully!")
    logger.info("   - face_recognition: Available")
    logger.info("   - OpenCV: Available")
    logger.info("   - NumPy: Available")
except ImportError as e:
    FACE_RECOGNITION_ERROR = str(e)
    logger.warning("⚠️  Face recognition libraries not available")
    logger.warning(f"   Error: {e}")
    logger.info("🔄 Running in DEMO mode - will simulate face matching")
    logger.info("   Note: App will still function, but face matching will be simulated")
    import random

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Add configuration for face recognition settings
FACE_RECOGNITION_CONFIG = {
    'enabled': FACE_RECOGNITION_AVAILABLE,
    'tolerance': 0.5,  # Lower is stricter matching
    'min_face_distance': 0.5,  # Maximum allowed face distance
    'demo_mode': not FACE_RECOGNITION_AVAILABLE
}

# Simple health check endpoint
@app.route('/health')
def health_check():
    logger.info("Health check endpoint called")
    return "OK", 200

# Status endpoint to check face recognition availability
@app.route('/api/status')
def api_status():
    """Return application status including face recognition availability."""
    status = {
        'status': 'running',
        'face_recognition': {
            'available': FACE_RECOGNITION_CONFIG['enabled'],
            'demo_mode': FACE_RECOGNITION_CONFIG['demo_mode'],
            'error': FACE_RECOGNITION_ERROR if not FACE_RECOGNITION_AVAILABLE else None
        },
        'version': '1.0.0'
    }
    return jsonify(status), 200

# Root endpoint that also serves as a health check
@app.route('/')
def index():
    logger.info("Index endpoint called")
    return render_template('index.html')

def check_folder_sharing(folder_id):
    """Check if a Google Drive folder is publicly accessible."""
    try:
        # Try to access the folder
        folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        response = requests.get(folder_url)
        
        # Check if we got access denied
        if "Access denied" in response.text or "You need permission" in response.text:
            return False, "This folder is not publicly accessible. Please make sure the folder is shared with 'Anyone with the link can view'."
        
        # Check if we can see any files
        file_pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
        file_ids = re.findall(file_pattern, response.text)
        
        if not file_ids:
            return False, "No files found in this folder or the folder is empty."
        
        return True, "Folder is accessible and contains files."
        
    except Exception as e:
        logger.error(f"Error checking folder sharing: {str(e)}")
        return False, f"Error accessing the folder: {str(e)}"

@app.route('/process', methods=['POST'])
def process_photos():
    """Process photos with streaming Server-Sent Events (SSE) response."""
    logger.info("Processing photos endpoint called")
    
    # Check if selfie file is present
    if 'selfie' not in request.files:
        logger.error("No selfie file in request")
        return jsonify({'error': 'No selfie file uploaded'}), 400
    
    selfie_file = request.files['selfie']
    if selfie_file.filename == '':
        logger.error("Empty selfie filename")
        return jsonify({'error': 'No selfie file selected'}), 400
    
    # Check if drive link is present
    drive_link = request.form.get('drive_link')
    if not drive_link:
        logger.error("No drive link provided")
        return jsonify({'error': 'No Google Drive link provided'}), 400
    
    def generate():
        """Generator function for streaming Server-Sent Events."""
        try:
            # Extract folder ID and check sharing status
            folder_id = extract_folder_id(drive_link)
            if not folder_id:
                yield f"data: {json.dumps({'error': 'Invalid Google Drive folder link'})}\n\n"
                return
            
            # Check folder sharing status
            is_accessible, message = check_folder_sharing(folder_id)
            if not is_accessible:
                yield f"data: {json.dumps({'error': message})}\n\n"
                return
            
            # Save the selfie temporarily
            selfie_filename = secure_filename(selfie_file.filename)
            selfie_path = os.path.join(app.config['UPLOAD_FOLDER'], selfie_filename)
            selfie_file.save(selfie_path)
            logger.info(f"Selfie saved to {selfie_path}")

            # Load and encode the selfie face
            if FACE_RECOGNITION_CONFIG['enabled']:
                try:
                    selfie_image = face_recognition.load_image_file(selfie_path)
                    selfie_encodings = face_recognition.face_encodings(selfie_image)
                    
                    if not selfie_encodings:
                        yield f"data: {json.dumps({'error': 'No face detected in the selfie. Please upload a clear photo of your face.'})}\n\n"
                        os.remove(selfie_path)
                        return
                    
                    selfie_encoding = selfie_encodings[0]
                    logger.info("Selfie face encoded successfully")
                except Exception as e:
                    logger.error(f"Error processing selfie: {str(e)}")
                    yield f"data: {json.dumps({'error': 'Error processing selfie image. Please try a different photo.'})}\n\n"
                    if os.path.exists(selfie_path):
                        os.remove(selfie_path)
                    return
            else:
                # Demo mode - simulate face encoding
                selfie_encoding = [random.random() for _ in range(128)]
                logger.info("Running in demo mode - using simulated face encoding")
            
            # Get list of files from Google Drive
            drive_files = list_drive_files(folder_id)
            if not drive_files:
                yield f"data: {json.dumps({'error': 'No image files found in the specified Google Drive folder'})}\n\n"
                os.remove(selfie_path)
                return
            
            logger.info(f"Found {len(drive_files)} files in the Drive folder")
            
            # Create a temporary directory for matching photos
            temp_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_matches')
            os.makedirs(temp_dir, exist_ok=True)
            
            matching_photos = []
            total_photos = len(drive_files)
            processed_count = 0
            face_detection_errors = 0
            
            # Process each photo
            for file in drive_files:
                if not file['mimeType'].startswith('image/'):
                    continue
                    
                try:
                    # Download the photo
                    photo_path = download_drive_file(file['id'], temp_dir)
                    
                    if FACE_RECOGNITION_CONFIG['enabled']:
                        try:
                            # Load and encode the photo
                            photo_image = face_recognition.load_image_file(photo_path)
                            photo_encodings = face_recognition.face_encodings(photo_image)
                            
                            if not photo_encodings:
                                face_detection_errors += 1
                                logger.warning(f"No faces detected in {file['name']}")
                                # Clean up downloaded file
                                if os.path.exists(photo_path):
                                    os.remove(photo_path)
                                continue
                            
                            # Check if any face in the photo matches the selfie
                            matches = face_recognition.compare_faces(
                                [selfie_encoding], 
                                photo_encodings[0], 
                                tolerance=FACE_RECOGNITION_CONFIG['tolerance']
                            )
                            face_distances = face_recognition.face_distance([selfie_encoding], photo_encodings[0])
                            
                            if matches[0] and face_distances[0] < FACE_RECOGNITION_CONFIG['min_face_distance']:
                                original_name = file['name']
                                new_path = os.path.join(temp_dir, original_name)
                                if os.path.exists(photo_path):
                                    os.rename(photo_path, new_path)
                                matching_photos.append(new_path)
                                logger.info(f"Match found in {original_name} (distance: {face_distances[0]:.2f})")
                            else:
                                # Clean up non-matching photo
                                if os.path.exists(photo_path):
                                    os.remove(photo_path)
                        except Exception as e:
                            logger.error(f"Error processing photo {file['name']}: {str(e)}")
                            if os.path.exists(photo_path):
                                os.remove(photo_path)
                            continue
                    else:
                        # Demo mode - randomly match photos
                        if random.random() < 0.3:  # 30% chance of matching
                            matching_photos.append(photo_path)
                            logger.info(f"Demo mode: Matched {file['name']}")
                        else:
                            # Clean up non-matching photo in demo mode
                            if os.path.exists(photo_path):
                                os.remove(photo_path)
                    
                    processed_count += 1
                    progress = (processed_count / total_photos) * 100
                    logger.info(f"Processed {processed_count}/{total_photos} photos ({progress:.1f}%)")
                    
                    # Send progress update
                    yield f"data: {json.dumps({'progress': progress, 'status': f'Processing photo {processed_count} of {total_photos}'})}\n\n"
                    
                except Exception as e:
                    logger.error(f"Error processing photo {file['name']}: {str(e)}")
                    continue
            
            # Create ZIP file with matching photos
            if matching_photos:
                zip_filename = f"matching_photos_{int(time.time())}.zip"
                zip_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
                
                try:
                    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                        for photo_path in matching_photos:
                            if os.path.exists(photo_path):
                                # Use the original filename in the ZIP
                                arcname = os.path.basename(photo_path)
                                zipf.write(photo_path, arcname)
                    
                    logger.info(f"Created ZIP file with {len(matching_photos)} matching photos")
                    
                    # Clean up temporary files
                    cleanup_temp_files(temp_dir)
                    if os.path.exists(selfie_path):
                        os.remove(selfie_path)
                    
                    # Send final progress update
                    yield f"data: {json.dumps({'progress': 100, 'status': 'Processing complete!', 'download_url': f'/download/{zip_filename}'})}\n\n"
                    
                except Exception as e:
                    logger.error(f"Error creating ZIP file: {str(e)}")
                    yield f"data: {json.dumps({'error': 'Error creating ZIP file'})}\n\n"
            else:
                error_msg = 'No matching photos found'
                if face_detection_errors > 0:
                    error_msg += f'. Note: {face_detection_errors} photos had no detectable faces.'
                yield f"data: {json.dumps({'error': error_msg})}\n\n"
                
                # Clean up
                cleanup_temp_files(temp_dir)
                if os.path.exists(selfie_path):
                    os.remove(selfie_path)
                
        except Exception as e:
            logger.error(f"Error processing photos: {str(e)}")
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    
    # Return streaming response with proper headers for Server-Sent Events
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(
        os.path.join(app.config['UPLOAD_FOLDER'], filename),
        mimetype='application/zip',
        as_attachment=True,
        download_name=filename
    )

def extract_folder_id(drive_link):
    """Extract folder ID from Google Drive link."""
    pattern = r'/folders/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, drive_link)
    return match.group(1) if match else None

def list_drive_files(folder_id):
    """List files in a public Google Drive folder."""
    try:
        # Construct the folder URL
        folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        
        # Get the folder page
        response = requests.get(folder_url)
        response.raise_for_status()
        
        # Extract file IDs from the page
        # Google Drive uses a specific data structure in the page
        file_pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
        file_ids = re.findall(file_pattern, response.text)
        
        # Get file details
        files = []
        for file_id in file_ids:
            # Get file metadata
            file_url = f"https://drive.google.com/file/d/{file_id}/view"
            file_response = requests.get(file_url)
            
            # Check if it's an image
            if any(ext in file_response.text.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                files.append({
                    'id': file_id,
                    'name': f'photo_{file_id}.jpg',  # We'll determine the actual name when downloading
                    'mimeType': 'image/jpeg'  # We'll determine the actual type when downloading
                })
        
        return files
    except Exception as e:
        logger.error(f"Error listing Drive files: {str(e)}")
        return []

def download_drive_file(file_id, save_dir):
    """Download a file from a public Google Drive link."""
    try:
        # Construct the direct download URL
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        
        # Download the file
        response = requests.get(download_url, stream=True)
        response.raise_for_status()
        
        # Determine file type from content-type
        content_type = response.headers.get('content-type', '')
        if 'image' not in content_type:
            raise ValueError(f"Not an image file: {content_type}")
        
        # Determine file extension
        ext = '.jpg'  # default
        if 'png' in content_type:
            ext = '.png'
        elif 'gif' in content_type:
            ext = '.gif'
        
        # Save the file
        file_path = os.path.join(save_dir, f'photo_{file_id}{ext}')
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return file_path
    except Exception as e:
        logger.error(f"Error downloading file {file_id}: {str(e)}")
        raise

def cleanup_temp_files(directory):
    """Clean up temporary files."""
    for file in os.listdir(directory):
        try:
            os.remove(os.path.join(directory, file))
        except Exception as e:
            logger.error(f"Error deleting file {file}: {str(e)}")
    try:
        os.rmdir(directory)
    except Exception as e:
        logger.error(f"Error deleting directory {directory}: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    logger.info(f"Starting Flask development server on port {port}")
    app.run(host='0.0.0.0', port=port)
