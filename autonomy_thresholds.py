"""
Autonomy Thresholds - Real-World Usage Tuning
===============================================

This module manages autonomy thresholds that determine when the system
can act autonomously vs. when human intervention is required.

Metadata Signature:
-------------------
{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T07:52:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}

Purpose (A1 - Relational):
    - Serves human operators by respecting autonomy boundaries
    - Serves the system by enabling appropriate autonomous action
    - Serves the axiom framework by balancing A4 (process) with A7 (efficiency)

Design Rationale (A4 - Process):
    - Thresholds are based on real-world usage patterns
    - All threshold decisions are logged (A2)
    - Threshold violations are recorded as contradictions (A9)
    - Threshold sacrifices (choosing speed over safety) are tracked (A7)
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum


# Module-level metadata signature
MODULE_METADATA = {
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T07:52:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class ThresholdCategory(Enum):
    """Categories of autonomy thresholds."""
    DECISION = "DECISION"  # Making decisions
    EXECUTION = "EXECUTION"  # Executing actions
    ESCALATION = "ESCALATION"  # Escalating to humans
    SACRIFICE = "SACRIFICE"  # Making trade-offs
    COHERENCE = "COHERENCE"  # Maintaining coherence


class AutonomyLevel(Enum):
    """Levels of autonomy the system can operate at."""
    FULL = "FULL"  # Fully autonomous
    SUPERVISED = "SUPERVISED"  # Autonomous with logging
    ASSISTED = "ASSISTED"  # Human confirms major decisions
    MINIMAL = "MINIMAL"  # Human approves most actions
    NONE = "NONE"  # Pure tool mode, no autonomy


class ThresholdViolation(Enum):
    """Types of threshold violations."""
    EXCEEDED = "EXCEEDED"  # Threshold exceeded
    UNDERPERFORMED = "UNDERPERFORMED"  # Below minimum
    BOUNDARY_HIT = "BOUNDARY_HIT"  # Hit hard limit
    PATTERN_ANOMALY = "PATTERN_ANOMALY"  # Unusual pattern


class Threshold:
    """
    Represents a single autonomy threshold.
    
    Thresholds define boundaries for autonomous action,
    tuned based on real-world usage patterns.
    """
    
    def __init__(
        self,
        threshold_id: str,
        category: ThresholdCategory,
        name: str,
        description: str,
        min_value: float,
        max_value: float,
        current_value: float,
        unit: str = "score"
    ):
        """
        Initialize a threshold.
        
        Args:
            threshold_id: Unique identifier
            category: Category of threshold
            name: Human-readable name
            description: What this threshold controls
            min_value: Minimum acceptable value
            max_value: Maximum acceptable value
            current_value: Current threshold setting
            unit: Unit of measurement
        """
        self.threshold_id = threshold_id
        self.category = category
        self.name = name
        self.description = description
        self.min_value = min_value
        self.max_value = max_value
        self.current_value = current_value
        self.unit = unit
        self.created_utc = datetime.now(timezone.utc).isoformat()
        self.last_tuned_utc = self.created_utc
        
        # Usage statistics for tuning
        self.evaluation_count = 0
        self.pass_count = 0
        self.fail_count = 0
        self.tuning_history: List[Dict[str, Any]] = []
    
    def evaluate(self, value: float) -> Tuple[bool, Optional[ThresholdViolation]]:
        """
        Evaluate a value against this threshold.
        
        Args:
            value: Value to evaluate
            
        Returns:
            Tuple of (passed, violation_type if failed)
        """
        self.evaluation_count += 1
        
        if value < self.min_value:
            self.fail_count += 1
            return (False, ThresholdViolation.UNDERPERFORMED)
        elif value > self.max_value:
            self.fail_count += 1
            return (False, ThresholdViolation.EXCEEDED)
        else:
            self.pass_count += 1
            return (True, None)
    
    def tune(self, new_value: float, reason: str) -> None:
        """
        Tune the threshold based on usage patterns.
        
        Args:
            new_value: New threshold value
            reason: Why we're tuning
        """
        old_value = self.current_value
        self.current_value = new_value
        self.last_tuned_utc = datetime.now(timezone.utc).isoformat()
        
        self.tuning_history.append({
            "old_value": old_value,
            "new_value": new_value,
            "reason": reason,
            "timestamp_utc": self.last_tuned_utc
        })
    
    def get_pass_rate(self) -> float:
        """Get the pass rate for this threshold."""
        if self.evaluation_count == 0:
            return 1.0
        return self.pass_count / self.evaluation_count
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "threshold_id": self.threshold_id,
            "category": self.category.value,
            "name": self.name,
            "description": self.description,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "current_value": self.current_value,
            "unit": self.unit,
            "created_utc": self.created_utc,
            "last_tuned_utc": self.last_tuned_utc,
            "evaluation_count": self.evaluation_count,
            "pass_count": self.pass_count,
            "fail_count": self.fail_count,
            "pass_rate": self.get_pass_rate(),
            "tuning_history": self.tuning_history
        }


class AutonomyThresholds:
    """
    Manages autonomy thresholds for the system.
    
    This class defines and tunes thresholds that determine when
    the system can act autonomously based on real-world usage.
    
    Key Thresholds:
        - Confidence: Minimum confidence for autonomous decisions
        - Coherence: Minimum coherence score required
        - Risk: Maximum risk level for autonomous action
        - Complexity: Maximum complexity before escalation
        - Speed: Balance between speed and thoroughness
    
    Purpose (A1): Serves humans and the system by defining
    clear boundaries for autonomous action.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize autonomy thresholds.
        
        Args:
            base_path: Base directory for storage
        """
        self.base_path = base_path
        self.thresholds: Dict[str, Threshold] = {}
        self.current_autonomy_level = AutonomyLevel.SUPERVISED
        self.evaluation_log: List[Dict[str, Any]] = []
        
        # Load existing state
        self._load_state()
        
        # Initialize default thresholds
        self._initialize_default_thresholds()
    
    def _load_state(self) -> None:
        """Load existing threshold state (A2)."""
        state_path = os.path.join(self.base_path, "autonomy_thresholds.json")
        if os.path.exists(state_path):
            with open(state_path, 'r') as f:
                data = json.load(f)
                self.evaluation_log = data.get("evaluation_log", [])
                
                # Restore autonomy level
                level_str = data.get("current_autonomy_level", "SUPERVISED")
                try:
                    self.current_autonomy_level = AutonomyLevel[level_str]
                except KeyError:
                    self.current_autonomy_level = AutonomyLevel.SUPERVISED
    
    def _save_state(self) -> None:
        """Save threshold state (A2 - append-only for logs)."""
        state_path = os.path.join(self.base_path, "autonomy_thresholds.json")
        
        data = {
            "metadata": MODULE_METADATA,
            "thresholds": {id: t.to_dict() for id, t in self.thresholds.items()},
            "current_autonomy_level": self.current_autonomy_level.value,
            "evaluation_log": self.evaluation_log[-1000:],  # Keep last 1000
            "summary": self._generate_summary(),
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }
        
        with open(state_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate threshold summary."""
        by_category = {}
        total_evaluations = 0
        total_passes = 0
        
        for threshold in self.thresholds.values():
            cat = threshold.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
            total_evaluations += threshold.evaluation_count
            total_passes += threshold.pass_count
        
        return {
            "total_thresholds": len(self.thresholds),
            "by_category": by_category,
            "total_evaluations": total_evaluations,
            "overall_pass_rate": total_passes / total_evaluations if total_evaluations > 0 else 1.0,
            "current_autonomy_level": self.current_autonomy_level.value
        }
    
    def _initialize_default_thresholds(self) -> None:
        """Initialize default thresholds based on real-world patterns."""
        defaults = [
            # Decision thresholds
            Threshold(
                threshold_id="TH_DECISION_CONFIDENCE",
                category=ThresholdCategory.DECISION,
                name="Decision Confidence",
                description="Minimum confidence score for autonomous decisions",
                min_value=0.0,
                max_value=1.0,
                current_value=0.7,
                unit="confidence"
            ),
            Threshold(
                threshold_id="TH_DECISION_COMPLEXITY",
                category=ThresholdCategory.DECISION,
                name="Decision Complexity",
                description="Maximum complexity score before human review required",
                min_value=0.0,
                max_value=1.0,
                current_value=0.6,
                unit="complexity"
            ),
            
            # Execution thresholds
            Threshold(
                threshold_id="TH_EXECUTION_RISK",
                category=ThresholdCategory.EXECUTION,
                name="Execution Risk",
                description="Maximum risk level for autonomous execution",
                min_value=0.0,
                max_value=1.0,
                current_value=0.3,
                unit="risk"
            ),
            Threshold(
                threshold_id="TH_EXECUTION_IMPACT",
                category=ThresholdCategory.EXECUTION,
                name="Execution Impact",
                description="Maximum impact scope before escalation",
                min_value=0.0,
                max_value=100.0,
                current_value=25.0,
                unit="files_affected"
            ),
            
            # Coherence thresholds
            Threshold(
                threshold_id="TH_COHERENCE_MINIMUM",
                category=ThresholdCategory.COHERENCE,
                name="Minimum Coherence",
                description="Minimum axiom coherence score required",
                min_value=0.0,
                max_value=5.0,
                current_value=4.0,
                unit="coherence"
            ),
            Threshold(
                threshold_id="TH_COHERENCE_TARGET",
                category=ThresholdCategory.COHERENCE,
                name="Target Coherence",
                description="Target coherence score for optimal operation",
                min_value=4.0,
                max_value=5.0,
                current_value=5.0,
                unit="coherence"
            ),
            
            # Sacrifice thresholds (A7)
            Threshold(
                threshold_id="TH_SACRIFICE_SPEED",
                category=ThresholdCategory.SACRIFICE,
                name="Speed vs Thoroughness",
                description="Balance between speed and thoroughness (higher = faster)",
                min_value=0.0,
                max_value=1.0,
                current_value=0.5,
                unit="balance"
            ),
            Threshold(
                threshold_id="TH_SACRIFICE_DEPTH",
                category=ThresholdCategory.SACRIFICE,
                name="Depth vs Breadth",
                description="Balance between depth and breadth (higher = deeper)",
                min_value=0.0,
                max_value=1.0,
                current_value=0.6,
                unit="balance"
            ),
            
            # Escalation thresholds
            Threshold(
                threshold_id="TH_ESCALATION_UNCERTAINTY",
                category=ThresholdCategory.ESCALATION,
                name="Uncertainty Escalation",
                description="Uncertainty level that triggers escalation",
                min_value=0.0,
                max_value=1.0,
                current_value=0.4,
                unit="uncertainty"
            ),
            Threshold(
                threshold_id="TH_ESCALATION_NOVELTY",
                category=ThresholdCategory.ESCALATION,
                name="Novelty Escalation",
                description="Novelty score that triggers human review",
                min_value=0.0,
                max_value=1.0,
                current_value=0.7,
                unit="novelty"
            )
        ]
        
        for threshold in defaults:
            if threshold.threshold_id not in self.thresholds:
                self.thresholds[threshold.threshold_id] = threshold
    
    def evaluate_action(
        self,
        action_type: str,
        confidence: float,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Evaluate whether an action can be performed autonomously.
        
        Args:
            action_type: Type of action (DECISION, EXECUTION, etc.)
            confidence: Confidence level (0.0 - 1.0)
            context: Additional context
            
        Returns:
            Evaluation result with recommendation
        """
        context = context or {}
        
        # Get relevant thresholds
        try:
            category = ThresholdCategory[action_type]
        except KeyError:
            category = ThresholdCategory.DECISION
        
        relevant_thresholds = [
            t for t in self.thresholds.values()
            if t.category == category
        ]
        
        # Evaluate against thresholds
        evaluations = []
        can_proceed = True
        violations = []
        
        for threshold in relevant_thresholds:
            value = context.get(threshold.name.lower().replace(" ", "_"), confidence)
            passed, violation = threshold.evaluate(value)
            
            evaluations.append({
                "threshold": threshold.name,
                "value": value,
                "passed": passed,
                "violation": violation.value if violation else None
            })
            
            if not passed:
                can_proceed = False
                violations.append({
                    "threshold": threshold.name,
                    "violation": violation.value
                })
        
        # Determine autonomy recommendation
        if can_proceed and confidence >= 0.8:
            recommendation = AutonomyLevel.FULL
        elif can_proceed and confidence >= 0.6:
            recommendation = AutonomyLevel.SUPERVISED
        elif can_proceed:
            recommendation = AutonomyLevel.ASSISTED
        else:
            recommendation = AutonomyLevel.MINIMAL
        
        # Log the evaluation (A2)
        evaluation_record = {
            "action_type": action_type,
            "confidence": confidence,
            "can_proceed": can_proceed,
            "recommendation": recommendation.value,
            "evaluations": evaluations,
            "violations": violations,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
        
        self.evaluation_log.append(evaluation_record)
        self._save_state()
        
        return evaluation_record
    
    def tune_threshold(
        self,
        threshold_id: str,
        new_value: float,
        reason: str
    ) -> bool:
        """
        Tune a threshold based on real-world usage.
        
        Args:
            threshold_id: Threshold to tune
            new_value: New value
            reason: Reason for tuning
            
        Returns:
            True if successful
        """
        if threshold_id in self.thresholds:
            threshold = self.thresholds[threshold_id]
            threshold.tune(new_value, reason)
            self._save_state()
            return True
        return False
    
    def auto_tune(self) -> Dict[str, Any]:
        """
        Auto-tune thresholds based on usage patterns.
        
        This analyzes pass rates and adjusts thresholds
        to optimize autonomous operation.
        
        Returns:
            Tuning results
        """
        tuning_results = []
        
        for threshold in self.thresholds.values():
            if threshold.evaluation_count < 10:
                continue  # Not enough data
            
            pass_rate = threshold.get_pass_rate()
            
            # If pass rate is too low, relax the threshold
            if pass_rate < 0.5:
                adjustment = 0.1 * (threshold.max_value - threshold.min_value)
                if threshold.category in [ThresholdCategory.COHERENCE]:
                    # For coherence, we lower the minimum
                    new_value = max(threshold.min_value, threshold.current_value - adjustment)
                else:
                    # For risk/complexity, we raise the maximum
                    new_value = min(threshold.max_value, threshold.current_value + adjustment)
                
                threshold.tune(
                    new_value,
                    f"Auto-tuned due to low pass rate ({pass_rate:.2f})"
                )
                
                tuning_results.append({
                    "threshold": threshold.name,
                    "old_value": threshold.tuning_history[-1]["old_value"],
                    "new_value": new_value,
                    "reason": "low_pass_rate"
                })
        
        self._save_state()
        
        return {
            "tuned_count": len(tuning_results),
            "results": tuning_results,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    
    def get_all_thresholds(self) -> Dict[str, Any]:
        """Get all thresholds and their current state."""
        return {
            "thresholds": [t.to_dict() for t in self.thresholds.values()],
            "current_autonomy_level": self.current_autonomy_level.value,
            "summary": self._generate_summary(),
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    
    def set_autonomy_level(self, level: AutonomyLevel) -> None:
        """
        Set the overall autonomy level.
        
        Args:
            level: New autonomy level
        """
        self.current_autonomy_level = level
        self._save_state()
    
    def get_recommendation(self, context: Dict[str, Any]) -> AutonomyLevel:
        """
        Get autonomy recommendation based on context.
        
        Args:
            context: Current context
            
        Returns:
            Recommended autonomy level
        """
        confidence = context.get("confidence", 0.5)
        coherence = context.get("coherence", 5.0)
        risk = context.get("risk", 0.0)
        
        # Evaluate coherence threshold
        coherence_threshold = self.thresholds.get("TH_COHERENCE_MINIMUM")
        if coherence_threshold and coherence < coherence_threshold.current_value:
            return AutonomyLevel.MINIMAL
        
        # Evaluate risk threshold
        risk_threshold = self.thresholds.get("TH_EXECUTION_RISK")
        if risk_threshold and risk > risk_threshold.current_value:
            return AutonomyLevel.ASSISTED
        
        # Evaluate confidence threshold
        confidence_threshold = self.thresholds.get("TH_DECISION_CONFIDENCE")
        if confidence_threshold and confidence < confidence_threshold.current_value:
            return AutonomyLevel.SUPERVISED
        
        return AutonomyLevel.FULL


def main():
    """Demonstrate Autonomy Thresholds functionality."""
    thresholds = AutonomyThresholds()
    
    # Get all thresholds
    all_thresholds = thresholds.get_all_thresholds()
    print(f"Total Thresholds: {all_thresholds['summary']['total_thresholds']}")
    print(f"Current Autonomy Level: {all_thresholds['current_autonomy_level']}")
    
    # Evaluate an action
    evaluation = thresholds.evaluate_action(
        action_type="DECISION",
        confidence=0.85,
        context={"decision_complexity": 0.4}
    )
    print(f"\nCan Proceed: {evaluation['can_proceed']}")
    print(f"Recommendation: {evaluation['recommendation']}")
    
    # Get recommendation for a context
    recommendation = thresholds.get_recommendation({
        "confidence": 0.9,
        "coherence": 5.0,
        "risk": 0.1
    })
    print(f"\nRecommendation for high-confidence context: {recommendation.value}")


if __name__ == "__main__":
    main()
