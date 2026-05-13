document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const loginMessage = document.getElementById("loginMessage");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();
        
        const usernameInput = document.getElementById("username").value.trim();
        const passwordInput = document.getElementById("password").value.trim();
        
        // Reset previous message states
        loginMessage.textContent = "";
        loginMessage.style.color = "black";

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: usernameInput,
                    password: passwordInput
                })
            });

            const data = await response.json();

            if (response.ok) {
                loginMessage.style.color = "green";
                loginMessage.textContent = data.message || "Login successful!";
                
                setTimeout(() => {
                    window.location.href = "/view"; // Redirect to a protected page on success
                }, 1000);
            } else {
                loginMessage.style.color = "red";
                loginMessage.textContent = data.error || "Login failed.";
            }
        } catch (error) {
            console.error("Error during login:", error);
            loginMessage.style.color = "red";
            loginMessage.textContent = "A network error occurred. Please try again.";
        }
    });
});