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

   const solutionButtonContainer = document.getElementById('solutionButtonContainer');
   const solutionElements = document.getElementsByClassName('solutionContent');
   const solutionLength = solutionElements.length;

   if (!solutionButtonContainer || solutionLength === 0) {
      return;
   }

   for (let index = 1; index < solutionLength + 1; index++) {
      const button = document.createElement('button');
      button.id = `solutionButton-${index}`;
      button.className = 'btn btn-outline-secondary btn-sm me-2 py-0 px-3';
      button.textContent = `Solution ${index}`;
      button.onclick = () => {
         showSolution(index);
      };
      solutionButtonContainer.appendChild(button);
   }

   function showSolution(idx) {
      const selectedSolution = document.getElementById(`solution-${idx}`);
      const selectedContent = selectedSolution?.value || '';

      if (typeof setSolutionViewerContent === 'function') {
         setSolutionViewerContent(selectedContent);
      }

      for (let i = 1; i < solutionLength + 1; i++) {
         const btn = document.getElementById(`solutionButton-${i}`);

         if (i === idx) {
            btn.classList.replace('btn-outline-secondary', 'btn-secondary');
         } else {
            btn.classList.replace('btn-secondary', 'btn-outline-secondary');
         }
      }
   }

   if (solutionLength > 0) {
      showSolution(1);
   }
});
