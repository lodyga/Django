document.addEventListener('DOMContentLoaded', () => {
  const filterColumn = document.getElementById('problemFilterColumn');
  const listContentColumn = document.getElementById('problemListContentColumn');
  const filterContent = document.getElementById('problemFilterContent');
  const visibilityButton = document.getElementById('problemFilterVisibilityButton');
  const visibilityIcon = document.getElementById('problemFilterVisibilityIcon');

  const widths = [
    { filter: 'col-md-0', content: 'col-md-11' },
    { filter: 'col-md-3', content: 'col-md-8' },
  ];
  let widthIndex = 1;

  function setWidth(index) {
    widthIndex = index;
    const width = widths[index];
    filterColumn.classList.remove(...widths.map((size) => size.filter));
    filterColumn.classList.add(width.filter);
    listContentColumn.classList.remove(...widths.map((size) => size.content));
    listContentColumn.classList.add(width.content);
    filterContent.classList.toggle('d-none', index === 0);
    visibilityIcon.classList.toggle('fa-indent', index === 0);
    visibilityIcon.classList.toggle('fa-outdent', index !== 0);
    visibilityButton.setAttribute('aria-expanded', String(index !== 0));
    visibilityButton.setAttribute('aria-label', index === 0 ? 'Show problem filters' : 'Hide problem filters');
    visibilityButton.title = index === 0 ? 'Show problem filters' : 'Hide problem filters';
  }

  setWidth(widthIndex);

  visibilityButton.addEventListener('click', () => {
    setWidth(widthIndex === 0 ? 1 : 0);
  });
});
