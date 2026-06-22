---
name: online-mode-environment-detection
description: Use when when deploying an OpenMS streamlit application that must support both local development (offline mode with multiprocessing) and production cloud/HPC environments (online mode with Redis + RQ task queue), and you need to transparently route workflow job submissions to the correct backend.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker
  - RQ (Redis Queue)
  - Redis
  - multiprocessing
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
---

# online-mode-environment-detection

## Summary

Automatically detect and configure the OpenMS streamlit template runtime for online (Docker + Redis/RQ) versus offline (local multiprocessing) deployment modes. This skill enables a single codebase to adapt its job-submission strategy without code changes based on deployment context.

## When to use

When deploying an OpenMS streamlit application that must support both local development (offline mode with multiprocessing) and production cloud/HPC environments (online mode with Redis + RQ task queue), and you need to transparently route workflow job submissions to the correct backend without branching your application code.

## When NOT to use

- When offline-only deployment is guaranteed and you want to eliminate Redis/RQ dependencies entirely — use multiprocessing.Process directly.
- When you require cross-container or distributed job queuing — this skill assumes single-container architecture with Redis and RQ workers co-located in the same Docker image.
- When workflow state must be preserved across container rebuilds — job IDs stored in .job_id files survive container restart, but persisted results depend on external storage, not included here.

## Inputs

- settings.json configuration file (online_deployment boolean flag)
- Redis connection parameters (host, port, database URL)
- Workflow function, class name, and module path
- Workflow directory path (for job_id persistence)

## Outputs

- Mode flag (boolean: online=true, offline=false)
- Job metadata object (job_id, status, submission_timestamp)
- .job_id file persisted in workflow directory

## How to apply

The template performs environment detection by checking a settings flag (online_deployment: true/false in settings.json) and verifying Redis availability via QueueManager.is_available(). In online mode, workflow jobs are submitted to RQ via self._queue.enqueue() with timeout=7200 and result_ttl=86400 parameters; in offline mode, jobs are submitted to multiprocessing.Process without any changes to the workflow or user-facing API. The detection occurs at application startup and is cached; job submission calls then branch transparently based on this cached mode. Store the detected job_id as a .job_id file in the workflow directory for recovery across container restarts.

## Related tools

- **RQ (Redis Queue)** (Task queue backend for online mode job submission; replaces multiprocessing in Docker deployments) — https://github.com/OpenMS/streamlit-template
- **Redis** (In-process message broker and job store for RQ; runs locally within the same container at localhost:6379) — https://github.com/OpenMS/streamlit-template
- **multiprocessing** (Job execution backend for offline mode; remains unchanged and active for local and Windows installer deployments) — https://github.com/OpenMS/streamlit-template
- **Streamlit** (Web framework; runs in foreground as main process; mode detection ensures correct job submission pathway) — https://github.com/OpenMS/streamlit-template
- **Docker** (Container runtime for online mode; entrypoint.sh orchestrates Redis, RQ workers, and Streamlit startup) — https://github.com/OpenMS/streamlit-template

## Evaluation signals

- Verify settings.json online_deployment flag is correctly parsed and cached at application startup (check logs or Streamlit session state).
- Confirm QueueManager.is_available() returns True when Redis is running, False when not; job submission routes accordingly without errors.
- Check that job_id is returned from RQ enqueue response in online mode and persisted to workflow_dir/.job_id; confirm file exists after submission.
- Verify offline mode uses multiprocessing.Process with no Redis/RQ calls; inspect process pool or Streamlit session state for process objects instead of job_id strings.
- Test container restart: load persisted job_id from .job_id file; confirm RQ can query and recover job status using the recovered ID.

## Limitations

- Single-container architecture means no container-to-container communication; suitable for small-to-medium workloads but not for large distributed clusters requiring multiple worker containers.
- Workspace cleanup cron job is automatically skipped in Apptainer/Singularity read-only root filesystems; manual invocation of clean-up-workspaces.py required.
- No automatic failover if Redis becomes unavailable mid-session; application must detect and gracefully degrade or restart.
- Job recovery depends on .job_id file persistence; if workflow directory is ephemeral or deleted, job tracking is lost even if job continues in RQ.

## Evidence

- [other] No code changes required for offline mode. The detection happens automatically: "No code changes required for offline mode. The detection happens automatically"
- [other] Redis queue is purely additive and only activates in online Docker deployments: "Redis queue is purely additive and only activates in online Docker deployments"
- [other] The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer).: "The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer)."
- [other] All communication via localhost: "No networking issues: All communication via localhost"
- [other] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [other] job = self._queue.enqueue( func, args=args, kwargs=kwargs,: "job = self._queue.enqueue( func, args=args, kwargs=kwargs,"
- [other] def store_job_id(self, workflow_dir: Path, job_id: str) -> None: """Store job ID in workflow directory for recovery""": "def store_job_id(self, workflow_dir: Path, job_id: str) -> None: """Store job ID in workflow directory for recovery""""
