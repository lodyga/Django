document.addEventListener('DOMContentLoaded', initializeDarkMode);
function initializeDarkMode() {
  const darkModeToggle = document.getElementById('darkModeToggle');
  const darkModeLabel = document.getElementById('darkModeLabel');
  const htmlElement = document.querySelector('html');

  // Check if dark mode is enabled in local storage
  const storedDarkMode = localStorage.getItem('darkMode');
  darkModeToggle.checked = storedDarkMode === 'disabled' ? false : true;
  toggleDarkMode();

  // Function to toggle dark mode
  function toggleDarkMode() {
    const isChecked = darkModeToggle.checked;
    const darkMode = isChecked;

    darkModeLabel.textContent = isChecked ? 'Light Mode' : 'Dark Mode';

    // Update the data-bs-theme attribute of the html element
    if (darkMode) {
      htmlElement.setAttribute('data-bs-theme', 'dark');
    } else {
      htmlElement.removeAttribute('data-bs-theme');
    }

    // Store the dark mode state in local storage
    localStorage.setItem('darkMode', darkMode ? 'enabled' : 'disabled');
  }

  // Event listener for dark mode toggle
  darkModeToggle.addEventListener('change', toggleDarkMode);
}