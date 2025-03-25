// Function to compute SHA-256 hash
async function sha256(text, basic=16) {
    const encoder = new TextEncoder();
    const data = encoder.encode(text);
    const hashBuffer = await crypto.subtle.digest("SHA-256", data);
    let hashHex = Array.from(new Uint8Array(hashBuffer))
                .map(byte => byte.toString(basic).padStart(2, '0'))
                .join('');
    if (basic == 16) {
        return hashHex.padStart(64, '0')
    } else {
        return hashHex.padStart(256, '0')
    }
    
}

// Function to compute hashes and update table
async function computeHashes() {
    const table = document.getElementById("viewTable");
    const rows = table.getElementsByTagName("tr");

    for (let i = 1; i < rows.length; i++) { // Skip header
        rows[i].cells[0].textContent = i; // Count
        let firstText = rows[i].cells[0].textContent.trim(); // First column
        let hashValue_16 = await sha256(firstText, 16);
        rows[i].cells[7].textContent = hashValue_16;
        // let hashValue_2 = await sha256(firstText, 2);
        // rows[i].cells[7].textContent = hashValue_2;
    }
}

// Trigger computeHashes() after the page loads
window.onload = function() {
    computeHashes();
};