---
name: multiprocessing-process-spawning-and-pid-management
description: 'Use when when deploying a Streamlit workflow app in offline mode (online_deployment:
  false) or when Redis is unavailable in online mode, and you need to launch workflows
  as independent background processes while maintaining the ability to track, recover,
  or cancel them later by their PID.'
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - multiprocessing
  - Docker
  - Redis / RQ (Redis Queue)
  - Streamlit
  license_tier: restricted
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans:
- '| **Local** (`online_deployment: false`) | None | `multiprocessing.Process`'
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

# multiprocessing-process-spawning-and-pid-management

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Spawn detached local workflow processes using Python's multiprocessing.Process and persist their process IDs (PIDs) to a file-based registry for later recovery and monitoring. This skill enables offline/local execution of long-running workflows without blocking the Streamlit main thread or requiring external queue infrastructure.

## When to use

When deploying a Streamlit workflow app in offline mode (online_deployment: false) or when Redis is unavailable in online mode, and you need to launch workflows as independent background processes while maintaining the ability to track, recover, or cancel them later by their PID.

## When NOT to use

- When Redis Queue is available and online_deployment: true (use RQ enqueue instead for distributed execution and job tracking).
- When the workflow must complete synchronously before returning control (multiprocessing spawns detached processes; use direct execution if blocking is required).
- On Windows systems where multiprocessing.Process has limited daemon process support and PID persistence may be unreliable across app restarts.

## Inputs

- workflow_class (class object or string reference)
- workflow_module (import path string, e.g., 'workflows.my_workflow')
- workflow_directory (local Path to workspace with input files and parameters)
- online_deployment flag (boolean from settings.json or session state)
- Redis connection status (boolean, from _redis.ping() or equivalent)

## Outputs

- spawned Process object (multiprocessing.Process instance)
- process ID (integer, stored to disk in workflow_dir/process.pid)
- PID file (text file containing the integer PID for recovery)

## How to apply

Check the deployment mode flag (online_deployment from settings.json or session state). If offline or Redis unavailable, spawn a new multiprocessing.Process targeting the workflow_process() method rather than executing it in the Streamlit thread. Create a dedicated PID directory within the workflow workspace and write the spawned process ID to a file (e.g., process.pid) immediately after process creation. The same execution() method logic runs identically in both online and offline paths—only the process spawning mechanism differs. Store the PID persistently so it can be retrieved during session recovery (e.g., if the Streamlit app restarts). Validation requires confirming that in local mode a detached process is spawned (not executed inline), that the PID file is created and readable, and that fallback to multiprocessing occurs gracefully if Redis connectivity fails.

## Related tools

- **multiprocessing** (Process spawning and lifecycle management for local, offline workflow execution)
- **Redis / RQ (Redis Queue)** (Online mode alternative; fallback detection—if Redis unavailable, multiprocessing is triggered) — https://github.com/OpenMS/streamlit-template
- **Streamlit** (Web app framework hosting the workflow dispatcher; multiprocessing decouples long-running tasks from Streamlit's thread) — https://github.com/OpenMS/streamlit-template

## Examples

```
from multiprocessing import Process; from pathlib import Path; workflow_dir = Path('/workspaces/workflow_123'); proc = Process(target=self.workflow_process, kwargs={'workflow_dir': workflow_dir}); proc.start(); Path(workflow_dir, 'process.pid').write_text(str(proc.pid))
```

## Evaluation signals

- Process ID file exists in workflow_dir and contains a valid integer matching the spawned process PID.
- Streamlit UI returns control immediately after workflow submission (non-blocking confirmation) in offline mode.
- Spawned process continues executing after Streamlit session disconnects or app restarts.
- In online mode with Redis available, start_workflow routes to RQ enqueue, not multiprocessing.
- If Redis unavailable in online mode, fallback to multiprocessing.Process occurs without exception and PID is persisted.

## Limitations

- Multiprocessing on Windows exhibits limited daemon process support; PID file recovery may fail across app restarts on Windows.
- No built-in job queue or priority ordering—all processes spawn immediately without queueing.
- Process monitoring and cancellation depend on manual PID file inspection; no centralized job status API like RQ provides.
- Shared file system required between main Streamlit thread and worker process for workspace access; no remote execution possible.

## Evidence

- [other] The dispatch control logic in start_workflow routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false: "The dispatch control logic in start_workflow routes to RQ-queued execution under online_deployment:true and to multiprocessing.Process execution under online_deployment:false"
- [other] Call `_start_workflow_local()` to spawn a `multiprocessing.Process` targeting `self.workflow_process()`, create the PID directory, and write the process ID to a file.: "call `_start_workflow_local()` to spawn a `multiprocessing.Process` targeting `self.workflow_process()`, create the PID directory, and write the process ID to a file"
- [other] The existing multiprocessing system remains completely unchanged for offline/local deployments: "The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer)."
- [other] In both paths, the same `execution()` method logic runs identically—only the process spawning differs.: "In both paths, the same `execution()` method logic runs identically—only the process spawning differs."
- [other] | **Local** (`online_deployment: false`) | None | `multiprocessing.Process`: "| **Local** (`online_deployment: false`) | None | `multiprocessing.Process`"
