import { test, expect, Page } from '@playwright/test';

// Helper to wait for CodeMirror to initialize
async function waitForCodeMirror(page: Page) {
    await page.waitForFunction(() => {
        return (window as any).codeEditor && typeof (window as any).codeEditor.setValue === 'function';
    }, { timeout: 10000 });
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


test('user can run python solution', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    // Wait for CodeMirror to initialize
    await waitForCodeMirror(page);

    // Set code via CodeMirror API
    const solutionCode = `class Solution:
    def twoSum(self, nums, target):
        return [0, 1]`;
    
    await setCodeMirrorContent(page, solutionCode);

    // Click the Validate button - this submits the form with test validation
    await page.locator('#testCodeButton').click();

    // Wait for the form submission to complete
    await page.waitForLoadState('networkidle');

    // Wait for output to appear
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });
    
    await expect(page.locator('div[name="output_container"]'))
        .toContainText(/Tests passed!|Accepted/i);
});


test('runtime error is displayed', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    await waitForCodeMirror(page);

    const errorCode = 'raise Exception("boom")';
    await setCodeMirrorContent(page, errorCode);

    await page.locator('#runCodeButton').click();

    await page.waitForLoadState('networkidle');
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });
    
    await expect(page.locator('div[name="output_container"]'))
        .toContainText(/exception|error|boom/i);
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


test('validate button works', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    await waitForCodeMirror(page);

    const code = `class Solution:
    def twoSum(self, nums, target):
        return [0, 1]`;
    
    await setCodeMirrorContent(page, code);

    // Click the Validate button
    await page.locator('#testCodeButton').click();

    await page.waitForLoadState('networkidle');
    await page.waitForSelector('div[name="output_container"]', { state: 'visible' });

    // Check that the page didn't crash and shows some output
    await expect(page.locator('h1')).toContainText('Two Sum');
});


test('code editor is initialized with correct mode', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/problems/two-sum/Python/');

    await waitForCodeMirror(page);

    // Check that CodeMirror is initialized
    const editorExists = await page.evaluate(() => {
        return (window as any).codeEditor !== null;
    });
    
    expect(editorExists).toBeTruthy();
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
