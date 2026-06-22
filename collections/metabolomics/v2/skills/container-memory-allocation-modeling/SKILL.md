---
name: container-memory-allocation-modeling
description: Use when when configuring a multi-worker online deployment of a containerized Streamlit application (e.g., OpenMS workflows using RQ workers), you need to determine how many RQ worker processes can safely run in a single container given available RAM.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - RQ (Redis Queue)
  - Redis
  - Docker
  - Python
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
---

# container-memory-allocation-modeling

## Summary

Model and validate the maximum worker count for parallel task execution in a containerized application by applying a documented memory-sizing formula and verifying it against known test cases. This skill is essential for tuning online (Redis/RQ-based) deployments to avoid memory exhaustion while maximizing throughput.

## When to use

When configuring a multi-worker online deployment of a containerized Streamlit application (e.g., OpenMS workflows using RQ workers), you need to determine how many RQ worker processes can safely run in a single container given available RAM. Apply this skill before spinning up production containers to prevent out-of-memory crashes and ensure predictable scaling.

## When NOT to use

- Offline/local deployments using multiprocessing.Process instead of RQ — the formula is specific to online Docker mode with Redis queue and should not be applied to offline deployments, which do not use the same memory model.
- Single-worker or development environments — if you are running a single Streamlit instance without parallel workers, memory allocation is not determined by this formula.
- Non-OpenMS or non-RQ-based task queues — the formula is calibrated for RQ worker memory footprint (1.5GB per worker) and may not apply to Celery or other queue systems.

## Inputs

- available_memory (GB): float — total RAM available in the target Docker container
- reference_test_case (optional): known memory-to-worker mapping (e.g., 8GB → 4 workers) for validation

## Outputs

- max_workers: integer — maximum safe RQ worker process count for the container
- verification_report: document or log — test results and formula validation summary

## How to apply

Extract the worker-count memory formula from deployment documentation: max_workers = (available_memory - 2GB) / 1.5GB. Implement this as a Python function that accepts available_memory in GB as a floating-point input and returns the maximum safe worker count. Validate the formula against the reference example: 8GB container should yield 4 workers (verified by computing (8 - 2) / 1.5 = 4.0). Test boundary conditions: memory ≤ 2GB should clamp to 0 workers (no workers can run), 2GB exactly yields 0, and values like 5.5GB yield 2.4 (round or floor as per deployment policy). Generate a verification report documenting all test cases and confirming the 8GB example produces exactly 4 workers before applying the formula to your target container size.

## Related tools

- **RQ (Redis Queue)** (Task queue in which workers execute enqueued OpenMS workflow jobs; memory footprint (1.5GB per worker) is the basis of the sizing formula) — https://github.com/OpenMS/streamlit-template
- **Redis** (In-process message broker and job store for RQ; runs locally within the container; memory overhead (~2GB reserved) is subtracted in the formula) — https://github.com/OpenMS/streamlit-template
- **Docker** (Container runtime; available_memory is the total RAM allocated to the container via docker run -m or docker-compose memory limit) — https://github.com/OpenMS/streamlit-template
- **Python** (Language for implementing the formula calculation function and validation test suite)

## Examples

```
python -c "available_memory = 8.0; max_workers = int((available_memory - 2) / 1.5); print(f'Max workers for {available_memory}GB: {max_workers}')"
```

## Evaluation signals

- Formula implementation correctly computes (available_memory - 2GB) / 1.5GB with floating-point arithmetic and produces 4.0 for the 8GB reference example.
- Edge-case test passes: memory values ≤ 2GB return 0 workers (no negative workers); memory = 2GB exactly returns 0; memory = 5.5GB returns 2.4 or floor(2.4) = 2 depending on rounding policy.
- Verification report documents formula source, implementation, test cases, and confirmation that 8GB example produces exactly 4 workers.
- Formula result, when applied to actual container memory limit and multiplied by 1.5GB per worker, does not exceed available_memory minus 2GB reserved headroom.
- Deployed container with computed max_workers value does not experience out-of-memory errors or worker crashes during sustained parallel workflow execution.

## Limitations

- Formula assumes each RQ worker process consumes approximately 1.5GB of RAM under typical OpenMS workflow loads; jobs with exceptionally large in-memory data structures may require manual downward adjustment.
- The 2GB reserved overhead includes Redis, Streamlit, system processes, and margin; this is a static offset and does not scale with container size, so the formula may over-allocate workers on very large containers (e.g., 64GB+).
- The formula is calibrated for single-container online deployments as documented; distributed multi-container deployments or heterogeneous worker pools with different memory profiles require separate sizing analysis.
- No dynamic recomputation occurs if container memory limit is changed at runtime; the formula must be re-evaluated and workers restarted to adapt to new memory constraints.

## Evidence

- [other] max_workers formula and 8GB reference example: "max_workers = (available_memory - 2GB) / 1.5GB with stated example of 8GB container → max 4 workers"
- [readme] Online deployment mode and RQ worker memory footprint context: "All components run within the same Docker container, ensuring identical environments for the web app and worker processes."
- [readme] Redis memory overhead in single-container architecture: "Why Single Container? - No networking issues: All communication via localhost"
- [other] RQ as task queue technology choice for online mode: "Task Queue | **RQ (Redis Queue)** | Lightweight, Python-native, simpler than Celery"
- [other] Multiprocessing used in offline mode (not applicable to formula): "The existing multiprocessing system remains completely unchanged for offline/local deployments"
