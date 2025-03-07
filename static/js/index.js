// JavaScript to Toggle Forms
// Get references to the forms and buttons
const loginForm1 = document.getElementById('login-form-1');
const loginForm2 = document.getElementById('login-form-2');
const confirmButton = document.getElementById('confirm-button');
const backButton = document.getElementById('back-button');

const loginForm = document.getElementById('login-form');
const signupForm = document.getElementById('signup-form');
const showSignupButton = document.getElementById('show-signup');
const showLoginButton = document.getElementById('show-login');

// Show the second form and hide the first form
if (confirmButton) {
    confirmButton.addEventListener('click', function () {
        loginForm1.style.display = 'none';
        loginForm2.style.display = 'block';
    });
}

// Show the first form and hide the second form
if (backButton) {
    backButton.addEventListener('click', function () {
        loginForm2.style.display = 'none';
        loginForm1.style.display = 'block';
    });
}

// Show Sign Up Form and Hide Login Form
if (showSignupButton) {
    showSignupButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default link behavior
        loginForm.classList.add('hidden');
        signupForm.classList.remove('hidden');
    });
}

// Show Login Form and Hide Sign Up Form
if (showLoginButton) {
    showLoginButton.addEventListener('click', (e) => {
        e.preventDefault(); // Prevent default link behavior
        signupForm.classList.add('hidden');
        loginForm.classList.remove('hidden');
    });
}