const word = document.getElementById("wordInput");
const hashType = document.getElementById("hashTypeInput");
const user = document.getElementById("userInput");

const errorParagraph = document.getElementById("errorParagraph");

function sendData() {

    // Clear previous styles and error messages
    word.style.borderColor = "#4275c5";
    hashType.style.borderColor = "#4275c5";
    user.style.borderColor = "#4275c5";

    errorParagraph.style.color = "#ff0000"; // Reset to default color
    errorParagraph.textContent = ""; // Clear previous error message

    // Pre-send validation
    if (word.value.trim() === "") {
        // Red border for empty word input
        word.style.borderColor = "red";
        word.focus(); // Focus on the word input
        errorParagraph.textContent = "Please enter a word.";
        return;
    } else if (word.value.length > 255) {
        // Red border for invalid word length
        word.style.borderColor = "red";
        word.focus(); // Focus on the word input
        errorParagraph.textContent = "Word must be less than 255 characters.";
        return;
    } else if (hashType.value === "") {
        // Red border for empty hash type input
        hashType.style.borderColor = "red";
        hashType.focus(); // Focus on the hash type input
        errorParagraph.textContent = "Please select a hash type.";
        return;
    } else if (user.value > 31) {
        // Red border for invalid user length
        word.style.borderColor = "red";
        user.focus(); // Focus on the user input
        errorParagraph.textContent = "User must be less than 31 characters.";
        return;
    }

    

    fetch('/write', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "word": word.value,
            "hashType": hashType.value,
            "user": user.value 
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.errno === 0) { // No error
            errorParagraph.textContent = data.msg; // Display success message from server
            errorParagraph.style.color = "green"; // Change text color to green
            word.style.borderColor = "green"; // Change border color to green
        }
        if (data.errno === 1) {
            errorParagraph.textContent = data.msg; // Display error message from server
            word.style.borderColor = "red";
            word.focus();
        }
        else if (data.errno === 2) {
            errorParagraph.textContent = data.msg; // Display error message from server
            word.style.borderColor = "red";
            word.focus();
        } else if (data.errno === 3) {
            errorParagraph.textContent = data.msg; // Display error message from server
        }
    })
}


function clearInputs() {
    word.value = "";
    hashType.value = "";
    user.value = "";
    errorParagraph.textContent = ""; // Clear error message
    errorParagraph.style.color = "#ff0000"; // Reset to default color
    word.style.borderColor = "#4275c5"; // Reset border color
    user.style.borderColor = "#4275c5"; // Reset border color
}