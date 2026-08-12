import pytest
from app.policies.command_policy import CommandPolicy
from app.policies.git_policy import GitPolicy
from app.policies.permissions import PermissionChecker, PolicyViolationError
from app.config.constants import PermissionType, RiskLevel

def test_command_policy_allow():
    assert CommandPolicy.validate_command("npm test") is True
    assert CommandPolicy.validate_command("pytest") is True

def test_command_policy_deny():
    with pytest.raises(PolicyViolationError):
        CommandPolicy.validate_command("rm -rf /")

    with pytest.raises(PolicyViolationError):
        CommandPolicy.validate_command("DROP DATABASE production")

def test_git_policy_protected_branch():
    with pytest.raises(PolicyViolationError):
        GitPolicy.validate_branch_creation("main")

    with pytest.raises(PolicyViolationError):
        GitPolicy.validate_push("production")
