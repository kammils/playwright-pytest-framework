"""
Logger configuration using loguru for console and file logging.

This module provides a centralized logger configuration that outputs logs to both
console and file with appropriate formatting and rotation settings.
"""

import sys
from pathlib import Path
from loguru import logger

# Configure the logs directory
LOGS_DIR = Path(__file__).parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Remove default handler
logger.remove()

# Console handler configuration
logger.add(
    sink=sys.stdout,
    format="<level>{time:YYYY-MM-DD HH:mm:ss}</level> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG",
    colorize=True,
)

# File handler configuration
logger.add(
    sink=LOGS_DIR / "app_{time:YYYY-MM-DD_HH-mm-ss}.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="DEBUG",
    rotation="500 MB",
    retention="7 days",
    compression="zip",
    colorize=False,
)

__all__ = ["logger"]
