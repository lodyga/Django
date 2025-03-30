// Initiate codeMirror instances globally
let codeEditor = null;
let solutionViewer = null;

document.addEventListener('DOMContentLoaded', loadCodeMirror)

function loadCodeMirror() {
  const codeContainer = document.getElementById('codeContainer');
  const storedDarkMode = localStorage.getItem('darkMode');
  const theme = storedDarkMode === 'enabled' ? 'monokai' : 'default';
  const storedLanguageContainer = document.getElementById('languageContainer');
  const languageId = JSON.parse(storedLanguageContainer.getAttribute('languageId'));
  const languageModes = {
    1: 'python',
    2: 'javascript',
    3: 'python',
    4: 'text/x-mysql',
    5: 'text/x-pgsql',
    6: 'text/x-java',
    7: 'text/x-c++src',
  };

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
};


// Owners Solution Textarea
const solutionToggleButton = document.getElementById('solutionToggleButton');
const solutionContentContainer = document.getElementById('solutionContentContainer');
solutionToggleButton.addEventListener('click', toggleSolutionView);

function toggleSolutionView() {
  if (solutionViewer) {
    // Remove the existing editor
    solutionViewer.toTextArea(); // Detaches from DOM
    solutionViewer = null; // Clear the editor instance; Releases reference
  }

  const storedDarkMode = localStorage.getItem('darkMode');
  const theme = storedDarkMode === 'disabled' ? 'default' : 'monokai';

  solutionViewer = CodeMirror.fromTextArea(solutionContentContainer, {
    theme: theme,
    readOnly: true,
    lineNumbers: true,
  });

  // Dynamically adjust height to fit content
  solutionViewer.setSize(null, "auto");

  // Scroll the button to the top smoothly
  setTimeout(() => {
    this.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 500);

}


// `Run` button
const submitButton = document.getElementById('submitButton');
const submitButtonSpinner = document.getElementById('submitButtonSpinner');
document.getElementById('codeForm').addEventListener('submit', submitCode)
function submitCode() {
  submitButton.disabled = true;
  submitButton.firstChild.textContent = 'Running ';
  submitButtonSpinner.classList.remove('d-none');
}