"""Parser initialization"""

from .auth import AuthLogEvent, parse_auth_log_line

__all__ = ["AuthLogEvent", "parse_auth_log_line"]
