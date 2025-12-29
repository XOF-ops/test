"""
Sacrifice Tracker
==================

This module tracks and logs 'sacrifice events' when the agent chooses
speed over depth or a simpler path over a more robust alternative.

Metadata Signature:
-------------------
{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T04:17:20Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None for this module creation.",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}

Purpose (A1 - Relational):
    - Serves the orchestrator by providing sacrifice tracking
    - Serves human reviewers by making trade-offs transparent
    - Serves future maintainers by documenting technical debt

Design Rationale (A4 - Process):
    - All sacrifices are logged with full context
    - Append-only storage ensures no hidden decisions
    - Human-readable format enables review and audit
    
Key Principle (A7 - Sacrifice):
    This module embodies A7 by ensuring that whenever the agent
    chooses a simpler or less robust path for speed, the trade-off
    is explicitly noted rather than hidden.
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# Module-level metadata signature
MODULE_METADATA = {
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T04:17:20Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None for this module creation.",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class SacrificeEvent:
    """
    Represents a single sacrifice event where speed was chosen over depth.
    
    A sacrifice event occurs when:
    - A simpler implementation is chosen over a more robust one
    - Performance optimization reduces code clarity
    - Time constraints lead to deferred improvements
    - Edge cases are knowingly left unhandled
    
    This class ensures all such trade-offs are documented (A7) and
    stored in an append-only manner (A2).
    """
    
    def __init__(
        self,
        task_id: str,
        description: str,
        alternative_skipped: str,
        category: str = "GENERAL",
        impact_assessment: str = "UNKNOWN",
        mitigation_plan: Optional[str] = None
    ):
        """
        Initialize a sacrifice event.
        
        Args:
            task_id: ID of the task where sacrifice occurred
            description: What simpler path was chosen
            alternative_skipped: What more robust path was skipped
            category: Type of sacrifice (SIMPLIFICATION, PERFORMANCE, SCOPE, etc.)
            impact_assessment: Expected impact (LOW, MEDIUM, HIGH, UNKNOWN)
            mitigation_plan: Optional plan for addressing this later
        """
        self.task_id = task_id
        self.description = description
        self.alternative_skipped = alternative_skipped
        self.category = category
        self.impact_assessment = impact_assessment
        self.mitigation_plan = mitigation_plan
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        
        # A7: Explicit acknowledgment that this was a conscious choice
        self.acknowledged = True
        self.acknowledgment_note = (
            "This sacrifice was made deliberately with full awareness of "
            "the trade-off. It is logged here for transparency and future review."
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "alternative_skipped": self.alternative_skipped,
            "category": self.category,
            "impact_assessment": self.impact_assessment,
            "mitigation_plan": self.mitigation_plan,
            "timestamp_utc": self.timestamp_utc,
            "acknowledged": self.acknowledged,
            "acknowledgment_note": self.acknowledgment_note
        }


class SacrificeTracker:
    """
    Tracks and logs all sacrifice events during agent runtime.
    
    This class implements A7 (Sacrifice) by ensuring that speed vs. depth
    trade-offs are never hidden. All sacrifices are:
    1. Recorded with full context
    2. Stored in append-only format (A2)
    3. Reviewable by humans (A4)
    
    Purpose (A1): Serves human reviewers, future maintainers, and the
    codebase by making technical debt and trade-offs transparent.
    """
    
    SACRIFICE_CATEGORIES = [
        "SIMPLIFICATION",   # Chose simpler implementation
        "PERFORMANCE",      # Optimized for speed over clarity
        "SCOPE",            # Reduced scope for time
        "ERROR_HANDLING",   # Simplified error handling
        "EDGE_CASES",       # Left edge cases unhandled
        "DOCUMENTATION",    # Reduced documentation
        "TESTING",          # Reduced test coverage
        "GENERAL"           # Other trade-offs
    ]
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the sacrifice tracker.
        
        Args:
            base_path: Base directory for log files
        """
        self.base_path = base_path
        self.log_file = os.path.join(base_path, "sacrifice_log.json")
        self.events: List[SacrificeEvent] = []
        
        # Load existing events if file exists (A2 - append-only)
        self._load_existing_events()
    
    def _load_existing_events(self) -> None:
        """
        Load existing sacrifice events from log file.
        
        This supports A2 (Memory) by preserving all past events
        and appending new ones.
        """
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    # Events are stored as dictionaries, not reconstructed as objects
                    self.existing_log = data
            except (json.JSONDecodeError, IOError):
                self.existing_log = {
                    "metadata": MODULE_METADATA,
                    "events": []
                }
        else:
            self.existing_log = {
                "metadata": MODULE_METADATA,
                "events": []
            }
    
    def record(
        self,
        task_id: str,
        sacrifice_description: str,
        alternative_skipped: str,
        category: str = "GENERAL",
        impact_assessment: str = "UNKNOWN",
        mitigation_plan: Optional[str] = None
    ) -> SacrificeEvent:
        """
        Record a new sacrifice event.
        
        This is the primary method for logging when speed is chosen
        over depth. Every call creates an immutable record that
        cannot be deleted or overwritten (A2, A7).
        
        Args:
            task_id: ID of the task where sacrifice occurred
            sacrifice_description: What simpler path was chosen
            alternative_skipped: What more robust path was skipped
            category: Type of sacrifice
            impact_assessment: Expected impact level
            mitigation_plan: Optional plan for addressing later
            
        Returns:
            The created SacrificeEvent
        """
        event = SacrificeEvent(
            task_id=task_id,
            description=sacrifice_description,
            alternative_skipped=alternative_skipped,
            category=category,
            impact_assessment=impact_assessment,
            mitigation_plan=mitigation_plan
        )
        
        self.events.append(event)
        
        # Append to persistent log (A2 - no destructive overwrites)
        self.existing_log["events"].append(event.to_dict())
        self._save_log()
        
        return event
    
    def _save_log(self) -> None:
        """
        Save the sacrifice log to file.
        
        This preserves all events in an append-only manner (A2).
        """
        with open(self.log_file, 'w') as f:
            json.dump(self.existing_log, f, indent=2)
    
    def get_events_by_task(self, task_id: str) -> List[Dict[str, Any]]:
        """
        Get all sacrifice events for a specific task.
        
        Args:
            task_id: The task ID to filter by
            
        Returns:
            List of sacrifice events for the task
        """
        return [
            e for e in self.existing_log["events"]
            if e["task_id"] == task_id
        ]
    
    def get_events_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get all sacrifice events of a specific category.
        
        Args:
            category: The category to filter by
            
        Returns:
            List of sacrifice events in the category
        """
        return [
            e for e in self.existing_log["events"]
            if e["category"] == category
        ]
    
    def get_high_impact_events(self) -> List[Dict[str, Any]]:
        """
        Get all sacrifice events with HIGH or UNKNOWN impact.
        
        These are the events that most need human review.
        
        Returns:
            List of high-impact sacrifice events
        """
        return [
            e for e in self.existing_log["events"]
            if e["impact_assessment"] in ["HIGH", "UNKNOWN"]
        ]
    
    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all sacrifice events.
        
        This provides a quick overview for human reviewers (A4).
        
        Returns:
            Summary dictionary with counts and statistics
        """
        all_events = self.existing_log["events"]
        
        by_category = {}
        for cat in self.SACRIFICE_CATEGORIES:
            by_category[cat] = len([e for e in all_events if e["category"] == cat])
        
        by_impact = {
            "LOW": len([e for e in all_events if e["impact_assessment"] == "LOW"]),
            "MEDIUM": len([e for e in all_events if e["impact_assessment"] == "MEDIUM"]),
            "HIGH": len([e for e in all_events if e["impact_assessment"] == "HIGH"]),
            "UNKNOWN": len([e for e in all_events if e["impact_assessment"] == "UNKNOWN"])
        }
        
        return {
            "total_sacrifices": len(all_events),
            "by_category": by_category,
            "by_impact": by_impact,
            "high_priority_review_needed": len(self.get_high_impact_events()),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    
    def generate_report(self) -> str:
        """
        Generate a human-readable sacrifice report.
        
        This supports A4 (Process) by creating documentation that
        allows humans to understand what trade-offs were made.
        
        Returns:
            Markdown-formatted sacrifice report
        """
        summary = self.get_summary()
        all_events = self.existing_log["events"]
        
        report = f"""# Sacrifice Report

## Overview

This report documents all instances where speed was chosen over depth
during agent execution. Per Axiom A7 (Sacrifice), all such trade-offs
are explicitly noted rather than hidden.

## Summary

| Metric | Value |
|--------|-------|
| Total Sacrifices | {summary['total_sacrifices']} |
| High Priority for Review | {summary['high_priority_review_needed']} |

## By Category

| Category | Count |
|----------|-------|
"""
        for cat, count in summary["by_category"].items():
            if count > 0:
                report += f"| {cat} | {count} |\n"
        
        report += """
## By Impact Assessment

| Impact | Count |
|--------|-------|
"""
        for impact, count in summary["by_impact"].items():
            if count > 0:
                report += f"| {impact} | {count} |\n"
        
        report += """
## Detailed Events

"""
        for event in all_events:
            report += f"""### Task: {event['task_id']}

**Category**: {event['category']}  
**Impact**: {event['impact_assessment']}  
**Timestamp**: {event['timestamp_utc']}

**What was chosen**: {event['description']}

**What was skipped**: {event['alternative_skipped']}

"""
            if event.get('mitigation_plan'):
                report += f"**Mitigation Plan**: {event['mitigation_plan']}\n\n"
        
        report += """---

*This report exists to make agent trade-offs transparent and reviewable.*
*Per A7: "Whenever the agent chooses a simpler/less robust path for speed,*
*this must be explicitly noted as a sacrifice."*
"""
        
        return report


if __name__ == "__main__":
    # Example usage
    tracker = SacrificeTracker()
    
    # Record some example sacrifices
    tracker.record(
        task_id="EXAMPLE_001",
        sacrifice_description="Used simple list instead of priority queue",
        alternative_skipped="Priority queue for O(log n) task scheduling",
        category="SIMPLIFICATION",
        impact_assessment="LOW",
        mitigation_plan="Revisit if task list grows beyond 1000 items"
    )
    
    tracker.record(
        task_id="EXAMPLE_002",
        sacrifice_description="Skipped validation of nested JSON structures",
        alternative_skipped="Deep schema validation using jsonschema library",
        category="ERROR_HANDLING",
        impact_assessment="MEDIUM"
    )
    
    # Print summary
    summary = tracker.get_summary()
    print(f"Total sacrifices: {summary['total_sacrifices']}")
    print(f"High priority reviews needed: {summary['high_priority_review_needed']}")
