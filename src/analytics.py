"""
Glocal Policy Guardrail - Visualization & Analytics
컴플라이언스 검사 결과를 시각화하고 분석하는 도구
"""

import json
from datetime import datetime
from typing import Dict, List
from collections import defaultdict


class ComplianceAnalytics:
    """컴플라이언스 검사 결과 분석 및 시각화"""
    
    def __init__(self):
        self.results_history = []
    
    def add_result(self, result_dict: Dict):
        """결과 추가"""
        self.results_history.append(result_dict)
    
    def generate_risk_heatmap(self, results: Dict) -> str:
        """국가별 위험도 히트맵 생성 (ASCII 아트)"""
        country_scores = {}
        
        for deployment_id, result in results.items():
            country = result.country
            violations = len(result.violations)
            
            if country not in country_scores:
                country_scores[country] = {'total': 0, 'count': 0}
            
            country_scores[country]['total'] += violations
            country_scores[country]['count'] += 1
        
        # 평균 위반 수 계산
        avg_violations = {
            country: scores['total'] / scores['count']
            for country, scores in country_scores.items()
        }
        
        # 히트맵 생성
        heatmap = ["", "🌍 GLOBAL COMPLIANCE RISK HEATMAP", "=" * 70]
        
        max_violations = max(avg_violations.values()) if avg_violations else 1
        
        for country, avg in sorted(avg_violations.items(), key=lambda x: x[1], reverse=True):
            bar_length = int((avg / max_violations) * 40) if max_violations > 0 else 0
            risk_level = self._get_risk_emoji(avg)
            
            bar = "█" * bar_length + "░" * (40 - bar_length)
            heatmap.append(f"{risk_level} {country:20} │{bar}│ {avg:.2f} avg violations")
        
        heatmap.append("=" * 70)
        return "\n".join(heatmap)
    
    def _get_risk_emoji(self, avg_violations: float) -> str:
        """위반 수에 따른 위험도 이모지"""
        if avg_violations >= 5:
            return "🔴"
        elif avg_violations >= 3:
            return "🟠"
        elif avg_violations >= 1:
            return "🟡"
        else:
            return "🟢"
    
    def generate_violation_breakdown(self, results: Dict) -> str:
        """위반 유형별 분류"""
        violation_types = defaultdict(int)
        
        for result in results.values():
            for violation in result.violations:
                violation_types[violation['type']] += 1
        
        breakdown = ["", "📊 VIOLATION TYPE BREAKDOWN", "=" * 70]
        
        total_violations = sum(violation_types.values())
        
        for v_type, count in sorted(violation_types.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_violations * 100) if total_violations > 0 else 0
            bar_length = int(percentage / 2.5)  # 40칸 기준
            bar = "█" * bar_length
            
            breakdown.append(f"{v_type:30} │{bar:40}│ {count:3} ({percentage:5.1f}%)")
        
        breakdown.append("=" * 70)
        breakdown.append(f"Total Violations: {total_violations}")
        
        return "\n".join(breakdown)
    
    def generate_severity_distribution(self, results: Dict) -> str:
        """심각도 분포 차트"""
        severity_counts = defaultdict(int)
        
        for result in results.values():
            for violation in result.violations:
                severity_counts[violation['severity']] += 1
        
        chart = ["", "⚠️  SEVERITY DISTRIBUTION", "=" * 70]
        
        severity_order = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
        total = sum(severity_counts.values())
        
        for severity in severity_order:
            count = severity_counts.get(severity, 0)
            if count == 0:
                continue
            
            percentage = (count / total * 100) if total > 0 else 0
            bar_length = int(percentage / 2.5)
            
            emoji = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }[severity]
            
            bar = "█" * bar_length
            chart.append(f"{emoji} {severity:10} │{bar:40}│ {count:3} ({percentage:5.1f}%)")
        
        chart.append("=" * 70)
        return "\n".join(chart)
    
    def generate_executive_summary(self, results: Dict) -> str:
        """경영진용 요약 리포트"""
        total = len(results)
        passed = sum(1 for r in results.values() if r.status == "PASS")
        critical = sum(1 for r in results.values() if r.status == "CRITICAL")
        
        total_violations = sum(len(r.violations) for r in results.values())
        
        # 가장 위험한 국가
        country_risk = defaultdict(int)
        for result in results.values():
            if result.status == "CRITICAL":
                country_risk[result.country] += 1
        
        highest_risk_country = max(country_risk.items(), key=lambda x: x[1])[0] if country_risk else "N/A"
        
        summary = [
            "",
            "┏" + "━" * 68 + "┓",
            "┃" + " " * 15 + "EXECUTIVE COMPLIANCE SUMMARY" + " " * 25 + "┃",
            "┗" + "━" * 68 + "┛",
            "",
            f"📅 Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "📈 KEY METRICS:",
            f"   • Total Deployments Reviewed: {total}",
            f"   • Compliance Pass Rate: {(passed/total*100):.1f}%" if total > 0 else "   • Compliance Pass Rate: N/A",
            f"   • Critical Violations: {critical}",
            f"   • Total Violations Found: {total_violations}",
            "",
            "🎯 RISK ASSESSMENT:",
            f"   • Highest Risk Market: {highest_risk_country}",
            f"   • Average Violations per Deployment: {(total_violations/total):.2f}" if total > 0 else "   • Average Violations per Deployment: 0.00",
            "",
            "💡 RECOMMENDATIONS:",
            "   • Review and update policies for high-risk markets",
            "   • Implement additional content filtering for CRITICAL violations",
            "   • Schedule compliance training for content teams",
            "",
            "━" * 70
        ]
        
        return "\n".join(summary)
    
    def export_to_json(self, results: Dict, filepath: str = "compliance_report.json"):
        """JSON 형식으로 리포트 내보내기"""
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "total_deployments": len(results),
            "results": [result.to_dict() for result in results.values()]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return f"✅ Report exported to {filepath}"


def generate_full_analytics_report(results: Dict) -> str:
    """전체 분석 리포트 생성"""
    analytics = ComplianceAnalytics()
    
    report_sections = [
        analytics.generate_executive_summary(results),
        analytics.generate_risk_heatmap(results),
        analytics.generate_violation_breakdown(results),
        analytics.generate_severity_distribution(results)
    ]
    
    return "\n".join(report_sections)


if __name__ == "__main__":
    print("📊 Compliance Analytics Module")
    print("This module is imported by main.py for visualization")
