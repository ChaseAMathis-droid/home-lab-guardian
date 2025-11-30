"""Discord webhook notifier"""

from typing import Optional

import requests

from ..ai import ThreatAnalysis
from ..parsers import AuthLogEvent


class DiscordNotifier:
    """Send notifications to Discord via webhook"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_alert(self, event: AuthLogEvent, analysis: ThreatAnalysis) -> bool:
        """
        Send an alert to Discord

        Args:
            event: The log event
            analysis: AI analysis of the event

        Returns:
            True if notification was sent successfully
        """
        if not self.webhook_url:
            return False

        # Map severity to color
        color_map = {"low": 3447003, "medium": 16776960, "high": 16737095, "critical": 10038562}
        color = color_map.get(analysis.severity, 3447003)

        # Build embed
        embed = {
            "title": f"🚨 Security Alert: {event.event_type.replace('_', ' ').title()}",
            "description": analysis.explanation,
            "color": color,
            "fields": [
                {"name": "Severity", "value": analysis.severity.upper(), "inline": True},
                {"name": "Service", "value": event.service, "inline": True},
                {"name": "Username", "value": event.username or "N/A", "inline": True},
                {"name": "Source IP", "value": event.source_ip or "N/A", "inline": True},
                {
                    "name": "Timestamp",
                    "value": event.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    "inline": True,
                },
                {
                    "name": "Recommendations",
                    "value": "\n".join(f"• {rec}" for rec in analysis.recommendations[:3]),
                    "inline": False,
                },
            ],
            "footer": {"text": "Home Lab Guardian"},
        }

        payload = {"embeds": [embed]}

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to send Discord notification: {e}")
            return False
