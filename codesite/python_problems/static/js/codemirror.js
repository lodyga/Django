// Current Solution Textarea
document.addEventListener('DOMContentLoaded', loadCodeMirror)

function loadCodeMirror() {
  let storedDarkMode = localStorage.getItem('darkMode');
  let theme = storedDarkMode === 'enabled' ? 'monokai' : 'default';

  CodeMirror.fromTextArea(document.getElementById('code_area'), {
    mode: 'python',
    // mode: 'javascript',
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
  document.getElementById('submit_button').lastChild.textContent = 'Running';  // chhange 'Run' to 'Running'
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

