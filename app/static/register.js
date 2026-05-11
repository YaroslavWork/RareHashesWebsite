const registerForm = document.getElementById('registerForm');
const feedbackElement = document.getElementById('registerFeedback');

const showFeedback = (message, isError = true) => {
    feedbackElement.textContent = message;
    feedbackElement.style.color = isError ? '#dc2626' : '#166534';
};

const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
};

registerForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const username = document.getElementById('username').value.trim();
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;

    if (!username) {
        showFeedback('Username is required.');
        return;
    }

    if (!email) {
        showFeedback('Email is required.');
        return;
    }

    if (!validateEmail(email)) {
        showFeedback('Please enter a valid email address.');
        return;
    }

    if (!password) {
        showFeedback('Password is required.');
        return;
    }

    if (password.length < 8) {
        showFeedback('Password must be at least 8 characters long.');
        return;
    }

    if (password !== confirmPassword) {
        showFeedback('Passwords do not match.');
        return;
    }

    try {
        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, email, password })
        });

        const data = await response.json();

        if (!response.ok) {
            showFeedback(data.error || 'Unable to create user. Please try again.');
            return;
        }

        showFeedback(data.message || 'User created successfully.', false);
        registerForm.reset();
    } catch (error) {
        showFeedback('Network error. Please try again later.');
        console.error('Register error:', error);
    }
});
