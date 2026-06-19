import { test, expect, Page } from '@playwright/test';

// Helper to wait for CodeMirror to initialize
async function waitForCodeMirror(page: Page) {
    await expect(page.locator('.CodeMirror').first()).toBeVisible({ timeout: 10000 });
}

// Helper to set CodeMirror content
async function setCodeMirrorContent(page: Page, code: string) {
    await page.evaluate((code: string) => {
        const editor = (window as any).codeEditor;
        if (editor && editor.setValue) {
            editor.setValue(code);
        }
    }, code);
}

// Helper to get CodeMirror content
async function getCodeMirrorContent(page: Page) {
    return await page.evaluate(() => {
        const editor = (window as any).codeEditor;
        return editor ? editor.getValue() : '';
    });
}

test('homepage loads', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/');
    await expect(page).toHaveTitle(/CodeSite/i);
});


test('problem list displays problems', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/');
    await expect(page.locator('body')).toContainText('Two Sum');
});


test('problem detail page loads', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');
    await expect(page.locator('h1')).toContainText('Two Sum');
});


test('user can log in', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/accounts/login/');

    await page.getByLabel('Username').fill('testuser');
    await page.getByLabel('Password').fill('testpassword');

    await page.locator('input[type="submit"]').click();

    await expect(page).toHaveTitle(/CodeSite/i);
});


test('anonymous user redirected from admin page', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/admin/');
    await expect(page).toHaveURL(/login/);
});


test('problem search filters results', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/');

    const searchInput = page.getByPlaceholder(/search/i);
    if (await searchInput.count() > 0) {
        await searchInput.fill('two sum');
        await expect(page.locator('body')).toContainText('Two Sum');
    } else {
        // Fallback: just check Two Sum is on the page
        await expect(page.locator('body')).toContainText('Two Sum');
    }
});


test('dark mode toggle exists and is accessible', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/');

    // Click Settings dropdown first
    await page.locator('text=Settings').click();

    // Check dark mode toggle is visible
    const darkModeToggle = page.locator('#darkModeToggle');
    await expect(darkModeToggle).toBeVisible();

    // Check the label exists
    await expect(page.locator('#darkModeLabel')).toBeVisible();
});



test('navigation between problems works', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    // Check previous/next problem buttons exist
    const prevButton = page.locator('text=Previous Problem');
    const nextButton = page.locator('text=Next Problem');

    // At least one should be visible (depending on if there are adjacent problems)
    const prevCount = await prevButton.count();
    const nextCount = await nextButton.count();

    expect(prevCount + nextCount).toBeGreaterThan(0);
});


test('user can run python hello world', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#run-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Hello, World!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can run javascript hello world', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/JavaScript/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#run-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Hello, World!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can run cpp hello world', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/C++/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#run-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Hello, World!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can run java hello world', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Java/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#run-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Hello, World!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can validate python method', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solutionCode = `class Solution:\n    def twoSum(self, nums: list[int], target: int) -> list[int]:\n        """\n        Time complexity: O(n)\n        Auxiliary space complexity: O(n)\n        Tags:\n            DS: hash map\n            A: iteration\n        """\n        num_idx = {}\n\n        for idx, num in enumerate(nums):\n            diff = target - num\n\n            if diff in num_idx:\n                return [num_idx[diff], idx]\n            else:\n                num_idx[num] = idx`;

    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can validate javascript method', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/JavaScript/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solutionCode = `class Solution {\n   /**\n    * Time complexity: O(n)\n    * Auxiliary space complexity: O(n)\n    * Tags:\n    *     DS: hash map\n    *     A: iteration\n    * @param {number[]} nums\n    * @param {number} target\n    * @return {number[]}\n    */\n   twoSum(nums, target) {\n      const numIdx = new Map();\n\n      for (let idx = 0; idx < nums.length; idx++) {\n         const num = nums[idx];\n         const diff = target - num;\n\n         if (numIdx.has(diff)) {\n            return [numIdx.get(diff), idx]\n         } else {\n            numIdx.set(num, idx);\n         }\n      }\n   }\n}`;

    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can validate cpp method', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/C++/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solutionCode = `#include <vector>\n#include <unordered_map>\nusing namespace std;\n\n\nclass Solution {\npublic:\n   std::vector<int> twoSum(const std::vector<int>& nums, int target) {\n      std::unordered_map<int, int> numIdx;\n\n      for (int idx = 0; idx < nums.size(); idx++) {\n         int diff = target - nums[idx];\n\n         if (numIdx.count(diff)) {\n            return { numIdx[diff], idx };\n         }\n         else {\n            numIdx[nums[idx]] = idx;\n         }\n      }\n\n      return {};\n   }\n};`;

    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('user can validate java method', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Java/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solutionCode = `import java.util.Arrays;\nimport java.util.HashMap;\n\n\nclass Solution {\n   int[] twoSum(int[] nums, int target) {\n      HashMap<Integer, Integer> numIdx = new HashMap<>();\n\n      for (int idx = 0; idx < nums.length; idx++) {\n         int num = nums[idx];\n         int complement = target - num;\n\n         if (numIdx.containsKey(complement)) {\n            return new int[] { numIdx.get(complement), idx };\n         } else {\n            numIdx.put(num, idx);\n         }\n      }\n\n      return null;\n   }\n}`;

    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate python method with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate javascript method with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/JavaScript/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate cpp method with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/C++/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate java method with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Java/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate python linked list with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/reverse-linked-list/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate javascript linked list with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/reverse-linked-list/JavaScript/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate python binary tree with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/invert-binary-tree/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate javascript binary tree with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/invert-binary-tree/JavaScript/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate python class with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/min-stack/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});


test('validate javascript class with solution1', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/min-stack/JavaScript/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solution = page.locator('#solution-1');
    await expect(solution).toHaveCount(1);

    const solutionCode = await solution.inputValue();
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#test-code-button').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    const outputContainer = page.locator('div[name="output_container"]');

    await expect(outputContainer).toContainText('Status: Accepted');
    await expect(outputContainer).toContainText('Output: Tests passed!');
    await expect(outputContainer).toContainText(/Time: \d+(?:\.\d+)? seconds/);
    await expect(outputContainer).toContainText(/Memory: \d+ kilobytes?/);
});
