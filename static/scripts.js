const categoryDropdown = document.getElementById("category");
const optionDropdown = document.getElementById("option");
const resultsContainer = document.getElementById("results");
const spinner = document.getElementById("loading-spinner");

// Function to fetch data
async function fetchData(category, option) {
    resultsContainer.innerHTML = ""; // Clear previous results
    spinner.classList.remove("hidden"); // Show spinner

    try {
        const response = await fetch("/fetch", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ category, option }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();

        if (data.error) {
            resultsContainer.innerHTML = `<p class="error-message">Error: ${data.error}</p>`;
        } else {
            resultsContainer.innerHTML = data.data
                ? `<p class="success-message">${data.data}</p>`
                : `<p class="info-message">No data available.</p>`;
        }
    } catch (error) {
        resultsContainer.innerHTML = `<p class="error-message">Error: ${error.message}</p>`;
    } finally {
        spinner.classList.add("hidden"); // Hide spinner
    }
}

// Update options based on selected category
function updateOptions(category) {
    optionDropdown.innerHTML = ""; // Clear existing options

    const data =
        category === "consumers"
            ? JSON.parse(document.getElementById("information_for_consumers").textContent)
            : JSON.parse(document.getElementById("environmental_schemes").textContent);

    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Select an option";
    defaultOption.disabled = true;
    defaultOption.selected = true;
    optionDropdown.appendChild(defaultOption);

    for (const [key, value] of Object.entries(data)) {
        const option = document.createElement("option");
        option.value = key;
        option.textContent = key;
        optionDropdown.appendChild(option);
    }
}

// Event listener for category dropdown change
categoryDropdown.addEventListener("change", () => updateOptions(categoryDropdown.value));

// Event listener for option dropdown change
optionDropdown.addEventListener("change", () => {
    const category = categoryDropdown.value;
    const option = optionDropdown.value;
    if (category && option) {
        fetchData(category, option);
    }
});

// Add event listener for the form submission (to prevent reloads)
document.getElementById("energy-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const category = categoryDropdown.value;
    const option = optionDropdown.value;
    if (category && option) {
        fetchData(category, option);
    }
});
