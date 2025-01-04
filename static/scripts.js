const categoryDropdown = document.getElementById("category");
const optionDropdown = document.getElementById("option");
const resultsContainer = document.getElementById("results");

function fetchData(category, option) {
    // Show loading message
    resultsContainer.innerHTML = "<p>Loading...</p>";

    // Make AJAX request
    fetch("/fetch", {
        method: "POST",
        headers: {
            "Content-Type": "application/json", // Explicitly set Content-Type
        },
        body: JSON.stringify({ category, option }), // Convert data to JSON string
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json(); // Parse JSON response
        })
        .then((data) => {
            if (data.error) {
                resultsContainer.innerHTML = `<p>Error: ${data.error}</p>`;
            } else {
                resultsContainer.innerHTML = data.data || "<p>No data available.</p>";
            }
        })
        .catch((error) => {
            resultsContainer.innerHTML = `<p>Error: ${error.message}</p>`;
        });
}

// Event listener for category change
categoryDropdown.addEventListener("change", () => updateOptions(categoryDropdown.value));
optionDropdown.addEventListener("change", () => {
    const category = categoryDropdown.value;
    const option = optionDropdown.value;
    fetchData(category, option);
});
