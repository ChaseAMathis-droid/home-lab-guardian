"""CLI interface using Click"""

from pathlib import Path

import click

from .agent import HomeLabGuardian
from .config import Settings


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """🛡️  Home Lab Guardian - AI-powered security log monitoring"""
    pass


@cli.command()
@click.option(
    "--log-path",
    type=click.Path(exists=True),
    help="Path to the log file to monitor (default: /var/log/auth.log)",
)
@click.option("--model", type=str, help="Ollama model to use (default: llama3.1:8b)")
@click.option("--poll-interval", type=int, help="Polling interval in seconds (default: 1)")
@click.option("--discord-webhook", type=str, help="Discord webhook URL")
@click.option("--slack-webhook", type=str, help="Slack webhook URL")
def run(log_path, model, poll_interval, discord_webhook, slack_webhook):
    """Start the Home Lab Guardian agent"""
    # Load settings from env, then override with CLI args
    settings = Settings()

    if log_path:
        settings.log_path = log_path
    if model:
        settings.ollama_model = model
    if poll_interval:
        settings.poll_interval = poll_interval
    if discord_webhook:
        settings.discord_webhook_url = discord_webhook
    if slack_webhook:
        settings.slack_webhook_url = slack_webhook

    # Validate log path exists
    if not Path(settings.log_path).exists():
        click.echo(f"❌ Error: Log file not found: {settings.log_path}", err=True)
        click.echo("\n💡 Tip: Use --log-path to specify a different file", err=True)
        raise click.Abort()

    # Warn if no notifiers configured
    if not settings.discord_webhook_url and not settings.slack_webhook_url:
        click.echo("⚠️  Warning: No webhook URLs configured. Alerts will only print to console.")
        click.echo("💡 Set DISCORD_WEBHOOK_URL or SLACK_WEBHOOK_URL in .env")
        click.echo()

    # Start the agent
    agent = HomeLabGuardian(settings)
    agent.start()


@cli.command()
def test():
    """Test AI analyzer with a sample event"""
    from datetime import datetime

    from .ai import ThreatAnalyzer
    from .parsers import AuthLogEvent

    click.echo("🧪 Testing AI analyzer...")

    # Create a sample failed login event
    event = AuthLogEvent(
        timestamp=datetime.now(),
        hostname="testhost",
        service="sshd",
        message="Failed password for invalid user admin from 192.168.1.100 port 22 ssh2",
        event_type="failed_login",
        username="admin",
        source_ip="192.168.1.100",
        severity="high",
    )

    settings = Settings()
    analyzer = ThreatAnalyzer(base_url=settings.ollama_base_url, model=settings.ollama_model)

    click.echo(f"📊 Analyzing sample event: {event.event_type}")
    try:
        analysis = analyzer.analyze(event)
        click.echo(f"\n✅ Analysis complete!")
        click.echo(f"Severity: {analysis.severity}")
        click.echo(f"Explanation: {analysis.explanation}")
        click.echo(f"Recommendations:")
        for rec in analysis.recommendations:
            click.echo(f"  - {rec}")
    except Exception as e:
        click.echo(f"❌ Test failed: {e}", err=True)
        raise click.Abort()


@cli.command()
def config():
    """Show current configuration"""
    settings = Settings()

    click.echo("⚙️  Current Configuration:")
    click.echo("=" * 50)
    click.echo(f"Log Path:         {settings.log_path}")
    click.echo(f"Poll Interval:    {settings.poll_interval}s")
    click.echo(f"Ollama URL:       {settings.ollama_base_url}")
    click.echo(f"Ollama Model:     {settings.ollama_model}")
    click.echo(
        f"Discord Webhook:  {'✓ Configured' if settings.discord_webhook_url else '✗ Not set'}"
    )
    click.echo(f"Slack Webhook:    {'✓ Configured' if settings.slack_webhook_url else '✗ Not set'}")
    click.echo(f"Alert on Failed:  {settings.alert_on_failed_login}")
    click.echo(f"Alert on Sudo:    {settings.alert_on_sudo}")
    click.echo(f"Min Severity:     {settings.min_severity}")


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == "__main__":
    main()
