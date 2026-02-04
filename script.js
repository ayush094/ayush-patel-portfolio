// Mobile Menu Toggle
const mobileMenu = document.getElementById('mobile-menu');
const navLinks = document.querySelector('.nav-links');

mobileMenu.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

// Close menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
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

// Typewriter Effect for Hero Role
const roleElement = document.querySelector('.hero-role');
const roles = ["Backend Developer", "Django Expert", "AI Systems Engineer"];
let roleIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typeSpeed = 100;

function typeWriter() {
    const currentRole = roles[roleIndex];

    if (isDeleting) {
        roleElement.textContent = currentRole.substring(0, charIndex - 1) + "|";
        charIndex--;
        typeSpeed = 50;
    } else {
        roleElement.textContent = currentRole.substring(0, charIndex + 1) + "|";
        charIndex++;
        typeSpeed = 100;
    }

    if (!isDeleting && charIndex === currentRole.length) {
        isDeleting = true;
        typeSpeed = 2000; // Pause at end
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        roleIndex = (roleIndex + 1) % roles.length;
        typeSpeed = 500;
    }

    setTimeout(typeWriter, typeSpeed);
}

// Start the typing effect
document.addEventListener('DOMContentLoaded', typeWriter);

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
