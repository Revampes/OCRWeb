// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const fileName = document.getElementById('fileName');
const scanBtn = document.getElementById('scanBtn');
const changeFileBtn = document.getElementById('changeFileBtn');
const loadingSection = document.getElementById('loadingSection');
const resultSection = document.getElementById('resultSection');
const ocrResult = document.getElementById('ocrResult');
const errorSection = document.getElementById('errorSection');
const errorMessage = document.getElementById('errorMessage');
const copyBtn = document.getElementById('copyBtn');
const downloadBtn = document.getElementById('downloadBtn');
const scanAnotherBtn = document.getElementById('scanAnotherBtn');
const retryBtn = document.getElementById('retryBtn');
const toast = document.getElementById('toast');

let currentFile = null;

// Event Listeners
uploadArea.addEventListener('click', () => fileInput.click());
uploadArea.addEventListener('dragover', handleDragOver);
uploadArea.addEventListener('dragleave', handleDragLeave);
uploadArea.addEventListener('drop', handleDrop);
fileInput.addEventListener('change', handleFileSelect);
changeFileBtn.addEventListener('click', resetUpload);
scanBtn.addEventListener('click', performOCR);
copyBtn.addEventListener('click', copyToClipboard);
downloadBtn.addEventListener('click', downloadText);
scanAnotherBtn.addEventListener('click', resetUpload);
retryBtn.addEventListener('click', hideError);

// Drag and Drop Handlers
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
}

function handleFile(file) {
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 
                          'image/bmp', 'image/tiff', 'image/webp', 'application/pdf'];
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Please upload a valid image or PDF file', 'error');
        return;
    }

    const maxSize = 16 * 1024 * 1024; // 16MB
    if (file.size > maxSize) {
        showToast('File size must be less than 16MB', 'error');
        return;
    }

    currentFile = file;
    displayPreview(file);
}

function displayPreview(file) {
    const reader = new FileReader();
    
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        fileName.textContent = file.name;
        
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        scanBtn.style.display = 'block';
    };
    
    if (file.type === 'application/pdf') {
        imagePreview.src = 'https://via.placeholder.com/400x300?text=PDF+Document';
        fileName.textContent = file.name;
        uploadArea.style.display = 'none';
        previewSection.style.display = 'block';
        scanBtn.style.display = 'block';
    } else {
        reader.readAsDataURL(file);
    }
}

async function performOCR() {
    if (!currentFile) {
        showToast('Please select a file first', 'error');
        return;
    }

    // Hide previous sections
    previewSection.style.display = 'none';
    scanBtn.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    
    // Show loading
    loadingSection.style.display = 'block';

    try {
        const formData = new FormData();
        formData.append('file', currentFile);

        const response = await fetch('/api/ocr', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok && data.success) {
            displayResult(data.text);
        } else {
            throw new Error(data.error || 'OCR processing failed');
        }
    } catch (error) {
        showError(error.message);
    } finally {
        loadingSection.style.display = 'none';
    }
}

function displayResult(text) {
    ocrResult.textContent = text;
    resultSection.style.display = 'block';
    showToast('Text extracted successfully!', 'success');
}

function showError(message) {
    errorMessage.textContent = message;
    errorSection.style.display = 'block';
}

function hideError() {
    errorSection.style.display = 'none';
    previewSection.style.display = 'block';
    scanBtn.style.display = 'block';
}

function resetUpload() {
    currentFile = null;
    fileInput.value = '';
    previewSection.style.display = 'none';
    scanBtn.style.display = 'none';
    resultSection.style.display = 'none';
    errorSection.style.display = 'none';
    uploadArea.style.display = 'block';
}

function copyToClipboard() {
    const text = ocrResult.textContent;
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard!', 'success');
    }).catch(() => {
        showToast('Failed to copy', 'error');
    });
}

function downloadText() {
    const text = ocrResult.textContent;
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ocr-result-${Date.now()}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showToast('Downloaded successfully!', 'success');
}

function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type} show`;
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Check server health on load
async function checkHealth() {
    try {
        const response = await fetch('/api/health');
        const data = await response.json();
        console.log('Server status:', data.status);
    } catch (error) {
        console.error('Server connection failed:', error);
    }
}

checkHealth();
