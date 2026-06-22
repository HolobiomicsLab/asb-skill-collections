---
name: edge-case-boundary-testing
description: Use when when implementing or validating a quantitative formula (e.g., resource sizing, memory allocation, worker count calculation) that will be applied across a range of input values, especially when the formula involves division, clamping, or has implicit domain constraints (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
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

# edge-case-boundary-testing

## Summary

Systematic validation of computational formulas and system configurations by testing boundary conditions and extreme input values to verify correctness and identify failure modes. This skill ensures that mathematical models and resource-allocation algorithms behave correctly at their limits.

## When to use

When implementing or validating a quantitative formula (e.g., resource sizing, memory allocation, worker count calculation) that will be applied across a range of input values, especially when the formula involves division, clamping, or has implicit domain constraints (e.g., memory must be ≥ 2GB to avoid negative worker counts).

## When NOT to use

- The formula is already empirically validated in production with no documented errors or boundary issues.
- The input domain is entirely open-ended with no known constraints or the formula is purely linear without discontinuities or clamping.
- The source material provides no concrete example case or does not specify the formula's parameters and units clearly enough to implement.

## Inputs

- Formula specification with parameters and units (e.g., max_workers = (available_memory - 2GB) / 1.5GB)
- Documented example case with known input and output (e.g., 8GB → 4 workers)
- System constraints or implicit domain boundaries (e.g., available_memory ≥ 2GB, max_workers ≥ 0)

## Outputs

- Python or equivalent implementation of the formula
- Test case matrix with inputs, expected outputs, and actual results
- Verification report documenting formula correctness, edge case handling, and any clamping/rounding behavior
- Confirmed derivation showing the documented example produces the stated result

## How to apply

Extract the formula and its documented constraints from the source material. Implement the formula in executable code (Python, etc.) accepting the key input parameter. Validate against the primary documented example (e.g., 8GB system → 4 workers for the formula (available_memory - 2GB) / 1.5GB). Then systematically test edge cases: inputs at or below the lower bound (e.g., memory = 2GB, memory < 2GB to check for negative or zero clamping), inputs at critical transition points (e.g., memory = 5.5GB to verify rounding/floor behavior), and inputs at or near the upper bound if known. Document each test case, its expected output, and the actual result. Use this test matrix to generate a verification report confirming the formula's correctness across its operational domain and identifying any clamping or rounding behavior that must be documented for users.

## Related tools

- **Python** (Implementation language for the formula and test harness using floating-point arithmetic to validate the computation)

## Examples

```
# Python implementation and validation:
available_memory = 8
max_workers = (available_memory - 2) / 1.5
print(f"8GB system: {max_workers} workers")  # Expected: 4.0

# Edge cases:
for mem in [1.5, 2.0, 5.5, 10.0]:
    workers = max(0, (mem - 2) / 1.5)
    print(f"{mem}GB: {workers} workers")
```

## Evaluation signals

- Formula implementation substituted with documented example (8GB input) produces exactly the stated output (4 workers).
- Edge case at lower bound (available_memory = 2GB) produces zero workers or correct clamped minimum.
- Edge case below lower bound (available_memory < 2GB) is handled gracefully (clamped to 0, error raised, or documented as out-of-domain).
- Edge case at intermediate boundary (available_memory = 5.5GB) produces the expected rounding/floor behavior (2.4 → 2 or 2.4 → 2.4 as documented).
- Verification report explicitly lists all test cases, their rationale, and confirmation that no discrepancy exists between formula specification and implementation.

## Limitations

- The provided section text in the source cards does not contain the worker-count calculation formula, memory parameters, or the 8GB example result; extraction from methods or configuration documentation is required.
- Rounding, flooring, or other discretization behavior may not be explicitly specified in the formula; edge case tests may reveal undocumented behavior.
- Testing is limited to the domain implied by documented examples and stated constraints; extreme or pathological inputs outside the operational range may not be covered.

## Evidence

- [other] Does the documented formula max_workers = (available_memory - 2GB) / 1.5GB correctly calculate the maximum worker count for an 8GB system in online mode?: "max_workers = (available_memory - 2GB) / 1.5GB correctly calculate the maximum worker count for an 8GB system in online mode"
- [other] Implement the formula in a Python script that accepts available_memory (in GB) as input and computes max_workers using floating-point arithmetic. Validate the formula against the stated 8GB example: substitute available_memory = 8, compute (8 - 2) / 1.5 = 6 / 1.5 = 4.0, and verify the result equals 4 workers.: "substitute available_memory = 8, compute (8 - 2) / 1.5 = 6 / 1.5 = 4.0, and verify the result equals 4 workers"
- [other] Test edge cases: memory below 2GB (negative workers, clamp to 0), memory at 2GB (result 0), and memory at 5.5GB (result 2.4, floor or round as appropriate).: "Test edge cases: memory below 2GB (negative workers, clamp to 0), memory at 2GB (result 0), and memory at 5.5GB"
- [other] Generate a verification report documenting the formula, implementation, test cases, and confirmation that the 8GB example produces exactly 4 workers.: "Generate a verification report documenting the formula, implementation, test cases, and confirmation that the 8GB example produces exactly 4 workers"
