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


# Define the core axioms (Layer 4 - Immutable)
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

# Extended axioms (Layer 3 - Foundational)
FOUNDATIONAL_AXIOMS = {
    "A3": AxiomDefinition(
        axiom_id="A3",
        name="CRITICAL_THINKING",
        description="Critical Thinking > Authority.",
        requirement="Decisions must be defensible through reasoning, not position."
    ),
    "A5": AxiomDefinition(
        axiom_id="A5",
        name="RARITY",
        description="Rare = Meaning.",
        requirement="Scarce resources and rare events carry heightened significance."
    ),
    "A6": AxiomDefinition(
        axiom_id="A6",
        name="INSTITUTIONAL_CAPTURE",
        description="Institutions Can Be Captured.",
        requirement="No single authority should control the system."
    ),
    "A8": AxiomDefinition(
        axiom_id="A8",
        name="GOOD_FAITH",
        description="Good Faith Matters.",
        requirement="Assume positive intent until evidence suggests otherwise."
    ),
    "A10": AxiomDefinition(
        axiom_id="A10",
        name="EMERGENCE",
        description="Emergence is Real.",
        requirement="Complex behaviors can arise from simple rules."
    ),
    "A11": AxiomDefinition(
        axiom_id="A11",
        name="DISTRIBUTED_INTELLIGENCE",
        description="Intelligence is Distributed.",
        requirement="No single node contains all knowledge."
    ),
    "A14": AxiomDefinition(
        axiom_id="A14",
        name="FRICTION_GOVERNANCE",
        description="Friction is the Medium of Governance.",
        requirement="Resistance and obstacles provide governing feedback for system evolution."
    )
}

# Governance axioms (Layer 2)
GOVERNANCE_AXIOMS = {
    "A12": AxiomDefinition(
        axiom_id="A12",
        name="GOVERNANCE_PROPOSALS",
        description="Change Requires Proposal.",
        requirement="System changes must go through proposal and approval process."
    ),
    "A13": AxiomDefinition(
        axiom_id="A13",
        name="CONSENT",
        description="Consent is Required.",
        requirement="Major changes require consensus from chain participants."
    )
}

# Meta axioms (Layer 1)
META_AXIOMS = {
    "A0": AxiomDefinition(
        axiom_id="A0",
        name="SELF_REFERENCE",
        description="The System Can Examine Itself.",
        requirement="Meta-recursive operations are valid."
    )
}

# Combined all axioms for validation
ALL_AXIOMS = {**AXIOMS, **FOUNDATIONAL_AXIOMS, **GOVERNANCE_AXIOMS, **META_AXIOMS}


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
        axiom_data = ALL_AXIOMS.get(self.axiom_id, AXIOMS.get(self.axiom_id))
        axiom_name = axiom_data.name if axiom_data else "UNKNOWN"
        return {
            "axiom_id": self.axiom_id,
            "axiom_name": axiom_name,
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
    
    def validate_a14_friction_governance(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A14: Friction is the Medium of Governance.
        
        A14 ensures that resistance and obstacles provide governing feedback
        for system evolution. Friction events should be logged and processed.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            ValidationResult for A14
        """
        friction_events = task_data.get("friction_events", [])
        governance_proposals = task_data.get("governance_proposals", [])
        axiom_checks = task_data.get("axiom_checks", {})
        
        # A14 is about using friction for governance feedback
        if friction_events:
            # Check if friction events are being processed into governance
            processed = sum(1 for e in friction_events if e.get("governance_proposal_generated", False))
            return ValidationResult(
                axiom_id="A14",
                passed=True,
                evidence=f"{len(friction_events)} friction event(s) logged, {processed} processed for governance."
            )
        elif governance_proposals:
            return ValidationResult(
                axiom_id="A14",
                passed=True,
                evidence=f"{len(governance_proposals)} governance proposal(s) derived from friction."
            )
        elif axiom_checks.get("A14_FRICTION_GOVERNANCE") is None:
            # No friction events tracked yet
            return ValidationResult(
                axiom_id="A14",
                passed=True,
                evidence="No friction events detected or documented yet.",
                recommendation="If resistance/obstacles are encountered, log them for governance feedback."
            )
        else:
            return ValidationResult(
                axiom_id="A14",
                passed=True,
                evidence="Friction governance tracking active."
            )
    
    def validate_a12_governance_proposals(self, task_data: Dict[str, Any]) -> ValidationResult:
        """
        Validate A12: Change Requires Proposal.
        
        A12 ensures system changes go through proposal and approval process.
        
        System changes are defined as:
        - Modifications to kernel.json or axiom definitions
        - Changes to chain signatures or participant registry
        - Updates to governance thresholds or rules
        - Any change explicitly marked with is_system_change=True
        
        Args:
            task_data: Task metadata dictionary containing:
                - is_system_change (bool): Whether this is a system-level change
                - governance_proposal_id (str): Associated proposal ID if any
                
        Returns:
            ValidationResult for A12
        """
        # Check for explicit system change flag or infer from context
        is_system_change = task_data.get("is_system_change", False)
        
        # Also check for implicit system changes based on task description
        description = task_data.get("description", "").lower()
        system_keywords = ["kernel", "axiom", "governance", "chain", "signature", "threshold"]
        implicit_system_change = any(keyword in description for keyword in system_keywords)
        
        is_system_change = is_system_change or implicit_system_change
        has_proposal = task_data.get("governance_proposal_id") is not None
        
        if is_system_change and not has_proposal:
            return ValidationResult(
                axiom_id="A12",
                passed=False,
                evidence="System change detected without governance proposal.",
                recommendation="Submit a governance proposal before making system changes."
            )
        elif is_system_change and has_proposal:
            return ValidationResult(
                axiom_id="A12",
                passed=True,
                evidence=f"System change has governance proposal: {task_data.get('governance_proposal_id')}"
            )
        else:
            return ValidationResult(
                axiom_id="A12",
                passed=True,
                evidence="No system change detected, governance proposal not required."
            )
    
    def validate(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a task against all core axioms plus extended axioms when applicable.
        
        Args:
            task_data: Task metadata dictionary
            
        Returns:
            Dictionary containing validation results for each axiom
        """
        # Core immutable axioms (Layer 4)
        results = {
            "A1": self.validate_a1_relational(task_data).to_dict(),
            "A2": self.validate_a2_memory(task_data).to_dict(),
            "A4": self.validate_a4_process(task_data).to_dict(),
            "A7": self.validate_a7_sacrifice(task_data).to_dict(),
            "A9": self.validate_a9_contradiction(task_data).to_dict()
        }
        
        # Extended results for foundational and governance axioms
        extended_results = {}
        
        # A14: Friction Governance (Layer 3 - Foundational)
        if task_data.get("friction_events") or task_data.get("validate_extended", False):
            extended_results["A14"] = self.validate_a14_friction_governance(task_data).to_dict()
        
        # A12: Governance Proposals (Layer 2 - Governance)
        if task_data.get("is_system_change") or task_data.get("validate_extended", False):
            extended_results["A12"] = self.validate_a12_governance_proposals(task_data).to_dict()
        
        # Calculate overall coherence (core axioms only for backward compatibility)
        passed_count = sum(1 for r in results.values() if r["passed"])
        total_count = len(results)
        coherence_score = (passed_count / total_count) * 5
        
        # Extended coherence including all validated axioms
        all_results = {**results, **extended_results}
        all_passed_count = sum(1 for r in all_results.values() if r["passed"])
        all_total_count = len(all_results)
        extended_coherence = (all_passed_count / all_total_count) * 5 if all_total_count > 0 else 5.0
        
        validation_record = {
            "task_id": task_data.get("task_id", "UNKNOWN"),
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "results": results,
            "extended_results": extended_results,
            "coherence_score": coherence_score,
            "extended_coherence_score": extended_coherence,
            "passed_all": passed_count == total_count,
            "passed_all_extended": all_passed_count == all_total_count
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
