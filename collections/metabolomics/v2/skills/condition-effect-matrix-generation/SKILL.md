---
name: condition-effect-matrix-generation
description: 'Use when you need to create a synthetic feature table with known, ground-truth condition effects for method validation when: (1) testing normalization or batch-correction algorithms that must not confound condition signal with batch noise;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  - SummarizedExperiment
  - HMDB / MoNA databases
  techniques:
  - GC-MS
derived_from:
- doi: 10.1021/acs.analchem.5c01213
  title: mzrtsim
evidence_spans:
- if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager") BiocManager::install("mzrtsim")
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# condition-effect-matrix-generation

## Summary

Generate a feature-table matrix encoding controlled intensity modulations across experimental conditions for LC/GC-MS metabolomics simulations. This skill produces a condition-only effect matrix that modulates peak intensities across conditions according to user-specified allocation parameters, enabling benchmarking of statistical and normalization methods.

## When to use

You need to create a synthetic feature table with known, ground-truth condition effects for method validation when: (1) testing normalization or batch-correction algorithms that must not confound condition signal with batch noise; (2) you have defined a target number of compounds (ncomp), conditions (ncond), peaks per condition (ncpeaks), and allocation fraction (npercond); (3) you want deterministic, reproducible intensity profiles tied to specific conditions rather than random variation; (4) benchmarking requires separating true biological/condition signal from unwanted batch or technical variation.

## When NOT to use

- Input is already a finalized, real-world LC/GC-MS feature table with unknown or unmeasured condition structure; use this skill only for synthetic, controlled simulation.
- You need to estimate or infer condition effects from real data post-hoc rather than specify them a priori; this skill applies only to prospective, design-time specification of condition modulation.
- The condition effect must be confounded with batch effects for realism; this skill explicitly decouples them, so if your benchmark requires a more complex interplay, use a different simulation strategy.

## Inputs

- ncomp: integer, number of compounds in the simulated feature table
- ncond: integer, number of experimental conditions
- ncpeaks: integer, number of peaks per condition
- npercond: numeric (0–1), fraction of peaks allocated to condition-only effects
- HMDB or MoNA spectral database (db parameter): real MS1 spectra with m/z, retention time, and intensity
- baseline feature matrix: ncomp × ncond×samples numeric matrix of simulated peak intensities

## Outputs

- condition-only effect matrix: same dimensions as baseline, containing only intensity modulations attributed to condition (orthogonal to batch)
- condition-effect assignments: vector or data frame mapping which peaks carry condition effects
- combined feature table: baseline matrix additively or multiplicatively merged with condition effects for downstream analysis

## How to apply

Within mzrtsim(), after parsing ncomp, ncond, ncpeaks, and npercond parameters against the HMDB or MoNA spectral database: (1) generate a baseline data matrix with ncomp compounds across ncond conditions, populating ncpeaks peaks per condition; (2) allocate npercond fraction of peaks to exhibit intensity modulation strictly across conditions (not batches); (3) modulate the baseline peak intensities in the condition-only matrix by scaling or shifting intensities in a condition-dependent manner (e.g., linear or multiplicative profiles); (4) retain the batch-orthogonal condition effect matrix as a separate output for downstream validation. The condition effect matrix must be additive or multiplicative to the baseline so that condition signal can be isolated from batch effects when testing correction methods.

## Related tools

- **mzrtsim** (Primary function wrapper; encapsulates condition-effect matrix generation within broader peak-list simulation pipeline) — https://github.com/yufree/mzrtsim
- **R** (Execution environment for mzrtsim and matrix operations)
- **SummarizedExperiment** (Optional wrapper for output matrix to integrate with Bioconductor batch-correction and normalization workflows)
- **HMDB / MoNA databases** (Source of real spectral data (m/z, intensity, retention time) for populating baseline and effect matrices) — https://hmdb.ca/downloads

## Examples

```
library(mzrtsim); data('hmdbcms'); sim <- mzrtsim(ncomp=100, ncond=3, ncpeaks=50, nbatch=2, nbpeaks=30, npercond=0.7, nperbatch=0.5, batchtype='linear', db=hmdbcms); head(sim$data); head(sim$condition_effect_matrix)
```

## Evaluation signals

- Condition-effect matrix sums or scales correctly: verify that the condition-only matrix, when combined with baseline, yields the expected feature table without introducing negative intensities or unrealistic fold-changes.
- Orthogonality to batch: confirm that condition-effect intensities are uncorrelated with batch assignments (Pearson r ≈ 0 or ANOVA F-ratio for batch is negligible when applied to condition-effect matrix alone).
- Peak allocation consistency: check that the number of peaks with condition effects matches ceil(ncpeaks × npercond × ncond) or the specified allocation scheme.
- Ground-truth recovery: pass the output feature table and condition labels to a normalization/batch-correction method; verify that condition signal is recovered with high sensitivity (e.g., t-test p < 0.05) and batch-correction does not artificially inflate or erase condition effects.
- Reproducibility: re-run with identical seed and parameters; verify bitwise identity of the condition-effect matrix.

## Limitations

- Condition effects are synthetic and uniform across allocated peaks; real MS1 data exhibits compound-specific and ionization-dependent condition responses that this model does not capture.
- The mzrtsim() function currently supports only linear and random batchtype profiles; condition-effect modulation logic is not separately parametrized, so users cannot fine-tune condition intensity dynamics (e.g., non-linear dose–response curves) without forking the package.
- Condition and batch effects are assumed additive or multiplicative; complex, higher-order interactions between conditions and batches (e.g., batch-specific condition slopes) are not modeled.
- Database-derived peaks must be present in HMDB or MoNA; custom or instrument-specific adducts or fragment ions not in these repositories cannot be simulated.

## Evidence

- [other] mzrtsim() accepts parameters ncomp, ncond, ncpeaks, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database) and returns a list including the data matrix, group assignments, and separate matrices for condition-only and batch-only effects.: "mzrtsim() accepts parameters ncomp, ncond, ncpeakes, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database) and returns a list including the data matrix, group assignments, and"
- [other] Simulate condition-only effects by modulating peak intensities across ncond conditions according to npercond allocation.: "Simulate condition-only effects by modulating peak intensities across ncond conditions according to npercond allocation."
- [intro] mzrtsim() generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "mzrtsim() generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods."
- [intro] Peak list simulation using mzrtsim() to generate feature tables with condition and batch effects: "Peak list simulation using mzrtsim() to generate feature tables with condition and batch effects"
- [intro] For seamless integration with Bioconductor workflows, use mzrtsim_se() which wraps the simulation in a SummarizedExperiment: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
