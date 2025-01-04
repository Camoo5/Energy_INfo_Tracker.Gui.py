const consumers = JSON.parse(document.getElementById("information_for_consumers").textContent);
const schemes = JSON.parse(document.getElementById("environmental_schemes").textContent);

const categoryDropdown = document.getElementById("category");
const optionDropdown = document.getElementById("option");

function updateOptions(category) {
    const options = category === "consumers" ? consumers : schemes;
    optionDropdown.innerHTML = "";

    for (const key in options) {
        const opt = document.createElement("option");
        opt.value = key;
        opt.textContent = key;
        optionDropdown.appendChild(opt);
    }
}

// Initialize options based on default category
updateOptions(categoryDropdown.value);

// Update options dynamically on category change
categoryDropdown.addEventListener("change", () => updateOptions(categoryDropdown.value));
