---
name: workflow-context-preservation
description: 'Use when when submitting OpenMS workflows to RQ (Redis Queue) in online Docker mode, you need to preserve the job ID and execution context for recovery after container restarts or worker failures. Apply this skill if: (1) you are using QueueManager.'
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker
  - RQ (Redis Queue)
  - Redis
  - QueueManager
  - Streamlit
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans:
- No code changes required for offline mode. The detection happens automatically
- as well as deployment with docker-compose.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_openms_webapps_cq
    doi: 10.1038/nmeth.3959
    title: OpenMS
  dedup_kept_from: coll_openms_webapps_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/nmeth.3959
  all_source_dois:
  - 10.1038/nmeth.3959
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-context-preservation

## Summary

Preserve workflow execution context and job metadata across distributed queue submissions and worker recoveries by storing and retrieving uniquely-keyed job identifiers and parameters in persistent workflow directories. This skill ensures RQ-based job artifacts remain traceable and recoverable in online Docker deployments.

## When to use

When submitting OpenMS workflows to RQ (Redis Queue) in online Docker mode, you need to preserve the job ID and execution context for recovery after container restarts or worker failures. Apply this skill if: (1) you are using QueueManager.submit_job() to enqueue a workflow, (2) the workflow requires timeout=7200 and result_ttl=86400 lifecycle parameters, and (3) you must ensure the job_id can be recovered from the workflow directory for status polling or cancellation.

## When NOT to use

- Offline mode (online_deployment: false): use multiprocessing.Process instead; Redis/RQ are not active and job persistence via .job_id is unnecessary.
- Redis is unavailable or QueueManager.is_available() returns False: fall back to synchronous or multiprocessing execution; do not attempt to store or recover job IDs.
- Workflow execution is local (non-Docker): job_id persistence is redundant if worker processes are co-located; consider simple in-memory state or file locks instead.

## Inputs

- workflow execution function (callable)
- workflow class name (string)
- workflow module path (string)
- workflow directory path (Path object)
- session workspace name (string)
- params.json file from workflow directory

## Outputs

- job metadata object (job_id, status, submission timestamp)
- .job_id file persisted in workflow directory
- job artifact in RQ queue with unique job_id
- Optional[str] job_id retrieved from .job_id file on recovery

## How to apply

After calling QueueManager.submit_job() with the workflow function, workflow class name, workflow module path, and job timeout/TTL parameters, immediately call QueueManager.store_job_id() to persist the returned job_id as a .job_id file in the workflow directory (e.g., `workflow_dir/.job_id`). Generate the job_id using the pattern `f"workflow-{workflow_dir.name}-{session_workspace_name}"` to ensure uniqueness and traceability. On worker startup or recovery, call QueueManager.load_job_id() to retrieve the persisted job_id from the workflow directory, then use it to query job status via QueueManager.get_job_info(). This two-phase pattern (store on submit, load on recovery) decouples job submission from worker lifecycle and allows stateless RQ workers to resume tracking without re-enqueuing.

## Related tools

- **RQ (Redis Queue)** (Enqueue workflow jobs with unique job_id and lifecycle parameters (timeout=7200, result_ttl=86400); provides job artifact and status tracking) — https://github.com/OpenMS/streamlit-template
- **Redis** (Backing store for RQ queue and job state; runs locally within single Docker container at localhost:6379/0) — https://github.com/OpenMS/streamlit-template
- **QueueManager** (High-level API to submit_job(), store_job_id(), load_job_id(), and get_job_info(); orchestrates context preservation) — https://github.com/OpenMS/streamlit-template
- **Streamlit** (Web application framework that triggers workflow submission via QueueManager in online mode) — https://github.com/OpenMS/streamlit-template
- **Docker** (Single-container runtime ensuring identical environments for web app and RQ worker; enables localhost communication between Redis, RQ worker, and Streamlit) — https://github.com/OpenMS/streamlit-template

## Examples

```
job_id = queue_manager.submit_job(func=workflow_func, args=(), kwargs={'workflow_class': 'MyWorkflow', 'workflow_module': 'module.path'}, timeout=7200, result_ttl=86400); queue_manager.store_job_id(workflow_dir=Path('/workflows/my-workflow'), job_id=job_id); recovered_id = queue_manager.load_job_id(workflow_dir=Path('/workflows/my-workflow'))
```

## Evaluation signals

- Verify .job_id file exists in the workflow directory immediately after QueueManager.submit_job() returns; file content matches the returned job_id string.
- Confirm QueueManager.load_job_id() retrieves the persisted job_id from the .job_id file on subsequent accesses (after container restart or worker recovery).
- Check RQ job artifact in Redis using redis-cli: `redis-cli hgetall job:<job_id>` should return a non-empty hash with job metadata (status, func, args, kwargs, timeout, result_ttl).
- Validate job_id follows the pattern `workflow-{workflow_dir.name}-{session_workspace_name}` (e.g., `workflow-my-workflow-session123`).
- Verify QueueManager.get_job_info(job_id) returns a JobInfo object with non-None status and submission timestamp immediately after store; status should transition from 'queued' to 'started' to 'finished' or 'failed'.

## Limitations

- Job persistence relies on the workflow directory filesystem; if the directory is deleted or moved, the .job_id file is lost and job recovery is impossible.
- Single-container architecture means Redis data is co-located with the app; if the container crashes or is removed without external volume mount, Redis queue state is lost and only the .job_id file remains as a recovery anchor.
- The job_id generation pattern `workflow-{workflow_dir.name}-{session_workspace_name}` assumes unique workspace and workflow directory names; name collisions in the same session could produce duplicate job_ids.
- Timeout (7200 s) and result_ttl (86400 s) are hardcoded; workflows exceeding 2 hours or requiring longer result retention will fail or lose job results before expiration.

## Evidence

- [other] In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique job_id and configures timeout=7200 and result_ttl=86400 parameters for job lifecycle management.: "In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique"
- [other] Call QueueManager.store_job_id() to persist the job ID as a .job_id file in the workflow directory for recovery.: "Call QueueManager.store_job_id() to persist the job ID as a .job_id file in the workflow directory for recovery"
- [other] def store_job_id(self, workflow_dir: Path, job_id: str) -> None: """Store job ID in workflow directory for recovery""": "def store_job_id(self, workflow_dir: Path, job_id: str) -> None: """Store job ID in workflow directory for recovery""""
- [other] def load_job_id(self, workflow_dir: Path) -> Optional[str]: """Load job ID from workflow directory""": "def load_job_id(self, workflow_dir: Path) -> Optional[str]: """Load job ID from workflow directory""""
- [other] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes"
- [other] Redis runs locally within the same container with no container-to-container communication needed: "Redis runs locally within the same container with no container-to-container communication needed"
- [other] f"workflow-{workflow_dir.name}-{session_workspace_name}": "f"workflow-{workflow_dir.name}-{session_workspace_name}""
- [other] The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer).: "The existing multiprocessing system remains completely unchanged for offline/local deployments"
