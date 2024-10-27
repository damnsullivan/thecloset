document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menu-toggle');
    const sideNav = document.getElementById('side-nav');

    menuToggle.addEventListener('click', function() {
        sideNav.classList.toggle('open');
    });

    // Fecha o menu lateral ao clicar fora dele
    document.addEventListener('click', function(event) {
        if (!sideNav.contains(event.target) && !menuToggle.contains(event.target)) {
            sideNav.classList.remove('open');
        }
    });
});
