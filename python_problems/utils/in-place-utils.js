function runTests(method) {
  for (const inputData of inputsList) {
    const dataCopy = inputData.slice();
    method(...dataCopy);
    console.log(JSON.stringify(...dataCopy));
  }
}

// run_tests(solution.moveZeroes)
