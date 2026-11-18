import { expect, test } from '@playwright/test';

test('grid path updates live and reports invalid input', async ({ page }) => {
    await page.goto('/dsa/grid_dfs');

    const inputPath = page.locator('#inputPath');
    const cells = page.locator('#grid .cell');
    const feedback = page.locator('#inputPathFeedback');

    await inputPath.fill('[[0, 0], [1, 0]]');
    await expect(cells).toHaveCount(2);
    await expect(feedback).toHaveText('Valid path (2 points).');

    await inputPath.fill('[[0, 0], [1, "x"]]');
    await expect(inputPath).toHaveAttribute('aria-invalid', 'true');
    await expect(feedback).toContainText('non-negative integer pairs');
    await expect(cells).toHaveCount(2);

    await inputPath.fill('[[2, 1]]');
    await expect(inputPath).not.toHaveAttribute('aria-invalid');
    await expect(cells).toHaveCount(6);

    const testCaseInput = page.locator('#testCaseInput');
    const solveButton = page.locator('#solveTestCaseBtn');
    const testCaseFeedback = page.locator('#testCaseInputFeedback');

    await expect(solveButton).toBeEnabled();
    await testCaseInput.fill('[["1", "2"]]');
    await expect(testCaseInput).toHaveAttribute('aria-invalid', 'true');
    await expect(solveButton).toBeDisabled();
    await expect(testCaseFeedback).toContainText('only the strings');

    await testCaseInput.fill('[["1"], ["0", "1"]]');
    await expect(testCaseInput).toHaveAttribute('aria-invalid', 'true');
    await expect(solveButton).toBeDisabled();

    await testCaseInput.fill('[["1", "0"], ["0", "1"]]');
    await expect(testCaseInput).not.toHaveAttribute('aria-invalid');
    await expect(solveButton).toBeEnabled();
    await expect(testCaseFeedback).toHaveText('Valid grid.');

    await testCaseInput.fill('[[1, 0], [0, 1]]');
    await expect(testCaseInput).toHaveAttribute('aria-invalid', 'true');
    await expect(solveButton).toBeDisabled();

    await testCaseInput.fill("[['1', '0'], ['0', '1']]");
    await expect(testCaseInput).not.toHaveAttribute('aria-invalid');
    await expect(solveButton).toBeEnabled();
    await expect(testCaseFeedback).toHaveText('Valid grid.');
});
