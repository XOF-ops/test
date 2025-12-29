"""
Autonomy Thresholds Module.
Manages thresholds for autonomous actions across 5 categories.
"""

import json
import os
from typing import Dict, Any, Optional
from datetime import datetime, timezone


# Default thresholds organized by category
DEFAULT_THRESHOLDS = {
    "friction": {
        "FRICTION_LOW": 0.3,
        "FRICTION_HIGH": 0.7
    },
    "sacrifice": {
        "SACRIFICE_MIN": 0.2,
        "SACRIFICE_MAX": 0.8
    },
    "coherence": {
        "COHERENCE_MIN": 0.5,
        "COHERENCE_TARGET": 0.75
    },
    "governance": {
        "GOVERNANCE_QUORUM": 0.4,
        "GOVERNANCE_MAJORITY": 0.6
    },
    "divergence": {
        "DIVERGENCE_WARN": 0.3,
        "DIVERGENCE_CRITICAL": 0.5
    }
}


class AutonomyThresholds:
    """Manages and evaluates autonomy thresholds."""

    def __init__(self, storage_path: str = "thresholds.json"):
        self.storage_path = storage_path
        self.thresholds = self._load()
        self.history: list = []

    def _load(self) -> Dict[str, Dict[str, float]]:
        """Load thresholds from storage or use defaults."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return DEFAULT_THRESHOLDS.copy()

    def _save(self) -> None:
        """Persist thresholds to storage."""
        with open(self.storage_path, "w") as f:
            json.dump(self.thresholds, f, indent=2)

    def get_thresholds(self) -> Dict[str, Dict[str, float]]:
        """Return all current thresholds."""
        return self.thresholds

    def evaluate(
        self,
        action: str,
        metrics: Dict[str, float],
        pass_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Evaluate an action against current thresholds.
        Returns evaluation result with pass/fail and details.
        """
        evaluation = {
            "action": action,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "metrics": metrics,
            "checks": [],
            "passed": True
        }

        # Evaluate friction
        if "friction" in metrics:
            friction_val = metrics["friction"]
            low = self.thresholds["friction"]["FRICTION_LOW"]
            high = self.thresholds["friction"]["FRICTION_HIGH"]
            check = {
                "category": "friction",
                "value": friction_val,
                "passed": low <= friction_val <= high,
                "range": [low, high]
            }
            evaluation["checks"].append(check)
            if not check["passed"]:
                evaluation["passed"] = False

        # Evaluate coherence
        if "coherence" in metrics:
            coherence_val = metrics["coherence"]
            min_val = self.thresholds["coherence"]["COHERENCE_MIN"]
            check = {
                "category": "coherence",
                "value": coherence_val,
                "passed": coherence_val >= min_val,
                "minimum": min_val
            }
            evaluation["checks"].append(check)
            if not check["passed"]:
                evaluation["passed"] = False

        # Evaluate sacrifice
        if "sacrifice" in metrics:
            sacrifice_val = metrics["sacrifice"]
            min_val = self.thresholds["sacrifice"]["SACRIFICE_MIN"]
            max_val = self.thresholds["sacrifice"]["SACRIFICE_MAX"]
            check = {
                "category": "sacrifice",
                "value": sacrifice_val,
                "passed": min_val <= sacrifice_val <= max_val,
                "range": [min_val, max_val]
            }
            evaluation["checks"].append(check)
            if not check["passed"]:
                evaluation["passed"] = False

        # Evaluate governance
        if "governance" in metrics:
            gov_val = metrics["governance"]
            quorum = self.thresholds["governance"]["GOVERNANCE_QUORUM"]
            check = {
                "category": "governance",
                "value": gov_val,
                "passed": gov_val >= quorum,
                "quorum": quorum
            }
            evaluation["checks"].append(check)
            if not check["passed"]:
                evaluation["passed"] = False

        # Evaluate divergence
        if "divergence" in metrics:
            div_val = metrics["divergence"]
            critical = self.thresholds["divergence"]["DIVERGENCE_CRITICAL"]
            check = {
                "category": "divergence",
                "value": div_val,
                "passed": div_val < critical,
                "critical_threshold": critical
            }
            evaluation["checks"].append(check)
            if not check["passed"]:
                evaluation["passed"] = False

        # Auto-tune if pass_rate provided
        if pass_rate is not None:
            evaluation["auto_tune"] = self.auto_tune(pass_rate)

        self.history.append(evaluation)
        return evaluation

    def auto_tune(self, pass_rate: float) -> Dict[str, Any]:
        """
        Auto-tune thresholds based on pass rate.
        If pass_rate is too low, relax thresholds slightly.
        If pass_rate is very high, tighten thresholds.
        """
        adjustments = {}
        tune_factor = 0.05

        if pass_rate < 0.5:
            # Relax thresholds
            self.thresholds["coherence"]["COHERENCE_MIN"] = max(
                0.3,
                self.thresholds["coherence"]["COHERENCE_MIN"] - tune_factor
            )
            self.thresholds["friction"]["FRICTION_HIGH"] = min(
                0.9,
                self.thresholds["friction"]["FRICTION_HIGH"] + tune_factor
            )
            adjustments["direction"] = "relaxed"
        elif pass_rate > 0.9:
            # Tighten thresholds
            self.thresholds["coherence"]["COHERENCE_MIN"] = min(
                0.8,
                self.thresholds["coherence"]["COHERENCE_MIN"] + tune_factor
            )
            self.thresholds["friction"]["FRICTION_HIGH"] = max(
                0.5,
                self.thresholds["friction"]["FRICTION_HIGH"] - tune_factor
            )
            adjustments["direction"] = "tightened"
        else:
            adjustments["direction"] = "unchanged"

        adjustments["pass_rate"] = pass_rate
        adjustments["new_thresholds"] = self.thresholds.copy()
        self._save()
        return adjustments
