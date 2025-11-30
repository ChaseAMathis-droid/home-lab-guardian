"""Parse Linux auth.log entries"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AuthLogEvent:
    """Parsed authentication log event"""

    timestamp: datetime
    hostname: str
    service: str
    message: str
    event_type: str  # "failed_login", "sudo", "session_opened", "unknown"
    username: Optional[str] = None
    source_ip: Optional[str] = None
    severity: str = "low"  # "low", "medium", "high"


def parse_auth_log_line(line: str) -> Optional[AuthLogEvent]:
    """
    Parse a single auth.log line into a structured event

    Example lines:
    - Nov 30 12:34:56 hostname sshd[1234]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2
    - Nov 30 12:35:01 hostname sudo: username : TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/usr/bin/apt update
    """
    # Basic auth.log pattern: timestamp hostname service[pid]: message
    pattern = r"^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+(\S+)\s+(\w+)(?:\[\d+\])?: (.+)$"
    match = re.match(pattern, line)

    if not match:
        return None

    timestamp_str, hostname, service, message = match.groups()

    # Parse timestamp (add current year since auth.log doesn't include it)
    try:
        timestamp = datetime.strptime(f"2025 {timestamp_str}", "%Y %b %d %H:%M:%S")
    except ValueError:
        return None

    # Determine event type and extract details
    event_type = "unknown"
    username = None
    source_ip = None
    severity = "low"

    # Failed password attempt
    if "Failed password" in message or "authentication failure" in message.lower():
        event_type = "failed_login"
        severity = "high"

        # Extract username and IP
        user_match = re.search(r"for (?:invalid user )?(\S+)", message)
        if user_match:
            username = user_match.group(1)

        ip_match = re.search(r"from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", message)
        if ip_match:
            source_ip = ip_match.group(1)

    # Sudo command
    elif service == "sudo":
        event_type = "sudo"
        severity = "medium"

        # Extract username
        user_match = re.search(r"^\s*(\S+)\s*:", message)
        if user_match:
            username = user_match.group(1)

    # Session opened (successful login)
    elif "session opened" in message.lower():
        event_type = "session_opened"
        severity = "low"

        user_match = re.search(r"for user (\S+)", message)
        if user_match:
            username = user_match.group(1)

    return AuthLogEvent(
        timestamp=timestamp,
        hostname=hostname,
        service=service,
        message=message,
        event_type=event_type,
        username=username,
        source_ip=source_ip,
        severity=severity,
    )
