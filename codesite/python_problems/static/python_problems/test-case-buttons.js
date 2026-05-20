document.addEventListener('DOMContentLoaded', () => {
   // Test Case buttons.
   const problemTestCaseElements = document.getElementsByClassName('problemTestCaseContent');
   const problemTestCaseLength = problemTestCaseElements.length;
   const problemTestCaseButtonContainer = document.getElementById('problemTestCaseButtonContainer');
   const copyProblemTestCasesBtn = document.getElementById('copyProblemTestCasesBtn');
   const clipboardNode = document.getElementById('clipboardProblemTestCases');
   const clipboardProblemTestCases = clipboardNode ? clipboardNode.innerText : '';
   const problemTestCaseUpdateLink = document.getElementById('problemTestCaseUpdateLink');
   const currentUserId = problemTestCaseUpdateLink?.dataset.currentUserId || '';

   // Collapsable paragraph.
   const problemTestCasesWrapper = document.getElementById('problemTestCases');
   if (!problemTestCasesWrapper) {
      return;
   }
   const problemTestCaseCollapse = new bootstrap.Collapse(problemTestCasesWrapper, { toggle: false });
   const problemTestCaseToggle = document.querySelector('[data-bs-target="#problemTestCases"]');
   const icon = problemTestCaseToggle.querySelector('i');
   const isProblemTestCaseVisible = localStorage.getItem('problemTestCaseState') !== 'false';
   isProblemTestCaseVisible ? problemTestCaseCollapse.show() : problemTestCaseCollapse.hide();

   problemTestCasesWrapper.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('problemTestCaseState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      problemTestCaseToggle.setAttribute('aria-expanded', 'true');
   });

   problemTestCasesWrapper.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('problemTestCaseState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      problemTestCaseToggle.setAttribute('aria-expanded', 'false');
   });

   function buildActionUrl(linkElement, problemTestCaseId) {
      if (!linkElement?.dataset.urlTemplate) {
         return null;
      }

      const baseUrl = linkElement.dataset.urlTemplate.replace('/0/', `/${problemTestCaseId}/`);
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

   if (problemTestCaseButtonContainer) {
      for (let index = 1; index < problemTestCaseLength + 1; index++) {
         const button = document.createElement('button');
         button.id = `problemTestCaseButton-${index}`;
         button.className = 'btn btn-secondary btn-sm me-2 py-0 px-3';
         button.textContent = `Case ${index}`;
         button.onclick = () => { showProblemTestCase(index); };
         problemTestCaseButtonContainer.appendChild(button);
      }
   }

   function showProblemTestCase(idx) {
      for (let problemTestCase of problemTestCaseElements) {// problem
         problemTestCase.style.display = 'none';
      }

      const selectedProblemTestCase = document.getElementById(`problemTestCase-${idx}`);
      selectedProblemTestCase.style.display = 'block';

      if (problemTestCaseUpdateLink) {
         const selectedProblemTestCaseId = selectedProblemTestCase?.dataset.problemTestCaseId || '';
         const selectedOwnerId = selectedProblemTestCase?.dataset.ownerId || '';
         const selectedSource = selectedProblemTestCase?.dataset.source || '';
         const isCurrentUserOwner = (
            Boolean(currentUserId)
            && currentUserId === selectedOwnerId
         );
         const isSharedCase = selectedSource === 'shared';

         if (isSharedCase && isCurrentUserOwner && selectedProblemTestCaseId) {
            problemTestCaseUpdateLink.classList.remove('d-none');
            const updateHref = buildActionUrl(problemTestCaseUpdateLink, selectedProblemTestCaseId);
            if (updateHref) {
               problemTestCaseUpdateLink.href = updateHref;
            }
         } else {
            problemTestCaseUpdateLink.classList.add('d-none');
         }
      }

      for (let i = 1; i < problemTestCaseLength + 1; i++) {
         const btn = document.getElementById(`problemTestCaseButton-${i}`);
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

   if (problemTestCaseLength > 0) {
      showProblemTestCase(1);
   }

   if (copyProblemTestCasesBtn) {
      copyProblemTestCasesBtn.addEventListener('click', () => {
         navigator.clipboard.writeText(clipboardProblemTestCases)
            .then(() => {
               copyProblemTestCasesBtn.classList.replace('btn-secondary', 'btn-success');
               copyProblemTestCasesBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
               setTimeout(() => {
                  copyProblemTestCasesBtn.innerHTML = '<i class="far fa-copy"></i> Copy';
                  copyProblemTestCasesBtn.classList.replace('btn-success', 'btn-secondary');
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
