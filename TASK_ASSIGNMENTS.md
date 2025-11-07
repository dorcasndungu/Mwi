# Task Assignments - Photo Extractor Team Project

## 📋 Detailed Task Breakdown

### 🎯 Student 1: Project Lead & Backend Core
**GitHub Username:** ________________
**Branch:** `feature/backend-core`

**Week 1 Tasks:**
- [ ] Set up team repository permissions
- [ ] Create Flask app skeleton with basic routing
- [ ] Implement file upload handling in `/process` route
- [ ] Set up error handling and logging

**Week 2 Tasks:**
- [ ] Implement ZIP file creation logic
- [ ] Add file validation and security checks
- [ ] Create API response handling
- [ ] Coordinate with other team members for integration

**Files to Work On:**
- `app.py` (main structure, routing, file handling)
- Integration with other team members' functions

---

### 🤖 Student 2: AI/Face Recognition Specialist
**GitHub Username:** ________________
**Branch:** `feature/face-recognition`

**Week 1 Tasks:**
- [ ] Research face_recognition library documentation
- [ ] Implement `load_and_encode_face(image_path)` function
- [ ] Create basic face detection with error handling
- [ ] Test with sample images

**Week 2 Tasks:**
- [ ] Implement `check_face_match(image_url, reference_encoding)` function
- [ ] Add tolerance adjustment and optimization
- [ ] Create fallback/demo mode for development
- [ ] Performance testing and benchmarking

**Files to Work On:**
- Face recognition functions in `app.py`
- Create `face_recognition_utils.py` if needed

---

### 🎨 Student 3: Frontend Developer
**GitHub Username:** ________________
**Branch:** `feature/frontend-design`

**Week 1 Tasks:**
- [ ] Design main page layout and structure
- [ ] Create upload interface with drag & drop area
- [ ] Design progress indicators and loading states
- [ ] Create error and success message displays

**Week 2 Tasks:**
- [ ] Implement responsive design for mobile
- [ ] Add photography-themed styling
- [ ] Create professional color scheme and typography
- [ ] Polish UI/UX details

**Files to Work On:**
- `templates/index.html`
- `static/css/style.css`

---

### ⚡ Student 4: JavaScript Developer
**GitHub Username:** ________________
**Branch:** `feature/javascript-interactions`

**Week 1 Tasks:**
- [ ] Implement file upload drag & drop functionality
- [ ] Create form validation (file types, sizes)
- [ ] Add image preview functionality
- [ ] Basic AJAX form submission

**Week 2 Tasks:**
- [ ] Implement progress bar animations
- [ ] Add real-time status updates
- [ ] Create error handling and user feedback
- [ ] Optimize user experience and interactions

**Files to Work On:**
- `static/js/main.js`
- Integration with HTML elements from Student 3

---

### ☁️ Student 5: Google Drive Integration Specialist
**GitHub Username:** ________________
**Branch:** `feature/google-drive-integration`

**Week 1 Tasks:**
- [ ] Research Google Drive public folder structure
- [ ] Implement `extract_folder_id(drive_url)` function
- [ ] Create `get_drive_images(folder_id)` function
- [ ] Add URL validation and error handling

**Week 2 Tasks:**
- [ ] Optimize image extraction and rate limiting
- [ ] Add support for different Drive URL formats
- [ ] Implement error handling for private folders
- [ ] Test with various folder sizes and types

**Files to Work On:**
- Google Drive functions in `app.py`
- Create `drive_utils.py` if needed

---

### 🚀 Student 6: DevOps & Deployment
**GitHub Username:** ________________
**Branch:** `feature/deployment-config`

**Week 1 Tasks:**
- [ ] Create deployment configuration files
- [ ] Set up requirements.txt with proper versions
- [ ] Write comprehensive README.md
- [ ] Create development setup instructions

**Week 2 Tasks:**
- [ ] Deploy to Railway/Render
- [ ] Set up environment variables
- [ ] Create testing framework
- [ ] Write deployment troubleshooting guide

**Files to Work On:**
- `requirements.txt`
- `README.md`
- `Procfile` or deployment configs
- Documentation files

---

## 🔄 Weekly Milestones

### Week 1: Foundation
- [ ] All team members have working development environment
- [ ] Basic functions implemented in each area
- [ ] First integration test successful

### Week 2: Integration & Polish
- [ ] All features integrated and working together
- [ ] UI/UX polished and responsive
- [ ] Successfully deployed to production
- [ ] Documentation complete

## 📞 Communication Plan
- **Daily Standups:** 15 minutes via Discord/Slack
- **Weekly Team Meeting:** 1 hour progress review
- **Code Reviews:** All PRs require 2 approvals
- **Integration Testing:** Fridays

## 🏆 Definition of Done
Each task is complete when:
- [ ] Code is written and tested
- [ ] Pull request created and reviewed
- [ ] Documentation updated
- [ ] Integration tested with other components
