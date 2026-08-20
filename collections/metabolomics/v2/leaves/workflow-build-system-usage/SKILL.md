---
name: workflow-build-system-usage
description: 'Use when when you have a Nextflow workflow repository with a Makefile,
  and you need to execute the workflow for local testing or validation. Triggers include:
  (1) first-time setup of a downloaded workflow; (2) regression testing after code
  changes;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - Nextflow
  - Make
  - conda/mamba
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41586-023-06906-8
  title: Reverse metabolomics
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_reverse_metabolomics_cq
    doi: 10.1038/s41586-023-06906-8
    title: Reverse metabolomics
  dedup_kept_from: coll_reverse_metabolomics_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41586-023-06906-8
  all_source_dois:
  - 10.1038/s41586-023-06906-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# workflow-build-system-usage

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Use a build system (Make) to invoke and test a Nextflow workflow, encapsulating the workflow entrypoint and runtime environment setup. This skill ensures reproducible, documented execution of complex bioinformatics pipelines without manual parameter assembly.

## When to use

When you have a Nextflow workflow repository with a Makefile, and you need to execute the workflow for local testing or validation. Triggers include: (1) first-time setup of a downloaded workflow; (2) regression testing after code changes; (3) need to capture and validate runtime outputs before deploying to a production GNPS2 system.

## When NOT to use

- Workflow is already deployed on GNPS2 production or dev servers; use web interface or deployment Make targets (deploy-prod, deploy-dev) instead.
- Build system is not available or Makefile does not define a 'run' target; fall back to direct Nextflow CLI invocation.
- Input data is not suitable for the workflow's expected schema (e.g., missing required metadata fields); validate inputs against workflow documentation before invoking.

## Inputs

- Nextflow workflow repository root directory
- Conda/mamba environment with Nextflow installed
- Makefile with 'run' target defined

## Outputs

- Nextflow workflow execution logs (stdout/stderr)
- Workflow output artifacts (task-specific; defined by nextflow.config and bin/ scripts)
- Nextflow trace/timeline reports (if enabled in nextflow.config)

## How to apply

Navigate to the root of the Nextflow workflow repository (e.g., Reverse_metabolomics_library_generation). Invoke the `make run` target, which encapsulates the documented test entrypoint. The Make target abstracts away direct Nextflow CLI invocation, ensuring correct parameter passing and conda/mamba environment activation. Verify that conda, mamba, and Nextflow are installed locally before execution. Capture stdout and stderr outputs to validate that the workflow completes without errors and produces expected intermediate or final outputs matching the workflow's DAG definition.

## Related tools

- **Nextflow** (Workflow orchestration and execution engine; Make target abstracts direct Nextflow CLI calls) — https://www.nextflow.io/docs/latest/index.html
- **Make** (Build system used to define and invoke the 'run' test entrypoint for the Nextflow workflow)
- **conda/mamba** (Environment and dependency management; required to be installed locally for workflow execution)

## Examples

```
make run
```

## Evaluation signals

- Make target completes with exit code 0 and no fatal errors in stderr.
- Nextflow trace report (if generated) shows all expected tasks in COMPLETED state with no FAILED or CACHED states indicating retry loops.
- Output files are created in the expected directory structure (e.g., results/, work/) matching workflow DAG and output definitions.
- Workflow execution time and resource usage are within expected range for test data; anomalies (e.g., infinite loops, hung tasks) indicate configuration or script errors.
- Output schema and file format match expectations defined in workflow documentation (e.g., JSON, CSV, or task-specific binary formats).

## Limitations

- Make target assumes local environment (conda/mamba/Nextflow installed); fails if dependencies are missing or misconfigured.
- Test workflow may use small toy datasets and may not exercise all branches of the full pipeline; supplementary testing with realistic data is recommended before production deployment.
- Makefile and Nextflow config are tightly coupled; changes to one may require updates to the other to maintain reproducibility.
- No isolation between test runs; successive invocations may reuse cached intermediate results from the work/ directory, potentially masking bugs; explicit cache cleanup may be needed.

## Evidence

- [readme] To run the workflow to test simply do

```
make run
```: "To run the workflow to test simply do

```
make run
```"
- [readme] You will need to have conda, mamba, and nextflow installed to run things locally.: "You will need to have conda, mamba, and nextflow installed to run things locally."
- [other] The Reverse_metabolomics_library_generation Nextflow template is executed using the `make run` command as its test entrypoint.: "The Reverse_metabolomics_library_generation Nextflow template is executed using the `make run` command as its test entrypoint."
- [other] Capture and validate the runtime outputs generated by the workflow execution.: "Capture and validate the runtime outputs generated by the workflow execution."
- [readme] To learn NextFlow checkout this documentation:

https://www.nextflow.io/docs/latest/index.html: "To learn NextFlow checkout this documentation:

https://www.nextflow.io/docs/latest/index.html"
