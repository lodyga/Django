// Toggle on/off tag buttons in problem list view
function toggleTags() {
  const tags = document.querySelectorAll('form button.tags_js');
  for (const tag of tags) {
    if (tag.style.display === 'none') {
      tag.style.display = 'inline-block';
    } else {
      tag.style.display = 'none';
    }
  }
}