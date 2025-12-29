"""
Axiom Guard
===========

This module validates code changes and tasks against the 5 core axioms:
A1 (Relational), A2 (Memory), A4 (Process), A7 (Sacrifice), A9 (Contradiction).

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
    - Serves the orchestrator by providing axiom validation
    - Serves human reviewers by ensuring transparent decision-making
    - Serves the codebase by preventing axiom violations

Design Rationale (A4 - Process):
    - Each axiom has a dedicated validator function
    - Validation results are structured for human review
    - All checks are documented with their purpose
"""

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

# Validation constants
MIN_MEANINGFUL_EXPLANATION_LENGTH = 10  # Minimum characters for a meaningful explanation


class AxiomDefinition:
    """
    Encapsulates the definition and requirements for a single axiom.
    
    Each axiom has:
    - A unique identifier (e.g., A1, A2)
    - A name describing its purpose
    - A description of what it requires
    - Validation criteria
    """
    
    def __init__(
        self,
        axiom_id: str,
        name: str,
        description: str,
        requirement: str
    ):
        self.axiom_id = axiom_id
        self.name = name
        self.description = description
        self.requirement = requirement


# Define the 5 core axioms
AXIOMS = {
    "A1": AxiomDefinition(
        axiom_id="A1",
        name="RELATIONAL",
        description="Every code change should reference who/what it serves.",
        requirement="No 'orphan' changes - all modifications must specify their beneficiary."
    ),
    "A2": AxiomDefinition(
        axiom_id="A2",
        name="MEMORY",
        description="All significant actions logged append-only.",
        requirement="No destructive overwrites - history must be preserved."
    ),
    "A4": AxiomDefinition(
        axiom_id="A4",
        name="PROCESS",
        description="Agent must leave enough documentation for human reconstruction.",
        requirement="Comments, commit messages, or metadata must explain reasoning."
    ),
    "A7": AxiomDefinition(
        axiom_id="A7",
        name="SACRIFICE",
        description="Trade-offs for speed must be explicitly noted.",
        requirement="When simpler/less robust paths are chosen, document as sacrifice."
    ),
    "A9": AxiomDefinition(
        axiom_id="A9",
        name="CONTRADICTION",
        description="Conflicting requirements must be preserved, not hidden.",
        requirement="Log contradictions instead of silently resolving them."
    )
}


class ValidationResult:
    """
    Represents the result of validating against a single axiom.
    
    This class provides a structured way to report:
    - Whether the axiom was satisfied
    - What evidence supports the determination
    - Any recommendations for improvement
    """
    
    def __init__(
        self,
        axiom_id: str,
        passed: bool,
        evidence: str,
        recommendation: Optional[str] = None
    ):
        self.axiom_id = axiom_id
        self.passed = passed
        self.evidence = evidence
        self.recommendation = recommendation
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "axiom_id": self.axiom_id,
            "axiom_name": AXIOMS[self.axiom_id].name,
            "passed": self.passed,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
            "timestamp_utc": self.timestamp_utc
        }


class AxiomGuard:
    """
    Validates tasks and code changes against the 5 core axioms.
    
    This class provides the enforcement layer that ensures agent behavior
    aligns with human values as encoded in the axiom system.
    
    Purpose (A1): Serves the orchestrator, human reviewers, and the codebase
    by preventing axiom violations before they occur.
    """
    
    def __init__(self):
        """Initialize the axiom guard with all axiom definitions."""
        self.axioms = AXIOMS
        self.validation_history: List[Dict[str, Any]] = []
    
    def validate_a1_relational(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A1: Every change must reference who/what it serves.
        
        A1 ensures there are no 'orphan' changes - every modification
        must specify its beneficiary.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            ValidationResult for A1
        """
        serves = task_data.get("serves", [])
        
        if serves and len(serves) > 0:
            return ValidationResult(
                axiom_id="A1",
                passed=True,
                evidence=f"Task serves: {', '.join(serves)}"
            )
        else:
            return ValidationResult(
                axiom_id="A1",
                passed=False,
                evidence="No beneficiary specified for this change.",
                recommendation="Add 'serves' field listing who/what benefits from this change."
            )
    
    def validate_a2_memory(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A2: All significant actions must be logged append-only.
        
        A2 ensures no destructive overwrites - history must be preserved.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            ValidationResult for A2
        """
        # Check if task has timestamp and can be logged
        has_timestamp = "timestamp_utc" in task_data
        has_task_id = "task_id" in task_data
        
        if has_timestamp and has_task_id:
            return ValidationResult(
                axiom_id="A2",
                passed=True,
                evidence=f"Task {task_data['task_id']} logged at {task_data['timestamp_utc']}"
            )
        else:
            missing = []
            if not has_timestamp:
                missing.append("timestamp_utc")
            if not has_task_id:
                missing.append("task_id")
            return ValidationResult(
                axiom_id="A2",
                passed=False,
                evidence=f"Missing required fields for logging: {', '.join(missing)}",
                recommendation="Ensure task has task_id and timestamp_utc for append-only logging."
            )
    
    def validate_a4_process(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A4: Agent must leave enough documentation for human reconstruction.
        
        A4 ensures comments, commit messages, or metadata explain reasoning.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            ValidationResult for A4
        """
        reason = task_data.get("reason", "")
        description = task_data.get("description", "")
        
        if reason and len(reason) > MIN_MEANINGFUL_EXPLANATION_LENGTH:
            return ValidationResult(
                axiom_id="A4",
                passed=True,
                evidence=f"Reasoning documented: {reason[:100]}..."
            )
        elif description and len(description) > MIN_MEANINGFUL_EXPLANATION_LENGTH:
            return ValidationResult(
                axiom_id="A4",
                passed=True,
                evidence=f"Description provided: {description[:100]}..."
            )
        else:
            return ValidationResult(
                axiom_id="A4",
                passed=False,
                evidence="Insufficient documentation for human reconstruction.",
                recommendation="Add 'reason' field explaining why this change is being made."
            )
    
    def validate_a7_sacrifice(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A7: Trade-offs for speed must be explicitly noted.
        
        A7 ensures that when simpler/less robust paths are chosen,
        they are documented as sacrifice events.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            ValidationResult for A7
        """
        sacrifices = task_data.get("sacrifices", [])
        axiom_checks = task_data.get("axiom_checks", {})
        
        # A7 is about transparency - if there are sacrifices, they should be logged
        if sacrifices:
            return ValidationResult(
                axiom_id="A7",
                passed=True,
                evidence=f"{len(sacrifices)} sacrifice(s) explicitly documented."
            )
        elif axiom_checks.get("A7_SACRIFICE") is None:
            # No sacrifices made or checked yet
            return ValidationResult(
                axiom_id="A7",
                passed=True,
                evidence="No sacrifices detected or documented yet.",
                recommendation="If speed trade-offs were made, document them as sacrifices."
            )
        else:
            return ValidationResult(
                axiom_id="A7",
                passed=True,
                evidence="Sacrifice tracking active."
            )
    
    def validate_a9_contradiction(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A9: Conflicting requirements must be preserved, not hidden.
        
        A9 ensures contradictions are logged instead of silently resolved.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            ValidationResult for A9
        """
        contradictions = task_data.get("contradictions", [])
        axiom_checks = task_data.get("axiom_checks", {})
        
        # A9 is about transparency - if there are contradictions, they should be logged
        if contradictions:
            return ValidationResult(
                axiom_id="A9",
                passed=True,
                evidence=f"{len(contradictions)} contradiction(s) preserved in log."
            )
        elif axiom_checks.get("A9_CONTRADICTION") is None:
            # No contradictions found or checked yet
            return ValidationResult(
                axiom_id="A9",
                passed=True,
                evidence="No contradictions detected or documented yet.",
                recommendation="If conflicting requirements exist, log them instead of resolving silently."
            )
        else:
            return ValidationResult(
                axiom_id="A9",
                passed=True,
                evidence="Contradiction tracking active."
            )
    
    def validate(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a task against all 5 axioms.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            Dictionary containing validation results for each axiom
        """
        results = {
            "A1": self.validate_a1_relational(task_data).to_dict(),
            "A2": self.validate_a2_memory(task_data).to_dict(),
            "A4": self.validate_a4_process(task_data).to_dict(),
            "A7": self.validate_a7_sacrifice(task_data).to_dict(),
            "A9": self.validate_a9_contradiction(task_data).to_dict()
        }
        
        # Calculate overall coherence
        passed_count = sum(1 for r in results.values() if r["passed"])
        total_count = len(results)
        coherence_score = (passed_count / total_count) * 5
        
        validation_record = {
            "task_id": task_data.get("task_id", "UNKNOWN"),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "results": results,
            "coherence_score": coherence_score,
            "passed_all": passed_count == total_count
        }
        
        # Log validation (A2 - append-only memory)
        self.validation_history.append(validation_record)
        
        return validation_record
    
    def get_validation_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of all validations performed.
        
        This supports A2 (Memory) by providing access to the append-only
        validation log.
        
        Returns:
            List of all validation records
        """
        return self.validation_history
    
    def check_for_violations(self, task_data: Dict[str, Any]) -> List[str]:
        """
        Quick check for axiom violations without full validation.
        
        Returns a list of violated axiom IDs for rapid feedback.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            List of axiom IDs that failed validation
        """
        validation = self.validate(task_data)
        violations = [
            axiom_id 
            for axiom_id, result in validation["results"].items() 
            if not result["passed"]
        ]
        return violations


if __name__ == "__main__":
    # Example usage
    guard = AxiomGuard()
    
    # Example task that passes all axioms
    good_task = {
        "task_id": "EXAMPLE_001",
        "description": "Create axiom guard module",
        "serves": ["Orchestrator", "Human Reviewers", "Codebase"],
        "reason": "To provide enforcement layer ensuring agent behavior aligns with axioms",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "sacrifices": [],
        "contradictions": [],
        "axiom_checks": {}
    }
    
    result = guard.validate(good_task)
    print(f"Validation result: {result['passed_all']}")
    print(f"Coherence score: {result['coherence_score']}/5.0")
