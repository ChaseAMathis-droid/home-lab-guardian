"""Main agent orchestrator"""

import signal
import sys
from typing import Optional

from .config import Settings
from .log_watcher import watch_log_file
from .parsers import parse_auth_log_line
from .ai import ThreatAnalyzer
from .notifiers import DiscordNotifier, SlackNotifier


class HomeLabGuardian:
    """Main security monitoring agent"""

    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.analyzer = ThreatAnalyzer(
            base_url=self.settings.ollama_base_url, model=self.settings.ollama_model
        )

        # Initialize notifiers
        self.notifiers = []
        if self.settings.discord_webhook_url:
            self.notifiers.append(DiscordNotifier(self.settings.discord_webhook_url))
        if self.settings.slack_webhook_url:
            self.notifiers.append(SlackNotifier(self.settings.slack_webhook_url))

        self.running = True

    def start(self) -> None:
        """Start monitoring logs"""
        print(f"🛡️  Home Lab Guardian starting...")
        print(f"📁 Monitoring: {self.settings.log_path}")
        print(f"🤖 AI Model: {self.settings.ollama_model}")
        print(f"📢 Notifiers: {len(self.notifiers)} configured")
        print("=" * 60)

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            for line in watch_log_file(self.settings.log_path, self.settings.poll_interval):
                if not self.running:
                    break

                # Parse the log line
                event = parse_auth_log_line(line)
                if not event:
                    continue

                # Filter based on settings
                if not self._should_alert(event):
                    continue

                print(f"\n⚠️  Event detected: {event.event_type} - {event.username}")

                # Analyze with AI
                try:
                    analysis = self.analyzer.analyze(event)
                    print(f"🔍 Severity: {analysis.severity.upper()}")
                    print(f"💡 {analysis.explanation}")

                    # Send notifications if it's a real threat
                    if analysis.is_threat:
                        self._send_notifications(event, analysis)

                except Exception as e:
                    print(f"❌ Analysis failed: {e}")

        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"❌ Fatal error: {e}")
            sys.exit(1)
        finally:
            print("\n🛑 Home Lab Guardian stopped.")

    def _should_alert(self, event) -> bool:
        """Determine if we should analyze and potentially alert on this event"""
        if event.event_type == "failed_login" and self.settings.alert_on_failed_login:
            return True
        if event.event_type == "sudo" and self.settings.alert_on_sudo:
            return True
        return False

    def _send_notifications(self, event, analysis) -> None:
        """Send notifications to all configured channels"""
        for notifier in self.notifiers:
            try:
                success = notifier.send_alert(event, analysis)
                if success:
                    print(f"✅ Notification sent via {notifier.__class__.__name__}")
                else:
                    print(f"⚠️  Notification failed via {notifier.__class__.__name__}")
            except Exception as e:
                print(f"❌ Notification error ({notifier.__class__.__name__}): {e}")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print("\n⚠️  Shutdown signal received...")
        self.running = False
