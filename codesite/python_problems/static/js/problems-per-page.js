document.addEventListener("DOMContentLoaded", () => {
    const storedValue = localStorage.getItem("problemsPerPage");

    // Get both dropdowns
    const primarySelect = document.getElementById("problems_per_page_primary");
    const secondarySelect = document.getElementById("problems_per_page_secondary");

    // Apply stored value and trigger form submission if needed
    if (storedValue) {
        let needsUpdate = false;

        if (primarySelect.value !== storedValue) {
            primarySelect.value = storedValue;
            secondarySelect.value = storedValue;
            needsUpdate = true;
        }

        if (needsUpdate) primarySelect.form.submit();
    }

    // Attach event listeners
    primarySelect.addEventListener("change", syncDropdowns);
    secondarySelect.addEventListener("change", syncDropdowns);

    // Function to sync dropdowns and store value
    function syncDropdowns(event) {
        const newValue = event.target.value;
        localStorage.setItem("problemsPerPage", newValue);
        primarySelect.value = newValue;
        secondarySelect.value = newValue;
        event.target.form.submit();
    }
});