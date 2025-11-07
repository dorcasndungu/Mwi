# Photo Extractor - Team Collaboration Setup

## 🎯 Project Overview
AI-powered photo extraction app that finds photos containing your face from Google Drive folders using real face recognition.

## 👥 Team Structure (6 Students)

### Student 1: Project Lead & Backend Core 🎯
**Branch:** `feature/backend-core`
**Files:** `app.py`, main Flask routing, file handling
**Tasks:**
- [ ] Set up Flask app structure
- [ ] Handle file uploads and ZIP creation
- [ ] Coordinate team integration
- [ ] Manage pull requests

### Student 2: AI/Face Recognition Specialist 🤖
**Branch:** `feature/face-recognition`
**Files:** Face recognition functions in `app.py`
**Tasks:**
- [ ] Implement `load_and_encode_face()` function
- [ ] Implement `check_face_match()` function
- [ ] Add error handling for face detection
- [ ] Optimize performance and accuracy

### Student 3: Frontend Developer 🎨
**Branch:** `feature/frontend-design`
**Files:** `templates/index.html`, `static/css/style.css`
**Tasks:**
- [ ] Design main page layout
- [ ] Create upload interface
- [ ] Style progress indicators
- [ ] Make responsive design

### Student 4: JavaScript Developer ⚡
**Branch:** `feature/javascript-interactions`
**Files:** `static/js/main.js`
**Tasks:**
- [ ] File upload drag & drop
- [ ] Form validation and submission
- [ ] Progress animations
- [ ] Error handling

### Student 5: Google Drive Integration Specialist ☁️
**Branch:** `feature/google-drive-integration`
**Files:** Google Drive functions in `app.py`
**Tasks:**
- [ ] Implement `get_drive_images()` function
- [ ] URL validation and parsing
- [ ] Error handling for private folders
- [ ] Rate limiting optimization

### Student 6: DevOps & Deployment 🚀
**Branch:** `feature/deployment-config`
**Files:** `requirements.txt`, deployment configs, `README.md`
**Tasks:**
- [ ] Create deployment configurations
- [ ] Set up testing framework
- [ ] Write documentation
- [ ] Handle environment setup

## 🚀 Getting Started

### For Team Members:
1. Clone the repository
2. Create your feature branch: `git checkout -b feature/your-area`
3. Set up development environment
4. Start working on your assigned tasks

### Development Workflow:
1. Pull latest: `git pull origin class-collaboration`
2. Work on your feature
3. Commit regularly: `git commit -m "descriptive message"`
4. Push: `git push origin feature/your-branch`
5. Create Pull Request when ready

## 📁 Current File Structure
```
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css        # Styling
│   └── js/
│       └── main.js          # JavaScript interactions
└── README.md                # Project documentation
```

## 🎯 Integration Points
- **Backend ↔ AI:** Face recognition functions called from Flask routes
- **Backend ↔ Drive:** Google Drive functions called from processing endpoint
- **Frontend ↔ JavaScript:** HTML elements controlled by JS
- **JavaScript ↔ Backend:** AJAX calls to Flask endpoints

## 📚 Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [face_recognition Library](https://github.com/ageitgey/face_recognition)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)

## 🏆 Success Criteria
- [ ] All 6 students contribute meaningful code
- [ ] Working face recognition functionality
- [ ] Professional UI/UX
- [ ] Successful deployment
- [ ] Clean documentation
