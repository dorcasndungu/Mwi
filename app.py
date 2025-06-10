from flask import Flask, request, render_template, send_file, jsonify
import requests
import re
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename
import os
import logging

# Try to import face recognition libraries, fall back to demo mode if not available
try:
    import face_recognition
    import cv2
    import numpy as np
    FACE_RECOGNITION_AVAILABLE = True
    print("✅ Real face recognition libraries loaded successfully!")
except ImportError as e:
    FACE_RECOGNITION_AVAILABLE = False
    print(f"⚠️  Face recognition libraries not available: {e}")
    print("🔄 Running in DEMO mode - will simulate face matching")
    import random


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def is_valid_drive_url(url):
    """Validate Google Drive folder URL"""
    drive_patterns = [
        r'drive\.google\.com/drive/folders/',
        r'drive\.google\.com/drive/u/\d+/folders/'
    ]
    return any(re.search(pattern, url) for pattern in drive_patterns)

def extract_folder_id(drive_url):
    """Extract folder ID from Google Drive URL"""
    patterns = [
        r'folders/([a-zA-Z0-9_-]+)',
        r'id=([a-zA-Z0-9_-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, drive_url)
        if match:
            return match.group(1)
    return None

def get_drive_images(folder_id, max_images=50):
    """Extract image URLs from Google Drive folder"""
    try:
        # Use the public folder view to get file listings
        folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        response = requests.get(folder_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Extract file IDs from the page content
        file_id_pattern = r'"([a-zA-Z0-9_-]{25,})"'
        potential_ids = re.findall(file_id_pattern, response.text)
        
        image_urls = []
        for file_id in potential_ids[:max_images]:  # Limit to prevent timeout
            if len(file_id) >= 25:  # Google Drive file IDs are typically 25+ chars
                direct_url = f"https://drive.google.com/uc?id={file_id}&export=download"
                image_urls.append(direct_url)
        
        return image_urls[:max_images]
    
    except Exception as e:
        logger.error(f"Error extracting drive images: {str(e)}")
        return []

def load_and_encode_face(image_path):
    """Load image and extract face encoding (real or demo mode)"""
    try:
        if FACE_RECOGNITION_AVAILABLE:
            # Real face recognition mode
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)

            if not face_encodings:
                logger.warning("No face found in the uploaded image")
                return None

            logger.info("✅ Real face encoding created successfully")
            return face_encodings[0]
        else:
            # Demo mode - create simple hash
            from PIL import Image
            with Image.open(image_path) as img:
                img = img.convert('RGB').resize((100, 100))
                pixels = list(img.getdata())
                encoding = hash(str(pixels[:100])) % 1000000
                logger.info("🔄 Demo face encoding created (not real AI)")
                return encoding

    except Exception as e:
        logger.error(f"Error encoding face: {str(e)}")
        return None

def check_face_match(image_url, reference_encoding, timeout=10, tolerance=0.6):
    """Check if image contains the reference face (real or demo mode)"""
    try:
        response = requests.get(image_url, timeout=timeout, stream=True)
        response.raise_for_status()

        try:
            if FACE_RECOGNITION_AVAILABLE:
                # Real face recognition mode
                image_array = np.frombuffer(response.content, np.uint8)
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

                if image is None:
                    logger.warning(f"Could not decode image from {image_url}")
                    return False, None

                rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                face_encodings = face_recognition.face_encodings(rgb_image)

                if not face_encodings:
                    logger.debug(f"No faces found in image from {image_url}")
                    return False, None

                # Compare each face in the image with the reference face
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=tolerance)

                    if matches[0]:
                        logger.info(f"✅ Real face match found in image from {image_url}")
                        return True, response.content

                return False, None
            else:
                # Demo mode - simulate face matching
                from PIL import Image
                img = Image.open(BytesIO(response.content))
                img = img.convert('RGB').resize((100, 100))

                pixels = list(img.getdata())
                image_encoding = hash(str(pixels[:100])) % 1000000

                # Simulate matching with some randomness
                similarity_score = abs(image_encoding - reference_encoding) % 100
                is_match = similarity_score < 35 or random.random() < 0.25

                if is_match:
                    logger.info(f"🔄 Demo match found in image from {image_url}")
                    return True, response.content

                return False, None

        except Exception as img_error:
            logger.error(f"Error processing image from {image_url}: {str(img_error)}")
            return False, None

    except Exception as e:
        logger.error(f"Error downloading image from {image_url}: {str(e)}")
        return False, None

def create_photos_zip(matched_images):
    """Create ZIP file with matched photos"""
    zip_buffer = BytesIO()
    
    try:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for i, image_data in enumerate(matched_images):
                filename = f"photo_{i+1:03d}.jpg"
                zipf.writestr(filename, image_data)
        
        zip_buffer.seek(0)
        return zip_buffer
    
    except Exception as e:
        logger.error(f"Error creating ZIP: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_photos():
    try:
        # Validate inputs
        if 'selfie' not in request.files:
            return jsonify({'error': 'No selfie uploaded'}), 400
        
        if 'drive_link' not in request.form:
            return jsonify({'error': 'No Google Drive link provided'}), 400
        
        selfie = request.files['selfie']
        drive_link = request.form['drive_link'].strip()

        if selfie.filename == '':
            return jsonify({'error': 'No selfie selected'}), 400
        
        if not is_valid_drive_url(drive_link):
            return jsonify({'error': 'Invalid Google Drive folder URL'}), 400
        
        # Save uploaded selfie
        filename = secure_filename(selfie.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        selfie.save(filepath)
        
        # Extract face encoding from selfie
        reference_encoding = load_and_encode_face(filepath)
        if reference_encoding is None:
            os.remove(filepath)
            return jsonify({'error': 'No face detected in selfie. Please upload a clear photo.'}), 400
        
        # Extract folder ID and get images
        folder_id = extract_folder_id(drive_link)
        if not folder_id:
            os.remove(filepath)
            return jsonify({'error': 'Could not extract folder ID from URL'}), 400
        
        image_urls = get_drive_images(folder_id)
        if not image_urls:
            os.remove(filepath)
            return jsonify({'error': 'No images found in the folder or folder is private'}), 400
        
        # Process images and find matches
        matched_images = []
        processed_count = 0
        total_images = len(image_urls)

        # Smart automatic limits based on folder size
        if total_images <= 30:
            max_images = total_images  # Process all for small folders
            face_tolerance = 0.6  # Normal tolerance
            logger.info(f"Small folder detected ({total_images} photos) - processing all images")
        elif total_images <= 100:
            max_images = min(total_images, 60)  # Process most for medium folders
            face_tolerance = 0.6  # Normal tolerance
            logger.info(f"Medium folder detected ({total_images} photos) - processing first {max_images} images")
        else:
            max_images = 80  # Cap for large folders to prevent timeouts
            face_tolerance = 0.65  # Slightly more relaxed for large folders
            logger.info(f"Large folder detected ({total_images} photos) - processing first {max_images} images to prevent timeout")

        logger.info(f"Found {total_images} images in folder. Processing first {max_images} images.")

        # Process images with progress tracking
        for i, url in enumerate(image_urls[:max_images]):
            try:
                logger.info(f"Processing image {i+1}/{max_images} ({((i+1)/max_images)*100:.1f}%)")
                is_match, image_data = check_face_match(url, reference_encoding, timeout=15, tolerance=face_tolerance)
                processed_count += 1

                if is_match and image_data:
                    matched_images.append(image_data)
                    logger.info(f"✅ Match found! Total matches: {len(matched_images)}")
                else:
                    logger.debug(f"❌ No match in image {i+1}")

                # Early exit optimization for large folders
                if total_images > 50 and len(matched_images) >= 15:
                    logger.info(f"Found {len(matched_images)} matches in large folder - stopping early to save time")
                    break
                elif total_images > 100 and len(matched_images) >= 25:
                    logger.info(f"Found {len(matched_images)} matches in very large folder - stopping early")
                    break

            except Exception as e:
                logger.error(f"Error processing image {i+1}: {str(e)}")
                continue

        logger.info(f"Processing complete. Found {len(matched_images)} matches out of {processed_count} processed images (from {total_images} total)")
        
        # Clean up uploaded selfie
        os.remove(filepath)
        
        if not matched_images:
            return jsonify({'error': 'No photos found with your face'}), 404
        
        # Create ZIP file
        zip_data = create_photos_zip(matched_images)
        if not zip_data:
            return jsonify({'error': 'Error creating ZIP file'}), 500
        
        return send_file(
            zip_data,
            mimetype='application/zip',
            as_attachment=True,
            download_name='yourphotos.zip'
        )
    
    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        return jsonify({'error': 'An error occurred while processing your request'}), 500

@app.errorhandler(413)
def too_large(_):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
