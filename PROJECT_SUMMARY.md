# 🎯 Home Lab Guardian - Project Summary

## ✅ What Was Built

A production-ready AI-powered security monitoring agent that:
- Watches Linux authentication logs in real-time
- Detects suspicious activity (failed logins, sudo usage)
- Uses local LLM (via Ollama) to explain threats in plain English
- Sends alerts to Discord/Slack
- Runs entirely locally (no cloud APIs)

## 📁 Project Structure

```
Home Lab Guardian/
├── src/hlg/                    # Main package
│   ├── __init__.py
│   ├── agent.py                # Orchestrator (runs watcher→parser→analyzer→notifier)
│   ├── cli.py                  # Click CLI with run/test/config commands
│   ├── config.py               # Pydantic settings (from .env)
│   ├── log_watcher.py          # Watchdog-based log tailer
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── auth.py             # Parse auth.log (failed logins, sudo, etc.)
│   ├── ai/
│   │   ├── __init__.py
│   │   └── analyzer.py         # LangChain + Ollama integration
│   └── notifiers/
│       ├── __init__.py
│       ├── discord.py          # Discord webhook
│       └── slack.py            # Slack webhook
├── tests/
│   ├── test_auth_parser.py     # 5 passing tests
│   └── test_cli.py             # 3 passing tests
├── deploy/
│   └── hlg.service             # Systemd unit file
├── .github/workflows/
│   └── ci.yml                  # GitHub Actions (lint + test)
├── pyproject.toml              # PEP 621 packaging with hatchling
├── Dockerfile                  # Multi-stage (Python slim + non-root user)
├── docker-compose.yml          # Ollama + Agent services
├── Makefile                    # Dev commands (setup, format, lint, test, run)
├── quickstart.sh               # One-command setup script
├── sample_auth.log             # Test data
├── .env.example                # Config template
├── .gitignore
├── LICENSE (MIT)
└── README.md                   # Comprehensive documentation
```

## 🧪 Test Results

```
✅ 8/8 tests passing
✅ 46% code coverage
✅ Parser tests: failed logins, sudo, sessions
✅ CLI tests: version, config, error handling
```

## 🚀 Quick Start Commands

```bash
# Setup (automated)
./quickstart.sh

# Or manual setup
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Install Ollama and pull model
ollama pull llama3.1:8b

# Configure webhooks
cp .env.example .env
# Edit .env with your Discord/Slack webhook URLs

# Run with sample log
hlg run --log-path sample_auth.log

# Run tests
make test

# Docker deployment
docker-compose up -d
docker-compose logs -f agent
```

## 🎯 Resume Highlights

**Skills Demonstrated:**
- ✅ Python 3.9+ with modern practices (Pydantic, type hints)
- ✅ AI/LLM integration (LangChain, Ollama)
- ✅ Security monitoring and log parsing
- ✅ Real-time file watching (watchdog)
- ✅ API integrations (Discord, Slack webhooks)
- ✅ CLI development (Click framework)
- ✅ Testing (pytest, 8 tests with coverage)
- ✅ Docker containerization (multi-stage builds)
- ✅ Docker Compose orchestration
- ✅ CI/CD (GitHub Actions)
- ✅ Linux system administration
- ✅ Configuration management (Pydantic Settings)
- ✅ Package development (PEP 621, hatchling)

**Architecture Patterns:**
- Event-driven pipeline (watcher → parser → analyzer → notifier)
- Dependency injection (Settings passed to components)
- Strategy pattern (multiple notifier implementations)
- Fallback mechanisms (rule-based when AI fails)

## 📊 Key Features

1. **Real-time Monitoring**: Uses watchdog to tail log files efficiently
2. **Smart Parsing**: Regex-based extraction of usernames, IPs, event types
3. **AI Analysis**: LangChain + Ollama for threat assessment
4. **Multi-channel Alerts**: Discord and Slack webhook support
5. **Configurable**: All settings via .env or CLI flags
6. **Testable**: 46% coverage with unit and integration tests
7. **Deployable**: Docker Compose with Ollama service
8. **Production-ready**: Systemd service, health checks, signal handling

## 🔧 Configuration

All settings via `.env`:
```bash
LOG_PATH=/var/log/auth.log
DISCORD_WEBHOOK_URL=https://...
SLACK_WEBHOOK_URL=https://...
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
ALERT_ON_FAILED_LOGIN=true
ALERT_ON_SUDO=true
MIN_SEVERITY=medium
```

## 📝 CLI Commands

```bash
hlg run                             # Start monitoring
hlg config                          # Show current settings
hlg test                            # Test AI analyzer
hlg run --log-path /custom/path     # Custom log file
hlg run --model mistral             # Use different model
```

## 🐳 Docker Deployment

Two services:
1. **ollama**: Runs Ollama LLM service
2. **agent**: Runs Home Lab Guardian, mounts /var/log/auth.log

```bash
docker-compose up -d              # Start services
docker-compose logs -f agent      # View logs
docker-compose down               # Stop services
```

## 🎓 Learning Outcomes

This project demonstrates professional-grade Python development:
- Modern packaging (pyproject.toml, PEP 621)
- CLI development with Click
- AI/LLM integration without vendor lock-in
- Security monitoring fundamentals
- Real-time data processing
- Containerization best practices
- Testing and CI/CD

## 🔗 Repository

All code committed and ready for GitHub:
- Clear commit history
- Comprehensive README
- Tests passing
- Docker builds successfully
- CI workflow configured

## 🌟 Next Steps (Optional Enhancements)

1. Add more log parsers (nginx, apache, docker)
2. Web dashboard with real-time alerts
3. Alert aggregation and deduplication
4. Machine learning for anomaly detection
5. Integration with SIEM tools
6. Email notifications
7. Alert history database
8. Multi-node monitoring

---

**Built with:**
- Python 3.9+
- LangChain 0.3+
- Ollama
- Pydantic 2.x
- Click 8.x
- Watchdog 4.x
- Pytest 8.x
- Docker & Docker Compose

**License:** MIT
**Author:** Chase Mathis
**Purpose:** Portfolio project demonstrating AI integration, security monitoring, and Python best practices
