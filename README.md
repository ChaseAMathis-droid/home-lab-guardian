#🛡️ Home Lab Guardian

An AI-powered security monitoring agent that watches your Linux logs and alerts you to threats in plain English.
Project: The AI Security Translator
📖 The Simple Explanation (What does this do?)
The Problem: Computer servers keep detailed diaries of everything that happens (called "logs"). These logs are often millions of lines long and written in complex technical codes. For a human, finding a security threat in these logs is like trying to find a needle in a haystack while blindfolded.
The Solution: I built an intelligent "security guard" that never sleeps. It reads these complex logs in real-time. When it spots something suspicious—like a hacker trying to guess a password—it doesn't just record it; it translates the technical data into a plain English alert and sends it to me instantly.
The Result: Instead of seeing this:
> Failed password for invalid user admin from 192.168.1.55 port 22 ssh2
> 
I get a text message that says:
> "Alert: Someone is trying to break into your server using the username 'admin'. Location: Local Network."
> 
⚙️ How It Works (The Process)
 * Listen: The agent continuously monitors system files (Linux logs) for activity.
 * Detect: It uses pattern recognition to filter out "noise" (normal activity) and identify potential threats.
 * Translate: An integrated AI model analyzes the threat data and rewrites it into a human-readable summary.
 * Notify: The agent sends the simplified summary to my phone/dashboard immediately.
🚀 Why I Built This
 * Accessibility: To make server security understandable for non-experts.
 * Speed: To reduce the time it takes to respond to a cyber attack.
 * Automation: To remove the manual labor of reviewing thousands of log lines.
Tips for your Wiki:
 * Use Screenshots: If you can, take a screenshot of a "confusing" raw log next to a screenshot of your "simple" AI alert. Visuals explain things faster than text.
 * Keep the "Why": Recruiters love the "Why I Built This" section because it shows you solve business problems (saving time/reducing complexity).
Would you like me to write a short "Technical Stack" section to go under this, listing the specific tools (like Python, OpenAI API, Linux) you used?

## ✨ Features

- **Real-time Log Monitoring**: Watches `/var/log/auth.log` for suspicious activity
- **AI-Powered Analysis**: Uses local LLM (via Ollama) to explain threats in plain English
- **Smart Notifications**: Sends alerts to Discord or Slack when threats are detected
- **Privacy-First**: Runs entirely locally—no cloud APIs required
- **Easy Docker Deployment**: One command to get started

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐     ┌──────────────┐
│  auth.log   │────▶│ Log Watcher  │────▶│   Parser    │────▶│ AI Analyzer  │
│  (Linux)    │     │  (watchdog)  │     │ (failed SSH,│     │  (Ollama +   │
└─────────────┘     └──────────────┘     │  sudo, etc) │     │  LangChain)  │
                                          └─────────────┘     └──────┬───────┘
                                                                     │
                                                    ┌────────────────▼────────┐
                                                    │  Notifiers (Discord,   │
                                                    │  Slack, etc.)          │
                                                    └────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+ (or Docker)
- [Ollama](https://ollama.ai/) installed locally
- Discord or Slack webhook URL

### Installation

#### Option 1: Python Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install Ollama and pull the model
# Visit https://ollama.ai/download
ollama pull llama3.1:8b

# Configure
cp .env.example .env
# Edit .env with your webhook URLs and log path
```

#### Option 2: Docker (Recommended)

```bash
# Configure
cp .env.example .env
# Edit .env with your webhook URLs

# Start everything
docker-compose up -d

# Check logs
docker-compose logs -f agent
```

### Configuration

Edit `.env`:

```bash
LOG_PATH=/var/log/auth.log           # Path to monitor
DISCORD_WEBHOOK_URL=https://...      # Your Discord webhook
SLACK_WEBHOOK_URL=https://...        # Your Slack webhook (optional)
OLLAMA_MODEL=llama3.1:8b             # Model to use
```

### Running

```bash
# Activate your virtual environment first
source venv/bin/activate

# Run the agent
hlg run

# Or with custom config
hlg run --log-path /custom/path/to/auth.log --model mistral
```

## 🧪 Development

```bash
# Format code
make format

# Run linters
make lint

# Run tests
make test

# Run tests with coverage
make test-cov
```

## 📦 Project Structure

```
home-lab-guardian/
├── src/hlg/
│   ├── __init__.py
│   ├── cli.py              # Click CLI entry point
│   ├── agent.py            # Main orchestrator
│   ├── config.py           # Pydantic settings
│   ├── log_watcher.py      # Watchdog-based log tailer
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── auth.py         # Parse auth.log events
│   ├── ai/
│   │   ├── __init__.py
│   │   └── analyzer.py     # LangChain + Ollama integration
│   └── notifiers/
│       ├── __init__.py
│       ├── discord.py      # Discord webhook
│       └── slack.py        # Slack webhook
├── tests/
│   ├── test_auth_parser.py
│   └── test_cli_dry_run.py
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── Makefile
└── README.md
```

## 🐳 Docker Details

The `docker-compose.yml` includes two services:

- **ollama**: Runs the Ollama service with GPU support (if available)
- **agent**: Runs Home Lab Guardian, mounts your log files read-only

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f agent

# Stop services
docker-compose down
```

## 🎯 Example Alerts

When a failed SSH login is detected:

> **🚨 Security Alert: Failed Login Attempt**
>
> **Severity**: High
>
> **Event**: Failed password attempt for user `root` from IP `192.168.1.100`
>
> **AI Analysis**: This is a brute-force attack attempt. The attacker is trying to guess the root password from a local network IP. Consider:
> - Disabling root SSH login
> - Enabling key-based authentication
> - Setting up fail2ban
>
> **Time**: 2025-11-30 14:32:15

## 🔧 Systemd Service (Production)

To run as a system service:

```bash
sudo cp deploy/hlg.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable hlg
sudo systemctl start hlg
```

## 📊 Tech Stack

- **Python 3.11+**: Core language
- **watchdog**: File system monitoring
- **Ollama**: Local LLM inference
- **LangChain**: LLM orchestration framework
- **Pydantic**: Configuration and data validation
- **Click**: CLI framework
- **Docker**: Containerization

## 🤝 Contributing

PRs welcome! Please run `make lint` and `make test` before submitting.

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built for resume portfolio purposes. Demonstrates:
- Linux system administration
- Python automation
- AI/LLM integration
- Security monitoring
- Docker deployment
