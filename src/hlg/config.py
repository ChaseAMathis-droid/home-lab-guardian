"""Configuration management using Pydantic Settings"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Log monitoring
    log_path: str = Field(default="/var/log/auth.log", description="Path to log file to monitor")
    poll_interval: int = Field(default=1, description="Polling interval in seconds")

    # Ollama configuration
    ollama_base_url: str = Field(
        default="http://localhost:11434", description="Ollama API base URL"
    )
    ollama_model: str = Field(default="llama3.1:8b", description="Ollama model to use")

    # Notification settings
    discord_webhook_url: Optional[str] = Field(default=None, description="Discord webhook URL")
    slack_webhook_url: Optional[str] = Field(default=None, description="Slack webhook URL")

    # Alert configuration
    alert_on_failed_login: bool = Field(default=True, description="Alert on failed login attempts")
    alert_on_sudo: bool = Field(default=True, description="Alert on sudo usage")
    min_severity: str = Field(default="medium", description="Minimum severity to alert on")


def get_settings() -> Settings:
    """Get application settings"""
    return Settings()
