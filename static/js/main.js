/**
 * Main JavaScript file for Portfolio Application
 */

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

/**
 * Initialize the application
 */
function initializeApp() {
    initializeTooltips();
    initializeAnimations();
    initializeFormEnhancements();
    initializeImageLazyLoading();
    initializeSearchDebounce();
    initializeThemeToggle();
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Initialize scroll animations
 */
function initializeAnimations() {
    // Add fade-in animation to elements as they come into view
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe cards and major sections
    document.querySelectorAll('.card, .timeline-item, .hero-section').forEach(el => {
        observer.observe(el);
    });
}

/**
 * Enhance forms with better UX
 */
function initializeFormEnhancements() {
    // Auto-resize textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // File input preview
    document.querySelectorAll('input[type="file"]').forEach(input => {
        if (input.accept && input.accept.includes('image')) {
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function(e) {
                        showImagePreview(input, e.target.result);
                    };
                    reader.readAsDataURL(file);
                }
            });
        }
    });

    // Form validation feedback
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

/**
 * Show image preview for file inputs
 */
function showImagePreview(input, src) {
    let preview = input.parentNode.querySelector('.image-preview');
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'image-preview mt-2';
        input.parentNode.appendChild(preview);
    }
    
    preview.innerHTML = `
        <img src="${src}" class="img-thumbnail" style="max-width: 200px; max-height: 200px;">
        <button type="button" class="btn btn-sm btn-outline-danger ms-2" onclick="clearImagePreview(this)">
            <i class="fas fa-times"></i>
        </button>
    `;
}

/**
 * Clear image preview
 */
function clearImagePreview(button) {
    const preview = button.parentNode;
    const input = preview.parentNode.querySelector('input[type="file"]');
    input.value = '';
    preview.remove();
}

/**
 * Initialize lazy loading for images
 */
function initializeImageLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy-load');
                    imageObserver.unobserve(img);
                }
            });
        });

        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * Initialize search with debounce
 */
function initializeSearchDebounce() {
    const searchInputs = document.querySelectorAll('input[name="search"]');
    let searchTimeout;

    searchInputs.forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 500ms of no typing
                const form = input.closest('form');
                if (form && input.value.length >= 3) {
                    form.submit();
                }
            }, 500);
        });
    });
}

/**
 * Initialize theme toggle (if needed)
 */
function initializeThemeToggle() {
    // Future implementation for theme switching
    // Currently using fixed dark theme from Bootstrap
}

/**
 * Utility function to show loading state
 */
function showLoading(element) {
    if (element) {
        element.classList.add('loading');
        const originalHTML = element.innerHTML;
        element.dataset.originalHtml = originalHTML;
        
        if (element.tagName === 'BUTTON') {
            element.innerHTML = '<i class="fas fa-spinner spinner me-2"></i>Loading...';
            element.disabled = true;
        }
    }
}

/**
 * Utility function to hide loading state
 */
function hideLoading(element) {
    if (element && element.dataset.originalHtml) {
        element.classList.remove('loading');
        element.innerHTML = element.dataset.originalHtml;
        
        if (element.tagName === 'BUTTON') {
            element.disabled = false;
        }
        
        delete element.dataset.originalHtml;
    }
}

/**
 * Utility function to show toast notifications
 */
function showToast(message, type = 'info') {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }

    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="fas fa-${getToastIcon(type)} me-2 text-${type}"></i>
                <strong class="me-auto">Notification</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;

    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Show toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

/**
 * Get appropriate icon for toast type
 */
function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Utility function to copy text to clipboard
 */
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showToast('Copied to clipboard!', 'success');
        return true;
    } catch (err) {
        console.error('Failed to copy text: ', err);
        showToast('Failed to copy to clipboard', 'danger');
        return false;
    }
}

/**
 * Utility function to format dates
 */
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    const formatOptions = { ...defaultOptions, ...options };
    return new Date(date).toLocaleDateString(undefined, formatOptions);
}

/**
 * Utility function to truncate text
 */
function truncateText(text, maxLength = 100) {
    if (text.length <= maxLength) return text;
    return text.substr(0, maxLength) + '...';
}

/**
 * Utility function to validate email
 */
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Utility function to validate URL
 */
function isValidURL(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

/**
 * Handle like button clicks with AJAX
 */
function handleLikeButton(button, projectId) {
    showLoading(button);
    
    fetch(`/project/${projectId}/like`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        const likeCount = button.querySelector('.like-count');
        const likeText = button.querySelector('.like-text');
        
        if (likeCount) likeCount.textContent = data.like_count;
        if (likeText) likeText.textContent = data.liked ? 'Liked' : 'Like';
        
        if (data.liked) {
            button.classList.remove('btn-outline-danger');
            button.classList.add('btn-danger');
        } else {
            button.classList.remove('btn-danger');
            button.classList.add('btn-outline-danger');
        }
        
        showToast(data.liked ? 'Project liked!' : 'Like removed', 'success');
    })
    .catch(error => {
        console.error('Error:', error);
        showToast('Failed to update like', 'danger');
    })
    .finally(() => {
        hideLoading(button);
    });
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Add to favorites (localStorage)
 */
function addToFavorites(projectId, projectTitle) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    
    if (!favorites.some(fav => fav.id === projectId)) {
        favorites.push({ id: projectId, title: projectTitle, addedAt: new Date().toISOString() });
        localStorage.setItem('favorites', JSON.stringify(favorites));
        showToast(`"${projectTitle}" added to favorites!`, 'success');
        return true;
    } else {
        showToast('Project is already in favorites', 'info');
        return false;
    }
}

/**
 * Remove from favorites
 */
function removeFromFavorites(projectId) {
    let favorites = JSON.parse(localStorage.getItem('favorites') || '[]');
    favorites = favorites.filter(fav => fav.id !== projectId);
    localStorage.setItem('favorites', JSON.stringify(favorites));
    showToast('Removed from favorites', 'success');
}

/**
 * Get favorites from localStorage
 */
function getFavorites() {
    return JSON.parse(localStorage.getItem('favorites') || '[]');
}

// Export functions for use in templates
window.Portfolio = {
    showLoading,
    hideLoading,
    showToast,
    copyToClipboard,
    formatDate,
    truncateText,
    isValidEmail,
    isValidURL,
    handleLikeButton,
    addToFavorites,
    removeFromFavorites,
    getFavorites
};
