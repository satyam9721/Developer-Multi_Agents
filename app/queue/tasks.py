import asyncio
from app.orchestration.checkpoints import checkpoint_manager
from app.queue.celery import celery_app
from app.utils.logger import logger
from app.workflows.software import software_workflow

@celery_app.task(name="run_software_workflow")
def run_software_workflow_task(task_id: str) -> dict:
    """Celery background worker task wrapper for running software workflow."""
    logger.info(f"Celery executing software workflow for task {task_id}")
    state = checkpoint_manager.load_checkpoint(task_id)
    if not state:
        logger.error(f"Task state {task_id} not found for Celery execution.")
        return {"status": "error", "error": "Task not found"}

    loop = asyncio.get_event_loop()
    updated_state = loop.run_until_complete(
        software_workflow.execute(state.user_request, state.repository)
    )
    return {"status": "success", "task_status": updated_state.status}
