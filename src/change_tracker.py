"""
Change Tracker module for compliance system.
Tracks and logs policy/regulation changes.
"""

import datetime

class ChangeTracker:
    def __init__(self):
        self.changes = []

    def log_change(self, change_type, description, user=None):
        self.changes.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'type': change_type,
            'description': description,
            'user': user
        })

    def get_recent_changes(self, limit=10):
        return self.changes[-limit:]
