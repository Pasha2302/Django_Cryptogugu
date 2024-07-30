// static/js/override_admin_theme.js

document.addEventListener('DOMContentLoaded', function () {
    function setLightTheme() {
        document.documentElement.dataset.theme = 'light';
        localStorage.setItem('theme', 'light');
    }

    setLightTheme();

    // Отключение кнопок переключения темы
    const buttons = document.querySelector('button.theme-toggle');
    buttons.addEventListener('click', function (event) {
        event.preventDefault();
        setLightTheme();
    });

});
