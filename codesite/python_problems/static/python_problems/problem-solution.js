document.addEventListener('DOMContentLoaded', () => {
   const solutionPanel = document.getElementById('solution-panel');
   const infoToggle = document.querySelector('[data-bs-target="#solution-panel"]');

   if (!solutionPanel || !infoToggle) {
      return;
   }

   const icon = infoToggle.querySelector('i');
   const solutionCollapse = new bootstrap.Collapse(solutionPanel, {
      toggle: false,
   });

   const shouldOpenFromHash = window.location.hash === '#solution-panel';
   const isProblemSolutionVisible = shouldOpenFromHash
      || localStorage.getItem('solutionPanelState') === 'true';

   if (isProblemSolutionVisible) {
      solutionCollapse.show();
      localStorage.setItem('solutionPanelState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      infoToggle.setAttribute('aria-expanded', 'true');
   } else {
      solutionCollapse.hide();
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      infoToggle.setAttribute('aria-expanded', 'false');
   }

   solutionPanel.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('solutionPanelState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      infoToggle.setAttribute('aria-expanded', 'true');
   });

   solutionPanel.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('solutionPanelState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      infoToggle.setAttribute('aria-expanded', 'false');
   });

   const solutionButtonContainer = document.getElementById('solution-button-container');
   const solutionElements = document.getElementsByClassName('solutionContent');
   const solutionLength = solutionElements.length;
   const copySolutionBtn = document.getElementById('copy-solution-btn');
   const solutionUpdateLink = document.getElementById('solutionUpdateLink');
   const currentUserId = solutionUpdateLink?.dataset.currentUserId || '';
   let clipboardSolution = '';

   function buildSolutionActionUrl(linkElement, solutionId) {
      if (!linkElement?.dataset.urlTemplate) {
         return null;
      }

      const baseUrl = linkElement.dataset.urlTemplate.replace('/0/', `/${solutionId}/`);
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

   const createUrl = solutionButtonContainer.dataset.createUrl;
   const problemId = solutionButtonContainer.dataset.problemId;
   const languageSelect = document.getElementById('language-id');
   const languageId = languageSelect?.value || solutionButtonContainer.dataset.languageId;
   const redirectUrl = solutionButtonContainer.dataset.redirectUrl;
   const createButton = document.createElement('a');
   createButton.className = 'btn btn-outline-secondary btn-sm py-0 px-3';
   createButton.textContent = '+';

   if (createUrl && problemId && languageId) {
      const params = new URLSearchParams({
         problem: problemId,
         language: languageId,
         order: (solutionLength + 1).toString(),
         next: redirectUrl,
      });
      createButton.href = `${createUrl}?${params.toString()}`;
   } else {
      createButton.href = createUrl || '#';
   }

   solutionButtonContainer.appendChild(createButton);

   function showSolution(idx) {
      const selectedSolution = document.getElementById(`solution-${idx}`);
      const selectedContent = selectedSolution?.value || '';
      const selectedSolutionId = selectedSolution?.dataset.solutionId;
      const selectedSolutionOwnerId = selectedSolution?.dataset.ownerId || '';
      const isCurrentUserOwner = (
         Boolean(solutionUpdateLink)
         && Boolean(currentUserId)
         && currentUserId === selectedSolutionOwnerId
      );

      if (typeof setSolutionViewerContent === 'function') {
         setSolutionViewerContent(selectedContent);
      }

      clipboardSolution = selectedContent;
      
      if (solutionUpdateLink) {
         if (isCurrentUserOwner && selectedSolutionId) {
            solutionUpdateLink.classList.remove('d-none');
            const updateHref = buildSolutionActionUrl(solutionUpdateLink, selectedSolutionId);

            if (updateHref) {
               solutionUpdateLink.href = updateHref;
            }
         } else {
            solutionUpdateLink.classList.add('d-none');
         }
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

   copySolutionBtn?.addEventListener('click', () => {
      navigator.clipboard.writeText(clipboardSolution)
         .then(() => {
            copySolutionBtn.classList.replace('btn-secondary', 'btn-success');
            copySolutionBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
            setTimeout(() => {
               copySolutionBtn.innerHTML = '<i class="far fa-copy"></i> Copy';
               copySolutionBtn.classList.replace('btn-success', 'btn-secondary');
            }, 2000);
         })
   });   
});
