"""
Generate Architecture Diagrams for Glocal Policy Guardrail
Uses diagrams library to create professional system architecture visuals
"""

try:
    from diagrams import Diagram, Cluster, Edge
    from diagrams.onprem.client import Client
    from diagrams.onprem.compute import Server
    from diagrams.programming.framework import Flask
    from diagrams.programming.language import Python
    from diagrams.onprem.inmemory import Redis
    from diagrams.onprem.database import PostgreSQL
    from diagrams.onprem.container import Docker
    from diagrams.onprem.monitoring import Prometheus
    from diagrams.aws.compute import ECS, EC2
    from diagrams.aws.network import ELB
    from diagrams.aws.storage import S3
    from diagrams.custom import Custom
    import os
except ImportError:
    print(" 'diagrams' library not installed.")
    print(" Installing required package...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "diagrams"])
    print(" Installation complete. Please run this script again.")
    exit(0)


def create_high_level_architecture():
    """Generate high-level system architecture diagram"""
    
    graph_attr = {
        "fontsize": "14",
        "bgcolor": "transparent",
        "pad": "0.5",
        "nodesep": "0.8",
        "ranksep": "1.0"
    }
    
    with Diagram(
        "Glocal Policy Guardrail - High-Level Architecture",
        filename="docs/images/architecture_highlevel",
        direction="TB",
        graph_attr=graph_attr,
        show=False
    ):
        
        # Client Layer
        with Cluster("Client Layer"):
            web_ui = Client("Web Dashboard\n(Flask + Chart.js)")
            api_client = Client("REST API Client\n(Swagger UI)")
            cli = Python("CLI Interface\n(Batch Processor)")
        
        # Application Layer
        with Cluster("Application Layer (Policy-as-Code Engine)"):
            with Cluster("Compliance Scanner"):
                scanner = Flask("Compliance Engine\n(Flask + Gunicorn)")
                keyword_matcher = Python("Keyword Matcher\n(Regex + NLP)")
                time_validator = Python("Temporal Validator\n(dateutil)")
                feature_checker = Python("Feature Checker\n(Set Operations)")
            
            cache = Redis("Redis Cache\n(24h TTL)")
            analytics = Python("Analytics Engine\n(Visualization)")
        
        # Data Layer
        with Cluster("Data/Storage Layer"):
            policy_db = Python("Policy Database\n(YAML - 200+ rules)")
            report_store = PostgreSQL("Report Store\n(SQLite → PostgreSQL)")
            notification = Python("Notification Queue\n(Email/Slack/Discord)")
        
        # External Integration
        with Cluster("External Integration (Auto-Update Crawler)"):
            scheduler = Python("APScheduler\n(Daily @ 02:00 UTC)")
            scraper = Python("Multi-Source Scraper\n(BeautifulSoup + lxml)")
            rss_parser = Python("RSS Feed Parser\n(feedparser)")
        
        # Infrastructure
        with Cluster("Infrastructure"):
            docker = Docker("Docker Container\n(Multi-stage build)")
            prometheus = Prometheus("Prometheus\n(Metrics)")
        
        # Connections
        [web_ui, api_client, cli] >> Edge(label="HTTP/REST") >> scanner
        scanner >> keyword_matcher
        scanner >> time_validator
        scanner >> feature_checker
        [keyword_matcher, time_validator, feature_checker] >> cache
        scanner >> analytics
        
        cache >> policy_db
        scanner >> report_store
        scanner >> notification
        
        scheduler >> [scraper, rss_parser]
        [scraper, rss_parser] >> Edge(label="Policy Updates") >> policy_db
        
        scanner >> Edge(label="Metrics") >> prometheus
        docker >> Edge(label="Contains") >> scanner


def create_data_flow_diagram():
    """Generate detailed data flow diagram"""
    
    graph_attr = {
        "fontsize": "14",
        "bgcolor": "transparent",
        "pad": "0.5"
    }
    
    with Diagram(
        "Policy Validation Data Flow",
        filename="docs/images/architecture_dataflow",
        direction="LR",
        graph_attr=graph_attr,
        show=False
    ):
        
        client = Client("Content Deployment\nRequest")
        
        with Cluster("Validation Pipeline"):
            load_rules = Python("Load Country\nPolicy Rules")
            
            with Cluster("Parallel Validation"):
                check_keywords = Python("Forbidden Keywords\n(Regex Match)")
                check_time = Python("Ad Time Restrictions\n(Timezone Aware)")
                check_features = Python("Mandatory Features\n(Set Validation)")
            
            aggregate = Python("Result Aggregator\n(Severity-based)")
        
        decision = Python("Violation\nDecision")
        
        with Cluster("Output"):
            pass_result = Python(" PASS\nDeploy Approved")
            block_result = Python(" CRITICAL\nDeployment Blocked")
            report = PostgreSQL("Compliance Report\n(JSON Export)")
        
        # Flow
        client >> Edge(label="Content Metadata") >> load_rules
        load_rules >> [check_keywords, check_time, check_features]
        [check_keywords, check_time, check_features] >> aggregate
        aggregate >> Edge(label="Violations List") >> decision
        
        decision >> Edge(label="status=PASS", style="dashed", color="green") >> pass_result
        decision >> Edge(label="status=CRITICAL", style="bold", color="red") >> block_result
        [pass_result, block_result] >> report


def create_deployment_architecture():
    """Generate AWS deployment architecture diagram"""
    
    graph_attr = {
        "fontsize": "14",
        "bgcolor": "transparent",
        "pad": "0.5"
    }
    
    with Diagram(
        "Production Deployment Architecture (AWS)",
        filename="docs/images/architecture_deployment",
        direction="TB",
        graph_attr=graph_attr,
        show=False
    ):
        
        users = Client("Users/API Clients")
        
        with Cluster("AWS Cloud"):
            alb = ELB("Application Load Balancer\n(Multi-AZ)")
            
            with Cluster("Auto Scaling Group"):
                instances = [
                    ECS("Policy Guardrail\nContainer 1"),
                    ECS("Policy Guardrail\nContainer 2"),
                    ECS("Policy Guardrail\nContainer 3")
                ]
            
            with Cluster("Data Tier"):
                redis = Redis("ElastiCache Redis\n(Policy Cache)")
                rds = PostgreSQL("RDS PostgreSQL\n(Reports + Audit)")
                s3 = S3("S3 Bucket\n(Logs + Backups)")
            
            monitoring = Prometheus("CloudWatch\n(Metrics + Alarms)")
        
        # Connections
        users >> Edge(label="HTTPS") >> alb
        alb >> instances
        
        for instance in instances:
            instance >> Edge(label="Cache", style="dashed") >> redis
            instance >> Edge(label="Persist") >> rds
            instance >> Edge(label="Logs") >> s3
            instance >> Edge(label="Metrics") >> monitoring


def main():
    """Generate all architecture diagrams"""
    
    # Create output directory
    os.makedirs("docs/images", exist_ok=True)
    
    print(" Generating Architecture Diagrams...")
    print("=" * 70)
    
    try:
        print("1⃣  Creating High-Level Architecture Diagram...")
        create_high_level_architecture()
        print("    Saved: docs/images/architecture_highlevel.png")
        
        print("\n2⃣  Creating Data Flow Diagram...")
        create_data_flow_diagram()
        print("    Saved: docs/images/architecture_dataflow.png")
        
        print("\n3⃣  Creating Deployment Architecture Diagram...")
        create_deployment_architecture()
        print("    Saved: docs/images/architecture_deployment.png")
        
        print("\n" + "=" * 70)
        print(" All diagrams generated successfully!")
        print("\n Output files:")
        print("   • docs/images/architecture_highlevel.png")
        print("   • docs/images/architecture_dataflow.png")
        print("   • docs/images/architecture_deployment.png")
        print("\n Usage: Add these images to README.md or documentation")
        
    except Exception as e:
        print(f"\n Error generating diagrams: {e}")
        print("\n Troubleshooting:")
        print("   1. Ensure Graphviz is installed: sudo apt install graphviz")
        print("   2. Check Python environment: pip list | grep diagrams")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
