// CodeMirror textarea
document.addEventListener('DOMContentLoaded', loadCodeMirror)

function loadCodeMirror() {
  let storedDarkMode = localStorage.getItem('darkMode');
  let theme = storedDarkMode === 'enabled' ? 'monokai' : 'default';
  
  CodeMirror.fromTextArea(document.getElementById('code_area'), {
    mode: 'python',
    theme: theme,
    lineNumbers: true, // Enable line numbers
    autofocus: false, // Automatically focus on the editor
    // placeholder: 'Enter your Python code here...' // Placeholder text
  });
};

// Run button
document.getElementById('code_form').addEventListener('submit', submitCode) 
  function submitCode() {
    document.getElementById('submit_button').disabled = true;  // Disable the submit button
    document.getElementById('spinner').classList.remove('d-none');  // Show the spinner
    document.getElementById('submit_button').lastChild.textContent = 'Running';  // chhange 'Run' to 'Running'
  }
