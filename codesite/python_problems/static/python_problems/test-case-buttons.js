document.addEventListener('DOMContentLoaded', () => {
   const testcaseElements = document.getElementsByClassName('testCaseContent');
   const testCaseLength = testcaseElements.length;
   const testCaseButtonContainer = document.getElementById('testCaseButtonContainer');
   const copyBtn = document.getElementById('copyBtn');
   const rawTestCases = document.getElementById('rawTestCases').innerText;

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