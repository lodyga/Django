document.addEventListener('DOMContentLoaded', () => {
   const charInput = document.getElementById('char-input');
   const dequeDisplay = document.getElementById('deque-display');
   const pushLeftBtn = document.getElementById('push-left-btn');
   const pushRightBtn = document.getElementById('push-right-btn');
   const popLeftBtn = document.getElementById('pop-left-btn');
   const popRightBtn = document.getElementById('pop-right-btn');
   let deque = [];

   for (const char of ['1', '2', '3', '4', '5']) {
      deque.push(char);
      const element = document.createElement('div');
      element.className = 'deque-element entering';
      element.textContent = char;
      dequeDisplay.appendChild(element);
      setTimeout(() => {
         element.classList.remove('entering');
      }, 10);
   }

   const pushBtn = (position) => {
      const char = charInput.value.trim();
      if (char) {
         position === 'left' ? deque.unshift(char) : deque.push(char);
         const element = document.createElement('div');
         element.className = 'deque-element entering';
         element.textContent = char;
         position === 'left' ? dequeDisplay.prepend(element) : dequeDisplay.append(element);
         setTimeout(() => {
            element.classList.remove('entering');
         }, 10);
      }
   };

   const popBtn = (position) => {
      if (deque.length > 0) {
         const element = position === 'left' ? dequeDisplay.firstElementChild : dequeDisplay.lastElementChild;
         if (element) {
            element.classList.add('exiting');
            setTimeout(() => {
               dequeDisplay.removeChild(element);
               position === 'left' ? deque.shift() : deque.pop();
            }, 500);
         }
      }
   };

   pushLeftBtn.addEventListener('click', () => pushBtn('left'));
   pushRightBtn.addEventListener('click', () => pushBtn('right'));
   popLeftBtn.addEventListener('click', () => popBtn('left'));
   popRightBtn.addEventListener('click', () => popBtn('right'));
});