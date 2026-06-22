---
name: redis-queue-job-submission
description: 'Use when you have an OpenMS workflow ready to execute in online_deployment:true mode with Redis available, and you need to submit it as a queued job artifact rather than blocking the Streamlit thread. Trigger conditions: (1) online_deployment flag is true in settings;'
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - RQ (Redis Queue)
  - Redis
  - Docker
  - Streamlit
  - QueueManager
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans:
- Task Queue | **RQ (Redis Queue)** | Lightweight, Python-native, simpler than Celery
- Redis queue is purely additive and only activates in online Docker deployments
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

# redis-queue-job-submission

## Summary

Submit a workflow execution job to Redis Queue (RQ) with lifecycle parameters (timeout, result TTL) and persist the job ID for asynchronous tracking and recovery in online Docker deployments. This skill enables non-blocking workflow dispatch from a Streamlit web app to background workers while maintaining job state durability.

## When to use

Apply this skill when you have an OpenMS workflow ready to execute in online_deployment:true mode with Redis available, and you need to submit it as a queued job artifact rather than blocking the Streamlit thread. Trigger conditions: (1) online_deployment flag is true in settings; (2) Redis connectivity verified via QueueManager.is_available(); (3) workflow parameters loaded from params.json in the workflow directory; (4) job must survive container restarts or Streamlit reruns.

## When NOT to use

- Offline/local deployment (online_deployment:false): use multiprocessing.Process dispatch instead; RQ submission will fail or be unnecessary.
- Redis is unavailable or unreachable: QueueManager.is_available() returns False; graceful fallback to local multiprocessing should occur.
- Workflow execution is synchronous and must block the caller: RQ queuing is asynchronous; use direct execution (workflow.execution()) if blocking semantics are required.

## Inputs

- online_deployment flag (boolean) from settings.json or Streamlit session state
- workflow directory path (Path object) containing params.json and workflow metadata
- workflow class object (instantiated workflow derived from WorkflowBase)
- workflow module import path (string, e.g. 'workflows.lipid_analysis')
- session workspace name (string, used in job_id construction)

## Outputs

- Job ID (string, formatted as f'workflow-{workflow_dir.name}-{session_workspace_name}')
- .job_id file persisted in workflow directory (text file containing job ID)
- Job metadata object {job_id, status, submission_timestamp} returned to caller
- RQ Job artifact stored in Redis at redis://localhost:6379/0 with timeout and result_ttl parameters

## How to apply

First, verify online deployment mode by reading the online_deployment flag from session state or settings.json, and confirm Redis availability by calling QueueManager.is_available() (internally testing redis-cli ping). Second, instantiate QueueManager and load workflow parameters from params.json in the workflow directory. Third, call QueueManager.submit_job() with: the workflow execution function (workflow.execution), workflow class name, workflow module import path as kwargs, timeout=7200 seconds (2 hours), result_ttl=86400 seconds (24 hours), and a unique job_id formatted as f"workflow-{workflow_dir.name}-{session_workspace_name}". Fourth, capture the returned job ID from the RQ enqueue response. Fifth, persist the job ID by calling QueueManager.store_job_id() to write a .job_id file in the workflow directory, enabling recovery after container restart. Finally, return job metadata (job_id, status, submission timestamp) to the caller for display in the Streamlit UI.

## Related tools

- **RQ (Redis Queue)** (Task queue for asynchronous workflow job submission and lifecycle management (enqueue, timeout, result TTL)) — https://github.com/rq/rq
- **Redis** (In-process key-value store (redis://localhost:6379/0) for job artifact persistence and worker communication within single Docker container)
- **Streamlit** (Web UI framework; QueueManager.submit_job() is called from Streamlit app context to avoid blocking the main thread) — https://github.com/streamlit/streamlit
- **Docker** (Container runtime; single-container architecture runs Streamlit, Redis, RQ worker, and cron all together with localhost communication)
- **QueueManager** (Wrapper class providing submit_job(), store_job_id(), load_job_id(), and is_available() methods for RQ interaction) — https://github.com/OpenMS/streamlit-template

## Examples

```
job = QueueManager().submit_job(func=workflow.execution, workflow_class='LipidAnalysis', workflow_module='workflows.lipid_analysis', timeout=7200, result_ttl=86400, job_id='workflow-lipid_workflow_v1-session_abc123'); QueueManager().store_job_id(workflow_dir=Path('/workspaces/session_abc123/lipid_workflow_v1'), job_id=job.id)
```

## Evaluation signals

- Job ID is successfully stored in Redis at redis://localhost:6379/0 and retrievable via redis-cli GET or RQ job inspection.
- .job_id file exists in the workflow directory after submit_job() returns, and its content matches the returned job_id.
- Job metadata returned to caller contains non-null job_id, status='queued' or 'started', and submission_timestamp in ISO 8601 format.
- RQ job object carries timeout=7200 and result_ttl=86400 parameters (inspectable via rq job inspect <job_id>).
- Job can be recovered after container restart or Streamlit rerun by reading .job_id file and querying QueueManager.get_job_info().

## Limitations

- Single-container architecture means Redis and RQ worker run in the same container as Streamlit; resource contention or worker crashes may block the web app.
- Job submission to RQ does not guarantee execution; if no RQ worker is running (rq worker openms-workflows) the job remains queued indefinitely.
- Job ID format f'workflow-{workflow_dir.name}-{session_workspace_name}' requires unique workspace names; duplicate session names may cause job ID collisions.
- result_ttl=86400 (24 hours) means job results are automatically evicted from Redis after 1 day; long-running workflows may lose result data if not retrieved within this window.
- Fallback to multiprocessing is not automatic if Redis is unavailable during job submission; explicit error handling must check QueueManager.is_available() or catch connection exceptions.

## Evidence

- [other] In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique job_id and configures timeout=7200 and result_ttl=86400 parameters for job lifecycle management.: "In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique"
- [other] Call QueueManager.submit_job() with the workflow execution function, workflow class name, workflow module path as kwargs, timeout=7200, result_ttl=86400, and a generated job_id formatted as f"workflow-{workflow_dir.name}-{session_workspace_name}". Capture the returned job ID from RQ enqueue response. Call QueueManager.store_job_id() to persist the job ID as a .job_id file in the workflow directory for recovery.: "Call QueueManager.submit_job() with the workflow execution function, workflow class name, workflow module path as kwargs, timeout=7200, result_ttl=86400, and a generated job_id formatted as"
- [other] If online mode is true, initialize QueueManager and check Redis availability via _redis.ping(). If queue is available, call _start_workflow_queued() to submit the workflow to the RQ queue at redis://localhost:6379/0 using self._queue.enqueue() with the workflow class name, module, and workflow directory as kwargs, store the returned job ID, and display success feedback.: "If online mode is true, initialize QueueManager and check Redis availability via _redis.ping(). If queue is available, call _start_workflow_queued() to submit the workflow to the RQ queue at"
- [other] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [other] redis-server --daemonize yes: "# Start Redis server in background
    redis-server --daemonize yes"
- [other] rq worker openms-workflows --url redis://localhost:6379/0 &: "# Start RQ worker(s) in background
    rq worker openms-workflows --url redis://localhost:6379/0 &"
