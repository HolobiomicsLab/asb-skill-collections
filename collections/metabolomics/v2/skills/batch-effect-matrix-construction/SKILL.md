---
name: batch-effect-matrix-construction
description: 'Use when when you need to generate synthetic metabolomics feature tables
  with quantified batch effects for validating batch-correction methods. Use this
  skill when: (1) you want reproducible, ground-truth batch effects overlaid on condition-only
  variation;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3434
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  - bccenter, bcscaling, bcpareto, bcrange, bcvast, bclevel
  - SummarizedExperiment
  techniques:
  - GC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
  BiocManager::install("mzrtsim")
- github.com__yufree__mzrtsim
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrtsim_cq
    doi: 10.1021/acs.analchem.5c01213
    title: mzrtsim
  dedup_kept_from: coll_mzrtsim_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c01213
  all_source_dois:
  - 10.1021/acs.analchem.5c01213
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# batch-effect-matrix-construction

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a simulated batch-effect matrix for LC/GC-MS metabolomics feature tables by applying nbatch batch factors with configurable intensity modulation profiles (linear, random) across nperbatch samples per batch. This enables controlled benchmarking of batch-correction algorithms on realistic MS data with known ground truth.

## When to use

When you need to generate synthetic metabolomics feature tables with quantified batch effects for validating batch-correction methods. Use this skill when: (1) you want reproducible, ground-truth batch effects overlaid on condition-only variation; (2) you need to systematically test batch-correction normalization methods (centering, scaling, Pareto, VAST) with known batch structure; (3) you are developing or benchmarking batch effect detection or correction workflows and require controlled batch profiles (e.g., linear drift vs. random block effects).

## When NOT to use

- Input data is already a real LC/GC-MS feature table with unknown or heterogeneous batch structure—use empirical batch-correction methods (e.g., ComBat, QC-based normalization) instead.
- The goal is to simulate only condition effects without batch confounding—omit batch-effect construction and use mzrtsim() with nbatch=0 or nbpeaks=0.
- You require batch effects that are non-parametric or derived from observed batch patterns—this skill generates synthetic, model-based batch effects; use data-driven batch harmonization for empirical batches.

## Inputs

- baseline feature matrix (ncomp compounds × samples, from step 2 of mzrtsim workflow)
- nbatch (integer: number of batch factors to simulate)
- nperbatch (integer: number of samples per batch)
- batchtype (string: batch profile type, e.g. 'linear' or 'random')
- nbpeaks (integer: number of peaks affected per batch)
- sample-to-batch assignment vector (length = total samples)

## Outputs

- batch-only effect matrix (ncomp × samples: isolated batch contributions to each peak intensity)
- combined feature table (ncomp × samples: baseline + condition effects + batch effects)
- group assignments vector (length = samples, encoding condition and batch labels)
- batch factor parameters (nbatch, batchtype, nperbatch, nbpeaks for documentation)

## How to apply

Within the mzrtsim() function workflow: (1) After generating a baseline feature table across ncond conditions with ncpeaks peaks per condition, configure nbatch (number of batches) and nbpeaks (peaks per batch) parameters. (2) Specify batchtype as one of the supported profiles—e.g., 'linear' for monotonic intensity drift across batches or 'random' for batch-specific random offsets. (3) Allocate nperbatch samples per batch, ensuring the total sample count aligns with ncond × sample replicates. (4) Apply the batch-effect transformation by modulating peak intensities in the baseline matrix according to the batch factor assignments and profile type. (5) Combine the resulting batch-only effect matrix with the baseline and condition-only matrices to produce the final feature table. (6) Return the composite data matrix alongside the isolated batch-effect matrix and group labels (condition + batch assignments) to enable direct comparison and algorithm validation.

## Related tools

- **mzrtsim** (Host function wrapping batch-effect-matrix construction; orchestrates baseline generation, condition effects, batch effects, and final feature table assembly) — https://github.com/yufree/mzrtsim
- **bccenter, bcscaling, bcpareto, bcrange, bcvast, bclevel** (Downstream batch-correction normalization methods for validating the constructed batch-effect matrices; test whether each method can recover the true condition signal after batch contamination) — https://github.com/yufree/mzrtsim
- **R** (Runtime environment for mzrtsim() and matrix algebra for batch-effect modulation)
- **SummarizedExperiment** (Optional output wrapper (via mzrtsim_se()) for seamless integration into Bioconductor downstream analysis pipelines)

## Examples

```
library(mzrtsim)
result <- mzrtsim(ncomp=100, ncond=3, ncpeaks=50, nbatch=4, nbpeaks=30, npercond=10, nperbatch=15, batchtype='linear', db=hmdbcms)
```

## Evaluation signals

- Batch-only effect matrix has rank ≤ nbatch (dimensionality consistent with specified batch factors); peaks in nbpeaks subset show systematic intensity shift, peaks outside show zero/near-zero batch effect.
- Combined feature table = baseline + condition-only effect + batch-only effect (additive model); verify by subtracting condition and batch matrices from combined result, should recover baseline within numerical precision.
- Group assignment vector correctly partitions samples into nbatch × ncond groups; each group label uniquely identifies one condition–batch combination.
- Batch profile matches specification: 'linear' batches show monotonic intensity trend across batch indices; 'random' batches show uncorrelated batch-specific offsets with stable variance.
- Ground-truth batch-effect matrix can be reconstructed from combined table and condition-only matrix (subtractive proof); batch-correction algorithms applied to combined table should reduce error when validated against this known batch contribution.

## Limitations

- Batch effects are simulated as additive intensity modulations; real MS batch effects may be multiplicative, non-linear, or interact with condition effects (e.g., batch × condition interactions not currently modeled).
- Only parametric batch profiles (linear, random) are supported; complex batch patterns (e.g., cyclic drift, instrument calibration drift, systematic m/z shifts) are not simulated.
- Batch effects are uniform across all peaks within a batch; realistic instrument batches may show heterogeneous peak-specific effects (e.g., early-eluting compounds more affected by column conditioning than late-eluting ones).
- The simulated batches are orthogonal to condition structure; real experimental designs often have confounded batch and condition (e.g., all condition-A samples run in batch-1), which this skill does not capture.
- No changelog or version history available; parameters and output structure may change between mzrtsim releases without documented deprecation.

## Evidence

- [full_text] nbatch, nbpeaks, nperbatch, batchtype parameters: "mzrtsim() accepts parameters ncomp, ncond, ncpeaks, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database)"
- [full_text] batch-only effect matrix output: "returns a list including the data matrix, group assignments, and separate matrices for condition-only and batch-only effects"
- [full_text] batch-effect simulation workflow: "Simulate batch-only effects by applying nbatch batch factors with batchtype-specific profiles (e.g. linear, random) across nperbatch samples per batch"
- [full_text] combination step with condition effects: "Combine baseline matrix with condition and batch effect matrices to produce the feature table"
- [readme] batch-correction benchmarking use case: "`mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods"
- [readme] available batch-correction methods: "Available methods: `bccenter`, `bcscaling`, `bcpareto`, `bcrange`, `bcvast`, `bclevel`"
