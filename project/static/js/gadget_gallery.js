// Enhanced Theme Management
function toggleTheme() {
    const body = document.body;
    const themeIcon = document.querySelector('.theme-icon');
    
    if (body.classList.contains('dark')) {
        body.classList.remove('dark');
        themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark');
        themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    }
}

// Enhanced Category Navigation
function showCategory(category, element) {
    // Hide all sections with fade effect
    document.querySelectorAll('.category-section').forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(30px)';
        setTimeout(() => {
            section.style.display = 'none';
        }, 300);
    });
    
    // Show selected section with fade effect
    setTimeout(() => {
        const targetSection = document.getElementById(category + '-section');
        targetSection.style.display = 'block';
        setTimeout(() => {
            targetSection.style.opacity = '1';
            targetSection.style.transform = 'translateY(0)';
        }, 50);
    }, 300);
    
    // Update active tab
    document.querySelectorAll('.category-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    element.classList.add('active');
}

// Enhanced Search Functionality
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    searchInput.addEventListener('input', function(e) {
        const searchTerm = e.target.value.toLowerCase();
        const productCards = document.querySelectorAll('.product-card');
        
        productCards.forEach(card => {
            const title = card.querySelector('.product-title').textContent.toLowerCase();
            const brand = card.querySelector('.product-brand').textContent.toLowerCase();
            const description = card.querySelector('.product-description').textContent.toLowerCase();
            const productId = card.querySelector('.product-id').textContent.toLowerCase();
            
            const matches = title.includes(searchTerm) || 
                          brand.includes(searchTerm) ||
                          description.includes(searchTerm) || 
                          productId.includes(searchTerm);
            
            if (matches || searchTerm === '') {
                card.style.display = 'block';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            } else {
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                setTimeout(() => {
                    card.style.display = 'none';
                }, 300);
            }
        });
    });
}

// Enhanced Scroll Animations
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.classList.add('fade-in', 'visible');
                }, index * 100);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    document.querySelectorAll('.product-card').forEach(element => {
        element.classList.add('fade-in');
        observer.observe(element);
    });
}

// Smooth Scrolling
function initSmoothScroll() {
    document.querySelector('.cta-button').addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector('#categories').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    });
}

// Theme Initialization
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const themeIcon = document.querySelector('.theme-icon');
    
    // System theme detection
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches && !savedTheme) {
        document.body.classList.add('dark');
        themeIcon.textContent = '☀️';
    } else if (savedTheme === 'dark') {
        document.body.classList.add('dark');
        themeIcon.textContent = '☀️';
    }
}

// System Theme Detection
function detectSystemTheme() {
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
        if (!localStorage.getItem('theme')) {
            if (event.matches) {
                document.body.classList.add('dark');
                document.querySelector('.theme-icon').textContent = '☀️';
            } else {
                document.body.classList.remove('dark');
                document.querySelector('.theme-icon').textContent = '🌙';
            }
        }
    });
}

// Enhanced Card Animation Stagger
function initCardAnimations() {
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        
        // Add hover effect enhancement
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// Initialize App
document.addEventListener('DOMContentLoaded', function() {
    initTheme();
    initSearch();
    initScrollAnimations();
    initSmoothScroll();
    initCardAnimations();
    detectSystemTheme();
    
    // Add loading animation complete
    document.body.style.opacity = '1';
});

// Enhanced performance with debounced scroll
let ticking = false;
function updateOnScroll() {
    if (!ticking) {
        requestAnimationFrame(() => {
            // Add any scroll-based animations here
            ticking = false;
        });
        ticking = true;
    }
}
window.addEventListener('scroll', updateOnScroll);