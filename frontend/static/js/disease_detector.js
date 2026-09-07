/**
 * Smart Farmer Assistant — Disease Image Upload & CV Analysis Component
 * Handles client-side leaf image preview, dropzone drag-and-drop events, canvas image processing,
 * and diagnosis progress status animation.
 */

class DiseaseImageDetector {
  constructor(containerId, formId) {
    this.container = document.getElementById(containerId);
    this.form = document.getElementById(formId);
    if (!this.container || !this.form) return;
    this.initEvents();
  }

  initEvents() {
    const fileInput = this.form.querySelector('input[type="file"]');
    const previewImg = this.container.querySelector('#image-preview');
    const placeholder = this.container.querySelector('#upload-placeholder');
    const submitBtn = this.form.querySelector('button[type="submit"]');

    if (fileInput) {
      fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = (evt) => {
            if (previewImg) {
              previewImg.src = evt.target.result;
              previewImg.classList.remove('d-none');
            }
            if (placeholder) {
              placeholder.classList.add('d-none');
            }
            if (submitBtn) {
              submitBtn.disabled = false;
            }
          };
          reader.readAsDataURL(file);
        }
      });
    }

    this.form.addEventListener('submit', () => {
      const statusBox = document.getElementById('scan-status-box');
      if (statusBox) {
        statusBox.classList.remove('d-none');
        statusBox.innerHTML = `
          <div class="alert alert-info d-flex align-items-center gap-3 rounded-4 shadow-sm">
            <div class="spinner-border text-info" role="status"></div>
            <div>
              <h6 class="fw-bold mb-0">Running Offline Computer Vision Diagnosis...</h6>
              <small class="text-muted">Extracting RGB/HSV color histograms, GLCM texture matrix, and Sobel edge response.</small>
            </div>
          </div>
        `;
      }
    });
  }
}

window.DiseaseImageDetector = DiseaseImageDetector;
