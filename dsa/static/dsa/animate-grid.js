document.addEventListener("DOMContentLoaded", () => {
   let order = JSON.parse(document.getElementById("order").textContent);
   let rows = JSON.parse(document.getElementById("rows").textContent);
   let cols = JSON.parse(document.getElementById("cols").textContent);
   let animationId = 0;

   const startBtn = document.getElementById("startBtn");
   const resetBtn = document.getElementById("resetBtn");
   const gridContainer = document.getElementById("grid");
   const inputPath = document.getElementById("inputPath");
   const feedback = document.getElementById("inputPathFeedback");
   const testCaseForm = document.getElementById("testCaseForm");
   const testCaseInput = document.getElementById("testCaseInput");
   const testCaseFeedback = document.getElementById("testCaseInputFeedback");
   const solveTestCaseBtn = document.getElementById("solveTestCaseBtn");

   renderGrid();
   showValidFeedback(order.length);
   updateTestCaseValidity(!testCaseFeedback.textContent.trim());
   inputPath.addEventListener("input", updatePath);
   testCaseInput.addEventListener("input", () => updateTestCaseValidity(true));
   testCaseForm.addEventListener("submit", event => {
      if (!updateTestCaseValidity(true)) event.preventDefault();
   });
   startBtn.addEventListener("click", startAnimation);
   resetBtn.addEventListener("click", resetAnimation);

   function parsePath(value) {
      let parsed;
      try {
         parsed = JSON.parse(value);
      } catch {
         return null;
      }

      if (!Array.isArray(parsed) || !parsed.every(pair =>
         Array.isArray(pair)
         && pair.length === 2
         && pair.every(coordinate =>
            Number.isSafeInteger(coordinate) && coordinate >= 0
         )
      )) {
         return null;
      }

      return parsed;
   }

   function isValidTestCase(value) {
      let parsed;
      try {
         parsed = JSON.parse(value.replaceAll("'", '"'));
      }
      catch {
         return false;
      }

      if (!Array.isArray(parsed) || parsed.length === 0 || !Array.isArray(parsed[0])) {
         return false;
      }

      const columnCount = parsed[0].length;
      return columnCount > 0 && parsed.every(row =>
         Array.isArray(row)
         && row.length === columnCount
         && row.every(cell => cell === "0" || cell === "1")
      );
   }

   function updateTestCaseValidity(showFeedback) {
      const isValid = isValidTestCase(testCaseInput.value);
      solveTestCaseBtn.disabled = !isValid;

      if (!isValid) {
         testCaseInput.classList.add("is-invalid");
         testCaseInput.setAttribute("aria-invalid", "true");
         testCaseFeedback.className = "form-text text-danger";
         testCaseFeedback.textContent = "Enter a non-empty rectangular grid containing only the strings \"0\" or \"1\".";
         return false;
      }

      testCaseInput.classList.remove("is-invalid");
      testCaseInput.removeAttribute("aria-invalid");
      if (showFeedback) {
         testCaseFeedback.className = "form-text text-success";
         testCaseFeedback.textContent = "Valid grid.";
      }
      return true;
   }

   function updatePath() {
      const newOrder = parsePath(inputPath.value);
      if (newOrder === null) {
         inputPath.classList.add("is-invalid");
         inputPath.setAttribute("aria-invalid", "true");
         feedback.className = "form-text text-danger";
         feedback.textContent = "Enter a JSON list of non-negative integer pairs, for example [[0, 0], [1, 0]].";
         return;
      }

      order = newOrder;
      const gridSize = order.reduce((size, [row, col]) => ({
         rows: Math.max(size.rows, row + 1),
         cols: Math.max(size.cols, col + 1),
      }), { rows: 0, cols: 0 });
      rows = gridSize.rows;
      cols = gridSize.cols;
      inputPath.classList.remove("is-invalid");
      inputPath.removeAttribute("aria-invalid");
      showValidFeedback(order.length);
      renderGrid();
   }

   function showValidFeedback(pointCount) {
      feedback.className = "form-text text-success";
      feedback.textContent = `Valid path (${pointCount} ${pointCount === 1 ? "point" : "points"}).`;
   }

   function renderGrid() {
      animationId++;
      gridContainer.replaceChildren();
      gridContainer.style.setProperty("--cols", cols);

      for (let row = 0; row < rows; row++) {
         for (let col = 0; col < cols; col++) {
            const cell = document.createElement("div");
            cell.classList.add("cell");
            cell.id = `cell-${row}-${col}`;
            gridContainer.appendChild(cell);
         }
      }
   }

   function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }

   async function startAnimation() {
      const currentAnimationId = ++animationId;

      for (const [row, col] of order) {
         if (currentAnimationId !== animationId) return;

         const cell = document.getElementById(`cell-${row}-${col}`);
         cell.classList.add("visiting");
         await sleep(500);

         if (currentAnimationId !== animationId) return;
         cell.classList.remove("visiting");
         cell.classList.add("visited");
         await sleep(1000);
      }
   }

   function resetAnimation() {
      animationId++;
      gridContainer.querySelectorAll(".cell").forEach(cell => {
         cell.classList.remove("visited", "visiting");
      });
   }
});
