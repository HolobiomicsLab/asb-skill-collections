---
name: conditional-execution-dispatch-routing
description: Use when when you have a Streamlit workflow application that must support both offline (local machine, Windows installer) and online (Docker, cloud) deployment modes, and you need to decide at runtime whether to queue jobs remotely via Redis or spawn local processes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3307
  tools:
  - Docker
  - Redis
  - RQ (Redis Queue)
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

# conditional-execution-dispatch-routing

## Summary

Route workflow execution between distributed (Redis Queue) and local (multiprocessing) backends based on deployment mode, ensuring graceful fallback when remote infrastructure is unavailable. This skill enables a single codebase to scale from local development to cloud-hosted deployments without code changes.

## When to use

When you have a Streamlit workflow application that must support both offline (local machine, Windows installer) and online (Docker, cloud) deployment modes, and you need to decide at runtime whether to queue jobs remotely via Redis or spawn local processes. Apply this skill when `online_deployment` flag in settings indicates the deployment target and you must decide whether Redis is available before committing to a queuing strategy.

## When NOT to use

- Input is a single synchronous function that must complete immediately in the current thread—use conditional dispatch only if you need background execution.
- Redis is the only supported backend (e.g., mandatory cloud-only policy)—this skill is unnecessary if offline fallback is not required.
- Deployment mode is static and known at build time—you can hard-code the routing decision instead of checking flags at runtime.

## Inputs

- Deployment mode flag (`online_deployment: bool` from settings.json or session state)
- Workflow class name (string, qualified module path)
- Workflow directory path (Path object)
- Workflow kwargs (dict: module, workflow_class, workflow_dir)
- Redis connection handle (optional; checked at runtime)

## Outputs

- Job ID (str, returned by `RQ.enqueue()` or None for local mode)
- Process ID (int, written to file in local mode; stored in workflow directory)
- Execution status feedback (user-facing string indicating queued or spawned)
- Workflow execution log (produced by `execution()` method, independent of routing)

## How to apply

Check the `online_deployment` flag from `settings.json` or session state. If `online_deployment: true`, initialize `QueueManager`, attempt to ping Redis via `_redis.ping()` at `redis://localhost:6379/0`, and if successful, call `_start_workflow_queued()` to submit the workflow class name, module, and workflow directory as kwargs to `self._queue.enqueue()`, storing the returned job ID and displaying success feedback. If `online_deployment: false` or Redis is unreachable, call `_start_workflow_local()` to spawn a detached `multiprocessing.Process` targeting `self.workflow_process()`, create the PID directory, and write the process ID to file. In both paths, the identical `execution()` method logic runs—only the process spawning mechanism differs. Validate that online-mode jobs are queued (not executed in the main Streamlit thread), local-mode processes are detached, and multiprocessing gracefully activates if Redis is unreachable.

## Related tools

- **Redis** (Distributed job queue backend for online deployments; receives enqueued workflow tasks at redis://localhost:6379/0 and persists job state)
- **RQ (Redis Queue)** (Lightweight Python task queue used to enqueue workflow jobs and retrieve job IDs in online mode; selected over Celery for simpler configuration)
- **multiprocessing** (Local process spawning backend for offline deployments; creates detached workflow processes when Redis is unavailable or online_deployment is false)
- **Streamlit** (Web application framework hosting the dispatch logic; manages session state flags and user feedback display) — https://github.com/OpenMS/streamlit-template
- **Docker** (Container runtime that encapsulates all components (Streamlit, Redis, RQ worker, cron) in a single container to avoid container-to-container networking) — https://github.com/OpenMS/streamlit-template

## Examples

```
# Check deployment mode and route:
if settings.get('online_deployment', False):
    queue_mgr = QueueManager()
    if queue_mgr._redis.ping():
        job = queue_mgr._queue.enqueue('openms_workflows.MyWorkflow', kwargs={'workflow_dir': '/workspaces/ws123'})
    else:
        multiprocessing.Process(target=workflow_process, kwargs={'workflow_dir': '/workspaces/ws123'}).start()
else:
    multiprocessing.Process(target=workflow_process, kwargs={'workflow_dir': '/workspaces/ws123'}).start()
```

## Evaluation signals

- In online mode with Redis available: job is queued (call to `self._queue.enqueue()` succeeds, job ID is stored, execution does NOT occur in main Streamlit thread)
- In offline mode or when Redis is unreachable: `multiprocessing.Process` is spawned, PID file is written to disk, and `_start_workflow_local()` completes without raising an exception
- Graceful fallback occurs: when online_deployment is true but `_redis.ping()` fails, system automatically falls back to multiprocessing without user intervention
- Execution logic is identical in both paths: the same `workflow.execution()` method runs identically; only the process lifecycle differs (queued vs. spawned)
- Job recovery works: job ID stored in workflow directory can be retrieved and monitored via `load_job_id()` in subsequent sessions

## Limitations

- Redis is deployed locally within the same container; this architecture assumes single-container deployments and does not support multi-container distributed Redis setups without code refactoring
- Fallback from online to local mode is silent (no warning log); operators may not notice when Redis is unavailable if monitoring is absent
- Multiprocessing on Windows requires careful handling of entry points; the Windows installer falls back to multiprocessing but cross-platform testing of spawn behavior is required
- Job progress tracking and cancellation via `update_job_progress()` and `cancel_job()` are implemented for RQ but not for multiprocessing-spawned processes, creating API asymmetry

## Evidence

- [other] The dispatch control logic routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false, with the existing multiprocessing system remaining completely unchanged for offline/local deployments.: "routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false, with the existing multiprocessing system remaining completely"
- [other] If online mode is true, initialize QueueManager and check Redis availability via _redis.ping(). If queue is available, call _start_workflow_queued() to submit the workflow to the RQ queue at redis://localhost:6379/0 using self._queue.enqueue() with the workflow class name, module, and workflow directory as kwargs.: "initialize QueueManager and check Redis availability via _redis.ping(). If queue is available, call _start_workflow_queued() to submit the workflow to the RQ queue at redis://localhost:6379/0 using"
- [other] Otherwise (offline mode or Redis unavailable), call _start_workflow_local() to spawn a multiprocessing.Process targeting self.workflow_process(), create the PID directory, and write the process ID to a file.: "call _start_workflow_local() to spawn a multiprocessing.Process targeting self.workflow_process(), create the PID directory, and write the process ID to a file"
- [other] In both paths, the same execution() method logic runs identically—only the process spawning differs.: "In both paths, the same execution() method logic runs identically—only the process spawning differs"
- [readme] Redis Queue is purely additive and only activates in online Docker deployments; the existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer).: "Redis queue is purely additive and only activates in online Docker deployments; the existing multiprocessing system remains completely unchanged for offline/local deployments"
- [readme] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes"
