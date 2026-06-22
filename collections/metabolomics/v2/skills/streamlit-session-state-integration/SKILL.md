---
name: streamlit-session-state-integration
description: Use when when building a Streamlit web application that must coordinate stateful workflow execution across multiple reruns triggered by user interactions (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Streamlit
  - Docker
  - Redis Queue (RQ)
  - multiprocessing
  - settings.json
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans:
- OpenMS Streamlit Template's **online mode only**
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

# streamlit-session-state-integration

## Summary

Integrate Streamlit session state to persist workflow configuration, deployment mode flags, and user parameters across reruns, enabling stateful control of dual-mode execution (online vs. local) without losing context between widget interactions.

## When to use

When building a Streamlit web application that must coordinate stateful workflow execution across multiple reruns triggered by user interactions (e.g., parameter changes, file uploads, button clicks), and where deployment mode, job IDs, workspace paths, or execution status must be retrieved consistently without repeated computation or Redis/database queries.

## When NOT to use

- Input workflow parameters are stateless or single-shot (no multi-step interaction); use simple variables instead.
- Deployment mode is static and never changes during app lifetime; hardcoding the flag in settings.json suffices.
- Execution state (job IDs, PIDs) are guaranteed to persist in external storage (e.g., database, Redis); session state is ephemeral and will be lost if the Streamlit server restarts.

## Inputs

- Streamlit app context (st) with active session
- User-provided workflow parameters (dict or form inputs)
- Deployment configuration flag (online_deployment: bool from settings.json or session state)
- Workflow class name, module path, and workflow directory (strings)
- Optional: job ID or process PID from prior execution stored in session state

## Outputs

- Populated st.session_state dict with deployment mode, job ID, process PID, workflow metadata, and execution status
- Streamlit rerun signal (implicit, via widget interaction) that uses updated session state
- Display feedback (success/error messages) rendered to the user on next rerun

## How to apply

Store deployment configuration (e.g., `online_deployment` flag), workflow metadata (class name, module, directory), and execution state (job IDs, process PIDs, progress) in Streamlit's `st.session_state` dictionary at app initialization or after each execution event. At the start of each rerun, check `session_state` for the `online_deployment` flag to determine whether to route through RQ-queued execution (online) or multiprocessing.Process (local); if the flag is absent or falsy, default to offline mode and spawn a detached multiprocessing process. Store returned job IDs or process PIDs in session state immediately after submission so that subsequent reruns (triggered by user polls for status or progress) can retrieve and display execution state without resubmitting. Use `st.session_state` as the single source of truth for mode selection and execution metadata, eliminating repeated reads from `settings.json` and reducing latency in status checks.

## Related tools

- **Streamlit** (Web framework providing session_state context for persisting widget values and workflow metadata across reruns) — https://github.com/OpenMS/streamlit-template
- **Redis Queue (RQ)** (Job queue backend; job IDs returned from queued submissions are stored in session_state for status polling in online mode) — https://github.com/OpenMS/streamlit-template
- **multiprocessing** (Process spawning in offline/local mode; process IDs are stored in session_state for tracking and recovery) — https://github.com/OpenMS/streamlit-template
- **settings.json** (Source of truth for online_deployment flag and other app configuration; read once and cached in session_state to avoid repeated file I/O) — https://github.com/OpenMS/streamlit-template

## Examples

```
# In Streamlit app.py, initialize and read deployment mode from session state:
if 'online_deployment' not in st.session_state:
    settings = json.load(open('settings.json'))
    st.session_state.online_deployment = settings.get('online_deployment', False)
if st.session_state.online_deployment:
    job = queue_manager.enqueue(workflow_class, **kwargs)
    st.session_state.job_id = job.id
else:
    proc = multiprocessing.Process(target=workflow.execution)
    proc.start()
    st.session_state.process_pid = proc.pid
```

## Evaluation signals

- Session state contains `online_deployment` flag and matches the value read from settings.json at app startup.
- After workflow submission, session_state['job_id'] (online) or session_state['process_pid'] (local) is populated with a non-empty, unique identifier.
- Across consecutive reruns triggered by user interactions, the stored job ID or PID persists in session_state without being reset or resubmitted.
- Status queries (e.g., checking job progress or process state) retrieve the ID from session_state and do not resubmit the workflow.
- When deployment mode flag changes (e.g., from online to offline), the control logic in start_workflow correctly routes to the new execution path on the next rerun.

## Limitations

- Session state is ephemeral and lost when the Streamlit server restarts or the user closes the browser tab; long-running workflows must also store job IDs / PIDs in persistent storage (e.g., workflow directory, Redis) for recovery.
- Session state is not shared across multiple concurrent users; each user gets an isolated session, so shared coordination of workflows across users requires external state management.
- In Docker deployments with multiple Streamlit replicas, session state is not replicated across containers; for stateful workflows in load-balanced setups, use Redis or a shared volume.

## Evidence

- [other] Check deployment mode by reading `online_deployment` flag from settings in session state or `settings.json`.: "Check deployment mode by reading `online_deployment` flag from settings in session state or `settings.json`"
- [other] If online mode is true, initialize `QueueManager` and check Redis availability; if queue is available, call `_start_workflow_queued()` to submit the workflow to the RQ queue and store the returned job ID.: "If online mode is true, initialize `QueueManager` and check Redis availability via `_redis.ping()`. If queue is available, call `_start_workflow_queued()` to submit the workflow to the RQ queue at"
- [other] In both online and local paths, the same `execution()` method logic runs identically—only the process spawning differs.: "In both paths, the same `execution()` method logic runs identically—only the process spawning differs"
- [other] No code changes required for offline mode. The detection happens automatically.: "No code changes required for offline mode. The detection happens automatically"
