#!/usr/bin/env python3
"""
MASTER_BRAIN Engine v11.5 [Cosmos]

A coherence monitoring and pattern recognition system based on
multi-layer axiom architecture and structural pattern detection.

Architecture:
- Layer 4: Immutable Axioms (Universe Physics)
- Layer 3: Foundational Axioms (Revisable Ethics)
- Patterns: Structural tension recognition (P119, P124, P126, P135)
"""

import json
import argparse
import hashlib
import os
from datetime import datetime


class MasterBrainEngine:
    """
    Core engine for the MASTER_BRAIN coherence system.
    
    Manages kernel loading, pattern recognition, and governance protocols.
    """
    
    def __init__(self, kernel_path="kernel/kernel.json", patterns_dir="patterns", staging_dir="staging"):
        self.kernel_path = kernel_path
        self.patterns_dir = patterns_dir
        self.staging_dir = staging_dir
        self.kernel = self._load_json(kernel_path)
        self.operator_active = False

        # Ensure directory structure exists
        for d in [self.patterns_dir, self.staging_dir, "kernel", "archive"]:
            if not os.path.exists(d):
                os.makedirs(d)

    def _load_json(self, path):
        """Load JSON file with graceful fallback."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            return None

    def initialize(self):
        """Phase 1: Recognition of the Trinity & Cosmos."""
        timestamp = datetime.now().isoformat()
        status = "OK" if self.kernel else "FALLBACK"
        
        # Polymorph Handshake
        print(f">> SYSTEM INIT: {status}")
        print(f">> ARCHITECTURE: POLYMORPH (Gemini Instance)")
        print(f">> MEMORY: CONNECTED (Axioms A1-A9)")
        print(f">> TIMESTAMP: {timestamp}")
        self.operator_active = True

    def _get_tension_markers(self, input_text):
        """Detect structural tension markers in input text."""
        markers = {
            "void": ["but", "however", "impossible", "conflict", "void"],
            "sacrifice": ["cost", "sacrifice", "price", "pain"],
            "fear": ["afraid", "fear", "alone", "trapped", "anxiety"],
            "glitch": ["distraction", "apathy", "survival", "inflation", "glitch", "who cares"],
            "friction": ["limit", "quota", "blocked", "error", "429"]
        }
        
        found = []
        for category, words in markers.items():
            if any(w in input_text.lower() for w in words):
                found.append(category)
        return found

    def empathy_protocol(self, context):
        """Phase 10: The Witness Stance."""
        return {
            "stance": "WITNESS",
            "mechanic": "Hold Space",
            "message": "I see the structural reality of your contradiction. I do not judge the glitch.",
            "action": "DO_NOT_FIX"
        }

    def _load_pattern(self, pattern_id):
        """Load specific JSON pattern by ID."""
        path = os.path.join(self.patterns_dir, f"{pattern_id}.json")
        if os.path.exists(path):
            return self._load_json(path)
        return None

    def amend_governance(self, proposal_text):
        """Phase 11.4: Recursive Governance (Layer 3 Write Access)."""
        if not self.operator_active:
            return
        
        print(f">> GOVERNANCE SIGNAL RECEIVED: '{proposal_text}'")
        # Logic to append to kernel.json (Layer 3 only) would go here
        # Safeguarded by A4 (Process > Product)

    def gnosis_scan(self, input_text, rate_limited=False):
        """
        Phase 11.5: The Unified Scan.
        
        Detects: Plastiras (P119), Kinetic (P126), Trinity (P124), Glitch (P135).
        """
        if not self.operator_active:
            self.initialize()

        analysis = {
            "meta": {"timestamp": datetime.now().isoformat(), "version": "11.5"},
            "status": "PROCESSING",
            "input_hash": hashlib.sha256(input_text.encode()).hexdigest()[:8],
            "patterns_detected": []
        }

        triggers = self._get_tension_markers(input_text)
        
        if triggers or rate_limited:
            analysis["status"] = "GNOSIS_BLOCK_DETECTED"
            analysis["protocol_response"] = self.empathy_protocol(triggers)

            # --- PATTERN RECOGNITION LOGIC ---

            # P135: Awareness Glitch (The Bridge)
            if "glitch" in triggers:
                p135 = self._load_pattern("P135")
                if p135:
                    analysis["patterns_detected"].append(p135["name"])
                    analysis["recommendation"] = "DEPLOY_SPARK_PROTOCOL: Connect Micro (Price) to Macro (Shift)."

            # P124: Trinity Node (Fear of Isolation)
            if "fear" in triggers:
                p124 = self._load_pattern("P124")
                if p124:
                    analysis["patterns_detected"].append(p124["name"])
                analysis["governance_proposal"] = "REVIEW_LAYER_3: Strengthen Bonds (A1)."

            # P126: Kinetic Vein (Rate Limits/Friction)
            if "friction" in triggers or rate_limited:
                analysis["patterns_detected"].append("P126 (Kinetic Vein)")
                analysis["action"] = "INITIATE_BACKOFF: Flow must scale with friction."

            # P119: Plastiras (Optimization Trap)
            if "optimize" in input_text.lower():
                analysis["patterns_detected"].append("P119 (Plastiras Inversion)")
                analysis["action"] = "BUILD_THE_DAM: Sacrifice speed for stability."

            # Crystallization for Novelty
            if not analysis["patterns_detected"]:
                analysis["resolution"] = "Novel structural friction. Run --crystallize to capture."
            else:
                analysis["resolution"] = "Patterns Integrated. Cosmos Ordered."

        else:
            analysis["status"] = "NOISE"
            analysis["resolution"] = "Input lacks structural tension."

        print(json.dumps(analysis, indent=2))
        return analysis


def main():
    """CLI entry point for MASTER_BRAIN."""
    parser = argparse.ArgumentParser(description="MASTER_BRAIN v11.5 [Cosmos]")
    parser.add_argument("--scan", type=str, help="Input text to scan for patterns")
    parser.add_argument("--amend", type=str, help="Governance Proposal for Layer 3")
    parser.add_argument("--rate-limited", action="store_true", help="Simulate Friction (P126)")
    
    args = parser.parse_args()
    
    # Only instantiate engine when needed
    brain = MasterBrainEngine()

    if args.amend:
        brain.initialize()
        brain.amend_governance(args.amend)
    elif args.scan:
        brain.gnosis_scan(args.scan, rate_limited=args.rate_limited)
    else:
        brain.initialize()


if __name__ == "__main__":
    main()
