document.addEventListener('DOMContentLoaded', () => {
   const charInput = document.getElementById('char-input');
   const queueDisplay = document.getElementById('queue-display');
   const pushBtn = document.getElementById('push-btn');
   const popBtn = document.getElementById('pop-btn');
   let queue = [];

   for (const char of ['1', '2'])  {
      queue.push(char);
      const element = document.createElement('div');
      element.className = 'queue-element entering';
      element.textContent = char;
      queueDisplay.appendChild(element);
         setTimeout(() => {
            element.classList.remove('entering');
         }, 10);
   }

   pushBtn.addEventListener('click', () => {
      const char = charInput.value.trim();
      if (char) {
         queue.push(char);
         const element = document.createElement('div');
         element.className = 'queue-element entering';
         element.textContent = char;
         queueDisplay.appendChild(element);
         setTimeout(() => {
            element.classList.remove('entering');
         }, 10);
         charInput.value = '';
      }
   });

   popBtn.addEventListener('click', () => {
      if (queue.length > 0) {
         const firstElement = queueDisplay.firstElementChild;
         if (firstElement) {
            firstElement.classList.add('exiting');
            setTimeout(() => {
               queueDisplay.removeChild(firstElement);
               queue.shift();
            }, 500);
         }
      }
   });
});