from enum import Enum

class TaskStatus(str, Enum):
    CREATED = "CREATED"
    PLANNING = "PLANNING"
    RESEARCHING = "RESEARCHING"
    CODING = "CODING"
    REVIEWING = "REVIEWING"
    TESTING = "TESTING"
    BUILDING = "BUILDING"
    READY_FOR_PR = "READY_FOR_PR"
    PR_CREATED = "PR_CREATED"
    CI_RUNNING = "CI_RUNNING"
    DEPLOYING = "DEPLOYING"
    LIVE_TESTING = "LIVE_TESTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL"

class AgentRole(str, Enum):
    MANAGER = "manager"
    PLANNER = "planner"
    RESEARCHER = "researcher"
    CODER = "coder"
    REVIEWER = "reviewer"
    TESTER = "tester"
    BROWSER = "browser"

class RiskLevel(str, Enum):
    READ_ONLY = "READ_ONLY"
    WRITE_SAFE = "WRITE_SAFE"
    HIGH_RISK = "HIGH_RISK"
    DESTRUCTIVE = "DESTRUCTIVE"

class PermissionType(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    HIGH_RISK = "HIGH_RISK"

class LLMProvider(str, Enum):
    MOCK = "mock"
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"

class EventTypes(str, Enum):
    TASK_CREATED = "task_created"
    STATE_TRANSITION = "state_transition"
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_FAILED = "agent_failed"
    TOOL_EXECUTED = "tool_executed"
    POLICY_VIOLATION = "policy_violation"
    WORKFLOW_COMPLETED = "workflow_completed"
