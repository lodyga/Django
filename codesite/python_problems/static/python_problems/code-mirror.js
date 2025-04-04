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
  const storedLanguageContainer = document.getElementById('languageContainer');
  const languageId = JSON.parse(storedLanguageContainer.getAttribute('languageId'));
  return languageId
}


document.addEventListener('DOMContentLoaded', loadCodeMirror)
function loadCodeMirror() {
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

  codeEditor.setSize(null, "auto");


  const solutionContentContainer = document.getElementById('solutionContentContainer');
  solutionViewer = CodeMirror.fromTextArea(solutionContentContainer, {
    mode: languageModes[languageId] || 'text',
    theme: theme,
    readOnly: true,
    lineNumbers: true,
  });
  solutionViewer.setSize(null, "auto");
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

  const theme = getTheme();
  const languageId = getLanguageId();

  solutionViewer = CodeMirror.fromTextArea(solutionContentContainer, {
    mode: languageModes[languageId] || 'text',
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
