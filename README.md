# Mwi - AI Photo Extractor 📸
**Team Collaboration Project - 6 Students**

A professional Flask web application that uses AI face recognition to automatically find and extract photos containing your face from Google Drive folders.

## 👥 Team Project
This is a collaborative class project developed by 6 students, each responsible for different components of the application.

## 🌟 Features

- **AI Face Recognition**: Advanced face matching using state-of-the-art algorithms
- **Google Drive Integration**: Extract photos directly from shared Google Drive folders
- **Professional UI**: Modern, responsive design with photography theme
- **Privacy First**: Photos are processed securely and not stored on servers
- **Fast Processing**: Quick extraction and ZIP download
- **Mobile Friendly**: Works perfectly on all devices

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Google Drive folder with photos (set to "Anyone with the link can view")

### Local Development with Docker

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd yourphotos-app
   ```

2. **Start the application**
   ```bash
   docker-compose up --build
   ```

3. **Open your browser**
   Navigate to `http://localhost:5000`

The application will automatically reload when you make changes to the code.

### Manual Development (Without Docker)

If you prefer to run without Docker:

1. **Install Python 3.9+**
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**
   ```bash
   python app.py
   ```

## 🌐 Deployment on Render

### Method 1: Auto-Deploy from GitHub

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Click "New Web Service"
   - Connect your GitHub repository
   - Render will automatically detect the `render.yaml` configuration
   - Click "Deploy"

### Method 2: Manual Configuration

1. **Create New Web Service** on Render
2. **Configure Settings**:
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Python Version**: 3.9.18

## 📱 How to Use

1. **Upload Your Selfie**
   - Click the upload area or drag & drop your photo
   - Make sure your face is clearly visible
   - Supported formats: JPG, PNG, GIF (Max 16MB)

2. **Add Google Drive Link**
   - Share your Google Drive folder with "Anyone with the link can view"
   - Copy and paste the folder URL
   - Format: `https://drive.google.com/drive/folders/[FOLDER_ID]`

3. **Extract Photos**
   - Click "Extract My Photos"
   - Wait for AI processing (may take a few minutes)
   - Download the ZIP file containing your photos

## 🛠️ Technical Details

### Architecture

- **Backend**: Flask (Python web framework)
- **AI Engine**: face_recognition library with dlib
- **Image Processing**: OpenCV for image manipulation
- **Frontend**: Bootstrap 5 with custom CSS/JS
- **Deployment**: Gunicorn WSGI server

### Key Components

- `app.py`: Main Flask application with API endpoints
- `templates/index.html`: Professional frontend interface
- `static/css/style.css`: Custom photography-themed styling
- `static/js/main.js`: Frontend interactions and AJAX handling

### API Endpoints

- `GET /`: Main application interface
- `POST /process`: Photo processing and extraction endpoint

## 🔧 Configuration

### Environment Variables

- `PORT`: Server port (default: 5000)
- `SECRET_KEY`: Flask secret key for sessions

### File Limits

- Maximum upload size: 16MB
- Supported image formats: JPG, PNG, GIF
- Processing limit: 20 images per request (for demo)

## 🔒 Privacy & Security

- **No Data Storage**: Uploaded photos are processed and immediately deleted
- **Secure Processing**: All face recognition happens server-side
- **HTTPS**: Encrypted communication in production
- **Input Validation**: Comprehensive validation of uploads and URLs

## 🐛 Troubleshooting

### Common Issues

1. **"No face detected in selfie"**
   - Ensure your face is clearly visible and well-lit
   - Try a different photo with better quality

2. **"No images found in folder"**
   - Check that the Google Drive folder is shared publicly
   - Verify the folder contains image files
   - Make sure the URL format is correct

3. **"Processing timeout"**
   - Large folders may take longer to process
   - Try with a smaller folder first

### Dependencies Issues

If you encounter installation issues with face_recognition:

```bash
# On Ubuntu/Debian
sudo apt-get install build-essential cmake
sudo apt-get install libopenblas-dev liblapack-dev
sudo apt-get install libx11-dev libgtk-3-dev

# On macOS
brew install cmake
```

## 📈 Performance Optimization

- Images are processed in batches to prevent timeouts
- Face encodings are cached during processing
- ZIP files are created in memory for faster downloads
- Responsive design ensures fast loading on all devices

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) library by Adam Geitgey
- [OpenCV](https://opencv.org/) for image processing
- [Bootstrap](https://getbootstrap.com/) for responsive design
- [Font Awesome](https://fontawesome.com/) for icons

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Open an issue on GitHub
3. Contact the development team

---

**Made with ❤️ for photographers and AI enthusiasts**
