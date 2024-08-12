// static/js/navbar.js
document.addEventListener('DOMContentLoaded', function() {
    const toggler = document.querySelector('.navbar-toggler');
    const menu = document.querySelector('.navbar-menu');

    if (toggler) {
        toggler.addEventListener('click', function() {
            menu.classList.toggle('active');
        });
    }
});
