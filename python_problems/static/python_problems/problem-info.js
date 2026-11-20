document.addEventListener('DOMContentLoaded', () => {
  const infoToggle = document.querySelector('[data-bs-target="#problemInfo"]');
  const icon = infoToggle.querySelector('i');
  const b = infoToggle.querySelector('b');

  // Get saved state (default to true if not set)
  const isProblemInfoVisible = localStorage.getItem('problemInfoState') !== 'false';

  // Initialize Bootstrap collapse
  const infoCollapse = new bootstrap.Collapse('#problemInfo', {
    toggle: false
  });

  // Set initial icon and aria state
  if (isProblemInfoVisible) {
    infoCollapse.show();
    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
    infoToggle.setAttribute('aria-expanded', 'true');
  } else {
    infoCollapse.hide();
    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
    infoToggle.setAttribute('aria-expanded', 'false');
  }

  // Update state when collapse event occurs
  document.getElementById('problemInfo').addEventListener('shown.bs.collapse', () => {
    localStorage.setItem('problemInfoState', 'true');
    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
    // b.textContent = 'Hide Info';
  });

  document.getElementById('problemInfo').addEventListener('hidden.bs.collapse', () => {
    localStorage.setItem('problemInfoState', 'false');
    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
    // b.textContent = 'Show Info';
  });
});