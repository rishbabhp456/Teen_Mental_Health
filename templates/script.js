document.addEventListener('DOMContentLoaded', () => {
    // Helper function to display messages
    function displayMessage(elementId, message, isSuccess) {
        const messageElement = document.getElementById(elementId);
        if (messageElement) {
            messageElement.textContent = message;
            messageElement.className = `message ${isSuccess ? 'success' : 'error'}`;
            messageElement.style.display = 'block';
        }
    }

    // Helper function to hide messages
    function hideMessage(elementId) {
        const messageElement = document.getElementById(elementId);
        if (messageElement) {
            messageElement.style.display = 'none';
            messageElement.textContent = '';
            messageElement.className = 'message';
        }
    }

    // Handle Login Form Submission
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessage('loginMessage');

            const formData = new FormData(loginForm);
            const response = await fetch('/login', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                displayMessage('loginMessage', data.message + ' Redirecting...', true);
                // Store token (e.g., in localStorage or sessionStorage)
                localStorage.setItem('access_token', data.access_token);
                // Redirect to prediction page after a short delay
                setTimeout(() => {
                    window.location.href = '/prediction_form_page';
                }, 1500);
            } else {
                displayMessage('loginMessage', data.message, false);
            }
        });
    }

    // Handle Register Form Submission
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessage('registerMessage');

            const formData = new FormData(registerForm);
            const response = await fetch('/register', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                displayMessage('registerMessage', data.message + ' You can now login.', true);
                registerForm.reset(); // Clear form
                setTimeout(() => {
                    window.location.href = '/login_page'; // Redirect to login
                }, 2000);
            } else {
                displayMessage('registerMessage', data.message, false);
            }
        });
    }

    // Handle Forgot Password Form Submission
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessage('forgotPasswordMessage');

            const formData = new FormData(forgotPasswordForm);
            const response = await fetch('/forgot_password', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                displayMessage('forgotPasswordMessage', data.message, true);
                forgotPasswordForm.reset();
                setTimeout(() => {
                    window.location.href = '/login_page';
                }, 2000);
            } else {
                displayMessage('forgotPasswordMessage', data.message || 'Password reset failed', false);
            }
        });
    }

    // Handle Prediction Form Submission and Dynamic Dropdowns
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        // Function to load dropdown options
        async function loadDropdownOptions(selectId, apiUrl) {
            const selectElement = document.getElementById(selectId);
            if (!selectElement) return;

            try {
                const response = await fetch(apiUrl);
                const options = await response.json();
                selectElement.innerHTML = '<option value="" disabled selected>Select...</option>'; // Default option
                options.forEach(option => {
                    const opt = document.createElement('option');
                    opt.value = option;
                    opt.textContent = option;
                    selectElement.appendChild(opt);
                });
            } catch (error) {
                console.error(`Error loading ${selectId} options:`, error);
                displayMessage('predictionResult', `Failed to load ${selectId} options.`, false);
            }
        }

        // Load options when the prediction page loads
        loadDropdownOptions('gender', '/gender_options');
        loadDropdownOptions('social_interaction_level', '/social_interaction_level_options');
        loadDropdownOptions('platform_usage', '/platform_usage_options');

        predictionForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideMessage('predictionResult');

            const formData = new FormData(predictionForm);
            const response = await fetch('/predict_depression', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();

            if (data.status === 'success') {
                // Display the meaningful message returned from backend
                const isSuccess = data.prediction === 0; // 0 = not depressed (success), 1 = depressed (warning)
                displayMessage('predictionResult', data.message, isSuccess);
            } else {
                displayMessage('predictionResult', `Prediction failed: ${data.message || 'Unknown error'}`, false);
            }
        });
    }
});