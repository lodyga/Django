document.addEventListener('DOMContentLoaded', loadTestCaseButtons);
function loadTestCaseButtons() {
  const testCaseContainer = document.getElementById('testCaseContainer');
  const testCaseLength = JSON.parse(testCaseContainer.getAttribute('testCaseLength'));
  const buttonsContainer = document.getElementById('buttonsContainer');

  // Create buttons
  for (let index = 1; index < testCaseLength + 1; index++) {
    // Create a button
    const button = document.createElement('button');
    button.className = 'btn btn-secondary btn-sm me-2 py-0 px-3';
    button.textContent = index;
    button.onclick = (event) => {
      showTestCase(index);
    }
    buttonsContainer.appendChild(button);
  };

  function showTestCase(index) {
    // Hide all test cases
    const testcaseElements = document.getElementsByClassName('test_case_content');
    for (let testCase of testcaseElements) {
      testCase.style.display = 'none';
    }

    // Show selected test case
    document.getElementById(`testCase-${index}`).style.display = 'block';
  }

  // Show the first test case by default
  if (testCaseLength > 0) {
    showTestCase(1);
  }
}

document.getElementById('copyButton').addEventListener('click', function () {
  const rawTestCases = document.getElementById('rawTestCases').innerText;
  // Copy to clipboard
  navigator.clipboard.writeText(rawTestCases)
    .then(() => {
      // Show success message
      const copyButton = document.getElementById('copyButton');
      copyButton.classList.replace('btn-secondary', 'btn-success');
      copyButton.innerHTML = '<i class="fas fa-check"></i> Copied!';
      setTimeout(() => {
        copyButton.innerHTML = '<i class="far fa-copy"></i> Copy';
        copyButton.classList.replace('btn-success', 'btn-secondary');
      }, 2000);
    })
});