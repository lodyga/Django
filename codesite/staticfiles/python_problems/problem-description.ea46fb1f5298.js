document.addEventListener('DOMContentLoaded', () => {
  const descriptionToggle = document.querySelector('[data-bs-target="#problemDescription"]');
  const icon = descriptionToggle.querySelector('i');

  // Get saved state (default to true if not set)
  const isProblemDescriptionVisible = localStorage.getItem('problemDescriptionState') !== 'false';

  // Initialize Bootstrap collapse
  const descriptionCollapse = new bootstrap.Collapse('#problemDescription', {
    toggle: false
  });

  // Set initial icon and aria state
  if (isProblemDescriptionVisible) {
    descriptionCollapse.show();
    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
    descriptionToggle.setAttribute('aria-expanded', 'true');
  } else {
    descriptionCollapse.hide();
    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
    descriptionToggle.setAttribute('aria-expanded', 'false');
  }

  // Update state when collapse event occurs
  document.getElementById('problemDescription').addEventListener('shown.bs.collapse', () => {
    localStorage.setItem('problemDescriptionState', 'true');
    icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
  });

  document.getElementById('problemDescription').addEventListener('hidden.bs.collapse', () => {
    localStorage.setItem('problemDescriptionState', 'false');
    icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
  });
});