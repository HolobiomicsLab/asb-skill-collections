---
name: python-job-metadata-serialization
description: Use when implementing online task queue deployments (RQ + Redis) where job execution may outlive the originating web session, or where workers may restart unexpectedly.
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

# Serialize and recover job metadata in Python task queue workflows

## Summary

Persist and retrieve job identifiers and metadata (job_id, status, submission timestamp) from the filesystem to enable job recovery and status tracking in distributed RQ (Redis Queue) task execution pipelines. This skill is essential for maintaining job state across worker process restarts and providing users with queryable job history.

## When to use

Apply this skill when implementing online task queue deployments (RQ + Redis) where job execution may outlive the originating web session, or where workers may restart unexpectedly. Specifically, use this when you need to (1) generate a uniquely-keyed job artifact with deterministic naming, (2) persist the job ID to disk immediately after enqueue for recovery, and (3) reload job metadata on subsequent requests to report status and results to end users.

## When NOT to use

- Local/offline deployments using multiprocessing.Process—use in-memory job tracking instead; the template's multiprocessing backend has no Redis and does not require filesystem persistence.
- Synchronous or blocking workflow execution—this skill is designed for asynchronous queue submissions where the caller does not block waiting for job completion.
- Ephemeral single-shot batch jobs with no user-facing status reporting—serialization overhead is unnecessary if job artifacts are discarded immediately after completion.

## Inputs

- Workflow directory path (Path object or string)
- Workflow execution function (callable)
- Workflow class name (str)
- Workflow module path (str)
- Session workspace identifier (str)
- Job enqueue response from RQ (Job object with job_id attribute)

## Outputs

- Job metadata object with fields: job_id (str), status (str), submission_timestamp (datetime)
- .job_id file persisted in workflow directory (text file containing job ID)
- JobInfo dict/object with job_id, status, created_at, started_at, ended_at, result, exc_info

## How to apply

After calling QueueManager.enqueue() with timeout=7200 and result_ttl=86400 parameters, immediately serialize the returned job ID using QueueManager.store_job_id() to write a .job_id file in the workflow directory. Use a deterministic job_id format (e.g., f'workflow-{workflow_dir.name}-{session_workspace_name}') to enable idempotent lookups. On subsequent queries, call QueueManager.load_job_id() to retrieve the persisted job ID from the workflow directory, then use QueueManager.get_job_info() to fetch current job status (queued, started, finished, failed) and construct a metadata response object containing job_id, status, and submission timestamp. This pattern ensures job recovery even if the RQ worker or Redis connection is temporarily unavailable—the filesystem-resident .job_id file serves as a durable reference to query Redis asynchronously.

## Related tools

- **RQ (Redis Queue)** (Task queue backend that accepts enqueued jobs, assigns unique job_id, stores job state in Redis, and returns Job objects with metadata) — https://github.com/rq/rq
- **Redis** (In-memory data store that persists job state, queue membership, and results; enables QueueManager to retrieve job status and result_ttl configuration)
- **QueueManager** (Python class wrapper providing enqueue(), store_job_id(), load_job_id(), get_job_info(), and cancel_job() methods; abstracts RQ and filesystem I/O) — https://github.com/OpenMS/streamlit-template
- **Streamlit** (Web framework that calls QueueManager methods on user interaction (workflow submission) and polls load_job_id()/get_job_info() to render status updates) — https://github.com/OpenMS/streamlit-template
- **Docker** (Container runtime ensuring single-container architecture where Redis, RQ worker, and Streamlit run in the same process namespace with localhost communication)

## Examples

```
job_id = queue_manager.submit_job(func=workflow.execution, args=(workflow_dir,), kwargs={'workflow_class': 'MyWorkflow', 'workflow_module': 'myapp.workflows'}, timeout=7200, result_ttl=86400); queue_manager.store_job_id(workflow_dir, job_id); metadata = queue_manager.get_job_info(job_id); print(f"Job {metadata.job_id} status: {metadata.status}")
```

## Evaluation signals

- Verify .job_id file exists in the workflow directory after enqueue, contains a non-empty job ID string matching the RQ Job.job_id returned from enqueue().
- Call load_job_id() on the workflow directory and confirm it returns the same job ID that was stored—indicates idempotent persistence and retrieval.
- Query Redis (via get_job_info()) for the persisted job ID and confirm a JobInfo object with status in {queued, started, finished, failed} is returned—indicates RQ backend is tracking the job.
- After job completion, verify that submission_timestamp, created_at, started_at, and ended_at are all present and in chronological order in the metadata object.
- Simulate worker restart (stop RQ worker, reload Streamlit session) and confirm load_job_id() still retrieves the job ID and get_job_info() returns the final job status—validates durability.

## Limitations

- Relies on filesystem durability; if the workflow directory is deleted or mounted on a volatile filesystem, the .job_id file is lost and job recovery fails. Use a durable volume in Docker deployments.
- Job metadata on Redis expires after result_ttl=86400 (24 hours); queries for old job IDs will return None if the TTL has elapsed, even if the .job_id file persists on disk.
- Does not handle job_id collisions if two workflows with identical directory names and session IDs are submitted concurrently; consider adding a UUID suffix to the format string for multi-tenant scenarios.
- Single-container architecture (Redis, RQ worker, Streamlit in one container) does not scale to multiple workers; for horizontal scaling, migrate to multi-container or Kubernetes with shared Redis.
- No automatic cleanup of stale .job_id files; the template includes a separate cron job (clean-up-workspaces.py) for workspace pruning, but must be manually invoked or scheduled.

## Evidence

- [other] In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique job_id and configures timeout=7200 and result_ttl=86400 parameters for job lifecycle management.: "In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique"
- [other] Call QueueManager.submit_job() with the workflow execution function, workflow class name, workflow module path as kwargs, timeout=7200, result_ttl=86400, and a generated job_id formatted as f'workflow-{workflow_dir.name}-{session_workspace_name}'. Capture the returned job ID from RQ enqueue response. Call QueueManager.store_job_id() to persist the job ID as a .job_id file in the workflow directory for recovery. Return the job metadata object (job_id, status, submission timestamp) to the caller.: "Call QueueManager.store_job_id() to persist the job ID as a .job_id file in the workflow directory for recovery. Return the job metadata object (job_id, status, submission timestamp) to the caller."
- [other] def store_job_id(self, workflow_dir: Path, job_id: str) -> None: """Store job ID in workflow directory for recovery""": "def store_job_id(self, workflow_dir: Path, job_id: str) -> None:
        """Store job ID in workflow directory for recovery""""
- [other] def load_job_id(self, workflow_dir: Path) -> Optional[str]: """Load job ID from workflow directory""": "def load_job_id(self, workflow_dir: Path) -> Optional[str]:
        """Load job ID from workflow directory""""
- [other] def get_job_info(self, job_id: str) -> Optional[JobInfo]: """Get information about a job""": "def get_job_info(self, job_id: str) -> Optional[JobInfo]:
        """Get information about a job""""
- [other] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [other] The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer).: "The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer)."
