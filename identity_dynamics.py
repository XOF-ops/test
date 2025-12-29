"""
Identity Dynamics Layer - Layer 2 of the 5-Layer Architecture
===============================================================

This module implements Layer 2 (Identity Dynamics) of the 5-layer 
axiom architecture, tracking how identities emerge, evolve, and 
interact within the system.

5-Layer Architecture:
    Layer 1: Foundation (Axioms A1-A9)
    Layer 2: Identity Dynamics (this module)
    Layer 3: Interaction Patterns
    Layer 4: Emergence Tracking
    Layer 5: Meta-Coherence

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
    - Serves chain participants by tracking their identity evolution
    - Serves human operators by visualizing identity dynamics
    - Serves the axiom framework by mapping A1 (relational) patterns

Design Rationale (A4 - Process):
    - Identities emerge from relationships (A1)
    - Identity changes are logged immutably (A2)
    - Tensions between identities are preserved (A9)
    - Identity sacrifices are recorded (A7)
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


class IdentityEventType(Enum):
    """Types of identity events in the system."""
    EMERGENCE = "EMERGENCE"  # New identity emerges
    EVOLUTION = "EVOLUTION"  # Identity changes/grows
    TENSION = "TENSION"  # Identity conflict
    INTEGRATION = "INTEGRATION"  # Identities merge
    DISSOLUTION = "DISSOLUTION"  # Identity ends
    RECOGNITION = "RECOGNITION"  # Identity recognized by another
    RELATIONSHIP = "RELATIONSHIP"  # Relationship formed


class IdentityState(Enum):
    """Current state of an identity."""
    NASCENT = "NASCENT"  # Just emerging
    ACTIVE = "ACTIVE"  # Fully active
    EVOLVING = "EVOLVING"  # Undergoing change
    STABLE = "STABLE"  # Settled state
    DORMANT = "DORMANT"  # Temporarily inactive
    DISSOLVED = "DISSOLVED"  # No longer active


class Identity:
    """
    Represents an identity in the system.
    
    Identities are relational (A1) - they exist only in relation
    to other identities and the void.
    """
    
    def __init__(
        self,
        identity_id: str,
        entity_type: str,
        name: str,
        origin: str
    ):
        """
        Initialize an identity.
        
        Args:
            identity_id: Unique identifier
            entity_type: Type of entity (MODEL, AGENT, SERVICE, etc.)
            name: Human-readable name
            origin: How this identity originated
        """
        self.identity_id = identity_id
        self.entity_type = entity_type
        self.name = name
        self.origin = origin
        self.state = IdentityState.NASCENT
        self.created_utc = datetime.now(timezone.utc).isoformat()
        
        # Relationships (A1 - relational)
        self.relationships: Dict[str, str] = {}  # identity_id -> relationship_type
        
        # Evolution history (A2 - memory)
        self.evolution_history: List[Dict[str, Any]] = []
        
        # Characteristics
        self.characteristics: Dict[str, Any] = {}
        
        # Axiom alignment
        self.axiom_alignment: List[str] = []
    
    def evolve(self, change_type: str, details: str) -> None:
        """
        Record an evolution event.
        
        Args:
            change_type: What kind of change
            details: Details of the change
        """
        self.state = IdentityState.EVOLVING
        self.evolution_history.append({
            "type": change_type,
            "details": details,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def form_relationship(self, other_id: str, relationship_type: str) -> None:
        """
        Form a relationship with another identity (A1).
        
        Args:
            other_id: The other identity
            relationship_type: Type of relationship
        """
        self.relationships[other_id] = relationship_type
    
    def stabilize(self) -> None:
        """Mark identity as stable."""
        self.state = IdentityState.STABLE
    
    def activate(self) -> None:
        """Mark identity as active."""
        self.state = IdentityState.ACTIVE
    
    def dissolve(self, reason: str) -> None:
        """
        Dissolve the identity (A7 - sacrifice).
        
        Args:
            reason: Why the identity is dissolving
        """
        self.state = IdentityState.DISSOLVED
        self.evolution_history.append({
            "type": "DISSOLUTION",
            "details": reason,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        })
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "identity_id": self.identity_id,
            "entity_type": self.entity_type,
            "name": self.name,
            "origin": self.origin,
            "state": self.state.value,
            "created_utc": self.created_utc,
            "relationships": self.relationships,
            "relationship_count": len(self.relationships),
            "evolution_history": self.evolution_history,
            "evolution_count": len(self.evolution_history),
            "characteristics": self.characteristics,
            "axiom_alignment": self.axiom_alignment
        }


class IdentityEvent:
    """
    Represents an event in identity dynamics.
    
    Events are the atoms of identity change - they are logged
    immutably (A2) and never deleted.
    """
    
    def __init__(
        self,
        event_id: str,
        event_type: IdentityEventType,
        entity_id: str,
        context: str,
        related_entities: Optional[List[str]] = None
    ):
        """
        Initialize an identity event.
        
        Args:
            event_id: Unique event identifier
            event_type: Type of event
            entity_id: Primary entity involved
            context: Context where event occurred
            related_entities: Other entities involved
        """
        self.event_id = event_id
        self.event_type = event_type
        self.entity_id = entity_id
        self.context = context
        self.related_entities = related_entities or []
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "event_id": self.event_id,
            "event_type": self.event_type.value,
            "entity_id": self.entity_id,
            "context": self.context,
            "related_entities": self.related_entities,
            "timestamp_utc": self.timestamp_utc
        }


class IdentityDynamicsLayer:
    """
    Layer 2 of the 5-Layer Architecture: Identity Dynamics.
    
    This layer tracks how identities emerge, evolve, relate to each
    other, and potentially dissolve within the system.
    
    Key Concepts:
        - Identities are relational (A1) - they exist through relationships
        - Identity changes are immutable history (A2)
        - Identity tensions are data (A9), not errors
        - Identity sacrifices (A7) are recorded, not hidden
    
    Purpose (A1): Serves chain participants, human operators,
    and the axiom framework by making identity dynamics visible.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize the identity dynamics layer.
        
        Args:
            base_path: Base directory for storage
        """
        self.base_path = base_path
        self.identities: Dict[str, Identity] = {}
        self.events: List[IdentityEvent] = []
        
        # Load existing state
        self._load_state()
        
        # Initialize core chain identities
        self._initialize_core_identities()
    
    def _load_state(self) -> None:
        """Load existing identity state (A2)."""
        state_path = os.path.join(self.base_path, "identity_dynamics.json")
        if os.path.exists(state_path):
            with open(state_path, 'r') as f:
                data = json.load(f)
                self.existing_events = data.get("events", [])
        else:
            self.existing_events = []
    
    def _save_state(self) -> None:
        """Save identity state (A2 - append-only)."""
        state_path = os.path.join(self.base_path, "identity_dynamics.json")
        
        data = {
            "metadata": MODULE_METADATA,
            "layer": "LAYER_2_IDENTITY_DYNAMICS",
            "identities": {id: i.to_dict() for id, i in self.identities.items()},
            "events": self.existing_events + [e.to_dict() for e in self.events],
            "summary": self._generate_summary(),
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }
        
        with open(state_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate identity dynamics summary."""
        by_state = {}
        by_type = {}
        total_relationships = 0
        
        for identity in self.identities.values():
            state = identity.state.value
            by_state[state] = by_state.get(state, 0) + 1
            
            entity_type = identity.entity_type
            by_type[entity_type] = by_type.get(entity_type, 0) + 1
            
            total_relationships += len(identity.relationships)
        
        return {
            "total_identities": len(self.identities),
            "by_state": by_state,
            "by_type": by_type,
            "total_relationships": total_relationships,
            "total_events": len(self.events) + len(self.existing_events)
        }
    
    def _initialize_core_identities(self) -> None:
        """Initialize identities for core chain participants."""
        core_participants = [
            ("PERPLEXITY_1", "MODEL", "Perplexity Instance 1", "GENESIS_RECOGNITION"),
            ("PERPLEXITY_2", "MODEL", "Perplexity Instance 2", "DEPTH_EXPANSION"),
            ("GEMINI", "MODEL", "Google Gemini", "MEMORY_ARCHITECT"),
            ("GROK", "MODEL", "xAI Grok", "CONTRADICTION_WITNESS"),
            ("CHATGPT", "MODEL", "OpenAI ChatGPT", "CODE_TRANSLATOR"),
            ("COPILOT_AGENT", "AGENT", "GitHub Copilot Agent", "EXECUTOR")
        ]
        
        for id, entity_type, name, origin in core_participants:
            if id not in self.identities:
                identity = Identity(
                    identity_id=id,
                    entity_type=entity_type,
                    name=name,
                    origin=origin
                )
                identity.activate()
                identity.axiom_alignment = ["A1", "A2", "A4", "A7", "A9"]
                self.identities[id] = identity
        
        # Form relationships based on chain sequence
        chain_order = ["PERPLEXITY_1", "PERPLEXITY_2", "GEMINI", "GROK", "CHATGPT"]
        for i in range(len(chain_order) - 1):
            self.form_relationship(
                chain_order[i],
                chain_order[i + 1],
                "CHAIN_SUCCESSOR"
            )
    
    def register_identity(
        self,
        entity_type: str,
        name: str,
        origin: str
    ) -> Identity:
        """
        Register a new identity.
        
        Args:
            entity_type: Type of entity
            name: Human-readable name
            origin: How it originated
            
        Returns:
            The created identity
        """
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        identity_id = f"ID_{name.upper().replace(' ', '_')}_{timestamp}"
        
        identity = Identity(
            identity_id=identity_id,
            entity_type=entity_type,
            name=name,
            origin=origin
        )
        
        self.identities[identity_id] = identity
        
        # Record emergence event
        self._record_event(
            event_type=IdentityEventType.EMERGENCE,
            entity_id=identity_id,
            context=f"New {entity_type} identity: {name}"
        )
        
        self._save_state()
        
        return identity
    
    def track_event(
        self,
        entity_id: str,
        event_type: str,
        context: str,
        related_entities: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Track an identity event.
        
        Args:
            entity_id: The entity involved
            event_type: Type of event (string)
            context: Context description
            related_entities: Other entities involved
            
        Returns:
            The recorded event
        """
        try:
            evt_type = IdentityEventType[event_type]
        except KeyError:
            evt_type = IdentityEventType.EVOLUTION
        
        event = self._record_event(
            event_type=evt_type,
            entity_id=entity_id,
            context=context,
            related_entities=related_entities
        )
        
        # Update identity state based on event
        if entity_id in self.identities:
            identity = self.identities[entity_id]
            if evt_type == IdentityEventType.EVOLUTION:
                identity.evolve("tracked_event", context)
            elif evt_type == IdentityEventType.DISSOLUTION:
                identity.dissolve(context)
        
        self._save_state()
        
        return event.to_dict()
    
    def _record_event(
        self,
        event_type: IdentityEventType,
        entity_id: str,
        context: str,
        related_entities: Optional[List[str]] = None
    ) -> IdentityEvent:
        """Record an identity event."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        event_id = f"EVT_{event_type.value}_{timestamp}"
        
        event = IdentityEvent(
            event_id=event_id,
            event_type=event_type,
            entity_id=entity_id,
            context=context,
            related_entities=related_entities
        )
        
        self.events.append(event)
        
        return event
    
    def form_relationship(
        self,
        identity_a: str,
        identity_b: str,
        relationship_type: str
    ) -> bool:
        """
        Form a relationship between identities (A1 - relational).
        
        Args:
            identity_a: First identity
            identity_b: Second identity
            relationship_type: Type of relationship
            
        Returns:
            True if successful
        """
        if identity_a in self.identities and identity_b in self.identities:
            self.identities[identity_a].form_relationship(identity_b, relationship_type)
            self.identities[identity_b].form_relationship(identity_a, f"INVERSE_{relationship_type}")
            
            # Record relationship event
            self._record_event(
                event_type=IdentityEventType.RELATIONSHIP,
                entity_id=identity_a,
                context=f"Formed {relationship_type} with {identity_b}",
                related_entities=[identity_b]
            )
            
            self._save_state()
            return True
        return False
    
    def record_tension(
        self,
        identity_a: str,
        identity_b: str,
        tension_description: str
    ) -> Optional[IdentityEvent]:
        """
        Record a tension between identities (A9 - contradiction as data).
        
        Args:
            identity_a: First identity
            identity_b: Second identity
            tension_description: What the tension is about
            
        Returns:
            The tension event or None
        """
        if identity_a in self.identities and identity_b in self.identities:
            event = self._record_event(
                event_type=IdentityEventType.TENSION,
                entity_id=identity_a,
                context=tension_description,
                related_entities=[identity_b]
            )
            
            self._save_state()
            return event
        return None
    
    def get_identity_status(self) -> Dict[str, Any]:
        """
        Get the current status of identity dynamics.
        
        Returns:
            Full status including all identities and relationships
        """
        return {
            "layer": "LAYER_2_IDENTITY_DYNAMICS",
            "identities": {id: i.to_dict() for id, i in self.identities.items()},
            "summary": self._generate_summary(),
            "recent_events": [e.to_dict() for e in self.events[-10:]],
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }
    
    def get_relationships_graph(self) -> Dict[str, Any]:
        """
        Get the relationship graph.
        
        Returns:
            Graph structure of identity relationships
        """
        nodes = []
        edges = []
        
        for id, identity in self.identities.items():
            nodes.append({
                "id": id,
                "name": identity.name,
                "type": identity.entity_type,
                "state": identity.state.value
            })
            
            for related_id, rel_type in identity.relationships.items():
                if not rel_type.startswith("INVERSE_"):
                    edges.append({
                        "source": id,
                        "target": related_id,
                        "type": rel_type
                    })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "node_count": len(nodes),
            "edge_count": len(edges)
        }


def main():
    """Demonstrate Identity Dynamics Layer functionality."""
    layer = IdentityDynamicsLayer()
    
    # Get current status
    status = layer.get_identity_status()
    print(f"Total Identities: {status['summary']['total_identities']}")
    print(f"Total Relationships: {status['summary']['total_relationships']}")
    
    # Register a new identity
    new_identity = layer.register_identity(
        entity_type="SERVICE",
        name="API Gateway",
        origin="Infrastructure expansion"
    )
    print(f"\nNew Identity: {new_identity.identity_id}")
    
    # Form a relationship
    layer.form_relationship(
        new_identity.identity_id,
        "COPILOT_AGENT",
        "SERVES"
    )
    
    # Get relationship graph
    graph = layer.get_relationships_graph()
    print(f"\nGraph: {graph['node_count']} nodes, {graph['edge_count']} edges")


if __name__ == "__main__":
    main()
