document.addEventListener('DOMContentLoaded', () => {
   const order = JSON.parse(document.getElementById("order").textContent);
   const ROWS = JSON.parse(document.getElementById("rows").textContent);
   const COLS = JSON.parse(document.getElementById("cols").textContent);

   let isAnimating = true;
   const gridContainer = document.getElementById("grid");
   //gridContainer.style.gridTemplateColumns = `repeat(${COLS}, 60px)`;
   gridContainer.style.setProperty("--cols", COLS);

   // Create grid
   for (let r = 0; r < ROWS; r++) {
      for (let c = 0; c < COLS; c++) {
         const cell = document.createElement("div");
         cell.classList.add("cell");
         cell.id = `cell-${r}-${c}`;
         gridContainer.appendChild(cell);
      }
   }
   document.getElementById("startBtn").addEventListener("click", startAnimation);
   document.getElementById("resetBtn").addEventListener("click", resetAnimation);

   function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }

   async function startAnimation() {
      isAnimating = true;

      for (const [r, c] of order) {
         if (!isAnimating) return

         const cell = document.getElementById(`cell-${r}-${c}`);

         cell.classList.add("visiting");
         await sleep(500);

         cell.classList.remove("visiting");
         cell.classList.add("visited");
         await sleep(1000);
      }
   }

   async function resetAnimation() {
      isAnimating = false;
      await sleep(500);

      for (let r = 0; r < ROWS; r++) {
         for (let c = 0; c < COLS; c++) {
            const cell = document.getElementById(`cell-${r}-${c}`);
            cell.classList.remove("visited", "visiting");
            cell.classList.add("cell");
         }
      }
   }
});