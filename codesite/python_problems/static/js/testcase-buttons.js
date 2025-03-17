// testCasesData.dataset
// testCasesData.getAttribute('data-test-cases')

document.addEventListener('DOMContentLoaded', loadTestcaseButtons);
    
function loadTestcaseButtons() {
  //const testCases = {{ testcases|safe }};
  // const container = document.getElementById("testcase-container");
  // const testCases = JSON.parse(container.getAttribute("data-testcases"));
  const testCasesContainer = document.getElementById('testCasesContainer');
  const testCases = JSON.parse(testCasesContainer.dataset.testCases);
  
  //const testCasesData = document.getElementById('testCasesData');
  //const testCases = JSON.parse(testCasesData.dataset.testCases);
  //const testCases = JSON.parse(testCasesData.dataset.testCases);

  const buttonsContainer = document.getElementById('buttons_container');
  const testcasesContainer = document.getElementById('testcases_container');

  testCases.forEach((testCase, index) => {
    // Create button
    const button = document.createElement('button');
    button.className = 'btn btn-secondary btn-sm me-2 py-0 px-3';
    button.textContent = index + 1;
    button.onclick = (event) => {
      // event.preventDefault();
      showTestCase(index + 1);
    }
    buttonsContainer.appendChild(button);
  });

  function showTestCase(index) {
    // Hide all test cases
    const testcaseElements = document.getElementsByClassName('testcase-content');
    for (let testcase of testcaseElements) {
      testcase.style.display = 'none';
    }
    
    // Show selected test case
    document.getElementById(`testcase-${index}`).style.display = 'block';
  }

  // Show the first test case by default
  if (testCases.length > 0) {
    showTestCase(1);
  }
}