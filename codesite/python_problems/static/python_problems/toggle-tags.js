document.addEventListener('DOMContentLoaded', () => {
  const aretagsVisible = localStorage.getItem('tagsVisible');
  const toggleButton = document.getElementById('toggleTags');

  if (aretagsVisible == 'true') {
    toggleTags();
  }

  function toggleTags() {
    const tags = document.querySelectorAll('form button.tags');
    for (const tag of tags) {
      if (tag.style.display === 'none') {
        tag.style.display = 'inline-block';
        toggleButton.textContent = 'Hide tags'
        localStorage.setItem('tagsVisible', 'true')
      } else {
        tag.style.display = 'none';
        toggleButton.textContent = 'Show tags'
        localStorage.setItem('tagsVisible', 'false')
      }
    }
  }

  toggleButton.addEventListener('click', toggleTags);
});