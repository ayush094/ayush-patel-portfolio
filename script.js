// Mobile Menu Toggle
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.querySelector('.nav-links');

mobileMenu.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    const isOpen = navLinks.classList.contains('active');
    document.body.classList.toggle('nav-open', isOpen);
    document.documentElement.classList.toggle('nav-open', isOpen);
});

// Close menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        document.body.classList.remove('nav-open');
        document.documentElement.classList.remove('nav-open');
    });
});

// Smooth scroll for anchor links (if not supported natively)
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            const headerOffset = 70;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth"
            });
        }
    });
});

// Basic content protection deterrents
document.addEventListener('contextmenu', (event) => {
    event.preventDefault();
});

document.addEventListener('copy', (event) => {
    event.preventDefault();
});

document.addEventListener('cut', (event) => {
    event.preventDefault();
});

document.addEventListener('selectstart', (event) => {
    event.preventDefault();
});

document.addEventListener('dragstart', (event) => {
    event.preventDefault();
});

document.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    const ctrlOrCmd = event.ctrlKey || event.metaKey;

    if (event.key === 'F12') {
        event.preventDefault();
        return;
    }

    if (ctrlOrCmd && ['u', 's', 'c', 'x', 'a'].includes(key)) {
        event.preventDefault();
        return;
    }

    if (ctrlOrCmd && event.shiftKey && ['i', 'j', 'c'].includes(key)) {
        event.preventDefault();
    }
});

// Cursor Glow Follow
const cursorGlow = document.querySelector('.cursor-glow');
const prefersFinePointer = window.matchMedia('(pointer: fine)').matches;

if (cursorGlow && prefersFinePointer) {
    let targetX = window.innerWidth / 2;
    let targetY = window.innerHeight / 2;
    let currentX = targetX;
    let currentY = targetY;
    const followSpeed = 0.18;

    const updateGlow = () => {
        currentX += (targetX - currentX) * followSpeed;
        currentY += (targetY - currentY) * followSpeed;
        cursorGlow.style.left = `${currentX}px`;
        cursorGlow.style.top = `${currentY}px`;
        requestAnimationFrame(updateGlow);
    };

    window.addEventListener('mousemove', (event) => {
        targetX = event.clientX;
        targetY = event.clientY;
        cursorGlow.classList.add('is-visible');
    });

    window.addEventListener('mouseout', (event) => {
        if (!event.relatedTarget && !event.toElement) {
            cursorGlow.classList.remove('is-visible');
        }
    });

    updateGlow();
}
