document.addEventListener('DOMContentLoaded', () => {
   // Test Case buttons.
   const testcaseElements = document.getElementsByClassName('testCaseContent');
   const testCaseLength = testcaseElements.length;
   const testCaseButtonContainer = document.getElementById('testCaseButtonContainer');
   const copyBtn = document.getElementById('copyBtn');
   const rawTestCases = document.getElementById('rawTestCases').innerText;

   // Collapsable paragraph.
   const testCaseElements = document.getElementById('problemTestCases');
   const testCaseCollapse = new bootstrap.Collapse(testCaseElements, { toggle: false });
   const testCaseToggle = document.querySelector('[data-bs-target="#problemTestCases"]');
   const icon = testCaseToggle.querySelector('i');
   const isTestCaseVisible = localStorage.getItem('testCaseState') !== 'false';
   isTestCaseVisible ? testCaseCollapse.show() : testCaseCollapse.hide();

   testCaseElements.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('testCaseState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      testCaseToggle.setAttribute('aria-expanded', 'true');
   });

   testCaseElements.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('testCaseState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      testCaseToggle.setAttribute('aria-expanded', 'false');
   });

   for (let index = 1; index < testCaseLength + 1; index++) {
      const button = document.createElement('button');
      button.id = `testCaseButton-${index}`;
      button.className = 'btn btn-secondary btn-sm me-2 py-0 px-3';
      button.textContent = `Case ${index}`;
      button.onclick = (event) => { showTestCase(index); }
      testCaseButtonContainer.appendChild(button);
   };

   function showTestCase(idx) {
      for (let testCase of testcaseElements) {
         testCase.style.display = 'none';
      }

      document.getElementById(`testCase-${idx}`).style.display = 'block';

      for (let i = 1; i < testCaseLength + 1; i++) {
         const btn = document.getElementById(`testCaseButton-${i}`);

         if (i === idx) {
            btn.classList.replace('btn-outline-secondary', 'btn-secondary');
         } else {
            btn.classList.replace('btn-secondary', 'btn-outline-secondary');
         }
      }
   };

   if (testCaseLength > 0) {
      showTestCase(1);
   }

   copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(rawTestCases)
         .then(() => {
            copyBtn.classList.replace('btn-secondary', 'btn-success');
            copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
               copyBtn.innerHTML = '<i class="far fa-copy"></i> Copy';
               copyBtn.classList.replace('btn-success', 'btn-secondary');
            }, 2000);
         })
   });

});