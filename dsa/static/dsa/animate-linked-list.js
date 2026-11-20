document.addEventListener('DOMContentLoaded', () => {
   const charInput = document.getElementById('char-input');
   const listDisplay = document.getElementById('linked-list-display');
   const prependBtn = document.getElementById('prepend-btn');
   const appendBtn = document.getElementById('append-btn');
   const deleteHeadBtn = document.getElementById('delete-head-btn');
   const deleteTailBtn = document.getElementById('delete-tail-btn');
   let linkedList = ['1', '2', '3', '4', '5'];

   const createItem = (value, label = '') => {
      const item = document.createElement('div');
      item.className = 'list-item';

      const nodeWrap = document.createElement('div');
      nodeWrap.className = 'node-wrap';

      const nodeLabel = document.createElement('div');
      nodeLabel.className = 'node-label';
      nodeLabel.textContent = label;

      const node = document.createElement('div');
      node.className = 'node';
      node.textContent = value;

      nodeWrap.appendChild(nodeLabel);
      nodeWrap.appendChild(node);
      item.appendChild(nodeWrap);
      return item;
   };

   const createArrow = () => {
      const arrow = document.createElement('div');
      arrow.className = 'arrow';
      arrow.textContent = '→';
      return arrow;
   };

   const renderList = () => {
      listDisplay.innerHTML = '';
      if (linkedList.length === 0) {
         const empty = document.createElement('div');
         empty.className = 'null-label';
         empty.textContent = 'HEAD → NULL';
         listDisplay.appendChild(empty);
         return;
      }

      linkedList.forEach((value, idx) => {
         const label = idx === 0
            ? 'HEAD'
            : idx === linkedList.length - 1
               ? 'TAIL'
               : '';
         const item = createItem(value, label);
         listDisplay.appendChild(item);

         if (idx < linkedList.length - 1) {
            listDisplay.appendChild(createArrow());
         }
      });

      const nullLabel = document.createElement('div');
      nullLabel.className = 'null-label';
      nullLabel.textContent = '→ NULL';
      listDisplay.appendChild(nullLabel);
   };

   const animateAdd = (operation) => {
      const value = charInput.value.trim();
      if (!value) return;

      if (operation === 'prepend') {
         linkedList.unshift(value);
      } else {
         linkedList.push(value);
      }

      renderList();
      const index = operation === 'prepend' ? 0 : linkedList.length - 1;
      const node = listDisplay.querySelectorAll('.list-item')[index];
      if (node) {
         node.classList.add('entering');
         setTimeout(() => {
            node.classList.remove('entering');
         }, 10);
      }
   };

   const animateDelete = (operation) => {
      if (linkedList.length === 0) return;

      const items = listDisplay.querySelectorAll('.list-item');
      const index = operation === 'delete-head' ? 0 : items.length - 1;
      const node = items[index];

      if (!node) {
         linkedList = operation === 'delete-head' 
         ? linkedList.slice(1) : linkedList.slice(0, -1);
         renderList();
         return;
      }

      node.classList.add('exiting');
      setTimeout(() => {
         if (operation === 'delete-head') {
            linkedList.shift();
         } else {
            linkedList.pop();
         }
         renderList();
      }, 500);
   };

   prependBtn.addEventListener('click', () => animateAdd('prepend'));
   appendBtn.addEventListener('click', () => animateAdd('append'));
   deleteHeadBtn.addEventListener('click', () => animateDelete('delete-head'));
   deleteTailBtn.addEventListener('click', () => animateDelete('delete-tail'));

   renderList();
});
