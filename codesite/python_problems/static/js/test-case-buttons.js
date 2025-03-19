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