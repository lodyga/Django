let gridAlgorithmViewer;

document.addEventListener('DOMContentLoaded', () => {
   function getTheme() {
      const storedDarkMode = localStorage.getItem('darkMode');
      const theme = storedDarkMode === 'disabled' ? 'default' : 'monokai';
      return theme
   }

   const gridAlgorithmContentContainer = document.getElementById('gridAlgorithmContentContainer');
   const theme = getTheme();

   gridAlgorithmViewer = CodeMirror.fromTextArea(gridAlgorithmContentContainer, {
      mode: 'python',
      theme: theme,
      readOnly: true,
      lineNumbers: true,
   });

   gridAlgorithmViewer.setSize(null, "auto");
})