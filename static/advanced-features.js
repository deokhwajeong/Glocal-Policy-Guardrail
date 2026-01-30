// Advanced UI Features - Enterprise Grade

// Toast Notification System
class ToastManager {
    constructor() {
        this.container = document.getElementById('toastContainer');
    }
    
    show(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        
        const icons = {
            success: '✓',
            error: '✕',
            warning: '⚠',
            info: 'ℹ'
        };
        
        toast.innerHTML = `
            <div class="toast-icon">${icons[type] || icons.info}</div>
            <div class="toast-content">
                <div class="toast-title">${type.charAt(0).toUpperCase() + type.slice(1)}</div>
                <div class="toast-message">${message}</div>
            </div>
        `;
        
        this.container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, duration);
    }
}

const toast = new ToastManager();

// Loading Overlay
const loadingOverlay = {
    show(message = 'Processing...') {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            const text = overlay.querySelector('.loading-text');
            if (text) text.textContent = message;
            overlay.classList.add('active');
        }
    },
    
    hide() {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            overlay.classList.remove('active');
        }
    }
};

// Enhanced Form Submission with Loading
const originalFormHandler = document.getElementById('checkForm').onsubmit;
document.getElementById('checkForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    loadingOverlay.show('Checking compliance...');
    
    const formData = new FormData(e.target);
    const data = {
        country: formData.get('country'),
        content_metadata: {
            title: formData.get('title'),
            genre: formData.get('genre'),
            description: formData.get('description'),
            tags: formData.get('tags') ? formData.get('tags').split(',').map(t => t.trim()) : [],
            features: []
        }
    };
    
    if (formData.get('has_ads')) {
        const adDate = formData.get('ad_date');
        const adTime = formData.get('ad_time');
        if (adDate && adTime) {
            data.ad_schedule = {
                scheduled_time: `${adDate}T${adTime}:00`
            };
        }
    }
    
    try {
        const response = await fetch('/api/check', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        loadingOverlay.hide();
        
        if (result.status === 'PASS') {
            toast.show('All compliance checks passed!', 'success');
        } else if (result.status === 'WARNING') {
            toast.show('Compliance check completed with warnings', 'warning');
        } else {
            toast.show('Compliance violations detected', 'error');
        }
        
        displayResult(result);
        
        // Smooth scroll to results
        document.getElementById('resultCard').scrollIntoView({ 
            behavior: 'smooth',
            block: 'nearest'
        });
        
    } catch (error) {
        loadingOverlay.hide();
        toast.show('An error occurred during checking', 'error');
        console.error('Error:', error);
    }
});

// Chart Initialization with Animation
function initializeCharts() {
    // Violation Chart
    const violationCtx = document.getElementById('violationChart');
    if (violationCtx) {
        new Chart(violationCtx, {
            type: 'bar',
            data: {
                labels: ['South Korea', 'Japan', 'USA', 'EU', 'Brazil', 'India'],
                datasets: [{
                    label: 'Violations',
                    data: [12, 19, 3, 5, 2, 3],
                    backgroundColor: [
                        'rgba(26, 54, 93, 0.8)',
                        'rgba(26, 54, 93, 0.7)',
                        'rgba(26, 54, 93, 0.6)',
                        'rgba(26, 54, 93, 0.5)',
                        'rgba(26, 54, 93, 0.4)',
                        'rgba(26, 54, 93, 0.3)'
                    ],
                    borderColor: 'rgba(26, 54, 93, 1)',
                    borderWidth: 1,
                    borderRadius: 8
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        grid: {
                            color: 'rgba(0, 0, 0, 0.05)'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        }
                    }
                },
                animation: {
                    duration: 1500,
                    easing: 'easeInOutQuart'
                }
            }
        });
    }
    
    // Category Chart
    const categoryCtx = document.getElementById('categoryChart');
    if (categoryCtx) {
        new Chart(categoryCtx, {
            type: 'doughnut',
            data: {
                labels: ['Content Rating', 'Ad Compliance', 'Data Privacy', 'Geo-restrictions', 'Other'],
                datasets: [{
                    data: [35, 25, 20, 15, 5],
                    backgroundColor: [
                        'rgba(26, 54, 93, 0.9)',
                        'rgba(49, 130, 206, 0.9)',
                        'rgba(47, 133, 90, 0.9)',
                        'rgba(214, 158, 46, 0.9)',
                        'rgba(160, 174, 192, 0.9)'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 15,
                            usePointStyle: true
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1500
                }
            }
        });
    }
}

// Initialize charts when analytics tab is shown
const analyticsTab = document.querySelector('[onclick*="analytics"]');
if (analyticsTab) {
    analyticsTab.addEventListener('click', () => {
        setTimeout(initializeCharts, 100);
    });
}

// Scroll to Top Button
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.className = 'scroll-to-top';
scrollToTopBtn.innerHTML = '↑';
scrollToTopBtn.setAttribute('aria-label', 'Scroll to top');
document.body.appendChild(scrollToTopBtn);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTopBtn.classList.add('visible');
    } else {
        scrollToTopBtn.classList.remove('visible');
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// Counter Animation for Stats
function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

// Animate counters on page load
window.addEventListener('load', () => {
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        const target = parseInt(stat.textContent);
        if (!isNaN(target)) {
            animateCounter(stat, target, 1500);
        }
    });
});

// Enhanced Refresh Button with Animation
window.refreshUpdatesEnhanced = async function() {
    const btn = event.target.closest('.refresh-btn');
    const icon = btn.querySelector('.refresh-icon');
    
    // Show loading state
    btn.disabled = true;
    if (icon) {
        icon.style.animation = 'spin 1s linear infinite';
    }
    
    loadingOverlay.show('Fetching latest updates...');
    
    try {
        await refreshUpdates();
        toast.show('Updates refreshed successfully', 'success');
    } catch (error) {
        toast.show('Failed to refresh updates', 'error');
    } finally {
        loadingOverlay.hide();
        btn.disabled = false;
        if (icon) {
            icon.style.animation = '';
        }
    }
};

// Smooth Scroll for Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
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

// Progressive Enhancement - Add ripple effect to buttons
document.querySelectorAll('.btn, .filter-btn, .tab').forEach(button => {
    button.classList.add('ripple');
});

// Auto-hide alerts after interaction
document.addEventListener('click', (e) => {
    if (e.target.closest('.alert')) {
        setTimeout(() => {
            e.target.closest('.alert').style.animation = 'fadeOut 0.3s ease';
            setTimeout(() => e.target.closest('.alert').remove(), 300);
        }, 3000);
    }
});

// Keyboard Navigation Enhancement
document.addEventListener('keydown', (e) => {
    // ESC to close modal
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal[style*="flex"]');
        if (modal) {
            closeCountryModal();
        }
    }
});

// Performance Monitoring
if ('PerformanceObserver' in window) {
    const observer = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
            console.log(`${entry.name}: ${entry.duration}ms`);
        }
    });
    observer.observe({ entryTypes: ['measure'] });
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('Advanced UI features initialized');
    
    // Show welcome toast
    setTimeout(() => {
        toast.show('Welcome to Glocal Policy Guardrail', 'info', 4000);
    }, 500);
});

// ====== Update-link Tooltip Feature ======
function createTooltip() {
    let tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    document.body.appendChild(tooltip);
    return tooltip;
}

let tooltip = null;
document.addEventListener('mouseover', function(e) {
    if (e.target.classList.contains('update-link')) {
        if (!tooltip) tooltip = createTooltip();
        tooltip.textContent = e.target.getAttribute('data-summary');
        tooltip.style.display = 'block';
        tooltip.style.position = 'absolute';
        tooltip.style.left = (e.pageX + 15) + 'px';
        tooltip.style.top = (e.pageY + 15) + 'px';
        tooltip.style.zIndex = 9999;
        tooltip.style.maxWidth = '320px';
    }
});

document.addEventListener('mousemove', function(e) {
    if (tooltip && tooltip.style.display === 'block') {
        tooltip.style.left = (e.pageX + 15) + 'px';
        tooltip.style.top = (e.pageY + 15) + 'px';
    }
});

document.addEventListener('mouseout', function(e) {
    if (e.target.classList.contains('update-link') && tooltip) {
        tooltip.style.display = 'none';
    }
});
