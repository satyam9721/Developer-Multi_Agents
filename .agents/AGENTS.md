# Workspace Rules for Multi -AI Agents

## Project Memory Maintenance

- The file [`PROJECT_MEMORY.md`](file:///Users/satyam_007/Desktop/Multi%20-AI%20Agents/backend/PROJECT_MEMORY.md) acts as the living memory and architecture flow map for this repository.
- **MANDATORY**: Whenever you add a new file or directory, remove a file, or modify/implement logic in any file under `backend/`, you MUST update [`PROJECT_MEMORY.md`](file:///Users/satyam_007/Desktop/Multi%20-AI%20Agents/backend/PROJECT_MEMORY.md):
  1. Update the **Directory & File Structure** tree if file/folder structure changed.
  2. Update the **File Responsibilities & Implementation Details** table with the newly implemented or altered logic.
  3. Add an entry to the **Change Log** table with the date, modified file, summary of changes, and agent name.
     ECC/
     |-- agents/ # 71 specialized subagents for delegation
     |-- skills/ # 311 reusable workflows loaded on demand
     |-- commands/ # 97 maintained slash-command shims
     |-- rules/ # opt-in common and language standards
     |-- hooks/ # runtime automation and enforcement
     |-- scripts/ # install, repair, sync, orchestration, and checks
     |-- .claude-plugin/ # Claude Code marketplace manifest
     |-- .codex/ # Codex reference configuration and agent roles
     |-- .opencode/ # OpenCode plugin, commands, and instructions
     |-- .cursor/ # Cursor rules and hook adapter
     |-- docs/ # public setup, architecture, and operating guides
