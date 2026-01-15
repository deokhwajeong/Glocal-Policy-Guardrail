#!/usr/bin/env python3
"""
Generate realistic sample data for Glocal Policy Guardrail
Creates sample policy updates, compliance reports, and change history
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# Realistic OTT regulatory data based on actual global regulations
COUNTRIES = [
    "South_Korea", "United_States", "United_Kingdom", "Germany", "France",
    "Japan", "India", "Brazil", "Australia", "Canada", "Singapore",
    "Netherlands", "Spain", "Italy", "Mexico"
]

REGULATORY_UPDATES = {
    "South_Korea": [
        "K-Content mandatory subtitle requirements updated",
        "New content rating guidelines for streaming platforms",
        "Local content quota increased to 30%",
        "Platform registration requirements revised",
        "Advertisement time restrictions modified"
    ],
    "United_States": [
        "COPPA compliance requirements updated for children's content",
        "Closed captioning requirements for VOD services",
        "State-level privacy regulations harmonization",
        "FCC accessibility guidelines updated",
        "Content rating system aligned with MPAA standards"
    ],
    "European_Union": [
        "GDPR cookie consent requirements clarified",
        "Digital Services Act implementation deadline set",
        "AVMSD quota requirements for European content",
        "Age verification standards for mature content",
        "Cross-border content licensing simplified"
    ],
    "United_Kingdom": [
        "Ofcom streaming service regulations updated",
        "Brexit-related content licensing changes",
        "VOD accessibility requirements enhanced",
        "Harmful content regulation framework published",
        "Product placement disclosure rules revised"
    ],
    "Germany": [
        "Youth Protection Act amendments for streaming",
        "FSK rating system integration requirements",
        "Staatsvertrag obligations for VOD platforms",
        "Local language audio track requirements",
        "Advertising restrictions during children's programming"
    ],
    "Japan": [
        "Broadcasting Ethics regulations for streaming updated",
        "Content rating system alignment with EIRIN",
        "Disaster warning system integration required",
        "Local content promotion guidelines",
        "Privacy protection law compliance deadline"
    ],
    "India": [
        "Information Technology Rules for OTT platforms",
        "Self-classification system for content rating",
        "Regional language content requirements",
        "Parental control features mandatory",
        "Intermediary guidelines compliance required"
    ],
    "Brazil": [
        "Portuguese subtitles mandatory for foreign content",
        "ANCINE registration requirements updated",
        "Content rating (Classificação Indicativa) revised",
        "Tax obligations for streaming services clarified",
        "Accessibility features for hearing impaired required"
    ],
    "Australia": [
        "ACMA streaming service licensing framework",
        "Classification requirements for VOD content",
        "Australian content quota for SVOD services",
        "Closed captioning standards updated",
        "Privacy Act compliance for data collection"
    ],
    "Canada": [
        "CRTC online streaming regulations finalized",
        "CanCon requirements for streaming platforms",
        "French language content quotas in Quebec",
        "Accessibility standards for broadcasting",
        "Bill C-11 implementation guidelines"
    ]
}

SOURCES = [
    "Ministry of Culture, Sports and Tourism",
    "Federal Communications Commission",
    "European Commission",
    "Ofcom",
    "Bundesnetzagentur",
    "Ministry of Internal Affairs and Communications",
    "Ministry of Information and Broadcasting",
    "ANCINE",
    "ACMA",
    "CRTC"
]

VIOLATION_TYPES = [
    "Missing required subtitles",
    "Incorrect content rating",
    "Inadequate parental controls",
    "Non-compliant privacy policy",
    "Missing accessibility features",
    "Local content quota not met",
    "Advertisement time exceeded",
    "Age verification not implemented",
    "Required metadata missing",
    "Geographic restriction violation"
]

def generate_policy_updates(num_days=90, updates_per_day=2):
    """Generate realistic policy update logs"""
    updates_log = []
    
    for i in range(num_days):
        date = datetime.now() - timedelta(days=num_days - i)
        
        for _ in range(random.randint(1, updates_per_day)):
            country = random.choice(COUNTRIES)
            country_updates = REGULATORY_UPDATES.get(country, REGULATORY_UPDATES["South_Korea"])
            
            log_entry = {
                "timestamp": date.isoformat(),
                "updates_count": random.randint(1, 5),
                "updates": []
            }
            
            for _ in range(log_entry["updates_count"]):
                update = {
                    "country": country,
                    "source": random.choice(SOURCES),
                    "title": random.choice(country_updates),
                    "url": f"https://example.gov/{country.lower()}/regulation-{random.randint(1000, 9999)}",
                    "confidence": random.choice(["high", "high", "high", "medium"]),
                    "detected_at": date.isoformat(),
                    "status": "pending_review"
                }
                log_entry["updates"].append(update)
            
            updates_log.append(log_entry)
    
    return updates_log

def generate_compliance_report():
    """Generate comprehensive compliance report"""
    report = {
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "total_countries": len(COUNTRIES),
            "compliant_countries": random.randint(10, 13),
            "partial_compliance": random.randint(2, 4),
            "non_compliant": random.randint(0, 1),
            "total_checks": random.randint(450, 550),
            "violations_found": random.randint(15, 35)
        },
        "country_details": {}
    }
    
    for country in COUNTRIES:
        checks = random.randint(25, 45)
        violations = random.randint(0, 5)
        
        report["country_details"][country] = {
            "compliance_status": "compliant" if violations == 0 else "partial" if violations < 3 else "non_compliant",
            "total_checks": checks,
            "passed_checks": checks - violations,
            "violations": violations,
            "compliance_rate": round((checks - violations) / checks * 100, 2),
            "last_checked": (datetime.now() - timedelta(days=random.randint(0, 7))).isoformat(),
            "critical_issues": [],
            "warnings": []
        }
        
        if violations > 0:
            for _ in range(violations):
                issue = {
                    "type": random.choice(VIOLATION_TYPES),
                    "severity": random.choice(["high", "medium", "low"]),
                    "description": f"Compliance issue detected in {country}",
                    "remediation": "Update content metadata and implement required features"
                }
                
                if issue["severity"] == "high":
                    report["country_details"][country]["critical_issues"].append(issue)
                else:
                    report["country_details"][country]["warnings"].append(issue)
    
    return report

def generate_change_history():
    """Generate change tracking history"""
    changes = []
    change_id = 1
    
    for i in range(50):
        date = datetime.now() - timedelta(days=random.randint(0, 90))
        country = random.choice(COUNTRIES)
        
        change = {
            "id": change_id,
            "timestamp": date.isoformat(),
            "country": country,
            "change_type": random.choice(["update", "new", "deprecated"]),
            "field": random.choice(["content_rating", "subtitle_requirement", "quota", "privacy_policy", "accessibility"]),
            "old_value": "Previous requirement" if change_id > 10 else None,
            "new_value": random.choice(REGULATORY_UPDATES.get(country, REGULATORY_UPDATES["South_Korea"])),
            "source": random.choice(SOURCES),
            "source_url": f"https://example.gov/{country.lower()}/update-{change_id}",
            "confidence": random.choice(["high", "high", "medium"]),
            "approved": random.choice([True, True, True, False]),
            "applied": random.choice([True, True, False]),
            "reviewer": random.choice(["compliance_team", "legal_team", "product_manager", None])
        }
        
        changes.append(change)
        change_id += 1
    
    return {"changes": changes, "versions": []}

def main():
    """Generate all sample data"""
    print("Generating realistic sample data for OTT compliance platform...")
    
    # Create directories
    Path("reports").mkdir(exist_ok=True)
    Path("reports/change_history").mkdir(exist_ok=True)
    
    # Generate policy updates
    print("📝 Generating policy updates (90 days)...")
    updates = generate_policy_updates(num_days=90, updates_per_day=2)
    with open("reports/policy_updates.json", "w") as f:
        json.dump(updates, f, indent=2)
    print(f"   ✅ Created {len(updates)} policy update entries")
    
    # Generate compliance report
    print("📊 Generating compliance report...")
    report = generate_compliance_report()
    with open("reports/compliance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"   ✅ Created compliance report for {len(COUNTRIES)} countries")
    
    # Generate change history
    print("📜 Generating change history...")
    history = generate_change_history()
    with open("reports/change_history/changes.json", "w") as f:
        json.dump(history, f, indent=2)
    print(f"   ✅ Created {len(history['changes'])} change records")
    
    print("\n✨ Sample data generation complete!")
    print("\n📈 Summary:")
    print(f"   - Policy Updates: {len(updates)} entries over 90 days")
    print(f"   - Total Regulatory Changes: {sum(log['updates_count'] for log in updates)}")
    print(f"   - Countries Monitored: {len(COUNTRIES)}")
    print(f"   - Compliance Checks: {report['summary']['total_checks']}")
    print(f"   - Violations Found: {report['summary']['violations_found']}")
    print(f"   - Change Records: {len(history['changes'])}")
    
if __name__ == "__main__":
    main()
