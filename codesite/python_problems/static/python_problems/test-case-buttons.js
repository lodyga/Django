document.addEventListener('DOMContentLoaded', () => {
   // Test Case buttons.
   const testcaseElements = document.getElementsByClassName('testCaseContent');
   const testCaseLength = testcaseElements.length;
   const testCaseButtonContainer = document.getElementById('testCaseButtonContainer');
   const copyTestCasesBtn = document.getElementById('copyTestCasesBtn');
   const clipboardNode = document.getElementById('clipboardTestCases');
   const clipboardTestCases = clipboardNode ? clipboardNode.innerText : '';
   const testCaseUpdateLink = document.getElementById('testCaseUpdateLink');
   const currentUserId = testCaseUpdateLink?.dataset.currentUserId || '';

   // Collapsable paragraph.
   const testCasesWrapper = document.getElementById('problemTestCases');
   if (!testCasesWrapper) {
      return;
   }
   const testCaseCollapse = new bootstrap.Collapse(testCasesWrapper, { toggle: false });
   const testCaseToggle = document.querySelector('[data-bs-target="#problemTestCases"]');
   const icon = testCaseToggle.querySelector('i');
   const isTestCaseVisible = localStorage.getItem('testCaseState') !== 'false';
   isTestCaseVisible ? testCaseCollapse.show() : testCaseCollapse.hide();

   testCasesWrapper.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('testCaseState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      testCaseToggle.setAttribute('aria-expanded', 'true');
   });

   testCasesWrapper.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('testCaseState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      testCaseToggle.setAttribute('aria-expanded', 'false');
   });

   function buildActionUrl(linkElement, testCaseId) {
      if (!linkElement?.dataset.urlTemplate) {
         return null;
      }

      const baseUrl = linkElement.dataset.urlTemplate.replace('/0/', `/${testCaseId}/`);
      const currentHref = linkElement.getAttribute('href') || '';
      const currentUrl = new URL(currentHref, window.location.origin);
      const nextUrl = (
         linkElement.dataset.nextUrl
         || currentUrl.searchParams.get('next')
         || window.location.pathname
      );

      if (!nextUrl) {
         return baseUrl;
      }

      const params = new URLSearchParams({
         next: nextUrl,
      });

      return `${baseUrl}?${params.toString()}`;
   }

   if (testCaseButtonContainer) {
      for (let index = 1; index < testCaseLength + 1; index++) {
         const button = document.createElement('button');
         button.id = `testCaseButton-${index}`;
         button.className = 'btn btn-secondary btn-sm me-2 py-0 px-3';
         button.textContent = `Case ${index}`;
         button.onclick = () => { showTestCase(index); };
         testCaseButtonContainer.appendChild(button);
      }
   }

   function showTestCase(idx) {
      for (let testCase of testcaseElements) {
         testCase.style.display = 'none';
      }

      const selectedTestCase = document.getElementById(`testCase-${idx}`);
      selectedTestCase.style.display = 'block';

      if (testCaseUpdateLink) {
         const selectedTestCaseId = selectedTestCase?.dataset.testCaseId || '';
         const selectedOwnerId = selectedTestCase?.dataset.ownerId || '';
         const selectedSource = selectedTestCase?.dataset.source || '';
         const isCurrentUserOwner = (
            Boolean(currentUserId)
            && currentUserId === selectedOwnerId
         );
         const isSharedCase = selectedSource === 'shared';

         if (isSharedCase && isCurrentUserOwner && selectedTestCaseId) {
            testCaseUpdateLink.classList.remove('d-none');
            const updateHref = buildActionUrl(testCaseUpdateLink, selectedTestCaseId);
            if (updateHref) {
               testCaseUpdateLink.href = updateHref;
            }
         } else {
            testCaseUpdateLink.classList.add('d-none');
         }
      }

      for (let i = 1; i < testCaseLength + 1; i++) {
         const btn = document.getElementById(`testCaseButton-${i}`);
         if (!btn) {
            continue;
         }

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

   if (copyTestCasesBtn) {
      copyTestCasesBtn.addEventListener('click', () => {
         navigator.clipboard.writeText(clipboardTestCases)
            .then(() => {
               copyTestCasesBtn.classList.replace('btn-secondary', 'btn-success');
               copyTestCasesBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
               setTimeout(() => {
                  copyTestCasesBtn.innerHTML = '<i class="far fa-copy"></i> Copy';
                  copyTestCasesBtn.classList.replace('btn-success', 'btn-secondary');
               }, 2000);
            });
      });
   }

   const previewContentBtn = document.getElementById('previewContentBtn');
   const previewContents = document.querySelectorAll('.previewContent');

   if (previewContentBtn) {
      if (previewContents.length === 0) {
         previewContentBtn.checked = false;
         previewContentBtn.disabled = true;
      }

      const setPreviewVisibility = (isVisible) => {
         previewContents.forEach((content) => {
            content.style.display = isVisible ? '' : 'none';
         });
      };

      previewContentBtn.addEventListener('change', (event) => {
         setPreviewVisibility(event.target.checked);
      });

      setPreviewVisibility(previewContentBtn.checked);
   }
})
