document.addEventListener('DOMContentLoaded', () => {
    const infoToggle = document.querySelector('[data-bs-target="#problemSolution"]');
    const icon = infoToggle.querySelector('i');
    const b = infoToggle.querySelector('b');
  
    // Get saved state (default to true if not set)
    const isProblemSolutionVisible = localStorage.getItem('problemSolutionState') === 'true';
  
    // Initialize Bootstrap collapse
    const solutionCollapse = new bootstrap.Collapse('#problemSolution', {
      toggle: false
    });
  
    // Set initial icon and aria state
    if (isProblemSolutionVisible) {
      solutionCollapse.show();
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      infoToggle.setAttribute('aria-expanded', 'true');
    } else {
      solutionCollapse.hide();
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      infoToggle.setAttribute('aria-expanded', 'false');
    }
  
    // Update state when collapse event occurs
    document.getElementById('problemSolution').addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('problemSolutionState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      // b.textContent = 'Hide Info';
    });
  
    document.getElementById('problemSolution').addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('problemSolutionState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      // b.textContent = 'Show Info';
    });
  });