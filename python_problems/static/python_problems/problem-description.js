document.addEventListener('DOMContentLoaded', () => {
   // Collapsable paragraph.
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

   // Example buttons.
   const exampleElements = document.getElementsByClassName('exampleContent');
   const exampleLength = exampleElements.length;
   const exampleButtonContainer = document.getElementById('exampleButtonContainer');

   if (!exampleButtonContainer || exampleLength === 0) {
      return;
   }

   for (let index = 1; index < exampleLength + 1; index++) {
      const button = document.createElement('button');
      button.id = `exampleButton-${index}`;
      button.className = 'btn btn-outline-secondary btn-sm me-2 py-0 px-3';
      button.textContent = `Example ${index}`;
      button.onclick = () => { showExample(index); };
      exampleButtonContainer.appendChild(button);
   }

   function showExample(idx) {
      for (let example of exampleElements) {
         example.style.display = 'none';
      }

      document.getElementById(`example-${idx}`).style.display = 'block';

      for (let i = 1; i < exampleLength + 1; i++) {
         const btn = document.getElementById(`exampleButton-${i}`);

         if (i === idx) {
            btn.classList.replace('btn-outline-secondary', 'btn-secondary');
         } else {
            btn.classList.replace('btn-secondary', 'btn-outline-secondary');
         }
      }
   }

   if (exampleLength > 0) {
      showExample(1);
   }

});
