---
name: galaxy-workflow4metabolomics-reproducible-processing
description: Use when running an LC-MS or GC-MS preprocessing and statistics pipeline
  on a Galaxy Workflow4Metabolomics instance, or when a collaborator must re-execute
  the analysis without installing the toolchain — the stage order is fixed by the
  wrappers' own datatypes, not by convention.
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
  related_skills:
  - w4m-three-table-format-conformance
  license_tier: open
  provenance_tier: repository
  tool_license:
    tier: open
    requires_ack: false
    ref: GPL-3.0
    url: https://github.com/workflow4metabolomics/tools-metabolomics/blob/master/LICENSE.txt
  verified_against:
    repo_ref: master
    observed: '2026-08-21'
schema_version: 0.2.0
---

# galaxy-workflow4metabolomics-reproducible-processing

Run a metabolomics workflow on a shared Galaxy instance so the analysis can be
re-executed by someone who has neither the software nor the compute.

## When this applies

The barrier to reproducing a metabolomics analysis is rarely the method; it is
the environment. Workflow4Metabolomics packages the LC-MS, GC-MS and NMR
pipelines — preprocessing, annotation, normalisation, univariate and
multivariate statistics — as Galaxy tools, so a workflow is shared as a document
others execute rather than as instructions they reimplement.

Reach for it when the analysis must outlive the machine it was written on, when
a collaborator cannot install the toolchain, or when a submission requires an
executable record of what was run.

## The stage order is enforced, not conventional

The LC-MS wrappers declare intermediate Galaxy datatypes, and each stage accepts
only the datatype the previous one emits. The chain is therefore readable off
the tool definitions:

```
mzML / mzXML / netCDF / mzData
  → MSnbase readMSData          → rdata.msnbase.raw
  → xcms findChromPeaks         → rdata.xcms.findchrompeaks
  → xcms refineChromPeaks       → rdata.xcms.findchrompeaks     (optional)
  → xcms findChromPeaks Merger  → rdata.xcms.findchrompeaks     (multi-sample)
  → xcms groupChromPeaks        → rdata.xcms.group
  → xcms adjustRtime            → rdata.xcms.retcor
  → xcms groupChromPeaks        → rdata.xcms.group              (second pass)
  → xcms fillChromPeaks         → rdata.xcms.fillpeaks
  → CAMERA annotate             → rdata.camera.* + the three tables
```

Two consequences follow from the datatypes themselves. `adjustRtime` consumes a
grouped object, so correspondence precedes alignment and is then repeated
against the corrected retention times — the second grouping pass is required,
not a refinement. And `fillChromPeaks` accepts only `rdata.xcms.group`, so gap
filling cannot be moved after annotation.

Parameter optimisation sits beside the chain rather than in it: `IPO for
xcmsSet` reads raw files and `IPO for group and retcor` reads the xcms objects,
and both emit parameter tables you feed back into the corresponding step.

Downstream of CAMERA the pipeline works on the three-table format, and
`Check Format` is the entry point to it. Polarity modes are processed separately
and joined with `CAMERA combinexsAnnos`. `Mz(X)ML Shaper` reshapes open formats
into XCMS-readable mz(X)ML — it accepts mzML, mzXML and netCDF only, so vendor
conversion still happens before upload and outside the platform.

## Procedure

1. **Upload raw data in an open format.** Convert vendor files to mzML first.
   Uploading vendor formats defers the conversion problem to whoever reruns the
   workflow, which defeats the purpose.

2. **Build the sample metadata table before processing**, one row per file, with
   explicit columns for class, batch and injection order. Most downstream
   failures in this pipeline are metadata failures and they surface late. The
   `xcms get a sampleMetadata file` tool emits the skeleton to fill in.

3. **Keep the stages separate.** Preprocessing, annotation, normalisation and
   statistics stay distinct steps rather than one composite. A step you cannot
   inspect is a step you cannot defend, and the datatypes above give you the
   inspection points for free.

4. **Record every non-default parameter.** The workflow document stores them,
   but a reader needs to know which were chosen deliberately and why. Where a
   parameter came from IPO, say so and keep the IPO output.

5. **Export the workflow and the invocation**, not only the results. The
   workflow is the method; the invocation ties it to this dataset, these
   parameters and the tool versions that actually ran.

## Verification

- `xcms process history` summarises what ran; read it rather than trusting the
  workflow diagram, which shows what was requested.
- The exported workflow re-runs on the same inputs and yields the same feature
  count. A difference means a parameter was not captured or a tool version moved.
- The sample metadata row count matches the uploaded file count.
- The three tables agree on identifiers and order before any statistics step.
- Both polarities, if processed, were combined once and not double-counted.

## Limitations

- Public instances impose quotas on storage and runtime; a large study may need
  an institutional Galaxy rather than the shared one.
- Tool versions on the instance change over time, and most wrappers version
  themselves against the underlying R package. A workflow exported today may
  resolve to different versions later, so the invocation record matters more
  than the workflow alone.
- The available tools bound the method. A step the instance does not provide
  cannot be inserted without deploying a tool, which is an administrative task
  rather than an analytical one.
- The datatype chain above is the LC-MS line. The NMR tools and the
  isotope-labelling and flux tools in the same repository form separate chains
  that share only the three-table format.
