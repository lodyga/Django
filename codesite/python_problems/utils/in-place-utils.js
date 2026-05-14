function runTests(method) {
  for (const inputData of inputsList) {
    const dataCopy = inputData.slice();
    method(...dataCopy);
    console.log(...dataCopy);
  }
}

// run_tests(solution.moveZeroes)
