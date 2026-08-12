import re
from app.policies.permissions import PolicyViolationError
from app.utils.logger import logger

class CommandPolicy:
    """Enforces safety rules on shell command execution."""

    BANNED_COMMAND_PATTERNS = [
        r"rm\s+-rf\s+/",
        r"rm\s+-rf\s+~",
        r"drop\s+database",
        r"drop\s+table",
        r"truncate\s+table",
        r"sudo\s+",
        r"mkfs",
        r":\(\)\{\s*:\|:&\s*\};:",  # fork bomb
        r">\s*/dev/sd",
    ]

    ALLOWED_EXECUTABLES = [
        "npm", "node", "npx",
        "python", "python3", "pytest", "pip", "ruff", "mypy", "flake8", "black",
        "git", "ls", "pwd", "cat", "echo", "mkdir", "touch", "find", "grep"
    ]

    @classmethod
    def validate_command(cls, command_str: str) -> bool:
        """Validate if a command string is safe for execution."""
        clean_cmd = command_str.strip()

        for pattern in cls.BANNED_COMMAND_PATTERNS:
            if re.search(pattern, clean_cmd, re.IGNORECASE):
                logger.warning(f"BLOCKED COMMAND: Matched banned pattern '{pattern}' in '{clean_cmd}'")
                raise PolicyViolationError(f"Command contains prohibited pattern and was blocked.")

        executable = clean_cmd.split()[0] if clean_cmd.split() else ""
        if executable and executable not in cls.ALLOWED_EXECUTABLES:
            logger.warning(f"BLOCKED COMMAND: Executable '{executable}' not in allowed execution policy.")
            raise PolicyViolationError(f"Executable '{executable}' is not authorized in command execution policy.")

        return True
