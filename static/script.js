document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('loginForm');
  if (loginForm) {
    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(loginForm);
      const response = await fetch('/login', { method: 'POST', body: formData });
      const data = await response.json();
      console.log('login response:', data);

      if (data.status === 'success') {
        window.location.href = '/prediction_form_page';
      } else {
        alert(data.message || 'Login failed');
      }
    });
  }

  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(registerForm);
      const response = await fetch('/register', { method: 'POST', body: formData });
      const data = await response.json();
      console.log('register response:', data);

      if (data.status === 'success') {
        window.location.href = '/login_page';
      } else {
        alert(data.message || 'Registration failed');
      }
    });
  }

  const forgotPasswordForm = document.getElementById('forgotPasswordForm');
  if (forgotPasswordForm) {
    forgotPasswordForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const messageElement = document.getElementById('forgotPasswordMessage');
      
      const formData = new FormData(forgotPasswordForm);
      const response = await fetch('/forgot_password', { method: 'POST', body: formData });
      const data = await response.json();
      console.log('forgot password response:', data);
      
      if (data.status === 'success') {
        messageElement.textContent = data.message;
        messageElement.className = 'message success';
        messageElement.style.display = 'block';
        forgotPasswordForm.reset();
        setTimeout(() => {
          window.location.href = '/login_page';
        }, 2000);
      } else {
        messageElement.textContent = data.message || 'Password reset failed';
        messageElement.className = 'message error';
        messageElement.style.display = 'block';
      }
    });
  }

  const predictionForm = document.getElementById('predictionForm');
  if (predictionForm) {
    async function loadDropdownOptions(selectId, apiUrl) {
      const selectElement = document.getElementById(selectId);
      if (!selectElement) return;

      const response = await fetch(apiUrl);
      const options = await response.json();
      console.log(`${selectId} options:`, options);
      selectElement.innerHTML = '<option value="" disabled selected>Select...</option>';
      options.forEach((option) => {
        const opt = document.createElement('option');
        opt.value = option;
        opt.textContent = option;
        selectElement.appendChild(opt);
      });
    }

    loadDropdownOptions('gender', '/gender_options');
    loadDropdownOptions('social_interaction_level', '/social_interaction_level_options');
    loadDropdownOptions('platform_usage', '/platform_usage_options');

    predictionForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const formData = new FormData(predictionForm);
      const response = await fetch('/predict_depression', { method: 'POST', body: formData });
      const data = await response.json();
      console.log('prediction response:', data);

      if (data.status === 'success') {
        const resultDiv = document.getElementById('predictionResult');
        if (resultDiv) {
          resultDiv.textContent = data.message;
          resultDiv.className = data.prediction === 0 ? 'message success' : 'message error';
          resultDiv.style.display = 'block';
        }
      } else {
        alert(data.message || 'Prediction failed');
      }
    });
  }
});
