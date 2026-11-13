document.addEventListener('DOMContentLoaded', () => {
  const listView = document.getElementById('problemListView');
  const compactView = document.getElementById('problemCompactView');
  const gridView = document.getElementById('problemGridView');
  const listButton = document.getElementById('listViewButton');
  const compactButton = document.getElementById('compactViewButton');
  const gridButton = document.getElementById('gridViewButton');

  if (!listView || !compactView || !gridView || !listButton || !compactButton || !gridButton) return;

  function setView(view) {
    listView.classList.toggle('d-none', view !== 'list');
    compactView.classList.toggle('d-none', view !== 'compact');
    gridView.classList.toggle('d-none', view !== 'grid');
    listButton.classList.toggle('active', view === 'list');
    compactButton.classList.toggle('active', view === 'compact');
    gridButton.classList.toggle('active', view === 'grid');
    listButton.setAttribute('aria-pressed', String(view === 'list'));
    compactButton.setAttribute('aria-pressed', String(view === 'compact'));
    gridButton.setAttribute('aria-pressed', String(view === 'grid'));
    localStorage.setItem('problemView', view);
  }

  const savedView = localStorage.getItem('problemView');
  setView(['list', 'compact', 'grid'].includes(savedView) ? savedView : 'list');
  listButton.addEventListener('click', () => setView('list'));
  compactButton.addEventListener('click', () => setView('compact'));
  gridButton.addEventListener('click', () => setView('grid'));
});
