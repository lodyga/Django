// Current Solution Textarea
document.addEventListener('DOMContentLoaded', loadCodeMirror)

function loadCodeMirror() {
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

  CodeMirror.fromTextArea(document.getElementById('codeArea'), {
    mode: languageModes[languageId] || 'text',
    theme: theme,
    // tabSize: 4,
    indentUnit: 4, // Set indentation to 4 spaces (for Python)
    matchBrackets: true,
    autoCloseBrackets: true,
    lineNumbers: true, // Enable line numbers
    autofocus: false, // Automatically focus on the editor
    // placeholder: 'Enter your Python code here...' // Placeholder text
  });
};

// Current Solution Run button
document.getElementById('code_form').addEventListener('submit', submitCode)
function submitCode() {
  document.getElementById('submit_button').disabled = true;  // Disable the submit button
  document.getElementById('spinner').classList.remove('d-none');  // Show the spinner
  document.getElementById('submit_button').lastChild.textContent = 'Running';  // change 'Run' to 'Running'
}


// Owners Solution Textarea
document.getElementById('buttonCollapse').addEventListener('click', collapseButton);
let editor = null; // Store the editor instance globally

function collapseButton() {
  if (editor) {
    // Remove the existing editor
    editor.toTextArea(); // Revert the editor back to a <textarea>
    editor = null; // Clear the editor instance
  }

  let storedDarkMode = localStorage.getItem('darkMode');
  let theme = storedDarkMode === 'enabled' ? 'monokai' : 'default';

  editor = CodeMirror.fromTextArea(document.getElementById('ownerSolutionTextarea'), {
    theme: theme,
    readOnly: true,
    lineNumbers: true,
  });

  // Dynamically adjust height to fit content
  editor.setSize(null, "auto");

  // Scroll the button to the top smoothly
  setTimeout(() => {
    this.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }, 500);

}

