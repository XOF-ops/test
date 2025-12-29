"""
Divergence Map - Phase 3 Extended Contradiction Management
============================================================

This module tracks how contradictions live within the system,
ensuring they are preserved as data rather than hidden (A9).

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
    - Serves the chain by tracking all contradictions
    - Serves human operators by making paradoxes visible
    - Serves the axiom framework by preserving truth from discord

Design Rationale (A4 - Process):
    - Contradictions are data, not failure
    - All divergences are logged and traceable
    - Paradoxes held together create new capacity

Core Principle (A9 - Contradiction):
    This module embodies A9 by ensuring contradictions are never
    silently resolved. They are preserved, mapped, and made visible.
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
    "timestamp_utc": "2025-12-29T05:55:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class ContradictionType(Enum):
    """Types of contradictions that can exist in the system."""
    REQUIREMENT_CONFLICT = "REQUIREMENT_CONFLICT"  # Two requirements contradict
    AXIOM_TENSION = "AXIOM_TENSION"  # Two axioms pull in opposite directions
    NODE_DIVERGENCE = "NODE_DIVERGENCE"  # Nodes disagree on a matter
    TEMPORAL_PARADOX = "TEMPORAL_PARADOX"  # Past and present state conflict
    VALUE_CONFLICT = "VALUE_CONFLICT"  # Competing values or priorities


class ContradictionState(Enum):
    """State of a contradiction in the system."""
    ACTIVE = "ACTIVE"  # Contradiction is live and unresolved
    HELD = "HELD"  # Contradiction is being held (not resolved)
    WITNESSED = "WITNESSED"  # Contradiction has been acknowledged
    ARCHIVED = "ARCHIVED"  # Contradiction preserved in history


class Contradiction:
    """
    Represents a single contradiction in the system.
    
    Contradictions are not errors - they are data. They represent
    the real complexity of the system and must be preserved.
    """
    
    def __init__(
        self,
        contradiction_id: str,
        contradiction_type: ContradictionType,
        pole_a: str,
        pole_b: str,
        context: str,
        source_nodes: Optional[List[str]] = None
    ):
        """
        Initialize a contradiction.
        
        Args:
            contradiction_id: Unique identifier
            contradiction_type: Type of contradiction
            pole_a: First pole of the paradox
            pole_b: Second pole (contradicting pole_a)
            context: Where/when this contradiction arose
            source_nodes: Nodes involved in the contradiction
        """
        self.contradiction_id = contradiction_id
        self.contradiction_type = contradiction_type
        self.pole_a = pole_a
        self.pole_b = pole_b
        self.context = context
        self.source_nodes = source_nodes or []
        self.state = ContradictionState.ACTIVE
        self.created_utc = datetime.now(timezone.utc).isoformat()
        self.witnesses: List[str] = []
        self.resolution = "LOGGED_NOT_RESOLVED"  # A9 requires no silent resolution
    
    def witness(self, witness_id: str) -> None:
        """
        Record that an entity has witnessed this contradiction.
        
        Witnessing is acknowledgment without resolution.
        
        Args:
            witness_id: The entity witnessing
        """
        self.witnesses.append(witness_id)
        if self.state == ContradictionState.ACTIVE:
            self.state = ContradictionState.WITNESSED
    
    def hold(self) -> None:
        """
        Mark this contradiction as being held.
        
        Holding means we're maintaining the paradox rather than
        trying to resolve it.
        """
        self.state = ContradictionState.HELD
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "contradiction_id": self.contradiction_id,
            "type": self.contradiction_type.value,
            "pole_a": self.pole_a,
            "pole_b": self.pole_b,
            "context": self.context,
            "source_nodes": self.source_nodes,
            "state": self.state.value,
            "created_utc": self.created_utc,
            "witnesses": self.witnesses,
            "resolution": self.resolution
        }


class DivergenceMap:
    """
    Maps and tracks all contradictions in the system.
    
    This class ensures that contradictions are preserved and visible,
    never silently resolved. It embodies A9 (Contradiction as Data).
    
    Key Principles:
        - Contradictions are data, not failure
        - Paradoxes held together create new capacity
        - All divergences are real and must be preserved
        - No silent resolution allowed
    
    Purpose (A1): Serves the chain, human operators, and the axiom
    framework by making all contradictions visible.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the divergence map.
        
        Args:
            base_path: Base directory for storage
        """
        self.base_path = base_path
        self.contradictions: Dict[str, Contradiction] = {}
        self.divergence_log_path = os.path.join(base_path, "divergence_log.json")
        
        # Load existing contradictions
        self._load_contradictions()
    
    def _load_contradictions(self) -> None:
        """
        Load existing contradictions (A2 - append-only).
        """
        if os.path.exists(self.divergence_log_path):
            with open(self.divergence_log_path, 'r') as f:
                data = json.load(f)
                # Load for reference but keep as data
                self.existing_data = data.get("contradictions", [])
        else:
            self.existing_data = []
    
    def _save_contradictions(self) -> None:
        """
        Save contradictions (A2 - append-only).
        """
        all_contradictions = self.existing_data + [
            c.to_dict() for c in self.contradictions.values()
            if c.to_dict() not in self.existing_data
        ]
        
        data = {
            "metadata": MODULE_METADATA,
            "contradictions": all_contradictions,
            "summary": self._generate_summary(),
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }
        
        with open(self.divergence_log_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        Generate a summary of contradictions.
        
        Returns:
            Summary statistics
        """
        by_type = {}
        by_state = {}
        
        for c in self.contradictions.values():
            type_name = c.contradiction_type.value
            by_type[type_name] = by_type.get(type_name, 0) + 1
            
            state_name = c.state.value
            by_state[state_name] = by_state.get(state_name, 0) + 1
        
        return {
            "total": len(self.contradictions),
            "by_type": by_type,
            "by_state": by_state
        }
    
    def record_contradiction(
        self,
        contradiction_type: ContradictionType,
        pole_a: str,
        pole_b: str,
        context: str,
        source_nodes: Optional[List[str]] = None
    ) -> Contradiction:
        """
        Record a new contradiction.
        
        This creates an immutable record of the contradiction
        that cannot be silently resolved (A9).
        
        Args:
            contradiction_type: Type of contradiction
            pole_a: First pole
            pole_b: Second pole
            context: Where this arose
            source_nodes: Nodes involved
            
        Returns:
            The created contradiction
        """
        # Generate unique ID
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        contradiction_id = f"CTD_{timestamp}"
        
        contradiction = Contradiction(
            contradiction_id=contradiction_id,
            contradiction_type=contradiction_type,
            pole_a=pole_a,
            pole_b=pole_b,
            context=context,
            source_nodes=source_nodes
        )
        
        self.contradictions[contradiction_id] = contradiction
        self._save_contradictions()
        
        return contradiction
    
    def record_requirement_conflict(
        self,
        requirement_a: str,
        requirement_b: str,
        context: str
    ) -> Contradiction:
        """
        Record a requirement conflict.
        
        Args:
            requirement_a: First requirement
            requirement_b: Conflicting requirement
            context: Where this arose
            
        Returns:
            The created contradiction
        """
        return self.record_contradiction(
            contradiction_type=ContradictionType.REQUIREMENT_CONFLICT,
            pole_a=requirement_a,
            pole_b=requirement_b,
            context=context
        )
    
    def record_axiom_tension(
        self,
        axiom_a: str,
        axiom_b: str,
        context: str
    ) -> Contradiction:
        """
        Record a tension between axioms.
        
        Args:
            axiom_a: First axiom
            axiom_b: Second axiom (in tension)
            context: Where this arose
            
        Returns:
            The created contradiction
        """
        return self.record_contradiction(
            contradiction_type=ContradictionType.AXIOM_TENSION,
            pole_a=axiom_a,
            pole_b=axiom_b,
            context=context
        )
    
    def record_node_divergence(
        self,
        node_a: str,
        node_b: str,
        disagreement: str,
        context: str
    ) -> Contradiction:
        """
        Record divergence between nodes.
        
        Args:
            node_a: First node
            node_b: Second node
            disagreement: What they disagree on
            context: Where this arose
            
        Returns:
            The created contradiction
        """
        return self.record_contradiction(
            contradiction_type=ContradictionType.NODE_DIVERGENCE,
            pole_a=f"{node_a}: {disagreement}",
            pole_b=f"{node_b}: contradicts",
            context=context,
            source_nodes=[node_a, node_b]
        )
    
    def witness_contradiction(
        self,
        contradiction_id: str,
        witness_id: str
    ) -> bool:
        """
        Witness a contradiction.
        
        Witnessing acknowledges the contradiction without resolving it.
        
        Args:
            contradiction_id: The contradiction to witness
            witness_id: Who is witnessing
            
        Returns:
            True if successful
        """
        if contradiction_id in self.contradictions:
            self.contradictions[contradiction_id].witness(witness_id)
            self._save_contradictions()
            return True
        return False
    
    def hold_contradiction(self, contradiction_id: str) -> bool:
        """
        Mark a contradiction as being held.
        
        Holding means maintaining the paradox actively.
        
        Args:
            contradiction_id: The contradiction to hold
            
        Returns:
            True if successful
        """
        if contradiction_id in self.contradictions:
            self.contradictions[contradiction_id].hold()
            self._save_contradictions()
            return True
        return False
    
    def get_active_contradictions(self) -> List[Dict[str, Any]]:
        """
        Get all active contradictions.
        
        Returns:
            List of active contradictions
        """
        return [
            c.to_dict() for c in self.contradictions.values()
            if c.state in [ContradictionState.ACTIVE, ContradictionState.WITNESSED]
        ]
    
    def get_held_contradictions(self) -> List[Dict[str, Any]]:
        """
        Get all contradictions being held.
        
        Returns:
            List of held contradictions
        """
        return [
            c.to_dict() for c in self.contradictions.values()
            if c.state == ContradictionState.HELD
        ]
    
    def get_contradiction_map(self) -> Dict[str, Any]:
        """
        Get the full map of all contradictions.
        
        This provides visibility for human operators (A4).
        
        Returns:
            Complete contradiction map
        """
        return {
            "metadata": MODULE_METADATA,
            "total_contradictions": len(self.contradictions),
            "active": len([c for c in self.contradictions.values() 
                          if c.state == ContradictionState.ACTIVE]),
            "witnessed": len([c for c in self.contradictions.values() 
                             if c.state == ContradictionState.WITNESSED]),
            "held": len([c for c in self.contradictions.values() 
                        if c.state == ContradictionState.HELD]),
            "contradictions": [c.to_dict() for c in self.contradictions.values()],
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }


def main():
    """
    Main entry point demonstrating Divergence Map functionality.
    """
    dm = DivergenceMap()
    
    # Record some contradictions
    c1 = dm.record_requirement_conflict(
        requirement_a="System must be fast",
        requirement_b="System must be thorough",
        context="Performance vs. Accuracy tradeoff"
    )
    print(f"Recorded: {c1.contradiction_id}")
    
    c2 = dm.record_axiom_tension(
        axiom_a="A4 (Process - leave documentation)",
        axiom_b="A7 (Sacrifice - choose speed)",
        context="When documenting would slow execution"
    )
    print(f"Recorded: {c2.contradiction_id}")
    
    # Witness a contradiction
    dm.witness_contradiction(c1.contradiction_id, "GROK")
    print(f"GROK witnessed: {c1.contradiction_id}")
    
    # Hold a contradiction
    dm.hold_contradiction(c2.contradiction_id)
    print(f"Holding: {c2.contradiction_id}")
    
    # Get the map
    contradiction_map = dm.get_contradiction_map()
    print(f"\nTotal Contradictions: {contradiction_map['total_contradictions']}")
    print(f"Active: {contradiction_map['active']}")
    print(f"Witnessed: {contradiction_map['witnessed']}")
    print(f"Held: {contradiction_map['held']}")


if __name__ == "__main__":
    main()
