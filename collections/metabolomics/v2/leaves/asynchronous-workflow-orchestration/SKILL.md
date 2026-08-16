---
name: asynchronous-workflow-orchestration
description: Use when when you have a Streamlit-based scientific application (e.g.
  OpenMS workflows) that must support both online Docker deployments with multiple
  worker processes and offline local deployments, and you need to prevent long-running
  analyses from blocking the web UI thread.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3674
  tools:
  - Docker
  - RQ (Redis Queue)
  - Redis
  - multiprocessing
  - Streamlit
  - Docker / docker-compose
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

# asynchronous-workflow-orchestration

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Route scientific workflow execution between Redis Queue (online) and multiprocessing (offline) based on deployment mode, enabling non-blocking job submission in Streamlit web applications while maintaining identical execution logic across both paths. This skill decouples the web UI from long-running OpenMS analyses by selecting the appropriate task queue backend automatically.

## When to use

When you have a Streamlit-based scientific application (e.g. OpenMS workflows) that must support both online Docker deployments with multiple worker processes and offline local deployments, and you need to prevent long-running analyses from blocking the web UI thread. Specifically, use this skill when start_workflow() is called and you need to decide whether to queue the job remotely or spawn it locally.

## When NOT to use

- When the workflow is simple enough to execute synchronously within the Streamlit session without blocking the UI (use this skill only for long-running or parallelizable workflows).
- When Redis is required but unavailable and you cannot tolerate fallback to multiprocessing (online-only deployments must verify Redis connectivity before attempting online_deployment: true).
- When the workflow state or intermediate results must be immediately accessible in the same Python process (asynchronous dispatch prevents direct in-process state inspection; use result polling or callback mechanisms instead).

## Inputs

- online_deployment flag (boolean from settings.json or Streamlit session state)
- workflow class name (string, e.g. 'MyWorkflow')
- workflow module path (string, e.g. 'workflows.my_workflow')
- workflow directory path (Path object pointing to workspace)
- workflow parameters and input files (via workspace)

## Outputs

- job ID (string, returned from Redis queue or process ID from multiprocessing)
- execution status feedback (Streamlit UI message indicating queued vs. spawned)
- PID file (for local mode, written to workflow directory)
- RQ job metadata (for online mode, stored in Redis at queue)

## How to apply

First, read the `online_deployment` flag from `settings.json` or session state to determine the deployment mode. If online mode is true, initialize a QueueManager, check Redis availability via `redis-cli ping()` at `redis://localhost:6379/0`, and if available, call `_start_workflow_queued()` to submit the workflow to the RQ queue using `self._queue.enqueue()` with workflow class name, module, and workflow directory as kwargs; store and return the job ID. If offline mode or Redis is unreachable, call `_start_workflow_local()` to spawn a `multiprocessing.Process` targeting `self.workflow_process()`, create the PID directory, and write the process ID to a file. The critical insight is that both paths invoke the same `execution()` method logic identically—only the process spawning mechanism differs. This preserves the entire existing multiprocessing system for offline deployments without modification.

## Related tools

- **RQ (Redis Queue)** (Lightweight Python-native task queue for online mode job submission and worker coordination; stores queued workflows and job metadata at redis://localhost:6379/0) — https://github.com/OpenMS/streamlit-template
- **Redis** (In-memory data store and message broker for RQ; runs locally within the same Docker container (no container-to-container networking) and is checked via ping() before queue submission) — https://github.com/OpenMS/streamlit-template
- **multiprocessing** (Process spawning mechanism for offline mode; creates detached Process instances targeting workflow_process() and writes PID to file for local workflow execution without changes to existing system) — https://github.com/OpenMS/streamlit-template
- **Streamlit** (Web application framework hosting the UI and start_workflow() entry point; orchestration ensures the main Streamlit thread is never blocked by long-running analyses) — https://github.com/OpenMS/streamlit-template
- **Docker / docker-compose** (Deployment environment for online mode; all components (Streamlit, Redis, RQ worker) run in a single container, ensuring identical environments and localhost communication) — https://github.com/OpenMS/streamlit-template

## Examples

```
# In Streamlit callback, after user submits workflow form:
if st.session_state.get('online_deployment', False):
    job_id = workflow_manager.start_workflow(workflow_class='MyWorkflow', workflow_module='workflows.my_workflow', workflow_dir=workspace_path)
    st.success(f'Job queued: {job_id}')
else:
    pid = workflow_manager.start_workflow(workflow_class='MyWorkflow', workflow_module='workflows.my_workflow', workflow_dir=workspace_path)
    st.success(f'Local process spawned: PID {pid}')
```

## Evaluation signals

- In online mode: verify that the job is queued (stored in Redis) and not executed immediately in the main Streamlit thread; check via `rq info` or Redis CLI that the job appears in the queue.
- In offline mode: verify that a detached multiprocessing.Process is spawned (not blocking the Streamlit thread) and that the PID is written to a file in the workflow directory.
- Fallback behavior: confirm that if Redis is unreachable in online mode, execution gracefully falls back to multiprocessing without raising an exception or requiring manual intervention.
- Execution identity: confirm that the same `execution()` method logic runs in both paths by inspecting workflow output, logs, and results—the only difference should be process spawning, not workflow behavior.
- State consistency: verify that the job ID or PID can be recovered from the workflow directory and used to poll job status, retrieve results, or cancel execution post-submission.

## Limitations

- Single-container architecture means Redis, RQ workers, and Streamlit share the same container resources; if one fails (e.g. Redis crashes), the entire deployment is affected. No cross-container isolation.
- The existing multiprocessing system for offline mode is unchanged, which preserves backward compatibility but also preserves any concurrency limitations or platform-specific issues (e.g. Windows multiprocessing behavior differs from Unix).
- Fallback from online to offline mode occurs silently if Redis is unreachable; this can mask infrastructure issues in production (offline mode may appear to work but use local resources instead of distributed queuing).
- Job recovery and persistence: in multiprocessing mode, PID files may become stale if processes are killed externally; RQ jobs in Redis are lost if the container restarts without persistent Redis configuration.

## Evidence

- [other] The dispatch control logic in start_workflow routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false, with the existing multiprocessing system remaining completely unchanged for offline/local deployments.: "The dispatch control logic in start_workflow routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false, with the existing"
- [other] Check deployment mode by reading `online_deployment` flag from settings in session state or `settings.json`. If online mode is true, initialize `QueueManager` and check Redis availability via `_redis.ping()`. If queue is available, call `_start_workflow_queued()` to submit the workflow to the RQ queue at `redis://localhost:6379/0` using `self._queue.enqueue()` with the workflow class name, module, and workflow directory as kwargs, store the returned job ID, and display success feedback.: "Check deployment mode by reading `online_deployment` flag from settings in session state or `settings.json`. If online mode is true, initialize `QueueManager` and check Redis availability via"
- [other] In both paths, the same `execution()` method logic runs identically—only the process spawning differs.: "In both paths, the same `execution()` method logic runs identically—only the process spawning differs."
- [readme] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [other] Redis queue is purely additive and only activates in online Docker deployments. No code changes required for offline mode. The detection happens automatically.: "Redis queue is purely additive and only activates in online Docker deployments. No code changes required for offline mode. The detection happens automatically."
