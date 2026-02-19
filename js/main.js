/**
 * ICC JAPAN - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Show success message if redirected after form submission
    if (window.location.search.includes('success=true')) {
        var successDiv = document.getElementById('formSuccess');
        var form = document.getElementById('contactForm');
        if (successDiv) successDiv.style.display = 'block';
        if (form) form.style.display = 'none';
        // Scroll to contact section
        var contactSection = document.getElementById('contact');
        if (contactSection) {
            setTimeout(function() {
                contactSection.scrollIntoView({ behavior: 'smooth' });
            }, 300);
        }
    }
    
    // ==========================================================================
    // Mobile Navigation
    // ==========================================================================
    
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const nav = document.getElementById('nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenuBtn.classList.toggle('active');
            nav.classList.toggle('active');
        });
        
        // Close menu when clicking nav links
        const navLinks = nav.querySelectorAll('a');
        navLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                mobileMenuBtn.classList.remove('active');
                nav.classList.remove('active');
            });
        });
    }
    
    // ==========================================================================
    // Header Scroll Effect
    // ==========================================================================
    
    const header = document.getElementById('header');
    let lastScrollY = window.scrollY;
    
    function handleScroll() {
        const currentScrollY = window.scrollY;
        
        // Add shadow on scroll
        if (currentScrollY > 50) {
            header.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
        }
        
        lastScrollY = currentScrollY;
    }
    
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    // ==========================================================================
    // Back to Top Button
    // ==========================================================================
    
    const backToTopBtn = document.getElementById('backToTop');
    
    function toggleBackToTop() {
        if (window.scrollY > 500) {
            backToTopBtn.classList.add('visible');
        } else {
            backToTopBtn.classList.remove('visible');
        }
    }
    
    window.addEventListener('scroll', toggleBackToTop, { passive: true });
    
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ==========================================================================
    // Smooth Scroll for Anchor Links
    // ==========================================================================
    
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                
                const headerHeight = header.offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.scrollY - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ==========================================================================
    // Form Validation & Submission
    // ==========================================================================
    
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            // Basic validation
            const requiredFields = contactForm.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(function(field) {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#DA251D';
                } else {
                    field.style.borderColor = '#E0E0E0';
                }
            });
            
            // Email validation
            const emailField = contactForm.querySelector('#email');
            if (emailField && emailField.value) {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailRegex.test(emailField.value)) {
                    isValid = false;
                    emailField.style.borderColor = '#DA251D';
                }
            }
            
            if (!isValid) {
                e.preventDefault();
                alert('必須項目をすべてご入力ください。');
                return false;
            }
            
            // Netlify Forms handles submission natively
            // Form will POST and redirect via Netlify
        });
        
        // Clear error styling on input
        contactForm.querySelectorAll('input, textarea, select').forEach(function(field) {
            field.addEventListener('input', function() {
                this.style.borderColor = '#E0E0E0';
            });
        });
    }
    
    // ==========================================================================
    // Intersection Observer for Animations
    // ==========================================================================
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements
    const animateElements = document.querySelectorAll(
        '.feature-card, .service-card, .stat-card, .why-us-item, .process-step'
    );
    
    animateElements.forEach(function(el) {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Add animation class styles
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            opacity: 1 !important;
            transform: translateY(0) !important;
        }
    `;
    document.head.appendChild(style);
    
    // ==========================================================================
    // Stats Counter Animation
    // ==========================================================================
    
    function animateCounter(element, target, suffix = '') {
        const duration = 2000;
        const start = 0;
        const increment = target / (duration / 16);
        let current = start;
        
        const timer = setInterval(function() {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            element.textContent = Math.floor(current) + suffix;
        }, 16);
    }
    
    // Observe stats for animation
    const statsObserver = new IntersectionObserver(function(entries) {
        entries.forEach(function(entry) {
            if (entry.isIntersecting) {
                const statCards = entry.target.querySelectorAll('.stat-number-lg');
                statCards.forEach(function(stat) {
                    const text = stat.textContent;
                    const number = parseInt(text);
                    const suffix = text.replace(/[0-9]/g, '');
                    
                    if (!isNaN(number) && !stat.dataset.animated) {
                        stat.dataset.animated = 'true';
                        animateCounter(stat, number, suffix);
                    }
                });
                statsObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    const statsSection = document.querySelector('.stats-showcase');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
    
    // ==========================================================================
    // Console Easter Egg
    // ==========================================================================
    
    console.log('%c🇻🇳 ICC JAPAN 🇯🇵', 'font-size: 24px; font-weight: bold; color: #DA251D;');
    console.log('%cベトナム人材と日本企業をつなぐ架け橋', 'font-size: 14px; color: #424242;');
    console.log('%c採用のご相談は contact@iccjpn.com まで', 'font-size: 12px; color: #757575;');
    
});
