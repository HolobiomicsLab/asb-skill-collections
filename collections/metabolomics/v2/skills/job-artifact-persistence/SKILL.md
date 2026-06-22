---
name: job-artifact-persistence
description: Use when when deploying OpenMS workflows in online mode via RQ (Redis Queue) in a Docker container where the Streamlit frontend may restart or rerun without losing track of submitted jobs.
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

# job-artifact-persistence

## Summary

Persist RQ job identifiers to disk so that queued workflow jobs can be recovered and monitored across container restarts or Streamlit reruns. This skill ensures that asynchronous job submissions in online mode do not orphan jobs when the web frontend reconnects.

## When to use

When deploying OpenMS workflows in online mode via RQ (Redis Queue) in a Docker container where the Streamlit frontend may restart or rerun without losing track of submitted jobs. Specifically, apply this skill immediately after enqueuing a job to RQ and before returning control to the user, so the job_id can be reconstructed from disk if the container or session is interrupted.

## When NOT to use

- Offline/local mode using multiprocessing.Process instead of RQ — the multiprocessing system has its own lifecycle and does not require Redis-backed persistence.
- Job execution has already completed and results are stored in Redis with result_ttl — the job_id file is only needed for recovery of in-flight or queued jobs, not for historical lookups of completed results.
- Running workflows synchronously without job queueing — persistence is only relevant when jobs are submitted asynchronously to a remote queue.

## Inputs

- workflow_dir (Path)
- job_id (string, from RQ enqueue response)
- workflow execution function reference
- workflow class name (string)
- workflow module path (string)

## Outputs

- .job_id file (plain text, stored in workflow_dir)
- job metadata object (job_id, status, submission timestamp)
- restored job_id (string, on load from disk)

## How to apply

After calling QueueManager.submit_job() to enqueue a workflow function to RQ with timeout=7200 and result_ttl=86400, capture the returned job ID from the RQ enqueue response. Immediately call QueueManager.store_job_id() to persist the job ID as a .job_id file in the workflow directory (workflow_dir/.job_id). On subsequent reconnections, call QueueManager.load_job_id() to retrieve the persisted job_id from disk and use it to query job status via QueueManager.get_job_info(). This allows the Streamlit app to reconstruct the link between a workspace session and its queued or in-flight job, bridging the gap between stateless frontend reruns and stateful backend execution.

## Related tools

- **RQ (Redis Queue)** (Lightweight Python-native task queue used to enqueue workflow jobs with unique job_id and to manage job lifecycle (timeout=7200, result_ttl=86400))
- **Redis** (Backing store for RQ job artifacts and state; runs locally in the same Docker container at redis://localhost:6379/0)
- **QueueManager** (Abstraction layer that wraps RQ enqueue/dequeue operations and provides store_job_id(), load_job_id(), and get_job_info() methods for persistence and recovery) — github.com/OpenMS/streamlit-template
- **Streamlit** (Web frontend that reruns on user interaction; job_id persistence allows it to survive reruns and reconnect to in-flight jobs in online mode) — github.com/OpenMS/streamlit-template

## Examples

```
job = queue_manager.submit_job(workflow_func, args=(workflow_class, module_path), kwargs={}, timeout=7200, result_ttl=86400, job_id=f"workflow-{workflow_dir.name}-{session_id}"); queue_manager.store_job_id(workflow_dir, job.id); info = queue_manager.load_job_id(workflow_dir)  # recover on rerun
```

## Evaluation signals

- After job submission, .job_id file exists at workflow_dir/.job_id with contents matching the returned RQ job_id.
- On Streamlit rerun or container restart, load_job_id() successfully retrieves the persisted job_id from disk and returns a non-None string.
- QueueManager.get_job_info(restored_job_id) returns a valid JobInfo object with status matching the job's current state in Redis (queued, started, finished, or failed).
- Job submission timestamp and lifecycle parameters (timeout=7200, result_ttl=86400) are preserved and queryable via the restored job_id.
- If Redis or the container is restarted, the job_id can still be loaded from disk and used to query or cancel the job, demonstrating artifact independence from volatile Redis state.

## Limitations

- Requires filesystem write permissions in workflow_dir; will fail silently or raise OSError if the directory is read-only or mounted with no-write constraints.
- If workflow_dir is deleted externally, the persisted .job_id file is lost and the job becomes unrecoverable from this workspace, though the job may still exist in Redis with result_ttl=86400 seconds (24 hours).
- In Apptainer/Singularity HPC mode, the read-only root filesystem is auto-detected and runtime state (including job IDs) is moved to /tmp/openms-runtime-$$, which may not survive across multiple apptainer invocations; manual cleanup of workspaces is required.
- Persistence is only reliable within a single Docker container instance; if the container is destroyed and a new one is started with a fresh Redis instance, persisted job_ids will not resolve to any queued job.

## Evidence

- [other] In online mode, the template submits a workflow job to RQ by calling self._queue.enqueue() with the workflow function, arguments, and keyword arguments, which generates a job artifact with a unique job_id and configures timeout=7200 and result_ttl=86400 parameters for job lifecycle management.: "Call QueueManager.submit_job() with the workflow execution function, workflow class name, workflow module path as kwargs, timeout=7200, result_ttl=86400, and a generated job_id formatted as"
- [other] Job submission and persistence are integrated into the RQ workflow submission interface.: "def store_job_id(self, workflow_dir: Path, job_id: str) -> None:
        """Store job ID in workflow directory for recovery""""
- [other] Job IDs can be loaded from disk on reconnection.: "def load_job_id(self, workflow_dir: Path) -> Optional[str]:
        """Load job ID from workflow directory""""
- [other] Redis runs locally within the same container with no container-to-container communication needed: "All communication via localhost"
- [readme] The template supports recovery of persisted workflow state.: "Workspaces for user data with unique shareable IDs; Persistent parameters and input files within a workspace"
