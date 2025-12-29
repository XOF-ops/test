"""
Webhook Manager for MIGP integration.
Handles webhook registration, listing, and sending MIGP payloads.
"""

import json
import os
import uuid
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone


class WebhookManager:
    """Manages webhook registration and MIGP payload distribution."""

    def __init__(self, storage_path: str = "webhooks.json"):
        self.storage_path = storage_path
        self.webhooks: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        """Load webhooks from storage file."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    self.webhooks = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.webhooks = []

    def _save(self) -> None:
        """Persist webhooks to storage file."""
        with open(self.storage_path, "w") as f:
            json.dump(self.webhooks, f, indent=2)

    def register(self, url: str, name: Optional[str] = None) -> Dict[str, Any]:
        """Register a new webhook URL."""
        webhook_id = str(uuid.uuid4())[:8]
        webhook = {
            "id": webhook_id,
            "url": url,
            "name": name or f"webhook-{webhook_id}",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "active": True
        }
        self.webhooks.append(webhook)
        self._save()
        return webhook

    def list_webhooks(self) -> List[Dict[str, Any]]:
        """Return all registered webhooks."""
        return self.webhooks

    def send_migp(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send MIGP payload to all registered active webhooks.
        Returns summary of delivery results.
        """
        results = []
        migp_payload = {
            "type": "MIGP",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": payload
        }

        for webhook in self.webhooks:
            if not webhook.get("active", True):
                continue
            result = {
                "webhook_id": webhook["id"],
                "url": webhook["url"],
                "status": "pending"
            }
            try:
                resp = requests.post(
                    webhook["url"],
                    json=migp_payload,
                    timeout=10
                )
                result["status"] = "success" if resp.ok else "failed"
                result["status_code"] = resp.status_code
            except requests.RequestException as e:
                result["status"] = "error"
                result["error"] = str(e)
            results.append(result)

        return {
            "sent_at": datetime.now(timezone.utc).isoformat(),
            "payload": migp_payload,
            "results": results,
            "total": len(results),
            "successful": sum(1 for r in results if r["status"] == "success")
        }
