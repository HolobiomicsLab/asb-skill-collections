---
name: matplotlib-plot-reference-image-comparison
description: Use when you need to verify that visualization functions produce graphically correct output that matches previously validated baseline images. Use it as part of automated testing workflows (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3577
  - http://edamontology.org/topic_3304
  tools:
  - git
  - matplotlib
  - pytest
  - Hatch
  - Scanpy
derived_from:
- doi: 10.1186/s13059-017-1382-0
  title: scanpy
evidence_spans:
- This section of the docs covers our practices for working with git on our codebase
- matplotlib.testing.setup tries to establish a consistent environment for creating plots
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_scanpy
    doi: 10.1186/s13059-017-1382-0
    title: scanpy
  dedup_kept_from: coll_scanpy
schema_version: 0.2.0
---

# matplotlib-plot-reference-image-comparison

## Summary

Validate that programmatically generated matplotlib visualizations match expected reference images by comparing rendered plot outputs against stored baseline images. This skill ensures reproducibility and visual correctness of plots in test suites, particularly for complex single-cell analysis visualizations.

## When to use

Apply this skill when you need to verify that visualization functions produce graphically correct output that matches previously validated baseline images. Use it as part of automated testing workflows (e.g., continuous integration) where visual regression detection is required, such as when testing Scanpy's plotting functions that generate complex single-cell analysis plots.

## When NOT to use

- Input plots are inherently non-deterministic (e.g., include random jitter, timestamps, or data-dependent colors) unless randomness is seeded consistently.
- Reference images do not exist yet and you are in initial development (use manual visual inspection or snapshot generation first).
- Testing non-visual output such as numeric arrays, data structures, or file I/O; use standard assertion comparisons instead.

## Inputs

- matplotlib Figure objects or plotting function calls
- Reference image files (typically PNG or other raster format stored in test fixtures directory)
- Pytest test functions decorated to use the image_comparer fixture

## Outputs

- Test pass/fail status
- Pixel-level difference metrics (when available)
- Generated plot images (for manual inspection or baseline updates)

## How to apply

Invoke the matplotlib image_comparer fixture within a pytest test suite to automatically capture rendered plot output and compare it against stored reference images. The fixture handles image serialization, pixel-level comparison, and tolerance thresholds for anti-aliasing and rendering variations. Matplotlib's testing.setup establishes a consistent rendering environment to minimize spurious differences due to font rendering or backend variations. Pass the fixture to test functions that generate plots, and configure tolerance parameters (typically via pytest parametrization or fixture options) to account for minor rendering differences while catching substantial visual changes. The comparison succeeds when pixel differences fall within the configured tolerance; failures flag plots that have diverged from the reference baseline, indicating either a genuine bug or a deliberate change requiring baseline image regeneration.

## Related tools

- **pytest** (Test framework that hosts the image_comparer fixture and orchestrates test execution)
- **matplotlib** (Generates plot output and provides testing.setup for consistent rendering environment; image_comparer compares matplotlib Figure outputs)
- **Hatch** (Environment manager used to invoke the full test suite including image comparison tests via `hatch test`) — https://github.com/scverse/scanpy
- **Scanpy** (Source library whose plotting functions (e.g., visualization of single-cell data) are tested using image comparison) — https://github.com/scverse/scanpy

## Examples

```
hatch test test_plotting.py
```

## Evaluation signals

- Test exits with code 0 and reports zero failures for all image comparison assertions
- Generated plot images pixel-wise match reference images within configured tolerance (typically measured in mean squared error or max pixel difference)
- Pytest output explicitly confirms number of passed image comparison tests and any threshold violations
- No spurious failures due to anti-aliasing or font rendering by using matplotlib.testing.setup and consistent backend configuration
- When baseline images are intentionally updated, the diff or version control shows only the expected visual changes, not unrelated plot drift

## Limitations

- Image comparison is sensitive to font availability, anti-aliasing behavior, and graphics backend differences across systems; matplotlib.testing.setup mitigates but does not eliminate platform-specific rendering variance.
- Tolerance thresholds must be tuned per plotting function; too tight a threshold causes flaky tests on different hardware or OS versions, while too loose a threshold misses genuine regressions.
- Reference images can become outdated or incorrect if baselines are regenerated without visual review; maintainers must validate baseline updates carefully.
- Complex plots with many data-dependent visual elements (e.g., per-cluster colors, legend layouts) may be difficult to parameterize for stable comparison across data variants.

## Evidence

- [other] Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture.: "Check that any custom matplotlib plot reference images match expected outputs via the image_comparer fixture."
- [other] matplotlib.testing.setup tries to establish a consistent environment for creating plots: "matplotlib.testing.setup tries to establish a consistent environment for creating plots"
- [other] We use pytest to test scanpy. To run the tests, simply run `hatch test`: "We use pytest to test scanpy. To run the tests, simply run `hatch test`"
