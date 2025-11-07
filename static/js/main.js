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
    const uploadContent = document.querySelector('.upload-content');

    console.log('Setting up file upload...'); // Debug log

    // Click to upload
    uploadArea.addEventListener('click', function(e) {
        console.log('Upload area clicked'); // Debug log
        console.log('Click target:', e.target); // Debug log
        console.log('Is remove button:', e.target === removeButton); // Debug log
        console.log('Is remove button child:', e.target.closest('.remove-image')); // Debug log
        
        // Only trigger if not clicking the remove button
        if (e.target !== removeButton && !e.target.closest('.remove-image')) {
            console.log('Triggering file input click'); // Debug log
            e.preventDefault();
            e.stopPropagation();
            fileInput.click();
        }
    });

    // Add click handler to upload content as well
    uploadContent.addEventListener('click', function(e) {
        console.log('Upload content clicked'); // Debug log
        e.preventDefault();
        e.stopPropagation();
        fileInput.click();
    });

    // Add keyboard support for accessibility
    uploadArea.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            console.log('Keyboard trigger'); // Debug log
            e.preventDefault();
            fileInput.click();
        }
    });

    // File input change
    fileInput.addEventListener('change', function(e) {
        console.log('File input changed'); // Debug log
        const file = e.target.files[0];
        console.log('Selected file:', file); // Debug log
        if (file) {
            handleFileSelect(file);
        }
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // Remove image
    removeButton.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        removeImage();
    });

    function handleFileSelect(file) {
        console.log('Handling file select:', file); // Debug log
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

        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            uploadContent.style.display = 'none';
            previewContainer.style.display = 'block';
            console.log('Preview updated'); // Debug log
        };
        reader.readAsDataURL(file);
    }

    function removeImage() {
        console.log('Removing image'); // Debug log
        fileInput.value = '';
        previewContainer.style.display = 'none';
        uploadContent.style.display = 'block';
    }
}

// Form Submission
function setupFormSubmission() {
    const form = document.getElementById('photoForm');
    const submitBtn = document.getElementById('submitBtn');
    const progressSection = document.getElementById('progressSection');
    const progressBar = document.querySelector('.progress-bar');
    const statusMessage = document.getElementById('statusMessage');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log('Form submitted'); // Debug log
        
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
        const fileInput = document.getElementById('selfie');
        const selfie = fileInput.files[0];
        const driveLink = document.getElementById('drive_link').value.trim();

        console.log('Validating form...'); // Debug log
        console.log('File input:', fileInput); // Debug log
        console.log('Selected file:', selfie); // Debug log
        console.log('File input value:', fileInput.value); // Debug log

        // Check if file is actually selected
        if (!selfie || !fileInput.value) {
            showAlert('Please upload your selfie.', 'danger');
            return false;
        }

        // Additional file validation
        if (!selfie.type.startsWith('image/')) {
            showAlert('Please select a valid image file.', 'danger');
            return false;
        }

        if (selfie.size > 16 * 1024 * 1024) {
            showAlert('File size must be less than 16MB.', 'danger');
            return false;
        }

        if (!driveLink) {
            showAlert('Please enter your Google Drive folder link.', 'danger');
            document.getElementById('drive_link').focus();
            return false;
        }

        // Validate Google Drive URL
        const drivePattern = /drive\.google\.com\/drive\/folders\//;
        if (!drivePattern.test(driveLink)) {
            showAlert('Please enter a valid Google Drive folder link.', 'danger');
            document.getElementById('drive_link').focus();
            return false;
        }

        return true;
    }

    function showProgress() {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        progressSection.style.display = 'block';
        statusMessage.textContent = 'Starting processing...';
        hideAlert();
    }

    function submitForm(formData) {
        console.log('Submitting form...'); // Debug log
        
        // Use fetch with streaming response for Server-Sent Events
        fetch('/process', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            // Get the reader for streaming
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            
            // Function to process each chunk
            function processChunk() {
                return reader.read().then(({ done, value }) => {
                    if (done) {
                        console.log('Stream finished');
                        return;
                    }
                    
                    // Decode the chunk and add to buffer
                    buffer += decoder.decode(value, { stream: true });
                    
                    // Process complete lines (SSE format: "data: {...}\n\n")
                    const lines = buffer.split('\n\n');
                    buffer = lines.pop() || ''; // Keep incomplete line in buffer
                    
                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            try {
                                const jsonStr = line.substring(6); // Remove "data: " prefix
                                const data = JSON.parse(jsonStr);
                                console.log('Progress update:', data); // Debug log
                                
                                if (data.error) {
                                    showAlert(data.error, 'danger');
                                    resetForm();
                                    return;
                                }
                                
                                if (data.progress !== undefined) {
                                    progressBar.style.width = data.progress + '%';
                                    if (statusMessage) {
                                        statusMessage.textContent = data.status || 'Processing...';
                                    }
                                }
                                
                                if (data.download_url) {
                                    // Trigger download
                                    window.location.href = data.download_url;
                                    showAlert('Processing complete! Your photos are being downloaded.', 'success');
                                    resetForm();
                                    return;
                                }
                            } catch (e) {
                                console.error('Error parsing SSE data:', e, line);
                            }
                        }
                    }
                    
                    // Continue reading
                    return processChunk();
                });
            }
            
            // Start processing the stream
            return processChunk();
        })
        .catch(error => {
            console.error('Error:', error);
            showAlert('An error occurred while processing your request. Please try again.', 'danger');
            resetForm();
        });
    }

    function resetForm() {
        // Reset file input and preview
        const fileInput = document.getElementById('selfie');
        const previewContainer = document.getElementById('selfiePreview');
        const uploadContent = document.querySelector('.upload-content');
        
        fileInput.value = '';
        previewContainer.style.display = 'none';
        uploadContent.style.display = 'block';
        
        // Reset drive link input
        document.getElementById('drive_link').value = '';
        
        // Reset submit button
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fas fa-magic me-2"></i>Extract My Photos';
        
        // Hide progress section
        progressSection.style.display = 'none';
        
        // Reset progress bar
        progressBar.style.width = '0%';
        statusMessage.textContent = '';
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
