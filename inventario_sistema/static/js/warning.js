// JavaScript para ocultar la advertencia después de 10 segundos
setTimeout(function() {
    var warning = document.getElementById('login-warning');
    if (warning) {
        warning.classList.add('fade-out');
        setTimeout(function() {
            warning.style.display = 'none';
        }, 2000); // Espera a que la animación termine
    }
}, 10000); // 10 segundos = 10000 milisegundos