// YourPhotos - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initializeApp();
});

function initializeApp() {
    setupFileUpload();
    setupFormSubmission();
    setupSmoothScrolling();
    setupAnimations();
}

// File Upload Functionality
function setupFileUpload() {
    const uploadArea = document.getElementById('selfieUpload');
    const fileInput = document.getElementById('selfie');
    const previewContainer = document.getElementById('selfiePreview');
    const previewImage = document.getElementById('previewImage');
    const removeButton = document.querySelector('.remove-image');

    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        if (e.target !== removeButton && !e.target.closest('.remove-image')) {
            fileInput.click();
        }
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        handleFileSelect(e.target.files[0]);
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // Remove image
    removeButton.addEventListener('click', function(e) {
        e.stopPropagation();
        removeImage();
    });

    function handleFileSelect(file) {
        if (!file) return;

        // Validate file type
        if (!file.type.startsWith('image/')) {
            showAlert('Please select a valid image file.', 'danger');
            return;
        }

        // Validate file size (16MB)
        if (file.size > 16 * 1024 * 1024) {
            showAlert('File size must be less than 16MB.', 'danger');
            return;
        }

        // Update file input
        const dt = new DataTransfer();
        dt.items.add(file);
        fileInput.files = dt.files;

        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            document.querySelector('.upload-content').style.display = 'none';
            previewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    }

    function removeImage() {
        fileInput.value = '';
        previewContainer.style.display = 'none';
        document.querySelector('.upload-content').style.display = 'block';
    }
}

// Form Submission
function setupFormSubmission() {
    const form = document.getElementById('photoForm');
    const submitBtn = document.getElementById('submitBtn');
    const progressSection = document.getElementById('progressSection');
    const progressBar = document.querySelector('.progress-bar');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        if (!validateForm()) {
            return;
        }

        // Show progress
        showProgress();
        
        // Create FormData
        const formData = new FormData(form);
        
        // Submit form
        submitForm(formData);
    });

    function validateForm() {
        const selfie = document.getElementById('selfie').files[0];
        const driveLink = document.getElementById('drive_link').value.trim();

        if (!selfie) {
            showAlert('Please upload your selfie.', 'danger');
            return false;
        }

        if (!driveLink) {
            showAlert('Please enter your Google Drive folder link.', 'danger');
            return false;
        }

        // Validate Google Drive URL
        const drivePattern = /drive\.google\.com\/drive\/folders\//;
        if (!drivePattern.test(driveLink)) {
            showAlert('Please enter a valid Google Drive folder link.', 'danger');
            return false;
        }

        return true;
    }

    function showProgress() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        progressSection.style.display = 'block';
        hideAlert();

        // Animate progress bar
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress > 90) progress = 90;
            
            progressBar.style.width = progress + '%';
            
            if (progress >= 90) {
                clearInterval(interval);
            }
        }, 500);
    }

    function submitForm(formData) {
        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.ok) {
                // File download
                return response.blob().then(blob => {
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'yourphotos.zip';
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                    
                    showAlert('Photos downloaded successfully! Check your downloads folder.', 'success');
                    resetForm();
                });
            } else {
                return response.json().then(data => {
                    throw new Error(data.error || 'An error occurred');
                });
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert(error.message || 'An error occurred while processing your request.', 'danger');
            resetForm();
        });
    }

    function resetForm() {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Extract My Photos';
        progressSection.style.display = 'none';
        document.querySelector('.progress-bar').style.width = '0%';
    }
}

// Alert System
function showAlert(message, type) {
    const alertSection = document.getElementById('alertSection');
    const alertDiv = alertSection.querySelector('.alert');
    const alertMessage = document.getElementById('alertMessage');

    alertMessage.textContent = message;
    alertDiv.className = `alert alert-${type}`;
    alertSection.style.display = 'block';

    // Auto hide success messages
    if (type === 'success') {
        setTimeout(() => {
            hideAlert();
        }, 5000);
    }

    // Scroll to alert
    alertSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

function hideAlert() {
    const alertSection = document.getElementById('alertSection');
    alertSection.style.display = 'none';
}

// Smooth Scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Animations
function setupAnimations() {
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .upload-step').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Form validation helpers
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// Loading states
function setLoading(element, isLoading) {
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
    } else {
        element.disabled = false;
        element.innerHTML = element.getAttribute('data-original-text') || 'Submit';
    }
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    showAlert('An unexpected error occurred. Please try again.', 'danger');
});

// Prevent form resubmission on page refresh
if (window.history.replaceState) {
    window.history.replaceState(null, null, window.location.href);
}
