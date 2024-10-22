// Add any custom JavaScript functionality here
document.addEventListener('DOMContentLoaded', function() {
    // Example: Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// Здесь можно добавить пользовательские скрипты
console.log("Скрипт загружен");
