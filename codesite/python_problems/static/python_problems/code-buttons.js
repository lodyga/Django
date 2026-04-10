document.addEventListener('DOMContentLoaded', () => {
  const codeForm = document.getElementById('codeForm');
  const runCodeButton = document.getElementById('runCodeButton');
  const testCodeButton = document.getElementById('testCodeButton');

  // `Run` button
  runCodeButton.addEventListener('click', runCode)
  function runCode() {
    document.getElementById('codeFormAction').value = 'run';
    const runCodeButtonSpinner = document.getElementById('runCodeButtonSpinner');
    runCodeButton.disabled = true;
    runCodeButton.firstChild.textContent = 'Running ';
    runCodeButtonSpinner.classList.remove('d-none');
    codeForm.submit();
  }

  // `Test` button
  testCodeButton.addEventListener('click', testCode)
  function testCode() {
    document.getElementById('codeFormAction').value = 'test';
    const testCodeButtonSpinner = document.getElementById('testCodeButtonSpinner');
    testCodeButton.disabled = true;
    testCodeButton.firstChild.textContent = 'Testing ';
    testCodeButtonSpinner.classList.remove('d-none');
    codeForm.submit();
  }

  codeForm.addEventListener('keydown', (event) => {
    if (event.ctrlKey) {
      if (event.key === "'" || event.code == 'Quote') {
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
