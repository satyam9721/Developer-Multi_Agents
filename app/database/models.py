from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class RepositoryModel(Base):
    __tablename__ = "repositories"

    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    full_name = Column(String(255), unique=True, nullable=False)
    clone_url = Column(String(500), nullable=False)
    default_branch = Column(String(50), default="main")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(String(50), primary_key=True)
    repository = Column(String(255), nullable=False)
    user_request = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)
    state_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class TaskEventModel(Base):
    __tablename__ = "task_events"

    id = Column(String(50), primary_key=True)
    task_id = Column(String(50), ForeignKey("tasks.id"), nullable=False)
    event_type = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AgentRunModel(Base):
    __tablename__ = "agent_runs"

    id = Column(String(50), primary_key=True)
    task_id = Column(String(50), ForeignKey("tasks.id"), nullable=False)
    agent_name = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False)
    summary = Column(Text, nullable=True)
    output = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class MemoryRecordModel(Base):
    __tablename__ = "memory_records"

    id = Column(String(50), primary_key=True)
    repository = Column(String(255), nullable=False)
    category = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class WorkflowStateModel(Base):
    __tablename__ = "workflow_states"

    id = Column(String(50), primary_key=True)
    task_id = Column(String(50), ForeignKey("tasks.id"), nullable=False)
    current_step = Column(String(50), nullable=False)
    context_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
