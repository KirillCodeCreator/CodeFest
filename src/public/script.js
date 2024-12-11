const passwordInput = document.getElementById('password');
const togglePasswordButton = document.getElementById('toggle-password');

if (passwordInput && togglePasswordButton) {
    togglePasswordButton.addEventListener('click', () => {
        const isPasswordVisible = passwordInput.type === 'text';
        passwordInput.type = isPasswordVisible ? 'password' : 'text';

        togglePasswordButton.textContent = isPasswordVisible ? '👁️' : '🙈';
    });
} else {
    console.error('Не удалось найти элементы для поля пароля или кнопки!');
}
