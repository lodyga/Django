document.addEventListener('DOMContentLoaded', () => {
   const problemSolutionElement = document.getElementById('problemSolution');
   const infoToggle = document.querySelector('[data-bs-target="#problemSolution"]');

   if (!problemSolutionElement || !infoToggle) {
      return;
   }

   const icon = infoToggle.querySelector('i');
   const solutionCollapse = new bootstrap.Collapse(problemSolutionElement, {
      toggle: false,
   });

   const shouldOpenFromHash = window.location.hash === '#problemSolution';
   const isProblemSolutionVisible = shouldOpenFromHash
      || localStorage.getItem('problemSolutionState') === 'true';

   if (isProblemSolutionVisible) {
      solutionCollapse.show();
      localStorage.setItem('problemSolutionState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      infoToggle.setAttribute('aria-expanded', 'true');
   } else {
      solutionCollapse.hide();
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      infoToggle.setAttribute('aria-expanded', 'false');
   }

   problemSolutionElement.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('problemSolutionState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      infoToggle.setAttribute('aria-expanded', 'true');
   });

   problemSolutionElement.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('problemSolutionState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      infoToggle.setAttribute('aria-expanded', 'false');
   });
});
