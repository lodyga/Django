document.addEventListener('DOMContentLoaded', () => {
    const storedValue = localStorage.getItem('problemsPerPage');

    // Get both dropdowns
    const primarySelect = document.getElementById('problems_per_page_primary');
    const secondarySelect = document.getElementById('problems_per_page_secondary');
    const selects = [primarySelect, secondarySelect].filter(Boolean);

    if (selects.length === 0) return;

    // Apply stored value and trigger form submission if needed
    if (storedValue) {
        let needsUpdate = false;

        selects.forEach((select) => {
            if (select.value !== storedValue) {
                select.value = storedValue;
                needsUpdate = true;
            }
        });

        if (needsUpdate && primarySelect?.form) primarySelect.form.submit();
    }

    // Attach event listeners
    selects.forEach((select) => {
        select.addEventListener('change', syncDropdowns);
    });

    // Function to sync dropdowns and store value
    function syncDropdowns(event) {
        const newValue = event.target.value;
        localStorage.setItem('problemsPerPage', newValue);
        selects.forEach((select) => {
            select.value = newValue;
        });
        if (event.target.form) event.target.form.submit();
    }
});
