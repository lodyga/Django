/**
 * @param {Function} cls
 * @param {string[]} operations
 * @param {Array<Array<any>>} args
 * @return {Array<any>}
 */
const testInput = (cls, operations, args) => {
   const output = [];
   let instance;

   for (let idx = 0; idx < operations.length; idx++) {
      const operation = operations[idx];
      const argument = args[idx];

      // Constructor
      if (operation === cls.name) {
         instance = new cls(...argument);
         output.push(null);
         continue;
      }

      // Method call
      // method = instance[operation];
      // result = method(...argument);
      // can break when the method uses this.
      const result = instance[operation](...argument);
      output.push(result);
   }

   return output;
}

// Run tests
/**
 * @param {Function} cls
 * @param {string[][]} operationsList 
 * @param {number[][][]} argumentsList 
 * @returns {boolean}
 */
const runTests = (cls, operationsList, argumentsList) => {
   const output = [];

   for (let idx = 0; idx < operationsList.length; idx++) {
      const operations = operationsList[idx];
      const args = argumentsList[idx];
      console.log(JSON.stringify(testInput(cls, operations, args)));
   }

   return output;
}

// runTests(MinStack, operationsList, argumentsList)
