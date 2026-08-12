from app.policies.permissions import PolicyViolationError
from app.utils.logger import logger

class GitPolicy:
    """Enforces Git branching, commit, and pull request safety policies."""
    
    PROTECTED_BRANCHES = ["main", "master", "production", "release"]

    @classmethod
    def validate_branch_creation(cls, branch_name: str) -> bool:
        """Ensure feature branch naming follows conventions and avoids protected branches."""
        if branch_name.lower() in cls.PROTECTED_BRANCHES:
            raise PolicyViolationError(f"Cannot directly target or create protected branch '{branch_name}'.")
        return True

    @classmethod
    def validate_push(cls, target_branch: str) -> bool:
        """Validate if direct push to branch is permitted."""
        if target_branch.lower() in cls.PROTECTED_BRANCHES:
            raise PolicyViolationError(f"Direct push to protected branch '{target_branch}' is strictly prohibited.")
        return True

    @classmethod
    def validate_merge(cls, target_branch: str, user_approved: bool = False) -> bool:
        """Validate merge policy requiring explicit approval for protected target branches."""
        if target_branch.lower() in cls.PROTECTED_BRANCHES and not user_approved:
            raise PolicyViolationError(f"Merging into protected branch '{target_branch}' requires explicit user approval.")
        return True
