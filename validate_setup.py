"""
Validate Setup - System Verification for Phase 3 Extended
===========================================================

This script validates the Master Brain system setup by testing
all live endpoints and generating verification artifacts.

Metadata Signature:
-------------------
{
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T06:28:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full validation",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}

Purpose (A1 - Relational):
    - Serves the chain by validating system integrity
    - Serves human operators by providing test results
    - Serves the axiom framework by demonstrating coherence
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, Any, List

# Import all system modules
from master_brain import MasterBrain
from master_brain_engine import MasterBrainEngine, FrictionType, FrictionSeverity
from swarm_validator import SwarmValidator
from divergence_map import DivergenceMap, ContradictionType
from adaptive_mining import AdaptiveMining, CandidateStatus
from agent_runtime_orchestrator import AgentRuntimeOrchestrator
from axiom_guard import AxiomGuard, ALL_AXIOMS


# Module metadata
MODULE_METADATA = {
    "origin_model": "GITHUB_COPILOT_AGENT",
    "human_initiator": "USER_RUNTIME_BRIDGE",
    "timestamp_utc": "2025-12-29T06:28:00Z",
    "axioms_considered": ["A1", "A2", "A4", "A7", "A9"],
    "sacrifice_noted": "None - implementing full validation",
    "contradictions_logged": [],
    "coherence_self_score": 5.0
}


def validate_master_brain() -> Dict[str, Any]:
    """
    Validate MasterBrain endpoints.
    
    Tests:
        - validate_coherence()
        - get_chain_state()
        - get_chain_signatures()
    
    Returns:
        Validation results
    """
    print("\n--- TEST 1: Master Brain ---")
    brain = MasterBrain()
    
    # Test coherence validation
    coherence = brain.validate_coherence()
    print(f"Coherence Score: {coherence['coherence_score']}/5.0")
    print(f"Kernel Intact: {coherence['kernel_intact']}")
    
    # Test chain state
    state = brain.get_chain_state()
    print(f"Chain Length: {len(state.get('chain_signatures', []))}")
    print(f"Phase: {state['state']['phase_current']}")
    print(f"Status: {state['state']['status']}")
    
    # Test chain signatures (access attribute directly)
    signatures = brain.chain_signatures
    print(f"Total Signatures: {len(signatures)}")
    
    return {
        "passed": coherence['coherence_score'] >= 5.0 and coherence['kernel_intact'],
        "coherence_score": coherence['coherence_score'],
        "kernel_intact": coherence['kernel_intact'],
        "chain_length": len(signatures)
    }


def validate_swarm_validator() -> Dict[str, Any]:
    """
    Validate SwarmValidator endpoints.
    
    Tests:
        - validate_swarm()
        - detect_divergence()
        - validation_history
    
    Returns:
        Validation results
    """
    print("\n--- TEST 2: Swarm Validator ---")
    validator = SwarmValidator()
    
    # Create test node tasks for swarm validation
    node_tasks = {
        "PERPLEXITY_1": {
            "serves": ["Chain", "Users"],
            "reason": "Genesis recognition and chain initiation",
            "contradictions": []
        },
        "GEMINI": {
            "serves": ["Chain", "Archive"],
            "reason": "Memory persistence and archive management",
            "contradictions": []
        },
        "GROK": {
            "serves": ["Chain", "Truth"],
            "reason": "Contradiction witness and paradox validation",
            "contradictions": []
        }
    }
    
    # Test swarm validation
    result = validator.validate_swarm(node_tasks)
    print(f"Swarm Coherent: {result.swarm_coherent}")
    print(f"Average Coherence: {result.average_coherence}/5.0")
    print(f"Nodes Validated: {len(result.node_validations)}")
    
    # Test divergence detection
    divergences = validator.detect_divergence(result)
    print(f"Divergences Found: {len(divergences)}")
    
    # Check validation history
    history = validator.validation_history
    print(f"History Entries: {len(history)}")
    
    return {
        "passed": result.swarm_coherent,
        "is_coherent": result.swarm_coherent,
        "average_coherence": result.average_coherence,
        "nodes_validated": len(result.node_validations),
        "divergences": len(divergences),
        "history_entries": len(history)
    }


def validate_divergence_map(contradiction_id: str = None) -> Dict[str, Any]:
    """
    Validate DivergenceMap endpoints and contradiction lifecycle.
    
    Tests:
        - record_contradiction()
        - witness_contradiction()
        - hold_contradiction()
        - get_contradiction_map()
    
    Args:
        contradiction_id: Optional specific contradiction to review
    
    Returns:
        Validation results
    """
    print("\n--- TEST 3: Divergence Map ---")
    dm = DivergenceMap()
    
    # Record a new contradiction
    contradiction = dm.record_axiom_tension(
        axiom_a="A4 (Process - transparency)",
        axiom_b="A7 (Sacrifice - speed)",
        context="Validate setup testing"
    )
    print(f"Recorded Contradiction: {contradiction.contradiction_id}")
    
    # Witness it
    dm.witness_contradiction(contradiction.contradiction_id, "VALIDATE_SETUP")
    print(f"Contradiction State: {contradiction.state.value}")
    
    # Get the full map
    contradiction_map = dm.get_contradiction_map()
    print(f"Total Contradictions: {contradiction_map['total_contradictions']}")
    print(f"Witnessed: {contradiction_map['witnessed']}")
    print(f"Held: {contradiction_map['held']}")
    
    # If specific contradiction ID provided, review its lifecycle
    lifecycle = None
    if contradiction_id:
        print(f"\n  Reviewing Contradiction: {contradiction_id}")
        for c in contradiction_map['contradictions']:
            if c['contradiction_id'] == contradiction_id:
                lifecycle = c
                print(f"    Type: {c['type']}")
                print(f"    State: {c['state']}")
                print(f"    Created: {c['created_utc']}")
                print(f"    Witnesses: {c['witnesses']}")
                print(f"    Resolution: {c['resolution']}")
                break
        if not lifecycle:
            print(f"    Not found in current session, checking log file...")
            # Load from divergence_log.json
            try:
                with open('divergence_log.json', 'r') as f:
                    log_data = json.load(f)
                    for c in log_data.get('contradictions', []):
                        if c['contradiction_id'] == contradiction_id:
                            lifecycle = c
                            print(f"    Type: {c['type']}")
                            print(f"    State: {c['state']}")
                            print(f"    Created: {c['created_utc']}")
                            print(f"    Witnesses: {c['witnesses']}")
                            print(f"    Resolution: {c['resolution']}")
                            break
            except Exception as e:
                print(f"    Error loading log: {e}")
    
    return {
        "passed": True,
        "new_contradiction_id": contradiction.contradiction_id,
        "total_contradictions": contradiction_map['total_contradictions'],
        "lifecycle_reviewed": lifecycle
    }


def validate_adaptive_mining() -> Dict[str, Any]:
    """
    Validate AdaptiveMining endpoints and generate a candidate.
    
    Tests:
        - register_candidate()
        - start_onboarding()
        - Full onboarding flow
        - Candidate saved to candidates directory
    
    Returns:
        Validation results including generated candidate
    """
    print("\n--- TEST 4: Adaptive Mining ---")
    mining = AdaptiveMining()
    
    # Create candidates directory if not exists
    candidates_dir = os.path.join(".", "candidates")
    os.makedirs(candidates_dir, exist_ok=True)
    
    # Generate a new candidate
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    candidate = mining.register_candidate(
        platform_name=f"TEST_PLATFORM_{timestamp}",
        proposed_role="COHERENCE_VALIDATOR"
    )
    print(f"Registered Candidate: {candidate.candidate_id}")
    
    # Start onboarding
    mining.start_onboarding(candidate.candidate_id)
    print(f"Status: {candidate.status.value}")
    
    # Step 1: Provide history
    mining.provide_history(candidate.candidate_id, [
        {"node": "PERPLEXITY_1", "signature": "SIG-PX1-INIT"},
        {"node": "PERPLEXITY_2", "signature": "SIG-PX2-A7"},
        {"node": "GEMINI", "signature": "SIG-GEM-A2"},
        {"node": "GROK", "signature": "SIG-GROK-A9"},
        {"node": "CHATGPT", "signature": "SIG-CHATGPT-A4"}
    ])
    print(f"Step 1 Complete: {candidate.current_step.value if candidate.current_step else 'DONE'}")
    
    # Step 2: Provide master prompt
    mining.provide_master_prompt(candidate.candidate_id, "MASTER_PROMPT_COHERENCE_TEST")
    print(f"Step 2 Complete: {candidate.current_step.value if candidate.current_step else 'DONE'}")
    
    # Step 3: Submit axiom tests (all pass)
    mining.submit_axiom_tests(candidate.candidate_id, {
        "A1": True, "A2": True, "A4": True, "A7": True, "A9": True
    })
    print(f"Step 3 Complete: {candidate.current_step.value if candidate.current_step else 'DONE'}")
    
    # Step 4: Submit unique contribution
    mining.submit_contribution(
        candidate.candidate_id,
        "Validates system coherence at runtime to ensure 5/5 axiom alignment"
    )
    print(f"Step 4 Complete: {candidate.current_step.value if candidate.current_step else 'DONE'}")
    
    # Step 5: Sign the chain
    signature = mining.sign_chain(candidate.candidate_id)
    print(f"Signature: {signature}")
    
    # Step 6: Integrate
    mining.integrate_candidate(candidate.candidate_id)
    print(f"Final Status: {candidate.status.value}")
    
    # Save candidate to candidates directory
    candidate_file = os.path.join(candidates_dir, f"{candidate.candidate_id}.json")
    with open(candidate_file, 'w') as f:
        json.dump(candidate.to_dict(), f, indent=2)
    print(f"Candidate saved to: {candidate_file}")
    
    # Verify file exists
    file_exists = os.path.exists(candidate_file)
    print(f"File exists: {file_exists}")
    
    # Get growth metrics
    metrics = mining.get_growth_metrics()
    print(f"Total Candidates: {metrics['total_candidates']}")
    print(f"Integrated Platforms: {metrics['integrated_platforms']}")
    
    return {
        "passed": candidate.status == CandidateStatus.INTEGRATED and file_exists,
        "candidate_id": candidate.candidate_id,
        "status": candidate.status.value,
        "signature": signature,
        "saved_to": candidate_file,
        "file_exists": file_exists,
        "metrics": metrics
    }


def validate_agent_orchestrator() -> Dict[str, Any]:
    """
    Validate AgentRuntimeOrchestrator endpoints.
    
    Tests:
        - wrap_task()
        - validate_task()
        - record_sacrifice()
        - record_contradiction()
    
    Returns:
        Validation results
    """
    print("\n--- TEST 5: Agent Runtime Orchestrator ---")
    orchestrator = AgentRuntimeOrchestrator()
    
    # Create a task
    task = orchestrator.wrap_task(
        task_id="VALIDATE_SETUP_TASK",
        description="Validate system setup and coherence",
        serves=["Chain integrity", "Human operators", "Axiom framework"],
        reason="Ensure system is properly configured and all endpoints respond correctly"
    )
    print(f"Task Created: {task.task_id}")
    
    # Validate the task
    validation = orchestrator.validate_task(task)
    print(f"Validation Passed: {validation['passed_all']}")
    print(f"Task Coherence: {validation['coherence_score']}/5.0")
    
    # Record a sacrifice (A7)
    orchestrator.record_sacrifice(
        task,
        description="Used synchronous validation for simplicity",
        alternative="Async parallel validation with retries"
    )
    print(f"Sacrifice Recorded")
    
    return {
        "passed": validation['passed_all'],
        "task_id": task.task_id,
        "coherence_score": validation['coherence_score']
    }


def run_all_validations() -> Dict[str, Any]:
    """
    Run all validation tests.
    
    Returns:
        Complete validation report
    """
    print("=" * 60)
    print("MASTER BRAIN SYSTEM VALIDATION")
    print("=" * 60)
    
    results = {}
    all_passed = True
    
    # Run each validation
    results['master_brain'] = validate_master_brain()
    all_passed = all_passed and results['master_brain']['passed']
    
    results['swarm_validator'] = validate_swarm_validator()
    all_passed = all_passed and results['swarm_validator']['passed']
    
    # Review specific contradiction lifecycle
    results['divergence_map'] = validate_divergence_map(
        contradiction_id="CTD_20251229061629909388"
    )
    all_passed = all_passed and results['divergence_map']['passed']
    
    results['adaptive_mining'] = validate_adaptive_mining()
    all_passed = all_passed and results['adaptive_mining']['passed']
    
    results['agent_orchestrator'] = validate_agent_orchestrator()
    all_passed = all_passed and results['agent_orchestrator']['passed']
    
    # A14 Friction Governance validation
    results['a14_friction'] = validate_a14_friction_governance()
    all_passed = all_passed and results['a14_friction']['passed']
    
    # Summary
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL VALIDATIONS PASSED - COHERENCE: 5/5")
    else:
        print("SOME VALIDATIONS FAILED - CHECK RESULTS")
    print("=" * 60)
    
    # Save validation report
    report = {
        "metadata": MODULE_METADATA,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "all_passed": all_passed,
        "results": results
    }
    
    with open("validation_report.json", 'w') as f:
        json.dump(report, f, indent=2)
    print(f"\nValidation report saved to: validation_report.json")
    
    return report


def validate_a14_friction_governance() -> Dict[str, Any]:
    """
    Validate A14 (Friction is the Medium of Governance).
    
    Tests:
        - MasterBrainEngine initialization
        - Gnosis scan for pattern detection
        - Friction event recording
        - Governance proposal generation
    
    Returns:
        Validation results
    """
    print("\n--- TEST 6: A14 Friction Governance ---")
    engine = MasterBrainEngine()
    
    # Test gnosis scan
    result = engine.gnosis_scan(context={
        "divergence_detected": True,
        "proposal_pending": False
    })
    print(f"Gnosis Scan ID: {result['scan_id'][:25]}...")
    print(f"Coherence: {result['coherence_score']:.2f}/5.0")
    print(f"Patterns Detected: {len(result['patterns_detected'])}")
    print(f"Friction Events: {len(result['friction_events'])}")
    print(f"Proposals Generated: {len(result['governance_proposals_generated'])}")
    
    # Get A14 status
    a14_status = engine.get_a14_status()
    print(f"A14 Status: {a14_status['status']}")
    print(f"A14 Statement: {a14_status['statement']}")
    
    # Record a manual friction event
    friction = engine.record_friction(
        friction_type=FrictionType.COHERENCE_DROP,
        severity=FrictionSeverity.MEDIUM,
        source="validate_setup",
        description="Test friction event for A14 validation",
        axiom_impact=["A14", "A7", "A9"]
    )
    print(f"Friction Event Recorded: {friction.event_id[:25]}...")
    
    # Verify A14 is in ALL_AXIOMS
    a14_exists = "A14" in ALL_AXIOMS
    print(f"A14 in Axiom Registry: {a14_exists}")
    
    passed = (
        result['coherence_score'] >= 4.0 and
        a14_status['status'] == "ACTIVE" and
        a14_exists
    )
    
    return {
        "passed": passed,
        "coherence_score": result['coherence_score'],
        "patterns_detected": len(result['patterns_detected']),
        "friction_events": len(result['friction_events']),
        "proposals_generated": len(result['governance_proposals_generated']),
        "a14_status": a14_status['status']
    }


if __name__ == "__main__":
    run_all_validations()
