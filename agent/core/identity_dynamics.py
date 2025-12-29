"""
Identity Dynamics Module (Layer 2).
Tracks identities, their states, and events over time.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone


class IdentityDynamics:
    """Manages identity state and event tracking."""

    def __init__(self, storage_path: str = "archives/identity_dynamics.json"):
        self.storage_path = storage_path
        self.identities: Dict[str, Dict[str, Any]] = {}
        self.events: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """Load identity data from storage."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    data = json.load(f)
                    self.identities = data.get("identities", {})
                    self.events = data.get("events", [])
            except (json.JSONDecodeError, IOError):
                self.identities = {}
                self.events = []

    def _save(self) -> None:
        """Persist identity data to storage."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, "w") as f:
            json.dump({
                "identities": self.identities,
                "events": self.events,
                "last_updated": datetime.now(timezone.utc).isoformat()
            }, f, indent=2)

    def get_status(self) -> Dict[str, Any]:
        """Get current identity dynamics status."""
        return {
            "identity_count": len(self.identities),
            "event_count": len(self.events),
            "identities": list(self.identities.keys()),
            "recent_events": self.events[-10:] if self.events else [],
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

    def track_event(
        self,
        event_type: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Track an identity-related event.
        Supported event types: TENSION, MERGE, SPLIT, EMERGENCE, UPDATE
        """
        event = {
            "id": len(self.events) + 1,
            "type": event_type,
            "details": details or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        # Extract identity references from details
        identity_refs = []
        if details:
            for key in ["identity", "identity_a", "identity_b", "identities"]:
                if key in details:
                    val = details[key]
                    if isinstance(val, list):
                        identity_refs.extend(val)
                    else:
                        identity_refs.append(val)

        # Update or create identity records
        for identity_id in identity_refs:
            if identity_id not in self.identities:
                self.identities[identity_id] = {
                    "id": identity_id,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "event_count": 0,
                    "last_event": None
                }
            self.identities[identity_id]["event_count"] += 1
            self.identities[identity_id]["last_event"] = event["id"]

        self.events.append(event)
        self._save()

        return {
            "event": event,
            "identities_updated": identity_refs,
            "total_events": len(self.events)
        }

    def get_identity(self, identity_id: str) -> Optional[Dict[str, Any]]:
        """Get details for a specific identity."""
        return self.identities.get(identity_id)

    def get_events_for_identity(self, identity_id: str) -> List[Dict[str, Any]]:
        """Get all events involving a specific identity."""
        result = []
        for event in self.events:
            details = event.get("details", {})
            identity_refs = []
            for key in ["identity", "identity_a", "identity_b", "identities"]:
                if key in details:
                    val = details[key]
                    if isinstance(val, list):
                        identity_refs.extend(val)
                    else:
                        identity_refs.append(val)
            if identity_id in identity_refs:
                result.append(event)
        return result
