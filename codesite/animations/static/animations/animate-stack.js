document.addEventListener('DOMContentLoaded', () => {
   const charInput = document.getElementById('char-input');
   const stackDisplay = document.getElementById('stack-display');
   const pushBtn = document.getElementById('push-btn');
   const popBtn = document.getElementById('pop-btn');
   let stack = [];

   function resizeElements() {
      const elements = stackDisplay.children;
      const num = elements.length;
      if (num === 0) return;
      const containerHeight = 600;
      const totalMargin = 10 * num;
      const availableHeight = containerHeight - totalMargin;
      const size = Math.max(20, Math.min(50, availableHeight / num));
      for (let el of elements) {
         el.style.width = size + 'px';
         el.style.height = size + 'px';
         el.style.lineHeight = size + 'px';
         el.style.fontSize = Math.max(12, size * 0.48) + 'px';
      }
   }

   for (const char of ['1', '2', '3', '4', '5']) {
      stack.push(char);
      const element = document.createElement('div');
      element.className = 'stack-element entering';
      element.textContent = char;
      stackDisplay.prepend(element);
      setTimeout(() => {
         element.classList.remove('entering');
         resizeElements();
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
            resizeElements();
         }, 10);
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
               resizeElements();
            }, 500);
         }
      }
   });

});