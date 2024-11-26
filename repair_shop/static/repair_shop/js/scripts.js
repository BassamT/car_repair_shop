document.addEventListener("DOMContentLoaded", function () {
    const navbar = document.querySelector('.navbar');
    const logo = document.querySelector('.navbar-brand .logo');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Smooth scrolling effect for form interactions (optional)
    const forgotPasswordLink = document.querySelector('.text-yellow');
    forgotPasswordLink.addEventListener('click', (e) => {
        e.preventDefault();
        alert("Forgot password feature is under development.");
    });
});
