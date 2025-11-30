"""AI-powered threat analysis using LangChain and Ollama"""

from dataclasses import dataclass
from typing import Optional

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

from ..parsers import AuthLogEvent


@dataclass
class ThreatAnalysis:
    """AI analysis result for a log event"""

    severity: str  # "low", "medium", "high", "critical"
    explanation: str
    recommendations: list[str]
    is_threat: bool


class ThreatAnalyzer:
    """Analyze log events using local LLM via Ollama"""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.1:8b"):
        self.llm = ChatOllama(base_url=base_url, model=model, temperature=0.3)

    def analyze(self, event: AuthLogEvent) -> ThreatAnalysis:
        """
        Analyze a log event and determine if it's a threat
        
        Args:
            event: Parsed log event
            
        Returns:
            ThreatAnalysis with severity, explanation, and recommendations
        """
        # Build context for the LLM
        context = f"""
Event Type: {event.event_type}
Service: {event.service}
Username: {event.username or 'N/A'}
Source IP: {event.source_ip or 'N/A'}
Message: {event.message}
Initial Severity: {event.severity}
"""

        system_prompt = """You are a cybersecurity expert analyzing Linux authentication logs. 
Your task is to:
1. Assess the severity (low, medium, high, critical)
2. Explain why this event matters in plain English
3. Provide 2-3 actionable recommendations
4. Determine if this is a real threat or normal activity

Be concise but helpful. Focus on practical advice for system administrators."""

        user_prompt = f"""Analyze this authentication event and provide:
1. Severity level
2. Brief explanation (2-3 sentences)
3. List of recommendations

Event details:
{context}

Respond in this format:
SEVERITY: [level]
EXPLANATION: [your explanation]
RECOMMENDATIONS:
- [recommendation 1]
- [recommendation 2]
- [recommendation 3]
IS_THREAT: [yes/no]
"""

        try:
            messages = [SystemMessage(content=system_prompt), HumanMessage(content=user_prompt)]

            response = self.llm.invoke(messages)
            return self._parse_response(response.content, event)

        except Exception as e:
            # Fallback to rule-based analysis if LLM fails
            return self._fallback_analysis(event)

    def _parse_response(self, response: str, event: AuthLogEvent) -> ThreatAnalysis:
        """Parse LLM response into ThreatAnalysis"""
        lines = response.strip().split("\n")

        severity = "medium"
        explanation = "Security event detected."
        recommendations = []
        is_threat = False

        for line in lines:
            line = line.strip()
            if line.startswith("SEVERITY:"):
                severity = line.split(":", 1)[1].strip().lower()
            elif line.startswith("EXPLANATION:"):
                explanation = line.split(":", 1)[1].strip()
            elif line.startswith("-"):
                recommendations.append(line[1:].strip())
            elif line.startswith("IS_THREAT:"):
                is_threat_str = line.split(":", 1)[1].strip().lower()
                is_threat = is_threat_str in ["yes", "true", "1"]

        return ThreatAnalysis(
            severity=severity, explanation=explanation, recommendations=recommendations, is_threat=is_threat
        )

    def _fallback_analysis(self, event: AuthLogEvent) -> ThreatAnalysis:
        """Rule-based fallback analysis when LLM is unavailable"""
        if event.event_type == "failed_login":
            return ThreatAnalysis(
                severity="high",
                explanation=f"Failed login attempt for user '{event.username}' from {event.source_ip}. This could indicate a brute-force attack.",
                recommendations=[
                    "Monitor for repeated attempts from this IP",
                    "Consider implementing fail2ban",
                    "Use key-based authentication instead of passwords",
                ],
                is_threat=True,
            )
        elif event.event_type == "sudo":
            return ThreatAnalysis(
                severity="medium",
                explanation=f"User '{event.username}' executed a privileged command. Normal if expected.",
                recommendations=[
                    "Verify this was an authorized action",
                    "Review sudo logs regularly",
                    "Limit sudo access to necessary users only",
                ],
                is_threat=False,
            )
        else:
            return ThreatAnalysis(
                severity="low",
                explanation="Authentication event logged. No immediate action required.",
                recommendations=["Continue monitoring logs"],
                is_threat=False,
            )
