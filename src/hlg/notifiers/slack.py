"""Slack webhook notifier"""

from typing import Optional

import requests

from ..ai import ThreatAnalysis
from ..parsers import AuthLogEvent


class SlackNotifier:
    """Send notifications to Slack via webhook"""

    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_alert(self, event: AuthLogEvent, analysis: ThreatAnalysis) -> bool:
        """
        Send an alert to Slack

        Args:
            event: The log event
            analysis: AI analysis of the event

        Returns:
            True if notification was sent successfully
        """
        if not self.webhook_url:
            return False

        # Map severity to emoji
        emoji_map = {
            "low": ":information_source:",
            "medium": ":warning:",
            "high": ":rotating_light:",
            "critical": ":fire:",
        }
        emoji = emoji_map.get(analysis.severity, ":information_source:")

        # Build Slack message
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} Security Alert: {event.event_type.replace('_', ' ').title()}",
                },
            },
            {"type": "section", "text": {"type": "mrkdwn", "text": f"*{analysis.explanation}*"}},
            {"type": "divider"},
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*Severity:*\n{analysis.severity.upper()}"},
                    {"type": "mrkdwn", "text": f"*Service:*\n{event.service}"},
                    {"type": "mrkdwn", "text": f"*Username:*\n{event.username or 'N/A'}"},
                    {"type": "mrkdwn", "text": f"*Source IP:*\n{event.source_ip or 'N/A'}"},
                ],
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Recommendations:*\n"
                    + "\n".join(f"• {rec}" for rec in analysis.recommendations[:3]),
                },
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "mrkdwn",
                        "text": f"_Time: {event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}_",
                    }
                ],
            },
        ]

        payload = {"blocks": blocks}

        try:
            response = requests.post(self.webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"Failed to send Slack notification: {e}")
            return False
