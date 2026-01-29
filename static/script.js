// Leaflet.js 지도에 위반 국가 표시
function renderViolationMap(violationCountries) {
    if (!window.L) return;
    var map = L.map('violationMap').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors'
    }).addTo(map);
    violationCountries.forEach(function(country) {
        var marker = L.circleMarker([country.lat, country.lng], {
            color: country.status === 'critical' ? 'red' : (country.status === 'partial' ? 'orange' : 'green'),
            radius: 10,
            fillOpacity: 0.7
        }).addTo(map);
        marker.bindPopup(`<b>${country.name}</b><br>Status: ${country.status}`);
    });
}
// Tab switching functionality
function showTab(tabName) {
 // Hide all tab contents
 const tabContents = document.querySelectorAll('.tab-content');
 tabContents.forEach(content => {
 content.classList.remove('active');
 });
 // Deactivate all tab buttons
 const tabs = document.querySelectorAll('.tab');
 tabs.forEach(tab => {
 tab.classList.remove('active');
 });
 // Activate selected tab
 document.getElementById(tabName).classList.add('active');
 event.target.closest('.tab').classList.add('active');
 
 // Initialize charts when analytics tab is shown
 if (tabName === 'analytics') {
     console.log('Analytics tab activated, initializing charts...');
     setTimeout(initCharts, 200);
 }
}
// Ad schedule toggle
function toggleAdSchedule() {
 const adScheduleSection = document.getElementById('adScheduleSection');
 const hasAds = document.getElementById('has_ads').checked;
 adScheduleSection.style.display = hasAds ? 'block' : 'none';
}
// Form submission handler
document.getElementById('checkForm').addEventListener('submit', async (e) => {
 e.preventDefault();
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
 // Process ad schedule
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
 displayResult(result);
 } catch (error) {
 console.error('Error:', error);
 alert('An error occurred during checking.');
 }
});
// Display results
function displayResult(result) {
 const resultCard = document.getElementById('resultCard');
 const resultContent = document.getElementById('resultContent');
 let statusClass = 'status-' + result.status;
 let statusIcon = result.status === 'PASS' ? '✅' : (result.status === 'WARNING' ? '⚠️' : '❌');
 let html = `
 <div class="result-status ${statusClass}">
 ${statusIcon} ${result.status}
 </div>
 <div style="margin-bottom: 1.5rem;">
 <h3 style="margin-bottom: 0.5rem;">Inspection Information</h3>
 <p><strong>Country:</strong> ${result.country.replace('_', ' ')}</p>
 <p><strong>Content:</strong> ${result.metadata.title}</p>
 <p><strong>Genre:</strong> ${result.metadata.genre}</p>
 </div>
 `;
 if (result.violations && result.violations.length > 0) {
 html += `
 <div class="violations-list">
 <h3 style="margin-bottom: 1rem;">⚠️ Violations Found</h3>
 `;
 result.violations.forEach(violation => {
 html += `
 <div class="violation-item">
 <div class="violation-severity">${violation.severity}</div>
 <div><strong>Rule:</strong> ${violation.rule_id}</div>
 <div style="margin-top: 0.5rem; color: var(--text-secondary);">${violation.message}</div>
 ${violation.recommendation ? `<div style="margin-top: 0.5rem; color: var(--primary);">💡 ${violation.recommendation}</div>` : ''}
 </div>
 `;
 });
 html += '</div>';
 } else {
 html += `
 <div style="padding: 2rem; text-align: center; background: rgba(16, 185, 129, 0.05); border-radius: var(--radius); border: 1px solid rgba(16, 185, 129, 0.2);">
 <div style="font-size: 3rem; margin-bottom: 1rem;">🎉</div>
 <h3 style="color: var(--success); margin-bottom: 0.5rem;">All Checks Passed!</h3>
 <p style="color: var(--text-secondary);">This content complies with all regulations for the specified country.</p>
 </div>
 `;
 }
 resultContent.innerHTML = html;
 resultCard.style.display = 'block';
 // Scroll to results
 resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}
// Chart initialization (Analytics tab)
function initCharts() {
 // Violations by country chart
 const violationCtx = document.getElementById('violationChart');
 if (violationCtx) {
 new Chart(violationCtx, {
 type: 'bar',
 data: {
 labels: ['South Korea', 'United States', 'Germany', 'China', 'Saudi Arabia'],
 datasets: [{
 label: 'Violation Count',
 data: [12, 8, 15, 20, 5],
 backgroundColor: [
 'rgba(239, 68, 68, 0.8)',
 'rgba(245, 158, 11, 0.8)',
 'rgba(99, 102, 241, 0.8)',
 'rgba(139, 92, 246, 0.8)',
 'rgba(16, 185, 129, 0.8)'
 ],
 borderColor: [
 'rgb(239, 68, 68)',
 'rgb(245, 158, 11)',
 'rgb(99, 102, 241)',
 'rgb(139, 92, 246)',
 'rgb(16, 185, 129)'
 ],
 borderWidth: 2
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
 color: 'rgba(51, 65, 85, 0.5)'
 },
 ticks: {
 color: '#cbd5e1'
 }
 },
 x: {
 grid: {
 display: false
 },
 ticks: {
 color: '#cbd5e1'
 }
 }
 }
 }
 });
 }
 // Category distribution chart
 const categoryCtx = document.getElementById('categoryChart');
 if (categoryCtx) {
 new Chart(categoryCtx, {
 type: 'doughnut',
 data: {
 labels: ['Privacy', 'Advertising', 'Content', 'Data Protection', 'Cultural'],
 datasets: [{
 data: [30, 25, 20, 15, 10],
 backgroundColor: [
 'rgba(99, 102, 241, 0.8)',
 'rgba(139, 92, 246, 0.8)',
 'rgba(239, 68, 68, 0.8)',
 'rgba(245, 158, 11, 0.8)',
 'rgba(16, 185, 129, 0.8)'
 ],
 borderColor: [
 'rgb(99, 102, 241)',
 'rgb(139, 92, 246)',
 'rgb(239, 68, 68)',
 'rgb(245, 158, 11)',
 'rgb(16, 185, 129)'
 ],
 borderWidth: 2
 }]
 },
 options: {
 responsive: true,
 maintainAspectRatio: true,
 plugins: {
 legend: {
 position: 'bottom',
 labels: {
 color: '#cbd5e1',
 padding: 15,
 font: {
 size: 12
 }
 }
 }
 }
 }
 });
 }
}
// Initialize charts on page load
document.addEventListener('DOMContentLoaded', function() {
 // Initialize charts when analytics tab is activated
 const analyticsTab = document.querySelector('.tab[onclick*="analytics"]');
 if (analyticsTab) {
 analyticsTab.addEventListener('click', () => {
 setTimeout(initCharts, 100);
 });
 }
});
// Monitoring Filter Functions
function filterMonitoring(status) {
 const cards = document.querySelectorAll('.monitor-card');
 const buttons = document.querySelectorAll('.filter-btn');
 // Update active button
 buttons.forEach(btn => btn.classList.remove('active'));
 event.target.classList.add('active');
 // Filter cards
 cards.forEach(card => {
 if (status === 'all') {
 card.style.display = 'block';
 } else {
 const cardStatus = card.getAttribute('data-status');
 card.style.display = cardStatus === status ? 'block' : 'none';
 }
 });
}
// Show Country Details Modal
async function showCountryDetails(country) {
 const modal = document.getElementById('countryModal');
 const modalBody = document.getElementById('modalBody');
 const modalTitle = document.getElementById('modalCountryName');
 // Show modal with loading state
 modal.style.display = 'flex';
 modalTitle.textContent = country.replace(/_/g, ' ');
 modalBody.innerHTML = '<div class="loading">Loading country details...</div>';
 try {
 const response = await fetch(`/api/country/${country}`);
 const data = await response.json();
 if (data.error) {
 modalBody.innerHTML = `<div class="error">Error: ${data.error}</div>`;
 return;
 }
 // Build detailed view
 let html = '<div class="country-details">';
 // Compliance Overview
 html += '<div class="detail-section">';
 html += '<h3>📊 Compliance Overview</h3>';
 html += '<div class="compliance-metrics">';
 html += `<div class="metric">
 <span class="metric-label">Total Checks</span>
 <span class="metric-value">${data.compliance.total_checks}</span>
 </div>`;
 html += `<div class="metric">
 <span class="metric-label">Passed</span>
 <span class="metric-value success">${data.compliance.passed_checks}</span>
 </div>`;
 html += `<div class="metric">
 <span class="metric-label">Violations</span>
 <span class="metric-value critical">${data.compliance.violations}</span>
 </div>`;
 html += `<div class="metric">
 <span class="metric-label">Compliance Rate</span>
 <span class="metric-value ${data.compliance.compliance_rate >= 95 ? 'success' : data.compliance.compliance_rate >= 80 ? 'warning' : 'critical'}">
 ${data.compliance.compliance_rate}%
 </span>
 </div>`;
 html += '</div></div>';
 // Critical Issues
 if (data.compliance.critical_issues && data.compliance.critical_issues.length > 0) {
 html += '<div class="detail-section">';
 html += '<h3>🚨 Critical Issues</h3>';
 html += '<div class="issues-list">';
 data.compliance.critical_issues.forEach(issue => {
 html += `<div class="issue-item critical">
 <div class="issue-type">${issue.type}</div>
 <div class="issue-desc">${issue.description}</div>
 <div class="issue-fix"><strong>Fix:</strong> ${issue.remediation}</div>
 </div>`;
 });
 html += '</div></div>';
 }
 // Warnings
 if (data.compliance.warnings && data.compliance.warnings.length > 0) {
 html += '<div class="detail-section">';
 html += '<h3>⚠️ Warnings</h3>';
 html += '<div class="issues-list">';
 data.compliance.warnings.forEach(warning => {
 html += `<div class="issue-item warning">
 <div class="issue-type">${warning.type}</div>
 <div class="issue-desc">${warning.description}</div>
 </div>`;
 });
 html += '</div></div>';
 }
 // Recent Updates
 if (data.recent_updates && data.recent_updates.length > 0) {
 html += '<div class="detail-section">';
 html += `<h3>📝 Recent Updates (${data.update_count} total)</h3>`;
 html += '<div class="updates-timeline">';
 data.recent_updates.forEach(update => {
 html += `<div class="timeline-item">
 <div class="timeline-date">${update.date}</div>
 <div class="timeline-content">
 <div class="timeline-title">${update.title}</div>
 <div class="timeline-meta">
 <span class="source">${update.source}</span>
 <span class="confidence badge-${update.confidence}">${update.confidence}</span>
 </div>
 </div>
 </div>`;
 });
 html += '</div></div>';
 }
 // Monitoring Sources
 if (data.sources && data.sources.length > 0) {
 html += '<div class="detail-section">';
 html += '<h3>📡 Monitoring Sources</h3>';
 html += '<div class="sources-grid">';
 data.sources.forEach(source => {
 html += `<div class="source-card">
 <div class="source-name">${source.name}</div>
 <div class="source-meta">
 <span class="badge">${source.method}</span>
 <span class="badge">${source.frequency}</span>
 </div>
 </div>`;
 });
 html += '</div></div>';
 }
 html += '</div>';
 modalBody.innerHTML = html;
 } catch (error) {
 modalBody.innerHTML = `<div class="error">Failed to load country details: ${error.message}</div>`;
 }
}
// Close Country Modal
function closeCountryModal() {
 const modal = document.getElementById('countryModal');
 modal.style.display = 'none';
}
// Close modal when clicking outside
window.onclick = function(event) {
 const modal = document.getElementById('countryModal');
 if (event.target === modal) {
 closeCountryModal();
 }
}
// Refresh Regulatory Updates
async function refreshUpdates() {
 const btn = document.querySelector('.refresh-btn');
 const updatesList = document.getElementById('updatesList');
 // Add loading state
 btn.classList.add('loading');
 btn.disabled = true;
 try {
 const response = await fetch('/api/updates');
 const data = await response.json();
 if (data.success && data.updates) {
 // Clear current list
 updatesList.innerHTML = '';
 if (data.updates.length === 0) {
 updatesList.innerHTML = `
 <div class="empty-state">
 <p>No recent regulatory updates available.</p>
 <p style="color: var(--text-secondary); font-size: 0.9rem;">Updates will appear here when detected by the monitoring system.</p>
 </div>
 `;
 } else {
 // Render updates
 data.updates.forEach(update => {
 const updateItem = document.createElement('div');
 updateItem.className = 'update-item';
 // Build confidence badge
 let confidenceBadge = '';
 if (update.confidence) {
 confidenceBadge = `<span class="confidence-badge confidence-${update.confidence}">${update.confidence.toUpperCase()}</span>`;
 }
 // Build status badge
 let statusBadge = '';
 if (update.status) {
 const statusClass = update.status.replace(/_/g, '-');
 const statusText = update.status.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
 statusBadge = `<span class="status-badge status-${statusClass}">${statusText}</span>`;
 }
 // Build time display
 let timeDisplay = '';
 if (update.time) {
 timeDisplay = `<span class="update-time">${update.time}</span>`;
 }
 // Build URL link
 let urlLink = '';
 if (update.url) {
 urlLink = `<a href="${update.url}" target="_blank" class="update-link">View Details →</a>`;
 }
 updateItem.innerHTML = `
 <div class="update-header">
 <div>
 <span class="update-source">${update.source}</span>
 <span class="update-country">${update.country}</span>
 ${confidenceBadge}
 ${statusBadge}
 </div>
 <div>
 <span class="update-date">${update.date}</span>
 ${timeDisplay}
 </div>
 </div>
 <h3 class="update-title">${update.title}</h3>
 <p class="update-summary">${update.summary}</p>
 ${urlLink}
 `;
 updatesList.appendChild(updateItem);
 });
 }
 console.log(`Loaded ${data.updates.length} updates`);
 } else {
 throw new Error(data.error || 'Failed to load updates');
 }
 } catch (error) {
 console.error('Error refreshing updates:', error);
 updatesList.innerHTML = `
 <div class="error">
 <p>Failed to refresh updates: ${error.message}</p>
 <p style="margin-top: 0.5rem; font-size: 0.9rem;">Please try again later.</p>
 </div>
 `;
 } finally {
 // Remove loading state
 btn.classList.remove('loading');
 btn.disabled = false;
 }
}

// ==========================================
// CHARTS AND VISUALIZATIONS
// ==========================================

let violationChart = null;
let categoryChart = null;

// Initialize charts when analytics tab is shown
function initCharts() {
    console.log('initCharts called');
    
    if (violationChart || categoryChart) {
        console.log('Charts already initialized');
        return; // Already initialized
    }

    console.log('Fetching analytics data...');
    // Fetch analytics data
    fetch('/api/analytics')
        .then(response => {
            console.log('Analytics response received:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Analytics data:', data);
            createViolationChart(data);
            createCategoryChart(data);
            updateInsightsCards(data);
        })
        .catch(error => {
            console.error('Error loading analytics:', error);
            // Show error message in charts
            const violationCanvas = document.getElementById('violationChart');
            const categoryCanvas = document.getElementById('categoryChart');
            if (violationCanvas) {
                const ctx = violationCanvas.getContext('2d');
                ctx.fillStyle = '#e53e3e';
                ctx.font = '14px Inter';
                ctx.fillText('Failed to load chart data', 10, 50);
            }
        });
}

// Create violation by country chart
function createViolationChart(data) {
    const ctx = document.getElementById('violationChart');
    if (!ctx) {
        console.error('violationChart canvas not found');
        return;
    }

    console.log('Creating violation chart with data:', data.violations_by_country);
    
    const countries = data.violations_by_country || {};
    const labels = Object.keys(countries);
    const values = Object.values(countries);

    if (labels.length === 0) {
        console.warn('No violation data available');
        labels.push('No Data');
        values.push(0);
    }

    violationChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Violations',
                data: values,
                backgroundColor: [
                    'rgba(244, 63, 94, 0.8)',
                    'rgba(251, 146, 60, 0.8)',
                    'rgba(250, 204, 21, 0.8)',
                    'rgba(34, 197, 94, 0.8)',
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(236, 72, 153, 0.8)',
                    'rgba(20, 184, 166, 0.8)',
                    'rgba(132, 204, 22, 0.8)'
                ],
                borderColor: [
                    'rgb(244, 63, 94)',
                    'rgb(251, 146, 60)',
                    'rgb(250, 204, 21)',
                    'rgb(34, 197, 94)',
                    'rgb(59, 130, 246)',
                    'rgb(168, 85, 247)',
                    'rgb(236, 72, 153)',
                    'rgb(20, 184, 166)',
                    'rgb(132, 204, 22)'
                ],
                borderWidth: 2,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            return `Violations: ${context.parsed.y}`;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1,
                        font: {
                            size: 12
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                x: {
                    ticks: {
                        font: {
                            size: 11
                        },
                        maxRotation: 45,
                        minRotation: 45
                    },
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Create category distribution chart
function createCategoryChart(data) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) {
        console.error('categoryChart canvas not found');
        return;
    }

    console.log('Creating category chart with data:', data.distribution_by_category);
    
    const categories = data.distribution_by_category || {};
    const labels = Object.keys(categories);
    const values = Object.values(categories);
    
    if (labels.length === 0) {
        console.warn('No category data available');
        labels.push('No Data');
        values.push(1);
    }

    categoryChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: [
                    'rgba(59, 130, 246, 0.8)',
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(251, 146, 60, 0.8)',
                    'rgba(168, 85, 247, 0.8)',
                    'rgba(236, 72, 153, 0.8)',
                    'rgba(20, 184, 166, 0.8)',
                    'rgba(132, 204, 22, 0.8)',
                    'rgba(234, 179, 8, 0.8)'
                ],
                borderColor: '#fff',
                borderWidth: 3,
                hoverOffset: 10
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
                        font: {
                            size: 12
                        },
                        usePointStyle: true,
                        pointStyle: 'circle'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Update insights cards with real data
function updateInsightsCards(data) {
    const insightsGrid = document.querySelector('.insights-grid');
    if (!insightsGrid) return;

    const insights = data.insights || [];
    
    if (insights.length > 0) {
        insightsGrid.innerHTML = insights.map(insight => `
            <div class="insight-card">
                <div class="insight-icon">${getInsightIcon(insight.type)}</div>
                <div class="insight-content">
                    <h4>${insight.title}</h4>
                    <p>${insight.description}</p>
                    ${insight.value ? `<div class="insight-value">${insight.value}</div>` : ''}
                </div>
            </div>
        `).join('');
    }
}

// Get icon for insight type
function getInsightIcon(type) {
    const icons = {
        'coverage': '🌍',
        'compliance': '✅',
        'monitoring': '👁️',
        'updates': '🔄',
        'warning': '⚠️',
        'success': '🎉',
        'info': 'ℹ️'
    };
    return icons[type] || '📊';
}

// Listen for tab changes to initialize charts
document.addEventListener('DOMContentLoaded', function() {
    // Analytics 차트 초기화
    const analyticsSection = document.getElementById('analytics');
    if (analyticsSection && analyticsSection.classList.contains('active')) {
        setTimeout(initCharts, 500);
    }

    // 지도 렌더링 (예시 데이터, 실제로는 서버에서 동적으로 받아야 함)
    if (document.getElementById('violationMap')) {
        // 예시: 위반 국가 데이터 (실제 데이터로 교체 필요)
        const violationCountries = [
            {name: 'Germany', lat: 51, lng: 10, status: 'critical'},
            {name: 'South Korea', lat: 36, lng: 128, status: 'partial'},
            {name: 'United States', lat: 39, lng: -98, status: 'compliant'},
            {name: 'Saudi Arabia', lat: 24, lng: 45, status: 'critical'},
            {name: 'India', lat: 21, lng: 78, status: 'partial'}
        ];
        renderViolationMap(violationCountries);
    }
});