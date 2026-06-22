---
name: numerical-formula-implementation
description: Use when a formula is documented in a system or article (e.g., resource allocation, sizing, or tuning guidance) but lacks executable validation, or you need to confirm the formula produces the documented expected output (e.g., an 8GB system should yield exactly 4 workers).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_2269
  tools:
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

# numerical-formula-implementation

## Summary

Implement and validate a numerical formula by translating documented mathematical expressions into executable code, then verify correctness against worked examples and edge cases. This skill bridges formula documentation and operational deployment, ensuring computational correctness before production use.

## When to use

A formula is documented in a system or article (e.g., resource allocation, sizing, or tuning guidance) but lacks executable validation, or you need to confirm the formula produces the documented expected output (e.g., an 8GB system should yield exactly 4 workers). Use this skill when moving from paper/documentation to code, or when validating that a formula implementation matches its specification.

## When NOT to use

- Formula is already implemented and tested in a well-maintained library or framework (use the library instead).
- The input data is a real-world measurement or empirical sample that does not fit a closed-form formula (use statistical modeling or curve fitting instead).
- The formula exists only as a heuristic or empirical rule of thumb with no rigorous documentation or expected output; in that case, validate against domain expert judgment or empirical performance rather than formula verification alone.

## Inputs

- Mathematical formula (as text or pseudo-code from documentation)
- Worked example with concrete input values and expected output
- System parameters or constraints (e.g., memory limits, divisors, edge thresholds)

## Outputs

- Executable implementation (Python function or script)
- Test harness with test cases
- Verification report documenting formula, tests, and pass/fail results

## How to apply

Extract the mathematical formula from documentation and any worked example(s) provided. Implement the formula in a general-purpose language (Python recommended for scientific work) using typed inputs and floating-point arithmetic where appropriate. Create a test harness that validates the implementation against the documented worked example by substituting known inputs and comparing outputs to stated results. Define and test boundary or edge cases (e.g., inputs at or below minimum thresholds, zero divisors, negative intermediate results) to identify clamping, rounding, or error-handling behavior. Generate a verification report that documents the formula, implementation, test cases, and confirmation that all tests pass, especially the reference example.

## Related tools

- **Python** (Language for implementing numerical formulas with floating-point arithmetic and test harnesses)

## Examples

```
python -c "def max_workers(gb): return max(0, int((gb - 2) / 1.5)); print(f'8GB system: {max_workers(8)} workers'); assert max_workers(8) == 4, 'Formula verification failed'"
```

## Evaluation signals

- The implementation correctly reproduces the worked example output (e.g., 8GB input yields exactly 4 workers).
- Edge case tests execute without error and produce sensible outputs (e.g., memory below 2GB clamps to 0 workers, not negative).
- Intermediate arithmetic steps (e.g., (8 - 2) / 1.5 = 6 / 1.5 = 4.0) are transparent and can be traced in code or test output.
- Verification report explicitly lists all test cases and their pass/fail status, with no failing tests.
- Formula parameters (e.g., 2GB reserved memory, 1.5GB per-worker overhead) are clearly defined as constants or docstring-documented, enabling future maintenance.

## Limitations

- The worked example provided must be correct; if the documentation itself contains an arithmetic error, the implementation will reproduce it faithfully and pass validation against a wrong reference.
- Floating-point arithmetic may introduce rounding errors; edge cases near integer boundaries require explicit rounding or truncation logic whose behavior must be specified.
- The formula may not account for real-world operating-system overhead, garbage collection, or contention beyond the documented parameters; validation confirms formula correctness, not system performance.

## Evidence

- [other] max_workers = (available_memory - 2GB) / 1.5GB: "max_workers = (available_memory - 2GB) / 1.5GB"
- [other] 8GB container yields 4 workers: "with stated example of 8GB container → max 4 workers"
- [other] Workflow to extract, implement, validate, and test the formula: "Extract the worker-count formula and example from the methods text: max_workers = (available_memory - 2GB) / 1.5GB with stated example of 8GB container → max 4 workers. 2. Implement the formula in a"
- [other] Generate verification report: "Generate a verification report documenting the formula, implementation, test cases, and confirmation that the 8GB example produces exactly 4 workers."
