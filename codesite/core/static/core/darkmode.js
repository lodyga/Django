document.addEventListener('DOMContentLoaded', initializeDarkMode)

function initializeDarkMode() {
  const darkModeToggle = document.getElementById('darkModeToggle');
  const darkModeLabel = document.getElementById('darkModeLabel');
  const htmlDocument = document.querySelector('html');
  const storedDarkMode = localStorage.getItem('darkMode');

  if (!darkModeToggle || !darkModeLabel || !htmlDocument) {
    return;
  }

  darkModeToggle.checked = storedDarkMode === 'disabled' ? false : true;
  toggleDarkMode();

  function toggleDarkMode() {
    const darkMode = darkModeToggle.checked;

    if (darkMode) {
      darkModeLabel.textContent = 'Light Mode';
      htmlDocument.setAttribute('data-bs-theme', 'dark');
      localStorage.setItem('darkMode', 'enabled');
    } else {
      darkModeLabel.textContent = 'Dark Mode';
      htmlDocument.removeAttribute('data-bs-theme');
      localStorage.setItem('darkMode', 'disabled');
    }

    updateCodeMirrorThemes();
  };

  function updateCodeMirrorThemes() {
    const storedDarkMode = localStorage.getItem('darkMode');
    const theme = storedDarkMode === 'disabled' ? 'default' : 'monokai';

    if (typeof codeEditor !== 'undefined' && codeEditor) {
      codeEditor.setOption('theme', theme)
    }

    if (typeof solutionViewer !== 'undefined' && solutionViewer) {
      solutionViewer.setOption('theme', theme)
    }

    if (typeof gridAlgorithmViewer !== 'undefined' && gridAlgorithmViewer) {
      gridAlgorithmViewer.setOption('theme', theme)
    }
  };

  darkModeToggle.addEventListener('change', toggleDarkMode);
};
