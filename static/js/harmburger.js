const hamburger = document.getElementById('hamburger');
const nav = document.getElementById('nav');
const btn = document.getElementById('btn');
const navItem = document.getElementById('nav-links');

function toggleMobile() {
    nav.classList.toggle('visible');
    btn.classList.toggle('visible');
    navItem.classList.toggle('visible');
    hamburger.classList.toggle('visible');
}

hamburger.addEventListener('click', toggleMobile);
