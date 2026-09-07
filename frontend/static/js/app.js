/**
 * Smart Farmer Assistant — Core Application Client-Side JS Framework
 * Manages toast notifications, modal dialog triggers, AJAX API helpers,
 * dynamic search filters, and page initializations.
 */

document.addEventListener('DOMContentLoaded', () => {
  console.log('Smart Farmer Assistant — Web Application Initialized');

  // Auto-dismiss Flash Alerts
  const alerts = document.querySelectorAll('.alert-dismissible');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });

  // Modal Open/Close Triggers
  document.querySelectorAll('[data-toggle="modal"]').forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = trigger.getAttribute('data-target');
      const modal = document.querySelector(targetId);
      if (modal) modal.classList.add('show');
    });
  });

  document.querySelectorAll('.modal-close, .modal-backdrop').forEach(closeBtn => {
    closeBtn.addEventListener('click', () => {
      const modal = closeBtn.closest('.modal');
      if (modal) modal.classList.remove('show');
    });
  });

  // Drag and Drop File Upload Preview
  const dropzones = document.querySelectorAll('.dropzone');
  dropzones.forEach(zone => {
    const input = zone.querySelector('input[type="file"]');
    if (!input) return;

    zone.addEventListener('click', () => input.click());

    zone.addEventListener('dragover', (e) => {
      e.preventDefault();
      zone.classList.add('dragover');
    });

    zone.addEventListener('dragleave', () => zone.classList.remove('dragover'));

    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('dragover');
      if (e.dataTransfer.files.length > 0) {
        input.files = e.dataTransfer.files;
        updateDropzoneLabel(zone, input.files[0].name);
      }
    });

    input.addEventListener('change', () => {
      if (input.files.length > 0) {
        updateDropzoneLabel(zone, input.files[0].name);
      }
    });
  });

  function updateDropzoneLabel(zone, filename) {
    const textEl = zone.querySelector('.dropzone-text');
    if (textEl) {
      textEl.textContent = `Selected: ${filename}`;
    }
  }

  // Poll Notifications Badge
  function checkUnreadNotifications() {
    fetch('/api/v1/farmer/notifications')
      .then(res => res.json())
      .then(data => {
        if (data.success && data.meta) {
          const badge = document.querySelector('.badge-count');
          if (badge) badge.textContent = data.meta.total_items || 0;
        }
      })
      .catch(err => console.debug('Notifications poll omitted:', err));
  }

  // Initialize notifications polling if authenticated
  if (document.querySelector('.notification-badge')) {
    checkUnreadNotifications();
  }
});
