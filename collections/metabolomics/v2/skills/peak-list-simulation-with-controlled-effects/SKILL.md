---
name: peak-list-simulation-with-controlled-effects
description: Use when you need to validate batch correction or normalization algorithms, require ground-truth condition/batch effect annotations for method benchmarking, or want to systematically evaluate how different batch types (linear, random) and condition allocations affect feature recovery in metabolomic.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - R
  - mzrtsim
  - simmzml
  - mzrtsim_se
  - BiocManager
  - hmdbcms
  - monahrms1
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
---

# peak-list-simulation-with-controlled-effects

## Summary

Generate synthetic LC/GC-MS feature tables with controlled condition and batch effects using the mzrtsim() function to benchmark normalization and batch correction methods. This skill produces ground-truth peak-list simulations where effect magnitudes and patterns are known and reproducible.

## When to use

Use this skill when you need to validate batch correction or normalization algorithms, require ground-truth condition/batch effect annotations for method benchmarking, or want to systematically evaluate how different batch types (linear, random) and condition allocations affect feature recovery in metabolomic data.

## When NOT to use

- Input is already a real experimental feature table—use this skill to generate synthetic ground truth, not to re-simulate observed data.
- Your goal is to perform untargeted metabolomics on real biosamples—this skill produces simulated data for validation, not analysis of authentic samples.
- You need raw MS1/MS2 mzML files with realistic chromatographic peak shapes—use simmzml() instead for raw data simulation.

## Inputs

- ncomp (integer): number of compounds to simulate
- ncond (integer): number of experimental conditions
- ncpeaks (integer): number of peaks per condition
- nbatch (integer): number of batch effects to introduce
- nbpeaks (integer): number of peaks per batch
- npercond (numeric): allocation or proportion of peaks affected by condition effects
- nperbatch (numeric): allocation or proportion of peaks affected by batch effects
- batchtype (character): batch profile type (e.g., 'linear', 'random')
- db (database object): spectral database, typically hmdbcms (HMDB GC-MS) or monahrms1 (MoNA LC-HRMS)

## Outputs

- data matrix (numeric): feature table with compounds (rows) × samples (columns), intensity values
- group assignments (character vector): sample-level labels encoding condition and batch membership
- condition-only effect matrix (numeric): isolated condition effects on peak intensities
- batch-only effect matrix (numeric): isolated batch effects on peak intensities

## How to apply

Call mzrtsim() with parameters specifying: number of compounds (ncomp), conditions (ncond), and batches (nbatch); allocation of peaks per condition (npercond) and per batch (nperbatch); and batch profile type (batchtype, e.g., linear or random). The function generates a baseline feature matrix with ncpeaks peaks per condition and nbpeaks peaks per batch, then overlays condition-only effects (modulating intensities across ncond conditions) and batch-only effects (applying nbatch batch factors with type-specific profiles). The returned list contains the combined feature table, group assignments (condition + batch labels), and separate matrices for condition-only and batch-only effects, allowing downstream tools to assess whether normalization recovered true condition signals while removing known batch artifacts.

## Related tools

- **mzrtsim** (primary R package providing mzrtsim() function for feature table simulation with condition and batch effects) — https://github.com/yufree/mzrtsim
- **simmzml** (companion function in mzrtsim for raw data simulation (.mzML files) as input to peak-picking before feature-table generation) — https://github.com/yufree/mzrtsim
- **mzrtsim_se** (wrapper function to integrate simulated feature tables into SummarizedExperiment objects for Bioconductor workflow compatibility) — https://github.com/yufree/mzrtsim
- **R** (runtime environment for executing mzrtsim package functions)
- **BiocManager** (package manager for installing mzrtsim from Bioconductor)
- **hmdbcms** (built-in HMDB GC-MS spectral database object for realistic compound MS/MS profiles) — https://hmdb.ca/downloads
- **monahrms1** (built-in MoNA LC-HRMS spectral database object for high-resolution LC-MS profiles) — https://mona.fiehnlab.ucdavis.edu/downloads

## Examples

```
mzrtsim(ncomp=100, ncond=3, ncpeaks=50, nbatch=4, nbpeaks=30, npercond=0.3, nperbatch=0.2, batchtype='linear', db=hmdbcms)
```

## Evaluation signals

- Returned data matrix has correct dimensions: compounds × samples (ncomp compounds; ncond × nbatch samples).
- Group assignments vector matches sample count and correctly encodes all condition–batch combinations.
- Condition-only and batch-only effect matrices are non-zero and have expected direction (e.g., linear batch effects monotonically increase/decrease with batch index).
- Downstream batch correction tool recovers condition signal by removing batch effects while preserving condition-only matrix signal in normalized feature table.
- Reproducibility: identical input parameters and random seed produce identical output across runs.

## Limitations

- Simulation assumes peak intensities scale linearly with condition and batch factors; real data may exhibit non-linear, interactive, or hierarchical batch effects.
- batchtype parameter supports only predefined profiles (e.g., linear, random); custom or instrument-specific batch models are not directly supported.
- Spectral database (hmdbcms, monahrms1) must be pre-loaded or downloaded; simulations are constrained to compounds present in the selected database.
- Simulated data lacks realistic chromatographic artifacts (peak tailing, co-elution, matrix suppression); use simmzml() for raw data simulation if these are required.
- No direct support for missing data (NA, below-detection-limit intensity) common in real metabolomics; all peaks are simulated at positive intensities.

## Evidence

- [intro] mzrtsim() generates feature tables with controlled condition and batch effects for benchmarking normalisation and batch correction methods.: "`mzrtsim()` generates feature tables with controlled condition and batch
effects for benchmarking normalisation and batch correction methods."
- [other] mzrtsim() accepts parameters ncomp, ncond, ncpeaks, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database) and returns a list including the data matrix, group assignments, and separate matrices for condition-only and batch-only effects.: "mzrtsim() accepts parameters ncomp, ncond, ncpeaks, nbatch, nbpeaks, npercond, nperbatch, batchtype, and db (hmdbcms database) and returns a list including the data matrix, group assignments, and"
- [other] Simulate condition-only effects by modulating peak intensities across ncond conditions according to npercond allocation and batch-only effects by applying nbatch batch factors with batchtype-specific profiles.: "Simulate condition-only effects by modulating peak intensities across ncond conditions according to npercond allocation. 4. Simulate batch-only effects by applying nbatch batch factors with"
- [intro] produces `.mzML` files from real spectral databases (MoNA, HMDB): "produces `.mzML` files from real spectral databases (MoNA, HMDB)"
- [intro] Generate simulated LC/GC-MS data at two levels: raw data simulation producing .mzML files with realistic chromatographic peak shapes, tailing, noise, and matrix background; peak list simulation producing feature tables with configurable condition effects and batch effects.: "Generate simulated LC/GC-MS data at two levels: raw data simulation producing .mzML files with realistic chromatographic peak shapes, tailing, noise, and matrix background; peak list simulation"
