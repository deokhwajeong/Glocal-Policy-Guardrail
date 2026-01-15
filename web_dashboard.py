#!/usr/bin/env python3
"""
Web Dashboard for Glocal Policy Guardrail
Regulatory Update Monitoring Dashboard for Global OTT Platforms
"""

from flask import Flask, render_template, jsonify, request
import json
import yaml
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.policy_auto_updater import PolicyUpdateMonitor
from src.change_tracker import ChangeTracker

app = Flask(__name__)

# Global variables - lazy initialization
monitor = None
tracker = None

def init_globals():
    """Initialize global variables"""
    global monitor, tracker
    if monitor is None:
        try:
            print("Initializing PolicyUpdateMonitor...")
            monitor = PolicyUpdateMonitor()
            print(f"PolicyUpdateMonitor initialized with {len(monitor.sources)} sources")
        except Exception as e:
            print(f"Error initializing PolicyUpdateMonitor: {e}")
            import traceback
            traceback.print_exc()
            monitor = None
    
    if tracker is None:
        try:
            print("Initializing ChangeTracker...")
            tracker = ChangeTracker()
            print("ChangeTracker initialized")
        except Exception as e:
            print(f"Error initializing ChangeTracker: {e}")
            import traceback
            traceback.print_exc()
            tracker = None


@app.route('/')
def index():
    """Main dashboard page"""
    try:
        init_globals()
        
        # Generate basic statistics data
        stats = {
            'countries': len(set(s.country for s in monitor.sources)) if monitor else 0,
            'total_checks': 0,
            'success_rate': 0
        }
        
        # Country list
        countries = sorted(set(s.country for s in monitor.sources)) if monitor else []
        
        # Monitoring data (status by country)
        monitoring = {}
        if monitor:
            for country in countries:
                monitoring[country] = {
                    'status': 'active',
                    'checks': 0,
                    'violations': 0,
                    'pass_rate': 100
                }
        
        # Recent updates
        recent_updates = []
        
        # Load recent check results if available
        log_file = Path("reports/policy_updates.json")
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    logs = json.load(f)
                    if logs:
                        stats['total_checks'] = len(logs)
                        stats['success_rate'] = 95
                        
                        # Extract last 5 updates
                        for log in logs[-5:]:
                            for update in log.get('updates', []):
                                recent_updates.append({
                                    'source': update.get('source', 'Unknown'),
                                    'country': update.get('country', 'Unknown'),
                                    'date': log.get('timestamp', '')[:10],
                                    'title': update.get('title', 'Policy Update')
                                })
            except:
                pass
        
        return render_template('index.html', 
                             stats=stats, 
                             countries=countries,
                             monitoring=monitoring,
                             recent_updates=recent_updates)
    except Exception as e:
        print(f"Error in index: {e}")
        import traceback
        traceback.print_exc()
        # Render with default values on error
        return render_template('index.html', 
                             stats={'countries': 0, 'total_checks': 0, 'success_rate': 0},
                             countries=[],
                             monitoring={},
                             recent_updates=[])


@app.route('/api/status')
def get_status():
    """Get system status"""
    try:
        init_globals()
        if monitor is None or tracker is None:
            return jsonify({"error": "System not initialized"}), 500
        
        # Read recent update logs
        log_file = Path("reports/policy_updates.json")
        recent_log = None
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
                if logs and len(logs) > 0:
                    recent_log = logs[-1]
        
        # Pending changes
        pending_changes = tracker.get_pending_changes()
        approved_changes = tracker.get_approved_changes()
        
        status = {
            "total_sources": len(monitor.sources),
            "sources_by_frequency": {
                "daily": len([s for s in monitor.sources if s.check_frequency == "daily"]),
                "weekly": len([s for s in monitor.sources if s.check_frequency == "weekly"]),
                "monthly": len([s for s in monitor.sources if s.check_frequency == "monthly"])
            },
            "last_check": recent_log.get('timestamp') if recent_log else None,
            "last_update_count": recent_log.get('updates_count', 0) if recent_log else 0,
            "pending_changes": len(pending_changes),
            "approved_changes": len(approved_changes),
            "total_changes": len(tracker.changes),
            "system_status": "running"
        }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/sources')
def get_sources():
    """Get list of monitored sources"""
    try:
        init_globals()
        if monitor is None:
            return jsonify({"error": "System not initialized"}), 500
        sources = []
        for source in monitor.sources:
            sources.append({
                "country": source.country,
                "name": source.name,
                "url": source.url,
                "method": source.method,
                "frequency": source.check_frequency,
                "language": source.language
            })
        
        return jsonify({"sources": sources, "total": len(sources)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/updates')
def get_updates():
    """Get recent updates"""
    try:
        days = int(request.args.get('days', 30))
        log_file = Path("reports/policy_updates.json")
        
        if not log_file.exists():
            return jsonify({"updates": [], "total": 0})
        
        with open(log_file, 'r') as f:
            logs = json.load(f)
        
        # Filter last N days
        cutoff = datetime.now() - timedelta(days=days)
        recent_logs = [
            log for log in logs
            if datetime.fromisoformat(log['timestamp']) > cutoff
        ]
        
        # Extract all updates
        all_updates = []
        for log in recent_logs:
            for update in log.get('updates', []):
                update['log_timestamp'] = log['timestamp']
                all_updates.append(update)
        
        return jsonify({
            "updates": all_updates,
            "total": len(all_updates),
            "logs": len(recent_logs)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/changes')
def get_changes():
    """Get changes"""
    try:
        init_globals()
        if tracker is None:
            return jsonify({"error": "System not initialized"}), 500
        status_filter = request.args.get('status', 'all')
        
        if status_filter == 'pending':
            changes = tracker.get_pending_changes()
        elif status_filter == 'approved':
            changes = tracker.get_approved_changes()
        else:
            changes = tracker.changes
        
        return jsonify({
            "changes": changes,
            "total": len(changes)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/changes/<int:change_id>/approve', methods=['POST'])
def approve_change(change_id):
    """Approve a change"""
    try:
        init_globals()
        if tracker is None:
            return jsonify({"error": "System not initialized"}), 500
        data = request.get_json()
        reviewer = data.get('reviewer', 'Web User')
        
        success = tracker.approve_change(change_id, reviewer)
        
        if success:
            return jsonify({"success": True, "message": "Change approved"})
        else:
            return jsonify({"success": False, "message": "Change not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/check-now', methods=['POST'])
def check_now():
    """Run update check immediately"""
    try:
        init_globals()
        if monitor is None:
            return jsonify({"error": "System not initialized"}), 500
        data = request.get_json() or {}
        frequency = data.get('frequency', 'all')
        
        # Filter by frequency
        if frequency != 'all':
            original_sources = monitor.sources
            monitor.sources = [s for s in monitor.sources if s.check_frequency == frequency]
        
        updates = monitor.check_for_updates()
        
        # Restore original sources
        if frequency != 'all':
            monitor.sources = original_sources
        
        # Save log
        if updates:
            monitor.save_update_log(updates)
        
        return jsonify({
            "success": True,
            "updates": updates,
            "count": len(updates)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Get statistics data"""
    try:
        init_globals()
        if monitor is None:
            return jsonify({"error": "System not initialized"}), 500
        # 국가별 소스 수
        countries = {}
        for source in monitor.sources:
            country = source.country
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        # Update count for last 30 days
        log_file = Path("reports/policy_updates.json")
        daily_updates = {}
        
        if log_file.exists():
            with open(log_file, 'r') as f:
                logs = json.load(f)
            
            for log in logs[-30:]:  # Last 30 logs
                date = log['timestamp'][:10]
                count = log.get('updates_count', 0)
                daily_updates[date] = daily_updates.get(date, 0) + count
        
        return jsonify({
            "countries": countries,
            "daily_updates": daily_updates,
            "total_countries": len(countries)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    })


def main():
    """Main function"""
    import os
    
    # Create required directories
    Path("reports").mkdir(exist_ok=True)
    Path("reports/scheduler_logs").mkdir(exist_ok=True)
    
    # Run in development mode
    host = os.getenv('DASHBOARD_HOST', '0.0.0.0')
    port = int(os.getenv('DASHBOARD_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'
    
    print("=" * 70)
    print("GLOCAL POLICY GUARDRAIL - WEB DASHBOARD")
    print("=" * 70)
    print(f"Server starting on http://{host}:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    print()
    
    app.run(host=host, port=port, debug=debug)


if __name__ == '__main__':
    main()
