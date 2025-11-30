"""Tests for auth.log parser"""

import pytest
from datetime import datetime

from hlg.parsers.auth import parse_auth_log_line, AuthLogEvent


def test_parse_failed_password():
    """Test parsing failed password attempt"""
    line = "Nov 30 12:34:56 hostname sshd[1234]: Failed password for invalid user admin from 192.168.1.100 port 22 ssh2"
    event = parse_auth_log_line(line)

    assert event is not None
    assert event.event_type == "failed_login"
    assert event.username == "admin"
    assert event.source_ip == "192.168.1.100"
    assert event.severity == "high"
    assert event.service == "sshd"


def test_parse_sudo():
    """Test parsing sudo command"""
    line = "Nov 30 12:35:01 hostname sudo: testuser : TTY=pts/0 ; PWD=/home/user ; USER=root ; COMMAND=/usr/bin/apt update"
    event = parse_auth_log_line(line)

    assert event is not None
    assert event.event_type == "sudo"
    assert event.username == "testuser"
    assert event.severity == "medium"
    assert event.service == "sudo"


def test_parse_session_opened():
    """Test parsing session opened"""
    line = "Nov 30 12:36:00 hostname sshd[5678]: pam_unix(sshd:session): session opened for user john by (uid=0)"
    event = parse_auth_log_line(line)

    assert event is not None
    assert event.event_type == "session_opened"
    assert event.username == "john"
    assert event.severity == "low"


def test_parse_invalid_line():
    """Test parsing invalid log line"""
    line = "This is not a valid auth log line"
    event = parse_auth_log_line(line)

    assert event is None


def test_parse_failed_authentication():
    """Test parsing authentication failure"""
    line = "Nov 30 12:37:00 hostname sshd[9999]: authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=10.0.0.5 user=root"
    event = parse_auth_log_line(line)

    assert event is not None
    assert event.event_type == "failed_login"
    assert event.severity == "high"
