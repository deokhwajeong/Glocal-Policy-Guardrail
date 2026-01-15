// 탭 전환 기능
function showTab(tabName) {
    // 모든 탭 컨텐츠 숨기기
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // 모든 탭 버튼 비활성화
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 선택된 탭 활성화
    document.getElementById(tabName).classList.add('active');
    event.target.closest('.tab').classList.add('active');
}

// 광고 스케줄 토글
function toggleAdSchedule() {
    const adScheduleSection = document.getElementById('adScheduleSection');
    const hasAds = document.getElementById('has_ads').checked;
    
    adScheduleSection.style.display = hasAds ? 'block' : 'none';
}

// 폼 제출 처리
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
    
    // 광고 스케줄 처리
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
        alert('Checking...가 발생했습니다.');
    }
});

// 결과 표시
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
            <h3 style="margin-bottom: 0.5rem;">검사 정보</h3>
            <p><strong>국가:</strong> ${result.country.replace('_', ' ')}</p>
            <p><strong>콘텐츠:</strong> ${result.metadata.title}</p>
            <p><strong>장르:</strong> ${result.metadata.genre}</p>
        </div>
    `;
    
    if (result.violations && result.violations.length > 0) {
        html += `
            <div class="violations-list">
                <h3 style="margin-bottom: 1rem;">⚠️ 발견된 위반 사항</h3>
        `;
        
        result.violations.forEach(violation => {
            html += `
                <div class="violation-item">
                    <div class="violation-severity">${violation.severity}</div>
                    <div><strong>규정:</strong> ${violation.rule_id}</div>
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
                <h3 style="color: var(--success); margin-bottom: 0.5rem;">모든 검사를 Passed했습니다!</h3>
                <p style="color: var(--text-secondary);">이 콘텐츠는 해당 국가의 모든 규정을 준수합니다.</p>
            </div>
        `;
    }
    
    resultContent.innerHTML = html;
    resultCard.style.display = 'block';
    
    // 결과로 스크롤
    resultCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// 차트 초기화 (분석 탭)
function initCharts() {
    // 국가별 위반 현황 차트
    const violationCtx = document.getElementById('violationChart');
    if (violationCtx) {
        new Chart(violationCtx, {
            type: 'bar',
            data: {
                labels: ['South Korea', 'United States', 'Germany', 'China', 'Saudi Arabia'],
                datasets: [{
                    label: '위반 건수',
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
    
    // 카테고리별 분포 차트
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

// 페이지 로드 시 차트 초기화
document.addEventListener('DOMContentLoaded', () => {
    // 분석 탭이 활성화될 때 차트 초기화
    const analyticsTab = document.querySelector('.tab[onclick*="analytics"]');
    if (analyticsTab) {
        analyticsTab.addEventListener('click', () => {
            setTimeout(initCharts, 100);
        });
    }
});
