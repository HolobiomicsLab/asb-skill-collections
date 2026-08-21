---
name: galaxy-workflow4metabolomics-reproducible-processing
description: Use when running an LC-MS or GC-MS preprocessing and statistics workflow
  on the Galaxy Workflow4Metabolomics instance, or when a collaborator needs to re-execute
  an analysis without installing the toolchain locally.
license: CC-BY-4.0
status: hold
metadata:
  tools:
  - Workflow4Metabolomics
  - Galaxy
  techniques:
  - LC-MS
  - GC-MS
  repo_url: https://github.com/workflow4metabolomics/tools-metabolomics
  related_skills: []
  license_tier: open
  provenance_tier: repository
  tool_license:
    tier: open
    requires_ack: false
    ref: GPL-3.0
    url: https://github.com/workflow4metabolomics/tools-metabolomics/blob/main/LICENSE
schema_version: 0.2.0
---

# galaxy-workflow4metabolomics-reproducible-processing

Run a metabolomics workflow on a shared Galaxy instance so that the analysis can
be re-executed by someone who has neither the software nor the compute.

## When this applies

The barrier to reproducing a metabolomics analysis is rarely the method; it is
the environment. Workflow4Metabolomics packages the common LC-MS and GC-MS
pipeline — preprocessing, normalisation, annotation, univariate and multivariate
statistics — as Galaxy tools on a public instance, so a workflow can be shared as
a document that others execute rather than as instructions they reimplement.

Reach for it when the analysis must outlive the machine it was written on, when a
collaborator cannot install the toolchain, or when a submission requires an
executable record of what was run.

## Procedure

1. **Upload the raw data in an open format.** Convert vendor files to mzML first.
   Uploading vendor formats defers the conversion problem to whoever reruns the
   workflow, which defeats the purpose.
2. **Build the sample metadata table before processing**, with one row per file
   and explicit columns for class, batch and injection order. Most downstream
   failures in this pipeline are metadata failures, and they surface late.
3. **Assemble the workflow from the instance's tool set**, keeping preprocessing,
   normalisation and statistics as separate steps rather than one composite. A
   step you cannot inspect is a step you cannot defend.
4. **Record every non-default parameter.** The workflow document stores them, but
   a reader needs to know which ones were chosen deliberately and why.
5. **Export the workflow and the invocation**, not only the results. The workflow
   is the method; the invocation ties it to this dataset and these parameters.

## Verification

- The exported workflow re-runs on the same inputs and yields the same feature
  count. A difference means a parameter was not captured or a tool version moved.
- The sample metadata row count matches the uploaded file count.
- The feature table's sample columns match the metadata's sample identifiers
  exactly — a silent mismatch here produces statistics on mislabelled groups.

## Limitations

- Public instances impose quotas on storage and runtime; a large study may need a
  local or institutional Galaxy rather than the shared one.
- Tool versions on the instance change over time. A workflow exported today may
  resolve to different tool versions later, so the invocation record — which pins
  versions — matters more than the workflow alone.
- The available tools bound the method. A step the instance does not provide
  cannot be inserted without deploying a tool, which is an administrative task
  rather than an analytical one.
