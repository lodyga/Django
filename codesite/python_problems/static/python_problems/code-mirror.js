// Initiate codeMirror instances globally
let codeEditor = null;
let solutionViewer = null;
const languageModes = {
   1: 'python',
   2: 'javascript',
   3: 'python',
   4: 'text/x-mysql',
   5: 'text/x-pgsql',
   6: 'text/x-java',
   7: 'text/x-c++src',
}

function getTheme() {
   const storedDarkMode = localStorage.getItem('darkMode');
   const theme = storedDarkMode === 'disabled' ? 'default' : 'monokai';
   return theme
}

function getLanguageId() {
   return JSON.parse(document.getElementById('languageId').textContent);
}

function ensureSolutionViewer() {
   const solutionContentContainer = document.getElementById('solutionContentContainer');
   if (!solutionContentContainer) {
      return;
   }

   if (!solutionViewer) {
      const theme = getTheme();
      const languageId = getLanguageId();

      solutionViewer = CodeMirror.fromTextArea(solutionContentContainer, {
         mode: languageModes[languageId] || 'text',
         theme: theme,
         readOnly: true,
         lineNumbers: true,
      });

      solutionViewer.setSize(null, 'auto');
      return;
   }

   solutionViewer.refresh();
}


document.addEventListener('DOMContentLoaded', () => {
   // Collapsable paragraph.
   const problemCodeElements = document.getElementById('problemCode');
   const codeCollapse = new bootstrap.Collapse(problemCodeElements, { toggle: false });
   const codeToggle = document.querySelector('[data-bs-target="#problemCode"]');
   const icon = codeToggle.querySelector('i');
   const isProblemCodeVisible = localStorage.getItem('problemCodeState') !== 'false';
   isProblemCodeVisible ? codeCollapse.show() : codeCollapse.hide();

   problemCodeElements.addEventListener('shown.bs.collapse', () => {
      localStorage.setItem('problemCodeState', 'true');
      icon.classList.replace('fa-chevron-down', 'fa-chevron-up');
      codeToggle.setAttribute('aria-expanded', 'true');
   });

   problemCodeElements.addEventListener('hidden.bs.collapse', () => {
      localStorage.setItem('problemCodeState', 'false');
      icon.classList.replace('fa-chevron-up', 'fa-chevron-down');
      codeToggle.setAttribute('aria-expanded', 'false');
   });

   const codeContainer = document.getElementById('codeContainer');
   const theme = getTheme();
   const languageId = getLanguageId();

   codeEditor = CodeMirror.fromTextArea(codeContainer, {
      mode: languageModes[languageId] || 'text',
      theme: theme,
      // tabSize: 4,
      indentUnit: 4,
      matchBrackets: true,
      autoCloseBrackets: true,
      lineNumbers: true,
      autofocus: false,
   });

   codeEditor.setSize(null, 'auto');

   const problemSolution = document.getElementById('problemSolution');
   if (problemSolution) {
      problemSolution.addEventListener('shown.bs.collapse', () => {
         ensureSolutionViewer();
      });

      if (problemSolution.classList.contains('show') || window.location.hash === '#problemSolution') {
         ensureSolutionViewer();
      }
   }
});
