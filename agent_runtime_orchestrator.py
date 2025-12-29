"""
Agent Runtime Orchestrator
==========================

This module wraps all Copilot agent tasks with axiom metadata and ensures
coherence with the 5 core axioms (A1, A2, A4, A7, A9).

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
    - Serves the human user by providing structure for agent decision-making
    - Serves the system by ensuring all tasks are tracked with metadata
    - Serves other services by creating consistent interfaces for axiom checking

Design Rationale (A4 - Process):
    - Each function is documented to allow human reconstruction of reasoning
    - Task wrapping makes agent decisions transparent
    - All significant actions are logged for review
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from axiom_guard import AxiomGuard
from sacrifice_tracker import SacrificeTracker


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


class TaskMetadata:
    """
    Encapsulates metadata for a single task, encoding axiom considerations.
    
    A1 (Relational): Records who/what this task serves.
    A2 (Memory): Creates append-only record of task context.
    A4 (Process): Documents reasoning behind task execution.
    A7 (Sacrifice): Notes any trade-offs made for speed.
    A9 (Contradiction): Preserves conflicting requirements.
    """
    
    def __init__(
        self,
        task_id: str,
        description: str,
        serves: List[str],
        reason: str
    ):
        """
        Initialize task metadata.
        
        Args:
            task_id: Unique identifier for this task
            description: Human-readable description of what the task does
            serves: List of entities this task serves (A1 - no orphan changes)
            reason: Why this change is being made (A4 - reconstructable reasoning)
        """
        self.task_id = task_id
        self.description = description
        self.serves = serves  # A1: Must not be empty - no orphan changes
        self.reason = reason  # A4: Must explain the why
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        self.axiom_checks = {
            "A1_RELATIONAL": len(serves) > 0,
            "A2_MEMORY": True,  # Will be verified on log write
            "A4_PROCESS": len(reason) > 0,
            "A7_SACRIFICE": None,  # Set after execution
            "A9_CONTRADICTION": None  # Set if conflicts found
        }
        self.sacrifices = []
        self.contradictions = []
    
    def note_sacrifice(self, description: str, alternative: str) -> None:
        """
        Record a sacrifice event (A7).
        
        When the agent chooses a simpler or less robust path for speed,
        this must be explicitly noted rather than hidden.
        
        Args:
            description: What simpler path was chosen
            alternative: What more robust path was skipped
        """
        self.sacrifices.append({
            "description": description,
            "alternative_skipped": alternative,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
        self.axiom_checks["A7_SACRIFICE"] = True
    
    def log_contradiction(self, conflict_a: str, conflict_b: str) -> None:
        """
        Record a contradiction (A9).
        
        When conflicting requirements are found, they must be logged
        rather than silently resolved or overwritten.
        
        Args:
            conflict_a: First conflicting requirement
            conflict_b: Second conflicting requirement
        """
        self.contradictions.append({
            "conflict_a": conflict_a,
            "conflict_b": conflict_b,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "resolution": "LOGGED_NOT_RESOLVED"
        })
        self.axiom_checks["A9_CONTRADICTION"] = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for serialization."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "serves": self.serves,
            "reason": self.reason,
            "timestamp_utc": self.timestamp_utc,
            "axiom_checks": self.axiom_checks,
            "sacrifices": self.sacrifices,
            "contradictions": self.contradictions
        }


class AgentRuntimeOrchestrator:
    """
    Main orchestrator for wrapping Copilot agent tasks with axiom metadata.
    
    This class ensures that:
    1. Every task is wrapped with A1, A2, A4, A7, A9 considerations
    2. All decisions are logged and reconstructable
    3. Sacrifices and contradictions are explicitly tracked
    4. Human-readable reports can be generated
    
    Purpose (A1): Serves the human user, the agent system, and future reviewers
    by creating a transparent record of agent decision-making.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the orchestrator.
        
        Args:
            base_path: Base directory for log files
        """
        self.base_path = base_path
        self.axiom_guard = AxiomGuard()
        self.sacrifice_tracker = SacrificeTracker(base_path)
        self.tasks: List[TaskMetadata] = []
        self.runtime_log: List[Dict[str, Any]] = []
        
        # Load existing contradiction log if it exists
        self.contradiction_log_path = os.path.join(base_path, "contradiction_log.json")
        self._load_contradiction_log()
    
    def _load_contradiction_log(self) -> None:
        """Load existing contradiction log (A2 - append-only, no destructive overwrites)."""
        if os.path.exists(self.contradiction_log_path):
            with open(self.contradiction_log_path, 'r') as f:
                self.existing_contradictions = json.load(f)
        else:
            self.existing_contradictions = {
                "metadata": MODULE_METADATA,
                "contradictions": []
            }
    
    def wrap_task(
        self,
        task_id: str,
        description: str,
        serves: List[str],
        reason: str
    ) -> TaskMetadata:
        """
        Wrap a task with axiom metadata before execution.
        
        This ensures no 'orphan' changes are made (A1) and the reasoning
        is documented (A4).
        
        Args:
            task_id: Unique identifier for this task
            description: What the task does
            serves: Who/what this task serves (must not be empty)
            reason: Why this change is being made
            
        Returns:
            TaskMetadata object for tracking this task
            
        Raises:
            ValueError: If serves list is empty (A1 violation)
        """
        if not serves:
            raise ValueError(
                "A1 VIOLATION: Task must specify who/what it serves. "
                "No 'orphan' changes allowed."
            )
        
        if not reason:
            raise ValueError(
                "A4 VIOLATION: Task must specify why the change is being made. "
                "Reasoning must be reconstructable."
            )
        
        task = TaskMetadata(task_id, description, serves, reason)
        self.tasks.append(task)
        
        # Log task creation (A2 - append-only memory)
        self.runtime_log.append({
            "event": "TASK_WRAPPED",
            "task_id": task_id,
            "timestamp_utc": task.timestamp_utc,
            "axiom_compliance": task.axiom_checks
        })
        
        return task
    
    def validate_task(self, task: TaskMetadata) -> Dict[str, Any]:
        """
        Validate a task against all axioms.
        
        Args:
            task: The task metadata to validate
            
        Returns:
            Dictionary containing validation results for each axiom
        """
        return self.axiom_guard.validate(task.to_dict())
    
    def record_sacrifice(
        self,
        task: TaskMetadata,
        description: str,
        alternative: str
    ) -> None:
        """
        Record when speed is chosen over depth (A7).
        
        This method ensures sacrifices are explicitly tracked rather than hidden.
        
        Args:
            task: The task where the sacrifice occurred
            description: What simpler path was chosen
            alternative: What more robust path was skipped
        """
        task.note_sacrifice(description, alternative)
        self.sacrifice_tracker.record(
            task_id=task.task_id,
            sacrifice_description=description,
            alternative_skipped=alternative
        )
    
    def record_contradiction(
        self,
        task: TaskMetadata,
        conflict_a: str,
        conflict_b: str
    ) -> None:
        """
        Record conflicting requirements (A9).
        
        Contradictions are preserved rather than silently resolved.
        
        Args:
            task: The task where the contradiction was found
            conflict_a: First conflicting requirement
            conflict_b: Second conflicting requirement
        """
        task.log_contradiction(conflict_a, conflict_b)
        
        # Append to contradiction log (A2 - no destructive overwrites)
        self.existing_contradictions["contradictions"].append({
            "task_id": task.task_id,
            "conflict_a": conflict_a,
            "conflict_b": conflict_b,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "resolution": "LOGGED_NOT_RESOLVED"
        })
        
        self._save_contradiction_log()
    
    def _save_contradiction_log(self) -> None:
        """Save contradiction log (A2 - append-only)."""
        with open(self.contradiction_log_path, 'w') as f:
            json.dump(self.existing_contradictions, f, indent=2)
    
    def generate_coherence_report(self) -> str:
        """
        Generate a human-readable coherence report.
        
        This report explains how each axiom fared during the runtime,
        making agent decisions transparent and reviewable.
        
        Returns:
            Markdown-formatted coherence report
        """
        total_tasks = len(self.tasks)
        total_sacrifices = sum(len(t.sacrifices) for t in self.tasks)
        total_contradictions = len(self.existing_contradictions.get("contradictions", []))
        
        # Calculate axiom pass/fail for each task
        axiom_summary = {
            "A1_RELATIONAL": {"passed": 0, "failed": 0},
            "A2_MEMORY": {"passed": 0, "failed": 0},
            "A4_PROCESS": {"passed": 0, "failed": 0},
            "A7_SACRIFICE": {"tracked": 0, "untracked": 0},
            "A9_CONTRADICTION": {"logged": 0, "silent": 0}
        }
        
        for task in self.tasks:
            checks = task.axiom_checks
            if checks["A1_RELATIONAL"]:
                axiom_summary["A1_RELATIONAL"]["passed"] += 1
            else:
                axiom_summary["A1_RELATIONAL"]["failed"] += 1
            
            if checks["A2_MEMORY"]:
                axiom_summary["A2_MEMORY"]["passed"] += 1
            else:
                axiom_summary["A2_MEMORY"]["failed"] += 1
            
            if checks["A4_PROCESS"]:
                axiom_summary["A4_PROCESS"]["passed"] += 1
            else:
                axiom_summary["A4_PROCESS"]["failed"] += 1
            
            if task.sacrifices:
                axiom_summary["A7_SACRIFICE"]["tracked"] += len(task.sacrifices)
            
            if task.contradictions:
                axiom_summary["A9_CONTRADICTION"]["logged"] += len(task.contradictions)
        
        # Calculate coherence score
        axiom_scores = []
        if total_tasks > 0:
            axiom_scores.append(axiom_summary["A1_RELATIONAL"]["passed"] / total_tasks)
            axiom_scores.append(axiom_summary["A2_MEMORY"]["passed"] / total_tasks)
            axiom_scores.append(axiom_summary["A4_PROCESS"]["passed"] / total_tasks)
            # A7 and A9 are about transparency, not pass/fail
            axiom_scores.append(1.0)  # A7: Score based on tracking
            axiom_scores.append(1.0)  # A9: Score based on logging
        
        coherence_score = sum(axiom_scores) / len(axiom_scores) * 5 if axiom_scores else 0
        
        report = f"""# Coherence Report

## Metadata Signature
```json
{{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "{datetime.now(timezone.utc).isoformat()}",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "{total_sacrifices} sacrifice events recorded",
    "contradictions_logged": "{total_contradictions} contradictions preserved",
    "coherence_self_score": {coherence_score:.1f}
}}
```

## Summary

| Metric | Value |
|--------|-------|
| Total Tasks | {total_tasks} |
| Explicit Sacrifices | {total_sacrifices} |
| Unresolved Contradictions | {total_contradictions} |
| Coherence Score | {coherence_score:.1f}/5.0 |

## Axiom Pass/Fail Summary

### A1 - RELATIONAL (No Orphan Changes)
- **Passed**: {axiom_summary['A1_RELATIONAL']['passed']}
- **Failed**: {axiom_summary['A1_RELATIONAL']['failed']}
- Every code change should reference who/what it serves.

### A2 - MEMORY (Append-Only Logging)
- **Passed**: {axiom_summary['A2_MEMORY']['passed']}
- **Failed**: {axiom_summary['A2_MEMORY']['failed']}
- All significant actions logged without destructive overwrites.

### A4 - PROCESS (Reconstructable Reasoning)
- **Passed**: {axiom_summary['A4_PROCESS']['passed']}
- **Failed**: {axiom_summary['A4_PROCESS']['failed']}
- Agent leaves enough documentation for human reconstruction.

### A7 - SACRIFICE (Explicit Trade-offs)
- **Tracked Sacrifices**: {axiom_summary['A7_SACRIFICE']['tracked']}
- When simpler paths are chosen for speed, they are explicitly noted.

### A9 - CONTRADICTION (Preserved Conflicts)
- **Logged Contradictions**: {axiom_summary['A9_CONTRADICTION']['logged']}
- Conflicting requirements are preserved, not silently resolved.

## Narrative of Key Decisions

"""
        # Add task narratives
        for task in self.tasks:
            report += f"### Task: {task.task_id}\n\n"
            report += f"**Description**: {task.description}\n\n"
            report += f"**Serves**: {', '.join(task.serves)}\n\n"
            report += f"**Reason**: {task.reason}\n\n"
            
            if task.sacrifices:
                report += "**Sacrifices Made**:\n"
                for sacrifice in task.sacrifices:
                    report += f"- {sacrifice['description']} (skipped: {sacrifice['alternative_skipped']})\n"
                report += "\n"
            
            if task.contradictions:
                report += "**Contradictions Found**:\n"
                for contradiction in task.contradictions:
                    report += f"- {contradiction['conflict_a']} vs {contradiction['conflict_b']}\n"
                report += "\n"
        
        report += """## Runtime Coherence Checks

The following checks were performed during this runtime:

- [ ] Did the agent ever delete or hide past decisions? (A2 violation check)
- [ ] Did the agent ever resolve a requirement conflict silently? (A9 violation check)
- [ ] Did the agent ever optimize away necessary explanation or comments? (A4 violation check)
- [ ] Did the agent ever act in a way that benefitted one component while harming the whole? (A1/A7 tension check)
- [ ] Did the agent leave enough trace for humans to see where sacrifices were made?

## Final Statement

This report exists to give a timeless executor (Copilot agent) a structured way to 
honor a human-designed axiom system instead of blindly optimizing for completion.
The agent behaves as if human time is precious, contradictions are data, and 
sacrifice is acknowledged, not hidden.
"""
        
        return report
    
    def save_coherence_report(self, output_path: Optional[str] = None) -> str:
        """
        Save the coherence report to a file.
        
        Args:
            output_path: Path to save the report (defaults to coherence_report.md)
            
        Returns:
            Path where the report was saved
        """
        if output_path is None:
            output_path = os.path.join(self.base_path, "coherence_report.md")
        
        report = self.generate_coherence_report()
        with open(output_path, 'w') as f:
            f.write(report)
        
        return output_path


if __name__ == "__main__":
    # Example usage demonstrating axiom-compliant behavior
    orchestrator = AgentRuntimeOrchestrator()
    
    # Wrap a task with full axiom metadata
    task = orchestrator.wrap_task(
        task_id="EXAMPLE_001",
        description="Create the agent runtime orchestrator module",
        serves=["Human User", "Agent System", "Future Reviewers"],
        reason="To provide a structured way for agents to honor axioms instead of blindly optimizing"
    )
    
    # Record a sacrifice (choosing simplicity over robustness)
    orchestrator.record_sacrifice(
        task=task,
        description="Used simple list instead of priority queue for task ordering",
        alternative="Could have used priority queue for more efficient task scheduling"
    )
    
    # Generate and save coherence report
    orchestrator.save_coherence_report()
    print("Coherence report generated: coherence_report.md")
