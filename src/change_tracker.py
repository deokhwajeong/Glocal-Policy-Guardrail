#!/usr/bin/env python3
"""
Regulatory Policy Change Tracking System
"""
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import hashlib
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PolicyChange:
    """Policy change record"""
    timestamp: str
    country: str
    field: str
    old_value: Optional[str]
    new_value: str
    source: str

class ChangeTracker:
    """Tracks regulatory updates and manages change history"""
    
    def __init__(self):
        self.history_path = Path("reports/change_history/changes.json")
        self.history_path.parent.mkdir(parents=True, exist_ok=True)
        
    def track_change(self, change: PolicyChange) -> None:
        """Track a new policy change"""
        history = self._load_history()
        history.append({
            "timestamp": change.timestamp,
            "country": change.country,
            "field": change.field,
            "old_value": change.old_value,
            "new_value": change.new_value,
            "source": change.source
        })
        self._save_history(history)
        
    def _load_history(self) -> List[Dict]:
        """Load change history"""
        if self.history_path.exists():
            with open(self.history_path, 'r') as f:
                return json.load(f)
        return []
        
    def _save_history(self, history: List[Dict]) -> None:
        """Save change history"""
        with open(self.history_path, 'w') as f:
            json.dump(history[-100:], f, indent=2)
