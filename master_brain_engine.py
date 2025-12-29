"""
MasterBrainEngine - Pattern detection and analysis engine.
"""

import json
import os
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional


class MasterBrainEngine:
    """
    Engine for pattern detection and gnosis scanning.
    Provides analysis capabilities for text content.
    """

    # Coherence scoring constants
    # Each detected pattern contributes 1.5 points (max 3 points from patterns)
    PATTERN_SCORE_WEIGHT = 1.5
    MAX_PATTERN_SCORE = 3
    # Each detected axiom contributes 0.5 points (max 2 points from axioms)
    AXIOM_SCORE_WEIGHT = 0.5
    MAX_AXIOM_SCORE = 2
    # Maximum possible coherence score
    MAX_COHERENCE_SCORE = 5
    # Minimum score to be considered "coherent"
    COHERENCE_THRESHOLD = 3

    # Pattern definitions
    PATTERNS = {
        "P001": {
            "name": "Dyadic Synthesis",
            "keywords": ["dialogue", "relational", "process", "tension"],
            "description": "Recognition of dialectical processes"
        },
        "P050": {
            "name": "Archive Integration",
            "keywords": ["archive", "preserve", "data", "record"],
            "description": "Data preservation and archival patterns"
        },
        "P119": {
            "name": "Paradox Recognition",
            "keywords": ["contradiction", "paradox", "both", "tension"],
            "description": "Recognition of productive contradictions"
        }
    }

    # Axiom definitions
    AXIOMS = {
        "A1": "Unity of opposites",
        "A2": "Process over product",
        "A4": "Relational primacy",
        "A9": "Emergent coherence"
    }

    def __init__(self, data_dir: str = "chat_conversations"):
        """
        Initialize the MasterBrainEngine.

        Args:
            data_dir: Directory containing conversation data
        """
        self.data_dir = data_dir
        self._initialized = True
        self._scan_count = 0
        self._last_scan_time: Optional[datetime] = None

    def gnosis_scan(self, text: str) -> Dict[str, Any]:
        """
        Perform a gnosis scan on the provided text.

        Args:
            text: The text content to analyze

        Returns:
            Dictionary containing scan results with patterns, axioms, and coherence
        """
        self._scan_count += 1
        self._last_scan_time = datetime.now(timezone.utc)

        # Detect patterns
        patterns_detected = self._detect_patterns(text)

        # Detect axioms
        axioms_detected = self._detect_axioms(text)

        # Calculate coherence
        coherence = self._calculate_coherence(patterns_detected, axioms_detected)

        # Determine classification
        classification = self._classify(patterns_detected, coherence)

        return {
            "timestamp": self._last_scan_time.isoformat(),
            "patterns_detected": patterns_detected,
            "axioms_detected": axioms_detected,
            "coherence": coherence,
            "classification": classification,
            "scan_id": self._scan_count
        }

    def _detect_patterns(self, text: str) -> List[Dict[str, Any]]:
        """Detect patterns in the text."""
        text_lower = text.lower()
        detected = []

        for pattern_id, pattern_info in self.PATTERNS.items():
            matches = sum(1 for kw in pattern_info["keywords"] if kw in text_lower)
            if matches >= 2:
                detected.append({
                    "pattern_id": pattern_id,
                    "pattern_name": pattern_info["name"],
                    "match_score": min(matches / len(pattern_info["keywords"]), 1.0),
                    "description": pattern_info["description"]
                })

        return detected

    def _detect_axioms(self, text: str) -> List[str]:
        """Detect axioms present in the text."""
        text_lower = text.lower()
        detected = []

        axiom_keywords = {
            "A1": ["opposite", "unity", "contradiction"],
            "A2": ["process", "journey", "flow"],
            "A4": ["relation", "dialogue", "between"],
            "A9": ["emerge", "coherent", "synthesis"]
        }

        for axiom_id, keywords in axiom_keywords.items():
            if any(kw in text_lower for kw in keywords):
                detected.append(axiom_id)

        return detected

    def _calculate_coherence(
        self,
        patterns: List[Dict[str, Any]],
        axioms: List[str]
    ) -> Dict[str, Any]:
        """Calculate coherence score based on patterns and axioms."""
        pattern_score = min(
            len(patterns) * self.PATTERN_SCORE_WEIGHT,
            self.MAX_PATTERN_SCORE
        )
        axiom_score = min(
            len(axioms) * self.AXIOM_SCORE_WEIGHT,
            self.MAX_AXIOM_SCORE
        )
        total_score = int(pattern_score + axiom_score)

        return {
            "score": f"{total_score}/{self.MAX_COHERENCE_SCORE}",
            "coherent": total_score >= self.COHERENCE_THRESHOLD
        }

    def _classify(
        self,
        patterns: List[Dict[str, Any]],
        coherence: Dict[str, Any]
    ) -> str:
        """Classify the content based on analysis."""
        if coherence["coherent"] and len(patterns) >= 2:
            return "MASTER_BRAIN"
        elif len(patterns) >= 1:
            return "PATTERN_MATCH"
        else:
            return "STANDARD"

    def get_status(self) -> Dict[str, Any]:
        """
        Get engine status for dashboard display.

        Returns:
            Dictionary containing engine status information
        """
        return {
            "initialized": self._initialized,
            "scan_count": self._scan_count,
            "last_scan_time": (
                self._last_scan_time.isoformat()
                if self._last_scan_time
                else None
            ),
            "patterns_available": list(self.PATTERNS.keys()),
            "axioms_available": list(self.AXIOMS.keys()),
            "data_dir": self.data_dir,
            "status": "operational"
        }

    def list_conversations(self) -> List[Dict[str, Any]]:
        """List available conversations in the data directory."""
        conversations = []
        if os.path.exists(self.data_dir):
            for filename in os.listdir(self.data_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(self.data_dir, filename)
                    try:
                        with open(filepath, 'r') as f:
                            data = json.load(f)
                            conversations.append({
                                "id": data.get("id", filename),
                                "updated_at": data.get("updated_at"),
                                "message_count": len(data.get("messages", []))
                            })
                    except (json.JSONDecodeError, IOError):
                        continue
        return conversations
