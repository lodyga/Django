document.addEventListener('DOMContentLoaded', () => {
  const areTagsVisible = localStorage.getItem('tagsVisible');
  const toggleTagsButton = document.getElementById('toggleTagsButton');

  if (areTagsVisible == 'true') {
    toggleTags();
  }

  function toggleTags() {
    const tags = document.querySelectorAll('form button.tags');
    for (const tag of tags) {
      if (tag.style.display === 'none') {
        tag.style.display = 'inline-block';
        toggleTagsButton.textContent = 'Hide tags'
        localStorage.setItem('tagsVisible', 'true')
      } else {
        tag.style.display = 'none';
        toggleTagsButton.textContent = 'Show tags'
        localStorage.setItem('tagsVisible', 'false')
      }
    }
  }

  toggleTagsButton.addEventListener('click', toggleTags);
});