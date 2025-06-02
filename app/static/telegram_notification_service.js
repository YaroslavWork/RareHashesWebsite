const operation = document.getElementById("operationInput");
const telegramID = document.getElementById("telegramIdInput");
const rule = document.getElementById("ruleInput");
const minimumValue = document.getElementById("minimumValueInput");

const errorParagraph = document.getElementById("errorParagraph");

function sendData() {
    // Clear previous styles and error messages
    operation.style.borderColor = "#4275c5";
    telegramID.style.borderColor = "#4275c5";
    rule.style.borderColor = "#4275c5";
    minimumValue.style.borderColor = "#4275c5";

    errorParagraph.style.color = "#ff0000"; // Reset to default color
    errorParagraph.textContent = ""; // Clear previous error message

    // Pre-send validation
    if (telegramID.value.trim() === "") {
        telegramID.style.borderColor = "red";
        telegramID.focus();
        errorParagraph.textContent = "Provide a number.";
        return
    } else if (telegramID.value.length > 32) {
            telegramID.style.borderColor = "red";
            telegramID.focus();
            errorParagraph.textContent = "Telegram ID is too long.";
            return
    } else if (isNaN(Number(telegramID.value)) || !Number.isInteger(Number(telegramID.value))) {
        telegramID.style.borderColor = "red";
        telegramID.focus();
        errorParagraph.textContent = "Telegram ID must be a number.";
        return
    } else if (rule.value === "") {
        rule.style.borderColor = "red";
        rule.focus();
        errorParagraph.textContent = "Choose a rule.";
        return
    } else if (minimumValue.value.trim() === "") {
        minimumValue.style.borderColor = "red";
        minimumValue.focus();
        errorParagraph.textContent = "Provide a number.";
        return
    } else if (isNaN(Number(minimumValue.value)) || !Number.isInteger(Number(minimumValue.value))) {
        minimumValue.style.borderColor = "red";
        minimumValue.focus();
        errorParagraph.textContent = "Minimum value must be a number.";
        return
    } else if (Number(minimumValue.value < 0) || Number(minimumValue.value > 100000000)) {
        minimumValue.style.borderColor = "red";
        minimumValue.focus();
        errorParagraph.textContent = "Minimum value must be in a range between 1 and 100 000 000.";
        return
    }

    const operation_json = operation.value == "add_user" ? "add" : "remove"
    const rule_json = rule.value === "by_rarity" ? "rarity" : "ranking"

    fetch('/telegram_notification_service', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            "telegram_operation": operation_json,
            "telegram_id": telegramID.value,
            "rule_type": rule_json,
            "minimum_value": minimumValue.value,
        })
    })
    .then(response => response.json())
    .then(data => { 
        if (data.errno === 0) { // No error
            errorParagraph.textContent = data.msg; // Display success message from server
            errorParagraph.style.color = "green"; // Change text color to green
            telegramID.style.borderColor = "green"; // Change border color to green
        } else if (data.errno === 3) {
            errorParagraph.textContent = data.msg; // Display error message from server
            telegramID.style.borderColor = "red";
            telegramID.focus();
        } else {
            errorParagraph.textContent = data.msg; // Display error message from server
        }
    })
}

function clearInputs() {
    operation.value = "";
    telegramID.value = "";
    rule.value = "";
    minimumValue.value = "";
    errorParagraph.textContent = ""
    errorParagraph.style.color = "#ff0000"; // Reset to default color
    telegramID.style.borderColor = "#4275c5"; // Reset border color
    minimumValue.style.borderColor = "#4275c5"; // Reset border color
    telegramID.style.display = "none";
    rule.style.display = "none";
    minimumValue.style.display = "none";
}

operation.addEventListener("change", function () {
    if (operation.value == "add_user") {
        telegramID.style.display = "inline";
        rule.style.display = "inline";
        minimumValue.style.display = "inline";
    } else if (operation.value == "remove_user") {
        telegramID.style.display = "inline";
        rule.style.display = "none";
        minimumValue.style.display = "none";
    } else {
        telegramID.style.display = "none";
        rule.style.display = "none";
        minimumValue.style.display = "none";
    }
  });