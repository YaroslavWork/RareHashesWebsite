// Function to compute hashes and update table
async function computeHashes() {
    const table = document.getElementById("viewTable");
    const rows = table.getElementsByTagName("tr");
    let startCount = parseInt(document.getElementById("startCountValue").value, 10);

    for (let i = 1; i < rows.length; i++) { // Skip header
        rows[i].cells[0].textContent = i+startCount-1 // Count
    }
}

// Trigger computeHashes() after the page loads
window.onload = function() {
    computeHashes();
};