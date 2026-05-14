/** 
 * @param {string[]} operations
 * @param {number[][]} args
 * @return {number[][]}
 */
const testInput = (operations, args) => {
   const output = []
   let timeMap;

   for (let index = 0; index < operations.length; index++) {
      const operation = operations[index];
      const argument = args[index];

      if (operation === 'TimeMap') {
         timeMap = new TimeMap(...argument);
         output.push(null);
      } else if (operation === 'set') {
         timeMap.set(...argument);
         output.push(null);
      } else if (operation === 'get') {
         output.push(timeMap.get(...argument));
      }
   };
   return output
}

// Run tests
/**
 * Run a batch of TimeMap tests and compare outputs with expected results.
 * If show_output is True, returns [(actual, expected), ...] instead of booleans.
 * @param {string[][]} operationsList 
 * @param {number[][][]} argumentsList 
 * @returns {boolean}
 */
const runTests = (operationsList, argumentsList, expectedOutputList, showOutput) => {
   const output = [];

   for (let index = 0; index < operationsList.length; index++) {
      const operations = operationsList[index];
      const args = argumentsList[index];
         output.push([testInput(operations, args)])
   }
   return output
}

runTests(operationsList, argumentsList, expectedOutputList)

