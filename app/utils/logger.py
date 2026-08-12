import logging
import sys
import re
from typing import Any, Dict

SENSITIVE_PATTERNS = [
    r"(?i)api[_-]?key\s*[:=]\s*['\"]?([^'\"\s]+)['\"]?",
    r"(?i)password\s*[:=]\s*['\"]?([^'\"\s]+)['\"]?",
    r"(?i)token\s*[:=]\s*['\"]?([^'\"\s]+)['\"]?",
    r"(?i)secret\s*[:=]\s*['\"]?([^'\"\s]+)['\"]?",
]

def sanitize_message(msg: str) -> str:
    sanitized = msg
    for pattern in SENSITIVE_PATTERNS:
        sanitized = re.sub(pattern, r"\1=[REDACTED]", sanitized)
    return sanitized

class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original = super().format(record)
        return sanitize_message(original)

def get_logger(name: str = "multi_agent") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = RedactingFormatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

logger = get_logger("multi_agent")
