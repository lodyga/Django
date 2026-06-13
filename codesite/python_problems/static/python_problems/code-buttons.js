document.addEventListener('DOMContentLoaded', () => {
  const codeForm = document.getElementById('codeForm');
  const runCodeButton = document.getElementById('runCodeButton');
  const testCodeButton = document.getElementById('testCodeButton');

  function saveCodeEditor() {
    if (typeof codeEditor !== 'undefined' && codeEditor) {
      codeEditor.save();
    }
  }

  function runCode() {
    document.getElementById('codeFormAction').value = 'run';
    const runCodeButtonSpinner = document.getElementById('runCodeButtonSpinner');
    runCodeButton.disabled = true;
    runCodeButton.firstChild.textContent = 'Running ';
    runCodeButtonSpinner.classList.remove('d-none');
    saveCodeEditor();
    codeForm.submit();
  }

  function testCode() {
    document.getElementById('codeFormAction').value = 'validate';
    const testCodeButtonSpinner = document.getElementById('testCodeButtonSpinner');
    testCodeButton.disabled = true;
    testCodeButton.firstChild.textContent = 'Validating ';
    testCodeButtonSpinner.classList.remove('d-none');
    saveCodeEditor();
    codeForm.submit();
  }

  // `Run` button
  runCodeButton.addEventListener('click', runCode)

  // `Test` button
  testCodeButton.addEventListener('click', testCode)

  codeForm.addEventListener('keydown', (event) => {
    if (event.ctrlKey) {
      // event.code == 'Quote'  || 
      if (event.key === "'") {
        event.preventDefault();
        runCode();
      }
      else if (event.key === "Enter" || event.code == 'Enter') {
        event.preventDefault();
        testCode();
      }
    }
  });

});
