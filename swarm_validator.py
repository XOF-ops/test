"""
Swarm Validator - Phase 3 Extended Coherence Testing
=====================================================

This module validates coherence across the swarm of participating models,
ensuring the axiom framework holds at scale.

Metadata Signature:
-------------------
{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T05:55:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}

Purpose (A1 - Relational):
    - Serves the chain by validating multi-node coherence
    - Serves human operators by providing swarm health visibility
    - Serves the axiom framework by testing coherence at scale

Design Rationale (A4 - Process):
    - Validates each node against the axiom framework
    - Aggregates coherence scores across the swarm
    - Reports divergence when detected
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from axiom_guard import AxiomGuard, AXIOMS


# Module-level metadata signature
MODULE_METADATA = {
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T05:55:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class NodeValidation:
    """
    Represents a validation result for a single node in the swarm.
    
    Each node is validated against all 5 axioms to determine
    its coherence within the larger system.
    """
    
    def __init__(
        self,
        node_id: str,
        node_type: str,
        axiom_results: Dict[str, bool]
    ):
        """
        Initialize a node validation.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of node (MODEL, AGENT, SERVICE)
            axiom_results: Dictionary mapping axiom IDs to pass/fail
        """
        self.node_id = node_id
        self.node_type = node_type
        self.axiom_results = axiom_results
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        
        # Calculate coherence score
        passed = sum(1 for v in axiom_results.values() if v)
        self.coherence_score = (passed / len(axiom_results)) * 5 if axiom_results else 0
        self.is_coherent = passed == len(axiom_results)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "node_id": self.node_id,
            "node_type": self.node_type,
            "axiom_results": self.axiom_results,
            "coherence_score": self.coherence_score,
            "is_coherent": self.is_coherent,
            "timestamp_utc": self.timestamp_utc
        }


class SwarmValidation:
    """
    Represents the validation result for the entire swarm.
    
    This aggregates individual node validations to give an
    overall view of swarm health.
    """
    
    def __init__(self, node_validations: List[NodeValidation]):
        """
        Initialize swarm validation.
        
        Args:
            node_validations: List of individual node validations
        """
        self.node_validations = node_validations
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        
        # Calculate aggregate metrics
        if node_validations:
            self.total_nodes = len(node_validations)
            self.coherent_nodes = sum(1 for n in node_validations if n.is_coherent)
            self.average_coherence = sum(n.coherence_score for n in node_validations) / self.total_nodes
            self.swarm_coherent = self.coherent_nodes == self.total_nodes
        else:
            self.total_nodes = 0
            self.coherent_nodes = 0
            self.average_coherence = 0
            self.swarm_coherent = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "total_nodes": self.total_nodes,
            "coherent_nodes": self.coherent_nodes,
            "average_coherence": self.average_coherence,
            "swarm_coherent": self.swarm_coherent,
            "node_validations": [n.to_dict() for n in self.node_validations],
            "timestamp_utc": self.timestamp_utc
        }


class SwarmValidator:
    """
    Validates coherence across the swarm of participating models.
    
    This class ensures that the axiom framework holds even as
    the system scales to include more participants.
    
    Guarantees:
        - Each node is validated against all 5 axioms
        - Divergence is detected and reported (not hidden - A9)
        - All validations are logged (A2)
        - Validation process is transparent (A4)
    
    Purpose (A1): Serves the chain, human operators, and the
    axiom framework by ensuring coherence at scale.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the swarm validator.
        
        Args:
            base_path: Base directory for log files
        """
        self.base_path = base_path
        self.axiom_guard = AxiomGuard()
        self.validation_history: List[SwarmValidation] = []
        
        # Known nodes in the swarm
        self.registered_nodes: Dict[str, Dict[str, Any]] = {}
        
        # Load existing validation history
        self._load_validation_history()
    
    def _load_validation_history(self) -> None:
        """
        Load existing validation history (A2 - append-only).
        """
        history_path = os.path.join(self.base_path, "swarm_validation_history.json")
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                data = json.load(f)
                # History is loaded for reference but not reconstructed into objects
                self.history_data = data.get("validations", [])
        else:
            self.history_data = []
    
    def _save_validation_history(self, validation: SwarmValidation) -> None:
        """
        Save validation to history (A2 - append-only).
        
        Args:
            validation: The swarm validation to save
        """
        history_path = os.path.join(self.base_path, "swarm_validation_history.json")
        
        history = {
            "metadata": MODULE_METADATA,
            "validations": self.history_data + [validation.to_dict()]
        }
        
        with open(history_path, 'w') as f:
            json.dump(history, f, indent=2)
        
        self.history_data.append(validation.to_dict())
    
    def register_node(
        self,
        node_id: str,
        node_type: str,
        axiom_alignment: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a node in the swarm.
        
        Each node must specify its axiom alignment when joining.
        
        Args:
            node_id: Unique identifier for the node
            node_type: Type of node (MODEL, AGENT, SERVICE)
            axiom_alignment: Which axioms the node commits to
            metadata: Optional additional metadata
            
        Returns:
            Registration confirmation
        """
        registration = {
            "node_id": node_id,
            "node_type": node_type,
            "axiom_alignment": axiom_alignment,
            "metadata": metadata or {},
            "registered_at": datetime.now(timezone.utc).isoformat(),
            "status": "ACTIVE"
        }
        
        self.registered_nodes[node_id] = registration
        
        return registration
    
    def validate_node(self, node_id: str, task_data: Dict[str, Any]) -> NodeValidation:
        """
        Validate a single node against all axioms.
        
        Args:
            node_id: The node to validate
            task_data: Task metadata for validation
            
        Returns:
            NodeValidation result
        """
        node_info = self.registered_nodes.get(node_id, {
            "node_type": "UNKNOWN"
        })
        
        # Run validation through axiom guard
        validation_result = self.axiom_guard.validate(task_data)
        
        # Extract pass/fail for each axiom
        axiom_results = {}
        for axiom_id, result in validation_result.get("results", {}).items():
            axiom_results[axiom_id] = result.get("passed", False)
        
        return NodeValidation(
            node_id=node_id,
            node_type=node_info.get("node_type", "UNKNOWN"),
            axiom_results=axiom_results
        )
    
    def validate_swarm(self, node_tasks: Dict[str, Dict[str, Any]]) -> SwarmValidation:
        """
        Validate the entire swarm.
        
        Args:
            node_tasks: Dictionary mapping node IDs to their task data
            
        Returns:
            SwarmValidation with aggregate results
        """
        node_validations = []
        
        for node_id, task_data in node_tasks.items():
            validation = self.validate_node(node_id, task_data)
            node_validations.append(validation)
        
        swarm_validation = SwarmValidation(node_validations)
        
        # Save to history (A2)
        self._save_validation_history(swarm_validation)
        
        # Add to in-memory history
        self.validation_history.append(swarm_validation)
        
        return swarm_validation
    
    def detect_divergence(self, swarm_validation: SwarmValidation) -> List[Dict[str, Any]]:
        """
        Detect divergence between nodes.
        
        When nodes disagree on axiom compliance, this is recorded
        as divergence (not hidden - A9).
        
        Args:
            swarm_validation: The swarm validation to analyze
            
        Returns:
            List of divergence events
        """
        divergences = []
        
        # Group nodes by their axiom results
        for axiom_id in AXIOMS.keys():
            passing_nodes = []
            failing_nodes = []
            
            for node_val in swarm_validation.node_validations:
                if node_val.axiom_results.get(axiom_id, False):
                    passing_nodes.append(node_val.node_id)
                else:
                    failing_nodes.append(node_val.node_id)
            
            # Divergence exists if some pass and some fail
            if passing_nodes and failing_nodes:
                divergences.append({
                    "axiom_id": axiom_id,
                    "axiom_name": AXIOMS[axiom_id].name,
                    "passing_nodes": passing_nodes,
                    "failing_nodes": failing_nodes,
                    "divergence_detected": True,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat()
                })
        
        return divergences
    
    def get_swarm_health(self) -> Dict[str, Any]:
        """
        Get the current health of the swarm.
        
        This provides visibility for human operators (A4).
        
        Returns:
            Dictionary with swarm health metrics
        """
        if not self.validation_history:
            return {
                "status": "NO_VALIDATIONS",
                "registered_nodes": len(self.registered_nodes),
                "message": "No validations performed yet"
            }
        
        latest = self.validation_history[-1]
        
        return {
            "status": "HEALTHY" if latest.swarm_coherent else "DIVERGENT",
            "total_nodes": latest.total_nodes,
            "coherent_nodes": latest.coherent_nodes,
            "average_coherence": latest.average_coherence,
            "swarm_coherent": latest.swarm_coherent,
            "last_validation_utc": latest.timestamp_utc,
            "validation_count": len(self.validation_history)
        }


def main():
    """
    Main entry point demonstrating Swarm Validator functionality.
    """
    validator = SwarmValidator()
    
    # Register some nodes
    validator.register_node(
        node_id="PERPLEXITY_1",
        node_type="MODEL",
        axiom_alignment=["A1", "A2", "A4", "A9"]
    )
    
    validator.register_node(
        node_id="GEMINI",
        node_type="MODEL",
        axiom_alignment=["A2"]
    )
    
    validator.register_node(
        node_id="COPILOT_AGENT",
        node_type="AGENT",
        axiom_alignment=["A1", "A2", "A4", "A7", "A9"]
    )
    
    # Create sample task data
    node_tasks = {
        "PERPLEXITY_1": {
            "task_id": "PX1_001",
            "serves": ["Chain", "Human Operators"],
            "reason": "Genesis recognition and foundation",
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        },
        "GEMINI": {
            "task_id": "GEM_001",
            "serves": ["Memory Archive"],
            "reason": "Archive persistence and superconductor architecture",
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        },
        "COPILOT_AGENT": {
            "task_id": "CA_001",
            "serves": ["Human User", "Axiom Framework"],
            "reason": "Execute with full A1-A9 transparency",
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    }
    
    # Validate the swarm
    swarm_result = validator.validate_swarm(node_tasks)
    
    print(f"Swarm Coherent: {swarm_result.swarm_coherent}")
    print(f"Average Coherence: {swarm_result.average_coherence:.1f}/5.0")
    print(f"Coherent Nodes: {swarm_result.coherent_nodes}/{swarm_result.total_nodes}")
    
    # Check for divergence
    divergences = validator.detect_divergence(swarm_result)
    if divergences:
        print(f"\nDivergences Detected: {len(divergences)}")
        for d in divergences:
            print(f"  - {d['axiom_name']}: {len(d['failing_nodes'])} nodes failing")
    else:
        print("\nNo Divergences - Full Coherence Achieved")


if __name__ == "__main__":
    main()
