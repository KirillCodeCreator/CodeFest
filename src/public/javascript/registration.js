const passwordInput = document.getElementById('password');
const togglePasswordButton = document.getElementById('toggle-password');

const repeatPasswordInput = document.getElementById('repeat-password');
const repeatTogglePasswordButton = document.getElementById('repeat-toggle-password')

if (passwordInput && togglePasswordButton) {
    togglePasswordButton.addEventListener('click', () => {
        const isPasswordVisible = passwordInput.type === 'text';
        passwordInput.type = isPasswordVisible ? 'password' : 'text';

        togglePasswordButton.textContent = isPasswordVisible ? '👁️' : '🙈';
    });
} else {
    console.error('Не удалось найти элементы для поля пароля или кнопки!');
}