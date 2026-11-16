document.addEventListener('DOMContentLoaded', initializeDarkMode)

function initializeDarkMode() {
  const htmlDocument = document.querySelector('html');
  const storedColor = localStorage.getItem('appearanceColor');
  const storedDarkMode = localStorage.getItem('darkMode');
  let colorPreference = ['automatic', 'light', 'dark'].includes(storedColor)
    ? storedColor
    : storedDarkMode === 'disabled' ? 'light'
      : storedDarkMode === 'enabled' ? 'dark' : 'automatic';
  const colorScheme = window.matchMedia('(prefers-color-scheme: dark)');

  if (!htmlDocument) {
    return;
  }

  applyColorPreference(colorPreference);

  document.addEventListener('appearance-color-change', (event) => {
    const color = event.detail?.color;
    if (['automatic', 'light', 'dark'].includes(color)) {
      applyColorPreference(color);
    }
  });

  colorScheme.addEventListener('change', () => {
    if (colorPreference === 'automatic') applyColorPreference(colorPreference);
  });

  function applyColorPreference(preference) {
    colorPreference = preference;
    const darkMode = preference === 'dark'
      || (preference === 'automatic' && colorSchemeMatchesDark());

    if (darkMode) {
      htmlDocument.setAttribute('data-bs-theme', 'dark');
    } else {
      htmlDocument.removeAttribute('data-bs-theme');
    }

    localStorage.setItem('appearanceColor', preference);
    localStorage.setItem('darkMode', darkMode ? 'enabled' : 'disabled');
    updateCodeMirrorThemes();
  };

  function colorSchemeMatchesDark() {
    return window.matchMedia('(prefers-color-scheme: dark)').matches;
  }

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

};
