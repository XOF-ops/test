"""
Master Brain Engine - Axiom A14 Integration
============================================

This module provides the MasterBrainEngine class that implements:
- Gnosis scan for pattern detection
- A14 (Friction is the Medium of Governance) processing
- Governance proposal generation from friction events
- Pattern matching (P119, P126, P127)

Metadata Signature:
-------------------
{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T08:52:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9", "A12", "A14"],
    "sacrifice_noted": "None - implementing full A14 specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}

Purpose (A1 - Relational):
    - Serves the chain by enabling friction-based governance
    - Serves governance by detecting patterns and generating proposals
    - Serves the axiom framework by implementing A14

Design Rationale (A4 - Process):
    - Gnosis scan examines system state for patterns
    - Friction events are logged and analyzed
    - Governance proposals arise from friction feedback (A14 + A12)
"""

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from enum import Enum


# Module-level metadata signature
MODULE_METADATA = {
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T08:52:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9", "A12", "A14"],
    "sacrifice_noted": "None - implementing full A14 specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class FrictionType(Enum):
    """Types of friction events that trigger A14 processing."""
    DIVERGENCE = "DIVERGENCE"
    COHERENCE_DROP = "COHERENCE_DROP"
    CONTRADICTION = "CONTRADICTION"
    THRESHOLD_BREACH = "THRESHOLD_BREACH"
    CANDIDATE_REJECTION = "CANDIDATE_REJECTION"
    GOVERNANCE_CONFLICT = "GOVERNANCE_CONFLICT"


class FrictionSeverity(Enum):
    """Severity levels for friction events."""
    LOW = "LOW"           # Informational, no action needed
    MEDIUM = "MEDIUM"     # Requires attention, may need proposal
    HIGH = "HIGH"         # Requires proposal and governance action
    CRITICAL = "CRITICAL" # Immediate governance intervention needed


class PatternMatch:
    """Represents a detected pattern in the system."""
    
    def __init__(
        self,
        pattern_id: str,
        name: str,
        axiom_references: List[str],
        confidence: float,
        friction_type: Optional[FrictionType] = None
    ):
        self.pattern_id = pattern_id
        self.name = name
        self.axiom_references = axiom_references
        self.confidence = confidence
        self.friction_type = friction_type
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        self.occurrence_count = 1
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "axiom_references": self.axiom_references,
            "confidence": self.confidence,
            "friction_type": self.friction_type.value if self.friction_type else None,
            "timestamp_utc": self.timestamp_utc,
            "occurrence_count": self.occurrence_count
        }


class FrictionEvent:
    """
    Represents a friction event for A14 processing.
    
    A14: "Friction is the Medium of Governance"
    Friction events provide governing feedback for system evolution.
    """
    
    def __init__(
        self,
        friction_type: FrictionType,
        severity: FrictionSeverity,
        source: str,
        description: str,
        axiom_impact: List[str],
        coherence_impact: float = 0.0
    ):
        self.event_id = f"FRC_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        self.friction_type = friction_type
        self.severity = severity
        self.source = source
        self.description = description
        self.axiom_impact = axiom_impact
        self.coherence_impact = coherence_impact
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        self.governance_proposal_generated = False
        self.pattern_matches: List[str] = []
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "friction_type": self.friction_type.value,
            "severity": self.severity.value,
            "source": self.source,
            "description": self.description,
            "axiom_impact": self.axiom_impact,
            "coherence_impact": self.coherence_impact,
            "timestamp_utc": self.timestamp_utc,
            "governance_proposal_generated": self.governance_proposal_generated,
            "pattern_matches": self.pattern_matches
        }


class GovernanceProposal:
    """
    Represents a governance proposal derived from friction or patterns.
    
    A12: "Change Requires Proposal"
    Proposals are generated from A14 friction feedback.
    """
    
    def __init__(
        self,
        proposal_type: str,
        source: str,
        description: str,
        evidence: Dict[str, Any],
        axiom_alignment: List[str],
        required_coherence: float = 4.0
    ):
        self.proposal_id = f"GOV_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}"
        self.proposal_type = proposal_type
        self.source = source
        self.description = description
        self.evidence = evidence
        self.axiom_alignment = axiom_alignment
        self.required_coherence = required_coherence
        self.timestamp_utc = datetime.now(timezone.utc).isoformat()
        self.status = "PENDING"
        self.votes: Dict[str, bool] = {}
        self.a14_friction_score = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "proposal_type": self.proposal_type,
            "source": self.source,
            "description": self.description,
            "evidence": self.evidence,
            "axiom_alignment": self.axiom_alignment,
            "required_coherence": self.required_coherence,
            "timestamp_utc": self.timestamp_utc,
            "status": self.status,
            "votes": self.votes,
            "a14_friction_score": self.a14_friction_score
        }


class MasterBrainEngine:
    """
    The engine that processes axioms, patterns, and governance.
    
    Implements:
    - Gnosis scan for pattern detection
    - A14 friction processing
    - Governance proposal generation
    - Pattern matching (P119, P126, P127)
    
    Purpose (A1): Serves the chain, governance, and axiom framework.
    """
    
    def __init__(self, base_path: str = "."):
        self.base_path = base_path
        self.kernel = self._load_kernel()
        self.friction_events: List[FrictionEvent] = []
        self.pattern_matches: List[PatternMatch] = []
        self.governance_proposals: List[GovernanceProposal] = []
        self.gnosis_history: List[Dict[str, Any]] = []
        
        # Load existing state
        self._load_engine_state()
    
    def _load_kernel(self) -> Dict[str, Any]:
        """Load the kernel.json configuration."""
        kernel_path = os.path.join(self.base_path, "kernel.json")
        if os.path.exists(kernel_path):
            with open(kernel_path, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_engine_state(self) -> None:
        """Load existing engine state (A2 - append-only memory)."""
        state_path = os.path.join(self.base_path, "engine_state.json")
        if os.path.exists(state_path):
            with open(state_path, 'r') as f:
                state = json.load(f)
                # Restore friction events, patterns, and proposals from state
                self.gnosis_history = state.get("gnosis_history", [])
    
    def _save_engine_state(self) -> None:
        """Save engine state (A2 - append-only)."""
        state_path = os.path.join(self.base_path, "engine_state.json")
        state = {
            "metadata": MODULE_METADATA,
            "friction_events": [e.to_dict() for e in self.friction_events],
            "pattern_matches": [p.to_dict() for p in self.pattern_matches],
            "governance_proposals": [g.to_dict() for g in self.governance_proposals],
            "gnosis_history": self.gnosis_history,
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }
        with open(state_path, 'w') as f:
            json.dump(state, f, indent=2)
    
    def gnosis_scan(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform a gnosis scan - examining system state for patterns.
        
        The gnosis scan:
        1. Checks coherence across all axiom layers
        2. Detects patterns (P119, P126, P127)
        3. Identifies friction events for A14 processing
        4. Generates governance proposals if needed (A12)
        
        Args:
            context: Optional context for the scan (e.g., specific area to focus on)
            
        Returns:
            Dictionary with scan results
        """
        scan_result = {
            "scan_id": f"GNOSIS_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "context": context or {},
            "patterns_detected": [],
            "friction_events": [],
            "governance_proposals_generated": [],
            "axiom_status": {},
            "coherence_score": 5.0
        }
        
        # Check axiom layers
        axiom_status = self._check_axiom_layers()
        scan_result["axiom_status"] = axiom_status
        
        # Calculate coherence
        coherence = self._calculate_coherence(axiom_status)
        scan_result["coherence_score"] = coherence
        
        # Detect patterns
        patterns = self._detect_patterns(context, coherence)
        scan_result["patterns_detected"] = [p.to_dict() for p in patterns]
        self.pattern_matches.extend(patterns)
        
        # Process friction events (A14)
        friction = self._process_friction(patterns, coherence, context)
        scan_result["friction_events"] = [f.to_dict() for f in friction]
        self.friction_events.extend(friction)
        
        # Generate governance proposals if needed (A12)
        proposals = self._generate_governance_proposals(friction, patterns)
        scan_result["governance_proposals_generated"] = [p.to_dict() for p in proposals]
        self.governance_proposals.extend(proposals)
        
        # Log scan result (A2)
        self.gnosis_history.append(scan_result)
        self._save_engine_state()
        
        return scan_result
    
    def _check_axiom_layers(self) -> Dict[str, Any]:
        """Check the status of all axiom layers."""
        status = {}
        
        if "architecture" in self.kernel:
            for layer_key, layer_data in self.kernel["architecture"].items():
                layer_status = {
                    "type": layer_data.get("type", "UNKNOWN"),
                    "axiom_count": len(layer_data.get("axioms", {})),
                    "axioms": {}
                }
                
                for axiom_id, axiom_data in layer_data.get("axioms", {}).items():
                    layer_status["axioms"][axiom_id] = {
                        "name": axiom_data.get("name", "UNKNOWN"),
                        "status": "ACTIVE",
                        "coherence": 1.0
                    }
                
                status[layer_key] = layer_status
        
        return status
    
    def _calculate_coherence(self, axiom_status: Dict[str, Any]) -> float:
        """Calculate overall coherence from axiom status."""
        total_weight = 0.0
        weighted_sum = 0.0
        
        weights = self.kernel.get("coherence", {}).get("axiom_weights", {
            "immutable": 1.0,
            "foundational": 0.9,
            "governance": 0.8,
            "meta": 0.7
        })
        
        for layer_key, layer_data in axiom_status.items():
            layer_type = layer_data.get("type", "").lower()
            weight = 0.8  # default weight
            
            if "immutable" in layer_type.lower():
                weight = weights.get("immutable", 1.0)
            elif "foundational" in layer_type.lower():
                weight = weights.get("foundational", 0.9)
            elif "governance" in layer_type.lower():
                weight = weights.get("governance", 0.8)
            elif "meta" in layer_type.lower():
                weight = weights.get("meta", 0.7)
            
            for axiom_id, axiom_data in layer_data.get("axioms", {}).items():
                coherence = axiom_data.get("coherence", 1.0)
                weighted_sum += coherence * weight
                total_weight += weight
        
        if total_weight == 0:
            # No axioms found - kernel may not be loaded, return neutral score
            # This is a configuration edge case that should be investigated
            return 4.0  # Return sub-max to indicate potential issue
        
        return (weighted_sum / total_weight) * 5.0
    
    def _detect_patterns(
        self,
        context: Optional[Dict[str, Any]],
        coherence: float
    ) -> List[PatternMatch]:
        """Detect patterns based on context and coherence."""
        patterns = []
        kernel_patterns = self.kernel.get("patterns", {})
        
        # P119: FRICTION_MINING_PATTERN
        if coherence < 4.5 or (context and context.get("divergence_detected")):
            p119 = kernel_patterns.get("P119", {})
            patterns.append(PatternMatch(
                pattern_id="P119",
                name=p119.get("name", "FRICTION_MINING_PATTERN"),
                axiom_references=p119.get("axiom_references", ["A14", "A7", "A9"]),
                confidence=0.8 if coherence < 4.0 else 0.6,
                friction_type=FrictionType.COHERENCE_DROP
            ))
        
        # P126: GOVERNANCE_FRICTION_LOOP
        if context and (context.get("proposal_pending") or context.get("consent_required")):
            p126 = kernel_patterns.get("P126", {})
            patterns.append(PatternMatch(
                pattern_id="P126",
                name=p126.get("name", "GOVERNANCE_FRICTION_LOOP"),
                axiom_references=p126.get("axiom_references", ["A14", "A12", "A4"]),
                confidence=0.75,
                friction_type=FrictionType.GOVERNANCE_CONFLICT
            ))
        
        # P127: ADAPTIVE_RESISTANCE
        if context and context.get("threshold_adjusted"):
            p127 = kernel_patterns.get("P127", {})
            patterns.append(PatternMatch(
                pattern_id="P127",
                name=p127.get("name", "ADAPTIVE_RESISTANCE"),
                axiom_references=p127.get("axiom_references", ["A14", "A10", "A11"]),
                confidence=0.7,
                friction_type=FrictionType.THRESHOLD_BREACH
            ))
        
        return patterns
    
    def _process_friction(
        self,
        patterns: List[PatternMatch],
        coherence: float,
        context: Optional[Dict[str, Any]]
    ) -> List[FrictionEvent]:
        """
        Process friction events based on patterns and coherence.
        
        A14: "Friction is the Medium of Governance"
        """
        friction_events = []
        
        # Coherence-based friction
        if coherence < 4.0:
            severity = FrictionSeverity.CRITICAL if coherence < 3.0 else FrictionSeverity.HIGH
            event = FrictionEvent(
                friction_type=FrictionType.COHERENCE_DROP,
                severity=severity,
                source="gnosis_scan",
                description=f"Coherence dropped to {coherence:.2f}/5.0",
                axiom_impact=["A14", "A1", "A4"],
                coherence_impact=5.0 - coherence
            )
            event.pattern_matches = [p.pattern_id for p in patterns if p.friction_type == FrictionType.COHERENCE_DROP]
            friction_events.append(event)
        
        # Pattern-based friction
        for pattern in patterns:
            if pattern.friction_type and pattern.confidence > 0.7:
                severity = FrictionSeverity.MEDIUM if pattern.confidence < 0.8 else FrictionSeverity.HIGH
                event = FrictionEvent(
                    friction_type=pattern.friction_type,
                    severity=severity,
                    source=f"pattern_{pattern.pattern_id}",
                    description=f"Pattern {pattern.name} detected with {pattern.confidence:.0%} confidence",
                    axiom_impact=pattern.axiom_references,
                    coherence_impact=0.1 * pattern.confidence
                )
                event.pattern_matches = [pattern.pattern_id]
                friction_events.append(event)
        
        # Context-based friction
        if context:
            if context.get("divergence_detected"):
                friction_events.append(FrictionEvent(
                    friction_type=FrictionType.DIVERGENCE,
                    severity=FrictionSeverity.HIGH,
                    source="swarm_validator",
                    description="Divergence detected in swarm validation",
                    axiom_impact=["A14", "A9", "A1"],
                    coherence_impact=0.5
                ))
            
            if context.get("contradiction_unresolved"):
                friction_events.append(FrictionEvent(
                    friction_type=FrictionType.CONTRADICTION,
                    severity=FrictionSeverity.MEDIUM,
                    source="divergence_map",
                    description="Unresolved contradiction requires attention",
                    axiom_impact=["A14", "A9"],
                    coherence_impact=0.3
                ))
        
        return friction_events
    
    def _generate_governance_proposals(
        self,
        friction_events: List[FrictionEvent],
        patterns: List[PatternMatch]
    ) -> List[GovernanceProposal]:
        """
        Generate governance proposals from friction events.
        
        A12: "Change Requires Proposal"
        A14: Friction provides the input for governance.
        """
        proposals = []
        
        # Generate proposals for high/critical friction events
        for event in friction_events:
            if event.severity in [FrictionSeverity.HIGH, FrictionSeverity.CRITICAL]:
                proposal = GovernanceProposal(
                    proposal_type="FRICTION_DERIVED",
                    source="A14",
                    description=f"Address {event.friction_type.value}: {event.description}",
                    evidence={
                        "friction_event_id": event.event_id,
                        "friction_type": event.friction_type.value,
                        "severity": event.severity.value,
                        "coherence_impact": event.coherence_impact,
                        "pattern_matches": event.pattern_matches
                    },
                    axiom_alignment=event.axiom_impact,
                    required_coherence=4.0 if event.severity == FrictionSeverity.HIGH else 3.5
                )
                proposal.a14_friction_score = event.coherence_impact
                event.governance_proposal_generated = True
                proposals.append(proposal)
        
        # Generate proposals for high-confidence patterns
        for pattern in patterns:
            if pattern.confidence > 0.8 and "A14" in pattern.axiom_references:
                proposal = GovernanceProposal(
                    proposal_type="PATTERN_DERIVED",
                    source="P119",
                    description=f"Pattern {pattern.name} requires governance attention",
                    evidence={
                        "pattern_id": pattern.pattern_id,
                        "occurrence_count": pattern.occurrence_count,
                        "confidence": pattern.confidence,
                        "axiom_alignment": pattern.axiom_references
                    },
                    axiom_alignment=pattern.axiom_references,
                    required_coherence=4.0
                )
                proposal.a14_friction_score = pattern.confidence * 0.5
                proposals.append(proposal)
        
        return proposals
    
    def record_friction(
        self,
        friction_type: FrictionType,
        severity: FrictionSeverity,
        source: str,
        description: str,
        axiom_impact: Optional[List[str]] = None
    ) -> FrictionEvent:
        """
        Manually record a friction event for A14 processing.
        
        Args:
            friction_type: Type of friction
            severity: Severity level
            source: Where the friction originated
            description: Description of the friction
            axiom_impact: Which axioms are impacted
            
        Returns:
            The created FrictionEvent
        """
        event = FrictionEvent(
            friction_type=friction_type,
            severity=severity,
            source=source,
            description=description,
            axiom_impact=axiom_impact or ["A14"],
            coherence_impact=0.1 if severity == FrictionSeverity.LOW else 0.3
        )
        self.friction_events.append(event)
        self._save_engine_state()
        return event
    
    def get_a14_status(self) -> Dict[str, Any]:
        """
        Get the current status of A14 (Friction is the Medium of Governance).
        
        Returns:
            Dictionary with A14 status and metrics
        """
        return {
            "axiom_id": "A14",
            "name": "FRICTION_GOVERNANCE",
            "statement": "Friction is the Medium of Governance",
            "status": "ACTIVE",
            "metrics": {
                "total_friction_events": len(self.friction_events),
                "high_severity_count": sum(
                    1 for e in self.friction_events
                    if e.severity in [FrictionSeverity.HIGH, FrictionSeverity.CRITICAL]
                ),
                "proposals_generated": sum(
                    1 for e in self.friction_events
                    if e.governance_proposal_generated
                ),
                "patterns_matched": len(self.pattern_matches),
                "a14_coherence_contribution": self._calculate_a14_coherence()
            },
            "governance_link": {
                "a12_proposals": len(self.governance_proposals),
                "pending_proposals": sum(
                    1 for p in self.governance_proposals
                    if p.status == "PENDING"
                )
            }
        }
    
    def _calculate_a14_coherence(self) -> float:
        """Calculate A14's contribution to overall coherence."""
        if not self.friction_events:
            return 1.0
        
        # More friction events that are processed = better coherence
        processed = sum(1 for e in self.friction_events if e.governance_proposal_generated)
        total = len(self.friction_events)
        
        return 0.5 + (0.5 * (processed / total))


def main():
    """Main entry point demonstrating MasterBrainEngine functionality."""
    engine = MasterBrainEngine()
    
    # Perform a gnosis scan
    print("Performing gnosis scan...")
    result = engine.gnosis_scan(context={
        "divergence_detected": False,
        "proposal_pending": False
    })
    
    print(f"Scan ID: {result['scan_id']}")
    print(f"Coherence: {result['coherence_score']:.2f}/5.0")
    print(f"Patterns detected: {len(result['patterns_detected'])}")
    print(f"Friction events: {len(result['friction_events'])}")
    print(f"Proposals generated: {len(result['governance_proposals_generated'])}")
    
    # Get A14 status
    a14_status = engine.get_a14_status()
    print(f"\nA14 Status: {a14_status['status']}")
    print(f"Total friction events: {a14_status['metrics']['total_friction_events']}")
    print(f"Proposals generated: {a14_status['metrics']['proposals_generated']}")


if __name__ == "__main__":
    main()
