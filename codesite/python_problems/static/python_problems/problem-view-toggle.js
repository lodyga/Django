document.addEventListener('DOMContentLoaded', () => {
  const listView = document.getElementById('problemListView');
  const compactView = document.getElementById('problemCompactView');
  const gridView = document.getElementById('problemGridView');
  const listButton = document.getElementById('listViewButton');
  const compactButton = document.getElementById('compactViewButton');
  const gridButton = document.getElementById('gridViewButton');
  const filterColumn = document.getElementById('problemFilterColumn');
  const assistantColumn = document.getElementById('aiAssistantColumn');

  if (!listView || !compactView || !gridView || !listButton || !compactButton || !gridButton
      || !filterColumn || !assistantColumn) return;

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

  function updateGridColumns() {
    const hiddenColumns = Number(filterColumn.classList.contains('col-md-0'))
      + Number(assistantColumn.classList.contains('col-md-0'));
    const assistantExtended = assistantColumn.classList.contains('col-md-6');
    const columnCount = Math.max(1, 2 + hiddenColumns - Number(assistantExtended));
    gridView.classList.remove(
      'row-cols-md-1',
      'row-cols-md-2',
      'row-cols-md-3',
      'row-cols-md-4',
    );
    gridView.classList.add(`row-cols-md-${columnCount}`);
  }

  const layoutObserver = new MutationObserver(updateGridColumns);
  layoutObserver.observe(filterColumn, { attributes: true, attributeFilter: ['class'] });
  layoutObserver.observe(assistantColumn, { attributes: true, attributeFilter: ['class'] });
  updateGridColumns();

  const savedView = localStorage.getItem('problemView');
  setView(['list', 'compact', 'grid'].includes(savedView) ? savedView : 'list');
  listButton.addEventListener('click', () => setView('list'));
  compactButton.addEventListener('click', () => setView('compact'));
  gridButton.addEventListener('click', () => setView('grid'));
});
