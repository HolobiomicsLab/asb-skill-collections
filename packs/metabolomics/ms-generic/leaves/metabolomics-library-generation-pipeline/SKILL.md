---
name: metabolomics-library-generation-pipeline
description: Use when when you have cloned or accessed the Reverse_metabolomics_library_generation repository and need to verify that the Nextflow workflow is properly configured, executable, and produces expected spectral library outputs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3937
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Nextflow
  - conda
  - mamba
  - make
  techniques:
  - mass-spectrometry
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

# metabolomics-library-generation-pipeline

## Summary

Execute a Nextflow-based workflow to generate reverse-phase metabolomics spectral libraries by running a documented test entrypoint. This skill enables reproducible invocation of the Reverse_metabolomics_library_generation pipeline to validate workflow structure and outputs.

## When to use

When you have cloned or accessed the Reverse_metabolomics_library_generation repository and need to verify that the Nextflow workflow is properly configured, executable, and produces expected spectral library outputs. Use this when establishing a working reference state for the pipeline or validating environment setup (conda, mamba, Nextflow installed).

## When NOT to use

- You do not have Nextflow, conda, or mamba installed in your environment.
- You need to run the workflow with custom parameters or non-test inputs — use Nextflow CLI directly instead.
- The repository has not been cloned or you cannot access the Makefile.

## Inputs

- Nextflow workflow definition files (*.nf)
- nextflow.config configuration file
- Test dataset (if embedded in repository)
- Makefile with 'run' target

## Outputs

- Nextflow execution logs and console output
- Generated spectral library files
- Workflow execution report
- Intermediate processed data artifacts

## How to apply

Navigate to the root of the Reverse_metabolomics_library_generation repository and invoke the `make run` command, which is the documented test entrypoint. This command triggers the Nextflow workflow execution with predefined test parameters. Capture the runtime console output and generated artifacts (intermediate files, final library outputs) to validate that the workflow completed without errors and produced expected file types and structure. Check that execution status shows completion and no Nextflow runtime errors occurred.

## Related tools

- **Nextflow** (Workflow execution engine that orchestrates the pipeline steps for metabolomics library generation) — https://www.nextflow.io/docs/latest/index.html
- **conda** (Environment manager required to install and isolate workflow dependencies)
- **mamba** (Fast dependency resolver for setting up conda environments required by the workflow)
- **make** (Build automation tool that provides the 'run' target for invoking the test workflow)

## Examples

```
make run
```

## Evaluation signals

- Nextflow command exits with status 0 (no runtime errors reported).
- Console output contains completion message indicating successful workflow execution.
- Expected output files are created in designated output directory with non-zero file sizes.
- No error or warning messages appear in the Nextflow execution report.
- Workflow execution time falls within expected range (indicates normal resource allocation and no hanging processes).

## Limitations

- Test execution uses predefined test data; results may not reflect performance or accuracy on real user datasets.
- Requires local installation of conda, mamba, and Nextflow — cannot run in minimal or restricted environments.
- The `make run` command executes only the documented test entrypoint; custom workflows or parameters require direct Nextflow CLI invocation.

## Evidence

- [intro] The Reverse_metabolomics_library_generation Nextflow template is executed using the `make run` command as its test entrypoint.: "To run the workflow to test simply do

```
make run
```"
- [readme] Nextflow is the core execution framework; conda and mamba are prerequisite dependency managers.: "You will need to have conda, mamba, and nextflow installed to run things locally."
- [other] The workflow is documented and publicly hosted on GitHub.: "Clone or navigate to the Reverse_metabolomics_library_generation repository from github.com/Wang-Bioinformatics-Lab/Reverse_metabolomics_library_generation."
- [readme] Nextflow documentation provides comprehensive reference material for users.: "To learn NextFlow checkout this documentation:

https://www.nextflow.io/docs/latest/index.html"
