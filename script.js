/* ==========================================================================
   Ayush Patel — Portfolio behaviour
   Small, dependency-free enhancements. Content works without JS.
   ========================================================================== */

(function () {
    'use strict';

    var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ----------------------------------------------------------------------
       Header: add depth once the page is scrolled
       ---------------------------------------------------------------------- */

    var header = document.querySelector('.site-header');
    var onScroll = function () {
        if (!header) return;
        header.classList.toggle('is-scrolled', window.scrollY > 8);
    };

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    /* ----------------------------------------------------------------------
       Mobile navigation
       ---------------------------------------------------------------------- */

    var toggle = document.getElementById('nav-toggle');
    var nav = document.getElementById('primary-nav');

    if (toggle && nav) {
        var setNavState = function (open) {
            nav.classList.toggle('is-open', open);
            document.body.classList.toggle('nav-open', open);
            toggle.setAttribute('aria-expanded', String(open));
            toggle.setAttribute('aria-label', open ? 'Close navigation menu' : 'Open navigation menu');
        };

        toggle.addEventListener('click', function () {
            var isOpen = toggle.getAttribute('aria-expanded') === 'true';
            setNavState(!isOpen);
            if (!isOpen) {
                var firstLink = nav.querySelector('a');
                if (firstLink) firstLink.focus({ preventScroll: true });
            }
        });

        // Close when a destination is chosen
        nav.addEventListener('click', function (event) {
            if (event.target.closest('a')) setNavState(false);
        });

        // Close on Escape and return focus to the toggle
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && nav.classList.contains('is-open')) {
                setNavState(false);
                toggle.focus();
            }
        });

        // Close when clicking the scrim (anything outside the drawer)
        document.addEventListener('click', function (event) {
            if (!nav.classList.contains('is-open')) return;
            if (nav.contains(event.target) || toggle.contains(event.target)) return;
            setNavState(false);
        });

        // Reset state when the desktop layout returns
        var desktopQuery = window.matchMedia('(min-width: 901px)');
        var handleDesktop = function (event) {
            if (event.matches) setNavState(false);
        };

        if (typeof desktopQuery.addEventListener === 'function') {
            desktopQuery.addEventListener('change', handleDesktop);
        } else if (typeof desktopQuery.addListener === 'function') {
            desktopQuery.addListener(handleDesktop);
        }
    }

    /* ----------------------------------------------------------------------
       Back to top (the sticky header makes a plain #top anchor unreliable)
       ---------------------------------------------------------------------- */

    document.querySelectorAll('a[href="#top"]').forEach(function (link) {
        link.addEventListener('click', function (event) {
            event.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: prefersReducedMotion ? 'auto' : 'smooth'
            });
            if (history.replaceState) history.replaceState(null, '', window.location.pathname);
        });
    });

    /* ----------------------------------------------------------------------
       Cursor accent — a trailing ring and soft glow over fine pointers
       ---------------------------------------------------------------------- */

    var finePointer = window.matchMedia('(pointer: fine)').matches;

    if (finePointer && !prefersReducedMotion) {
        var glow = document.querySelector('.cursor-glow');
        var ring = document.querySelector('.cursor-ring');

        if (glow && ring) {
            var pointer = { x: window.innerWidth / 2, y: window.innerHeight / 2 };
            var glowPos = { x: pointer.x, y: pointer.y };
            var ringPos = { x: pointer.x, y: pointer.y };
            var animating = false;

            var renderCursor = function () {
                glowPos.x += (pointer.x - glowPos.x) * 0.08;
                glowPos.y += (pointer.y - glowPos.y) * 0.08;
                ringPos.x += (pointer.x - ringPos.x) * 0.32;
                ringPos.y += (pointer.y - ringPos.y) * 0.32;

                glow.style.transform = 'translate3d(' + glowPos.x + 'px,' + glowPos.y + 'px,0)';
                ring.style.transform = 'translate3d(' + ringPos.x + 'px,' + ringPos.y + 'px,0)';

                requestAnimationFrame(renderCursor);
            };

            document.addEventListener(
                'pointermove',
                function (event) {
                    pointer.x = event.clientX;
                    pointer.y = event.clientY;

                    if (!animating) {
                        animating = true;
                        glow.classList.add('is-visible');
                        ring.classList.add('is-visible');
                        renderCursor();
                    }
                },
                { passive: true }
            );

            document.addEventListener('pointerover', function (event) {
                var target = event.target;
                var interactive =
                    target && typeof target.closest === 'function'
                        ? target.closest('a, button, [role="button"], input, textarea, select, summary')
                        : null;
                ring.classList.toggle('is-interactive', Boolean(interactive));
            });

            var hideCursor = function () {
                glow.classList.remove('is-visible');
                ring.classList.remove('is-visible', 'is-interactive');
            };

            document.addEventListener('mouseleave', hideCursor);
            window.addEventListener('blur', hideCursor);
        }
    }

    /* ----------------------------------------------------------------------
       Active section highlighting
       ---------------------------------------------------------------------- */

    var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav-list a[href^="#"]'));
    var sections = navLinks
        .map(function (link) {
            return document.querySelector(link.getAttribute('href'));
        })
        .filter(Boolean);

    if (sections.length && 'IntersectionObserver' in window) {
        var visibleSections = new Map();

        var sectionObserver = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (entry.isIntersecting) {
                        visibleSections.set(entry.target.id, entry.intersectionRatio);
                    } else {
                        visibleSections.delete(entry.target.id);
                    }
                });

                var activeId = null;
                var bestRatio = 0;
                visibleSections.forEach(function (ratio, id) {
                    if (ratio > bestRatio) {
                        bestRatio = ratio;
                        activeId = id;
                    }
                });

                navLinks.forEach(function (link) {
                    var isActive = activeId !== null && link.getAttribute('href') === '#' + activeId;
                    link.classList.toggle('is-active', isActive);
                    if (isActive) {
                        link.setAttribute('aria-current', 'true');
                    } else {
                        link.removeAttribute('aria-current');
                    }
                });
            },
            { rootMargin: '-35% 0px -55% 0px', threshold: [0, 0.25, 0.5, 1] }
        );

        sections.forEach(function (section) {
            sectionObserver.observe(section);
        });
    }

    /* ----------------------------------------------------------------------
       Scroll reveal (progressive, skipped for reduced motion)
       ---------------------------------------------------------------------- */

    if (!prefersReducedMotion && 'IntersectionObserver' in window) {
        var revealTargets = document.querySelectorAll(
            '.section-head, .focus-card, .skill-card, .timeline-item, .project-card, .edu-card, .cert-card, .contact-panel'
        );

        var revealObserver = new IntersectionObserver(
            function (entries, observer) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;
                    entry.target.classList.add('is-visible');
                    observer.unobserve(entry.target);
                });
            },
            { rootMargin: '0px 0px -8% 0px', threshold: 0.08 }
        );

        revealTargets.forEach(function (element, index) {
            element.classList.add('reveal');
            // Small stagger for cards sitting side by side
            element.style.transitionDelay = Math.min(index % 4, 3) * 60 + 'ms';
            revealObserver.observe(element);
        });
    }

    /* ----------------------------------------------------------------------
       Footer year
       ---------------------------------------------------------------------- */

    var year = document.getElementById('year');
    if (year) year.textContent = String(new Date().getFullYear());
})();
