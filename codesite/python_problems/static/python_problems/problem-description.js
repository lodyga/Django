document.addEventListener('DOMContentLoaded', () => {
   const problemDescriptionElements = document.getElementById('problemDescription');
   const descriptionCollapse = new bootstrap.Collapse(problemDescriptionElements, { toggle: false });
   const descriptionToggle = document.querySelector('[data-bs-target="#problemDescription"]');
   const icon = descriptionToggle.querySelector('i');
   const isProblemDescriptionVisible = localStorage.getItem('problemDescriptionState') !== 'false';

   isProblemDescriptionVisible ? descriptionCollapse.show() : descriptionCollapse.hide();

   problemDescriptionElements.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('problemDescriptionState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      descriptionToggle.setAttribute('aria-expanded', 'true');
   });

   problemDescriptionElements.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('problemDescriptionState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      descriptionToggle.setAttribute('aria-expanded', 'false');
   });
});