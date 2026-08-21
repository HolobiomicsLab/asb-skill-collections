---
name: resource-capacity-calculation
description: Use when when configuring an OpenMS Streamlit application for online
  deployment with Redis and RQ worker processes, you need to determine how many worker
  processes can safely run in parallel within a Docker container's memory constraint.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - Docker
  - Redis
  - RQ (Redis Queue)
  - Streamlit
  - Python
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/nmeth.3959
  title: OpenMS
evidence_spans: []
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

# resource-capacity-calculation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Calculate the maximum number of parallel worker processes that can be deployed in a containerized task queue system based on available system memory. This skill applies a memory-per-worker overhead formula to determine safe parallelism limits for online (Redis/RQ-based) deployments.

## When to use

When configuring an OpenMS Streamlit application for online deployment with Redis and RQ worker processes, you need to determine how many worker processes can safely run in parallel within a Docker container's memory constraint. This skill is triggered when you know the total available memory (in GB) and need to compute the maximum worker count to avoid out-of-memory errors and ensure stable job queue operation.

## When NOT to use

- Offline/local deployment mode (online_deployment: false) — use multiprocessing.Process instead; the formula applies only to online (Redis/RQ) deployments.
- When the container memory is already determined by external orchestration (Kubernetes, cloud provider) and you cannot adjust it — the formula calculates max_workers given a fixed memory, but does not itself allocate or reserve memory.
- When workflows have highly variable per-task memory requirements not captured by the 1.5GB average — the formula uses a fixed per-worker footprint and does not adapt to task-specific memory spikes.

## Inputs

- available_memory (numeric, in GB): total memory allocated to the Docker container
- deployment_mode (string): 'online' to trigger the formula; offline/local mode uses multiprocessing.Process instead

## Outputs

- max_workers (integer): safe maximum number of RQ worker processes to start
- memory_per_worker (numeric, in GB): per-worker memory footprint (1.5 GB)
- system_overhead (numeric, in GB): reserved non-worker memory (2 GB)

## How to apply

Apply the memory-sizing formula max_workers = (available_memory - 2GB) / 1.5GB, where available_memory is the total container memory allocated in GB. The formula reserves 2GB as baseline system overhead (Redis, Streamlit, OS), then divides remaining memory by 1.5GB per worker, which represents the per-worker memory footprint for OpenMS TOPP workflow execution. Implement this in code as floating-point arithmetic, then floor or round the result to an integer. For containers below 2GB total memory, clamp the result to 0 workers (queue runs but no parallel execution). This formula is specific to the single-container architecture where Redis, RQ workers, and Streamlit all run within one container with no inter-container networking.

## Related tools

- **Docker** (Container runtime; memory limit is set via docker run -m or docker-compose memory constraint, providing the available_memory input to the formula)
- **Redis** (In-memory message broker and queue store; consumes part of the 2GB system overhead reservation)
- **RQ (Redis Queue)** (Python-native task queue; spawns max_workers processes to consume jobs from the queue in online mode) — https://github.com/OpenMS/streamlit-template
- **Streamlit** (Web application framework; consumes part of the 2GB system overhead reservation for the UI and request handling) — https://github.com/OpenMS/streamlit-template
- **Python** (Implementation language for the formula calculation and worker process spawning logic)

## Examples

```
python -c "available_memory = 8; max_workers = int((available_memory - 2) / 1.5); print(f'max_workers = {max_workers}')"
```

## Evaluation signals

- Verify the 8GB container example: substitute available_memory = 8 into the formula, compute (8 - 2) / 1.5 = 6 / 1.5 = 4.0, and confirm max_workers equals 4.
- Test edge case at memory = 2GB: formula returns (2 - 2) / 1.5 = 0, confirming no workers are spawned and queue remains available (jobs enqueue but do not execute).
- Test edge case below memory = 2GB (e.g., 1.5GB): formula returns negative value, clamped to 0, preventing worker spawn and resource exhaustion.
- Deploy the Docker container and monitor memory usage with docker stats; verify that actual memory usage does not exceed the allocated available_memory even under full queue load with max_workers processes.
- Run a test workflow with max_workers processes in parallel and confirm all jobs complete without out-of-memory errors or worker process crashes.

## Limitations

- The formula assumes a fixed 1.5GB per-worker memory footprint, which may underestimate or overestimate for workflows with highly variable or asymmetric memory requirements.
- The 2GB system overhead is a fixed reservation; it does not adapt dynamically if Redis or Streamlit memory usage spikes above baseline.
- The formula does not account for operating system page cache, buffer memory, or other kernel allocations that may reduce available userspace memory.
- No guidance is provided on how to empirically measure or validate the 1.5GB per-worker estimate for custom or domain-specific workflows; the formula is calibrated for OpenMS TOPP tool execution in the template app.
- The single-container architecture means all components (Redis, workers, Streamlit, OS) compete for the same memory pool; no isolation or per-process memory limits are enforced within the container.

## Evidence

- [other] max_workers = (available_memory - 2GB) / 1.5GB with stated example of 8GB container → max 4 workers: "Extract the worker-count formula and example from the methods text: max_workers = (available_memory - 2GB) / 1.5GB with stated example of 8GB container → max 4 workers."
- [readme] All components run within the same Docker container, ensuring identical environments for the web app and worker processes.: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [readme] The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer).: "The existing multiprocessing system remains completely unchanged for offline/local deployments (including the Windows installer)."
- [other] Redis Queue is purely additive and only activates in online Docker deployments.: "Redis queue is purely additive and only activates in online Docker deployments"
