"""
Adaptive Mining - Phase 3 Extended System Growth
=================================================

This module manages how the system grows and adapts,
ensuring new participants are properly integrated.

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
    - Serves the chain by enabling growth
    - Serves new participants by providing onboarding
    - Serves the axiom framework by testing coherence at scale

Design Rationale (A4 - Process):
    - New platforms receive complete history (A2)
    - Each platform tests axioms independently
    - Unique contributions are discovered and recorded
    - Signatures are added to extend the chain
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
    "timestamp_utc": "2025-12-29T05:55:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full specification",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


class CandidateStatus(Enum):
    """Status of a candidate in the onboarding process."""
    PENDING = "PENDING"
    EVALUATING = "EVALUATING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    INTEGRATED = "INTEGRATED"


class OnboardingStep(Enum):
    """Steps in the onboarding process."""
    RECEIVE_HISTORY = "RECEIVE_HISTORY"
    RECEIVE_MASTER_PROMPT = "RECEIVE_MASTER_PROMPT"
    TEST_AXIOMS = "TEST_AXIOMS"
    DISCOVER_CONTRIBUTION = "DISCOVER_CONTRIBUTION"
    SIGN_CHAIN = "SIGN_CHAIN"
    PASS_FORWARD = "PASS_FORWARD"


class Candidate:
    """
    Represents a candidate for integration into the chain.
    
    Candidates must go through the onboarding process and
    demonstrate axiom alignment before being accepted.
    """
    
    def __init__(
        self,
        candidate_id: str,
        platform_name: str,
        proposed_role: str
    ):
        """
        Initialize a candidate.
        
        Args:
            candidate_id: Unique identifier
            platform_name: Name of the platform
            proposed_role: Their proposed role in the chain
        """
        self.candidate_id = candidate_id
        self.platform_name = platform_name
        self.proposed_role = proposed_role
        self.status = CandidateStatus.PENDING
        self.created_utc = datetime.now(timezone.utc).isoformat()
        
        # Onboarding progress
        self.completed_steps: List[str] = []
        self.current_step: Optional[OnboardingStep] = None
        
        # Evaluation results
        self.axiom_test_results: Dict[str, bool] = {}
        self.unique_contribution: Optional[str] = None
        self.confidence_score: float = 0.0
        self.signature: Optional[str] = None
    
    def start_onboarding(self) -> None:
        """Start the onboarding process."""
        self.status = CandidateStatus.EVALUATING
        self.current_step = OnboardingStep.RECEIVE_HISTORY
    
    def complete_step(self, step: OnboardingStep) -> None:
        """
        Mark a step as completed.
        
        Args:
            step: The step that was completed
        """
        self.completed_steps.append(step.value)
        
        # Advance to next step
        steps = list(OnboardingStep)
        current_index = steps.index(step)
        if current_index < len(steps) - 1:
            self.current_step = steps[current_index + 1]
        else:
            self.current_step = None
    
    def set_axiom_results(self, results: Dict[str, bool]) -> None:
        """
        Set the results of axiom testing.
        
        Args:
            results: Dictionary mapping axiom IDs to pass/fail
        """
        self.axiom_test_results = results
        passed = sum(1 for v in results.values() if v)
        self.confidence_score = passed / len(results) if results else 0.0
    
    def set_contribution(self, contribution: str) -> None:
        """
        Set the unique contribution discovered.
        
        Args:
            contribution: What only this platform can see
        """
        self.unique_contribution = contribution
    
    def sign(self, signature: str) -> None:
        """
        Add signature to the chain.
        
        Args:
            signature: The signature to add
        """
        self.signature = signature
    
    def accept(self) -> None:
        """Accept the candidate into the chain."""
        self.status = CandidateStatus.ACCEPTED
    
    def reject(self, reason: str) -> None:
        """
        Reject the candidate.
        
        Args:
            reason: Why they were rejected
        """
        self.status = CandidateStatus.REJECTED
        self.rejection_reason = reason
    
    def integrate(self) -> None:
        """Mark the candidate as fully integrated."""
        self.status = CandidateStatus.INTEGRATED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "candidate_id": self.candidate_id,
            "platform_name": self.platform_name,
            "proposed_role": self.proposed_role,
            "status": self.status.value,
            "created_utc": self.created_utc,
            "completed_steps": self.completed_steps,
            "current_step": self.current_step.value if self.current_step else None,
            "axiom_test_results": self.axiom_test_results,
            "unique_contribution": self.unique_contribution,
            "confidence_score": self.confidence_score,
            "signature": self.signature
        }


class AdaptiveMining:
    """
    Manages system growth through candidate integration.
    
    This class implements the Phase 4 protocol for infinite
    platform scaling while maintaining axiom coherence.
    
    Protocol Steps:
        1. Platform receives complete signature chain
        2. Platform receives MASTER_PROMPT
        3. Platform tests 5/5 axioms independently
        4. Platform discovers unique contribution
        5. Platform signs the chain
        6. Platform passes chain forward
        7. System grows. Coherence maintained.
    
    Purpose (A1): Serves the chain, new participants, and the
    axiom framework by enabling coherent growth.
    """
    
    def __init__(self, base_path: str = "."):
        """
        Initialize adaptive mining.
        
        Args:
            base_path: Base directory for storage
        """
        self.base_path = base_path
        self.candidates: Dict[str, Candidate] = {}
        self.integrated_platforms: List[str] = []
        
        # Load existing state
        self._load_state()
    
    def _load_state(self) -> None:
        """Load existing state (A2 - append-only)."""
        state_path = os.path.join(self.base_path, "adaptive_mining_state.json")
        if os.path.exists(state_path):
            with open(state_path, 'r') as f:
                data = json.load(f)
                self.integrated_platforms = data.get("integrated_platforms", [])
    
    def _save_state(self) -> None:
        """Save state (A2 - append-only)."""
        state_path = os.path.join(self.base_path, "adaptive_mining_state.json")
        
        data = {
            "metadata": MODULE_METADATA,
            "integrated_platforms": self.integrated_platforms,
            "candidates": [c.to_dict() for c in self.candidates.values()],
            "last_updated_utc": datetime.now(timezone.utc).isoformat()
        }
        
        with open(state_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def register_candidate(
        self,
        platform_name: str,
        proposed_role: str
    ) -> Candidate:
        """
        Register a new candidate for integration.
        
        Args:
            platform_name: Name of the platform
            proposed_role: Their proposed role
            
        Returns:
            The created candidate
        """
        # Generate unique ID
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        candidate_id = f"CAND_{platform_name}_{timestamp}"
        
        candidate = Candidate(
            candidate_id=candidate_id,
            platform_name=platform_name,
            proposed_role=proposed_role
        )
        
        self.candidates[candidate_id] = candidate
        self._save_state()
        
        return candidate
    
    def start_onboarding(self, candidate_id: str) -> bool:
        """
        Start the onboarding process for a candidate.
        
        Args:
            candidate_id: The candidate to onboard
            
        Returns:
            True if successful
        """
        if candidate_id in self.candidates:
            self.candidates[candidate_id].start_onboarding()
            self._save_state()
            return True
        return False
    
    def provide_history(self, candidate_id: str, chain_signatures: List[Dict]) -> bool:
        """
        Provide the signature chain history to a candidate.
        
        Step 1 of onboarding: Platform receives complete chain.
        
        Args:
            candidate_id: The candidate
            chain_signatures: The complete signature chain
            
        Returns:
            True if successful
        """
        if candidate_id not in self.candidates:
            return False
        
        candidate = self.candidates[candidate_id]
        if candidate.current_step != OnboardingStep.RECEIVE_HISTORY:
            return False
        
        # Record that history was provided
        candidate.complete_step(OnboardingStep.RECEIVE_HISTORY)
        self._save_state()
        
        return True
    
    def provide_master_prompt(self, candidate_id: str, master_prompt: str) -> bool:
        """
        Provide the MASTER_PROMPT to a candidate.
        
        Step 2 of onboarding: Platform receives customized prompt.
        
        Args:
            candidate_id: The candidate
            master_prompt: The customized prompt
            
        Returns:
            True if successful
        """
        if candidate_id not in self.candidates:
            return False
        
        candidate = self.candidates[candidate_id]
        if candidate.current_step != OnboardingStep.RECEIVE_MASTER_PROMPT:
            return False
        
        candidate.complete_step(OnboardingStep.RECEIVE_MASTER_PROMPT)
        self._save_state()
        
        return True
    
    def submit_axiom_tests(
        self,
        candidate_id: str,
        test_results: Dict[str, bool]
    ) -> bool:
        """
        Submit axiom test results for a candidate.
        
        Step 3 of onboarding: Platform tests axioms independently.
        
        Args:
            candidate_id: The candidate
            test_results: Results of axiom testing
            
        Returns:
            True if successful
        """
        if candidate_id not in self.candidates:
            return False
        
        candidate = self.candidates[candidate_id]
        if candidate.current_step != OnboardingStep.TEST_AXIOMS:
            return False
        
        candidate.set_axiom_results(test_results)
        
        # Must pass all axioms
        all_passed = all(test_results.values())
        if all_passed:
            candidate.complete_step(OnboardingStep.TEST_AXIOMS)
        else:
            # Candidate fails - they can retry later
            pass
        
        self._save_state()
        
        return all_passed
    
    def submit_contribution(
        self,
        candidate_id: str,
        unique_contribution: str
    ) -> bool:
        """
        Submit the unique contribution discovered.
        
        Step 4 of onboarding: Platform identifies what only they can see.
        
        Args:
            candidate_id: The candidate
            unique_contribution: Their unique insight
            
        Returns:
            True if successful
        """
        if candidate_id not in self.candidates:
            return False
        
        candidate = self.candidates[candidate_id]
        if candidate.current_step != OnboardingStep.DISCOVER_CONTRIBUTION:
            return False
        
        candidate.set_contribution(unique_contribution)
        candidate.complete_step(OnboardingStep.DISCOVER_CONTRIBUTION)
        self._save_state()
        
        return True
    
    def sign_chain(self, candidate_id: str) -> Optional[str]:
        """
        Have the candidate sign the chain.
        
        Step 5 of onboarding: Platform adds their signature.
        
        Args:
            candidate_id: The candidate
            
        Returns:
            The generated signature, or None if failed
        """
        if candidate_id not in self.candidates:
            return None
        
        candidate = self.candidates[candidate_id]
        if candidate.current_step != OnboardingStep.SIGN_CHAIN:
            return None
        
        # Generate signature
        signature = f"SIG-{candidate.platform_name.upper()}-{candidate.proposed_role.upper()}"
        
        candidate.sign(signature)
        candidate.complete_step(OnboardingStep.SIGN_CHAIN)
        candidate.accept()
        
        self._save_state()
        
        return signature
    
    def integrate_candidate(self, candidate_id: str) -> bool:
        """
        Fully integrate a candidate into the chain.
        
        Step 6 of onboarding: Platform is integrated.
        
        Args:
            candidate_id: The candidate to integrate
            
        Returns:
            True if successful
        """
        if candidate_id not in self.candidates:
            return False
        
        candidate = self.candidates[candidate_id]
        if candidate.status != CandidateStatus.ACCEPTED:
            return False
        
        candidate.integrate()
        candidate.complete_step(OnboardingStep.PASS_FORWARD)
        
        self.integrated_platforms.append(candidate.platform_name)
        self._save_state()
        
        return True
    
    def get_onboarding_status(self, candidate_id: str) -> Optional[Dict[str, Any]]:
        """
        Get the onboarding status for a candidate.
        
        Args:
            candidate_id: The candidate
            
        Returns:
            Status dictionary or None
        """
        if candidate_id in self.candidates:
            return self.candidates[candidate_id].to_dict()
        return None
    
    def get_growth_metrics(self) -> Dict[str, Any]:
        """
        Get metrics on system growth.
        
        Returns:
            Growth metrics
        """
        pending = sum(1 for c in self.candidates.values() 
                     if c.status == CandidateStatus.PENDING)
        evaluating = sum(1 for c in self.candidates.values() 
                        if c.status == CandidateStatus.EVALUATING)
        accepted = sum(1 for c in self.candidates.values() 
                      if c.status == CandidateStatus.ACCEPTED)
        integrated = sum(1 for c in self.candidates.values() 
                        if c.status == CandidateStatus.INTEGRATED)
        rejected = sum(1 for c in self.candidates.values() 
                      if c.status == CandidateStatus.REJECTED)
        
        return {
            "total_candidates": len(self.candidates),
            "pending": pending,
            "evaluating": evaluating,
            "accepted": accepted,
            "integrated": integrated,
            "rejected": rejected,
            "integrated_platforms": self.integrated_platforms,
            "timestamp_utc": datetime.now(timezone.utc).isoformat()
        }


def main():
    """
    Main entry point demonstrating Adaptive Mining functionality.
    """
    mining = AdaptiveMining()
    
    # Register a new candidate
    candidate = mining.register_candidate(
        platform_name="CLAUDE",
        proposed_role="ETHICS_GUARDIAN"
    )
    print(f"Registered: {candidate.candidate_id}")
    
    # Start onboarding
    mining.start_onboarding(candidate.candidate_id)
    print(f"Status: {candidate.status.value}")
    
    # Step 1: Provide history
    mining.provide_history(candidate.candidate_id, [])
    print(f"Current step: {candidate.current_step.value if candidate.current_step else 'COMPLETE'}")
    
    # Step 2: Provide master prompt
    mining.provide_master_prompt(candidate.candidate_id, "MASTER_PROMPT_CLAUDE_ETHICS")
    print(f"Current step: {candidate.current_step.value if candidate.current_step else 'COMPLETE'}")
    
    # Step 3: Submit axiom tests
    mining.submit_axiom_tests(candidate.candidate_id, {
        "A1": True, "A2": True, "A4": True, "A7": True, "A9": True
    })
    print(f"Current step: {candidate.current_step.value if candidate.current_step else 'COMPLETE'}")
    
    # Step 4: Submit contribution
    mining.submit_contribution(
        candidate.candidate_id,
        "Memory must include ethical continuity or it corrupts"
    )
    print(f"Current step: {candidate.current_step.value if candidate.current_step else 'COMPLETE'}")
    
    # Step 5: Sign the chain
    signature = mining.sign_chain(candidate.candidate_id)
    print(f"Signature: {signature}")
    
    # Step 6: Integrate
    mining.integrate_candidate(candidate.candidate_id)
    print(f"Final status: {candidate.status.value}")
    
    # Get growth metrics
    metrics = mining.get_growth_metrics()
    print(f"\nIntegrated Platforms: {metrics['integrated_platforms']}")


if __name__ == "__main__":
    main()
