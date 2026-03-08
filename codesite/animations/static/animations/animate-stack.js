document.addEventListener('DOMContentLoaded', () => {
   const charInput = document.getElementById('char-input');
   const stackDisplay = document.getElementById('stack-display');
   const pushBtn = document.getElementById('push-btn');
   const popBtn = document.getElementById('pop-btn');
   let stack = [];

   for (const char of ['1', '2'])  {
      stack.push(char);
      const element = document.createElement('div');
      element.className = 'stack-element entering';
      element.textContent = char;
      stackDisplay.prepend(element);
         setTimeout(() => {
            element.classList.remove('entering');
         }, 10);
   }

   pushBtn.addEventListener('click', () => {
      const char = charInput.value.trim();
      if (char) {
         stack.push(char);
         const element = document.createElement('div');
         element.className = 'stack-element entering';
         element.textContent = char;
         stackDisplay.prepend(element);
         setTimeout(() => {
            element.classList.remove('entering');
         }, 10);
         charInput.value = '';
      }
   });

   popBtn.addEventListener('click', () => {
      if (stack.length > 0) {
         const lastElement = stackDisplay.firstElementChild;
         if (lastElement) {
            lastElement.classList.add('exiting');
            setTimeout(() => {
               stackDisplay.removeChild(lastElement);
               stack.pop();
            }, 500);
         }
      }
   });
});