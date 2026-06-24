---
name: deployment-mode-detection-and-fallback-logic
description: Use when building a Streamlit application that must support both cloud
  deployments (with Redis task queuing) and local/offline execution (with multiprocessing),
  and you need to automatically select the execution path without requiring separate
  code paths or manual configuration switches at runtime.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker
  - Redis
  - RQ (Redis Queue)
  - multiprocessing
  - Streamlit
  license_tier: restricted
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# deployment-mode-detection-and-fallback-logic

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detect the active deployment mode (online vs. offline) from configuration and conditionally route workflow execution to either a Redis Queue for distributed execution or local multiprocessing, with transparent fallback if Redis becomes unavailable. This ensures a single codebase supports both cloud-deployed and local execution without code branching.

## When to use

Apply this skill when building a Streamlit application that must support both cloud deployments (with Redis task queuing) and local/offline execution (with multiprocessing), and you need to automatically select the execution path without requiring separate code paths or manual configuration switches at runtime.

## When NOT to use

- Your application only runs in a single deployment mode and does not need to support both online and offline execution—use direct RQ or direct multiprocessing instead.
- Workflow execution is synchronous and must complete before returning to the caller—this skill is designed for asynchronous/background execution only.
- You require guaranteed message delivery and persistence beyond a single Docker container—this architecture assumes Redis and workers colocate in the same container.

## Inputs

- settings.json file with `online_deployment` boolean flag
- session state or runtime configuration
- workflow class name (string)
- workflow module name (string)
- workflow directory path (Path object)
- Redis server endpoint (default: redis://localhost:6379/0)

## Outputs

- job ID (string) if queued to Redis, or process ID (int) if spawned locally
- job metadata stored in workflow directory (for recovery)
- execution initiated via either QueueManager or multiprocessing.Process

## How to apply

Read the `online_deployment` boolean flag from `settings.json` or session state to determine the deployment mode. If online mode is enabled, initialize a `QueueManager` and attempt to ping Redis at `redis://localhost:6379/0` via `_redis.ping()`. If Redis is available, call `_start_workflow_queued()` to submit the workflow to the RQ queue using `self._queue.enqueue()` with workflow class name, module, and directory as kwargs; store and track the returned job ID. If offline mode is active or Redis ping fails, gracefully fall back to `_start_workflow_local()`, which spawns a `multiprocessing.Process` targeting `self.workflow_process()` and writes the process ID to a file in the workspace. In both branches, the downstream `execution()` method logic runs identically—only process spawning differs. This design ensures zero code duplication in the actual workflow logic while cleanly separating transport concerns.

## Related tools

- **Redis** (In-memory message broker and task queue backend for online deployments; availability is checked at runtime to determine feasibility of queued execution.)
- **RQ (Redis Queue)** (Lightweight Python task queue used to enqueue workflows in online mode; workflows are submitted with `self._queue.enqueue()` and tracked by job ID.)
- **multiprocessing** (Standard library process spawning mechanism used to launch workflows locally in offline mode; `multiprocessing.Process` is created with `self.workflow_process()` as the target.)
- **Streamlit** (Web framework hosting the application; deployment mode flag is read from Streamlit session state or settings.) — https://github.com/OpenMS/streamlit-template
- **Docker** (Containerization platform that enables single-container architecture where Redis, RQ worker, and Streamlit all coexist, ensuring all components use localhost for communication.) — https://github.com/OpenMS/streamlit-template

## Evaluation signals

- In online mode with Redis available, verify that the workflow is queued (not executed immediately in the main Streamlit thread) by checking that `self._queue.enqueue()` is called and a job ID is returned.
- In offline mode or when Redis is unreachable, verify that a `multiprocessing.Process` is spawned (not queued) and a PID file is written to the workspace directory.
- Confirm graceful fallback: if online_deployment is true but `_redis.ping()` fails, execution should automatically fall back to `_start_workflow_local()` without raising an exception.
- Verify that the same downstream `execution()` method logic runs identically in both code paths by checking for no conditional logic inside `execution()` based on deployment mode.
- Monitor that in offline mode multiprocessing process remains detached and does not block the main Streamlit application thread.

## Limitations

- The existing multiprocessing system remains completely unchanged for offline/local deployments, including the Windows installer; no new features or optimizations apply to the local path.
- Redis connection failures trigger silent fallback to multiprocessing; no explicit user warning is shown if online mode was requested but Redis is unavailable.
- Single-container architecture limits horizontal scaling: Redis runs locally within the same container with no container-to-container communication, so this pattern does not support multi-container orchestration.
- Job recovery and persistence rely on storing job IDs in the workflow directory; if the directory is deleted or inaccessible, job tracking is lost.

## Evidence

- [other] The dispatch control logic in start_workflow routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false, with the existing multiprocessing system remaining completely unchanged for offline/local deployments.: "routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false, with the existing multiprocessing system remaining completely"
- [other] Check deployment mode by reading `online_deployment` flag from settings in session state or `settings.json`. If online mode is true, initialize `QueueManager` and check Redis availability via `_redis.ping()`. If queue is available, call `_start_workflow_queued()` to submit the workflow to the RQ queue at `redis://localhost:6379/0` using `self._queue.enqueue()` with the workflow class name, module, and workflow directory as kwargs, store the returned job ID, and display success feedback. Otherwise (offline mode or Redis unavailable), call `_start_workflow_local()` to spawn a `multiprocessing.Process` targeting `self.workflow_process()`, create the PID directory, and write the process ID to a file.: "Check deployment mode by reading `online_deployment` flag from settings in session state or `settings.json`. If online mode is true, initialize `QueueManager` and check Redis availability via"
- [other] No code changes required for offline mode. The detection happens automatically: "No code changes required for offline mode. The detection happens automatically"
- [other] In both paths, the same `execution()` method logic runs identically—only the process spawning differs.: "In both paths, the same `execution()` method logic runs identically—only the process spawning differs."
- [other] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [other] Redis queue is purely additive and only activates in online Docker deployments: "Redis queue is purely additive and only activates in online Docker deployments"
