---
name: feature-table-matrix-assembly
description: Use when when you need to generate a realistic LC/GC-MS feature table
  (peak intensity matrix) with controlled, quantifiable condition effects (e.g., differential
  metabolite abundance across disease states) and batch effects (e.g., instrument
  drift, sample processing day).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3635
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  - SummarizedExperiment
  - R base
  techniques:
  - GC-MS
  license_tier: restricted
  provenance_tier: literature
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

# feature-table-matrix-assembly

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a feature intensity matrix from baseline compound data by populating peaks across conditions and batches, then modulating intensities according to condition-specific and batch-specific effect profiles. This skill is essential for generating ground-truth LC/GC-MS peak-list simulations with known condition and batch effects for benchmarking normalisation and batch-correction algorithms.

## When to use

When you need to generate a realistic LC/GC-MS feature table (peak intensity matrix) with controlled, quantifiable condition effects (e.g., differential metabolite abundance across disease states) and batch effects (e.g., instrument drift, sample processing day). Use this when designing benchmarking experiments where the true magnitude and structure of condition and batch distortions must be known a priori.

## When NOT to use

- Input is already a real, experimentally-acquired LC/GC-MS feature table (use peak-picking and alignment tools instead).
- You only need raw MS1/MS2 spectral data (.mzML files) without a structured feature table; use simmzml() raw data simulation instead.
- Condition and batch effects are unknown or cannot be meaningfully parameterised (e.g., exploratory data with uncharacterised noise structure).

## Inputs

- ncomp: integer (number of compounds/metabolites in the database)
- ncond: integer (number of experimental conditions)
- ncpeaks: integer (number of peaks to assign per condition)
- nbatch: integer (number of batch groups)
- nbpeaks: integer (number of peaks to assign per batch)
- npercond: numeric (percentage or fraction of peaks affected by condition effects, 0–1)
- nperbatch: numeric (percentage or fraction of peaks affected by batch effects, 0–1)
- batchtype: string ('linear', 'random', or other profile type)
- db: list or data frame (spectral database, e.g., hmdbcms, monahrms1, containing m/z, retention time, and intensity vectors per compound)

## Outputs

- data matrix: numeric matrix [samples × compounds] with simulated peak intensities
- group assignments: character or factor vector mapping each sample to a condition and batch label
- condition-only effect matrix: numeric matrix [samples × compounds] containing isolated condition effects
- batch-only effect matrix: numeric matrix [samples × compounds] containing isolated batch effects

## How to apply

Parse input parameters specifying the number of compounds (ncomp), conditions (ncond), peaks per condition (ncpeaks), batches (nbatch), peaks per batch (nbpeaks), percentage of peaks affected per condition (npercond), and percentage of peaks affected per batch (nperbatch), along with a batchtype (e.g., 'linear', 'random'). Generate a baseline data matrix with dimensions [samples × compounds]. Populate ncpeaks peaks per condition and nbpeaks peaks per batch in this baseline. Simulate condition-only effects by modulating peak intensities across the ncond conditions according to the npercond allocation ratio. Simulate batch-only effects by applying nbatch batch factors with batchtype-specific intensity profiles (linear ramps, random perturbations) across nperbatch samples per batch. Combine the baseline matrix with condition and batch effect matrices using element-wise addition or multiplication to produce the final feature table. Return a list structure containing the combined data matrix, group assignments (condition + batch labels for each sample), the condition-only effect matrix, and the batch-only effect matrix separately, enabling later isolation of true signal from noise.

## Related tools

- **mzrtsim** (R package implementing mzrtsim() and mzrtsim_se() functions to generate feature tables with condition and batch effects; wraps output in SummarizedExperiment for Bioconductor integration) — https://github.com/yufree/mzrtsim
- **SummarizedExperiment** (Bioconductor container for wrapping simulated feature tables with metadata (condition, batch labels) for downstream normalisation and batch-correction workflows)
- **R base** (Matrix arithmetic, data structure manipulation (list, data frame), and vector allocation for assembling feature matrices)

## Examples

```
library(mzrtsim); result <- mzrtsim(ncomp=100, ncond=3, ncpeaks=20, nbatch=4, nbpeaks=15, npercond=0.5, nperbatch=0.3, batchtype='linear', db=hmdbcms); feature_table <- result$data; group_labels <- result$group
```

## Evaluation signals

- Verify matrix dimensions match expected sample count (number of samples = npercond × ncond × nperbatch × nbatch, or similar parameterisation).
- Check that condition-only effect matrix shows significant intensity modulation only across ncond conditions while batch-only effect matrix shows intensity variation across nbatch batch groups; verify orthogonality (low correlation between condition and batch matrices).
- Confirm that returned group assignments vector has length equal to number of samples and correctly encodes all combinations of condition and batch labels.
- Validate that peak intensities in the combined data matrix fall within realistic LC/GC-MS dynamic range (e.g., relative intensities 0–100 or log-scale equivalents) and that no negative intensities are introduced.
- Re-apply PCA or batch-effect detection tools (e.g., ComBat, sva::svaseq) to the simulated feature table and verify that condition effects are recoverable and batch effects are isolatable before and after batch correction.

## Limitations

- The assembly assumes independence of condition and batch effects (additive or multiplicative model); if true interactions exist (e.g., condition effects differ per batch), this model may not capture them.
- Peak allocation (npercond, nperbatch) is uniform across all compounds; no support for compound-specific effect magnitudes or sparse patterns of response.
- batchtype profiles (linear, random) are simplified; real batch effects (e.g., instrument maintenance, column degradation, detector nonlinearity) may follow more complex temporal or instrumental patterns.
- No simulation of missing values, detection limits, or instrument censoring, which are common in real MS data.
- Baseline intensities are drawn from the database without accounting for sample-specific dilution, extraction efficiency, or ionization suppression/enhancement.

## Evidence

- [other] mzrtsim() accepts parameters ncomp, ncond, ncpeaks, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database) and returns a list including the data matrix, group assignments, and separate matrices for condition-only and batch-only effects.: "mzrtsim() accepts parameters ncomp, ncond, ncpeaks, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database) and returns a list including the data matrix, group assignments, and"
- [other] Generate a baseline data matrix with ncomp compounds across ncond conditions, populating with ncpeaks peaks per condition and nbpeaks peaks per batch. Simulate condition-only effects by modulating peak intensities across ncond conditions according to npercond allocation. Simulate batch-only effects by applying nbatch batch factors with batchtype-specific profiles (e.g. linear, random) across nperbatch samples per batch.: "Generate a baseline data matrix with ncomp compounds across ncond conditions, populating with ncpeaks peaks per condition and nbpeaks peaks per batch. Simulate condition-only effects by modulating"
- [intro] mzrtsim() generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "`mzrtsim()` generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods."
- [intro] For seamless integration with Bioconductor workflows, use mzrtsim_se() which wraps the simulation in a SummarizedExperiment.: "For seamless integration with Bioconductor workflows, use `mzrtsim_se()` which wraps the simulation in a `SummarizedExperiment`"
- [intro] Peak list simulation using mzrtsim() to generate feature tables with condition and batch effects for benchmarking normalisation and batch correction methods.: "Peak list simulation using mzrtsim() to generate feature tables with condition and batch effects for benchmarking normalisation and batch correction"
