// Dark mode detection and toggle
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    document.documentElement.setAttribute('data-theme', 'dark');
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', event => {
    if (event.matches) {
        document.documentElement.setAttribute('data-theme', 'dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
    }
});

// FAQ toggle functionality
function toggleFAQ(button) {
    const faqItem = button.parentElement;
    const answer = button.nextElementSibling;
    const icon = button.querySelector('.faq-icon');
    
    // Close all other FAQ items
    document.querySelectorAll('.faq-item').forEach(item => {
        if (item !== faqItem) {
            item.classList.remove('active');
        }
    });
    
    // Toggle current FAQ item
    faqItem.classList.toggle('active');
}

// Smooth scrolling for scroll indicator
document.querySelector('.scroll-indicator')?.addEventListener('click', () => {
    document.querySelector('.contact-info-section').scrollIntoView({
        behavior: 'smooth'
    });
});

// Form validation and enhancement
document.querySelector('.contact-form')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Add loading state to submit button
    const submitBtn = this.querySelector('.submit-btn');
    const originalText = submitBtn.innerHTML;
    
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Sending...';
    submitBtn.disabled = true;
    
    // Simulate form submission
    setTimeout(() => {
        submitBtn.innerHTML = '<i class="fas fa-check"></i> Sent Successfully!';
        setTimeout(() => {
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
            this.reset();
        }, 2000);
    }, 2000);
});

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all cards and sections for scroll animations
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.contact-card, .category-card, .faq-item');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
});

// Newsletter form handling
document.querySelector('.newsletter button')?.addEventListener('click', function(e) {
    e.preventDefault();
    const input = this.previousElementSibling;
    const email = input.value;
    
    if (email && email.includes('@')) {
        this.innerHTML = '<i class="fas fa-check"></i>';
        input.value = '';
        setTimeout(() => {
            this.innerHTML = '<i class="fas fa-arrow-right"></i>';
        }, 2000);
    } else {
        this.style.background = '#ff4757';
        setTimeout(() => {
            this.style.background = '';
        }, 1000);
    }
});