---
name: feature-intensity-recovery-across-samples
description: Use when after sample alignment in untargeted LC-MS workflows, when the
  aligned feature table contains missing (NA or zero) intensity entries for features
  that are detected in some samples but fall below the instrument detection limit
  or are absent in others.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3557
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - manual expert review
  - SLAW
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-intensity-recovery-across-samples

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Recover missing feature intensity values in aligned LC-MS feature tables by recursively searching related samples at similar retention time and m/z to populate NA or below-detection intensities. This step follows peak picking and sample alignment to complete the feature matrix before downstream statistical or metabolomic analysis.

## When to use

After sample alignment in untargeted LC-MS workflows, when the aligned feature table contains missing (NA or zero) intensity entries for features that are detected in some samples but fall below the instrument detection limit or are absent in others. Particularly critical when processing large cohorts (hundreds to thousands of samples) where sparse detection across replicates is common.

## When NOT to use

- Input is a raw mzML or NetCDF file; gap-filling requires prior peak picking and alignment.
- Feature table contains no missing values (data are already complete).
- Analysis goal requires discriminating true absences from below-detection features; gap-filling may mask absence-presence patterns.
- Samples are unrelated singletons with no batch or replicate structure; recursion has no related samples to query.

## Inputs

- aligned feature table (CSV or mzTab format) with NA or zero entries for missing feature intensities
- retention time tolerance and m/z tolerance parameters (user-specified or auto-optimized)
- sample metadata defining batch and replicate relationships (optional but recommended)

## Outputs

- gap-filled feature table (CSV or mzTab format) with recovered intensity values
- feature completeness report (percentage of cells recovered per feature and sample)

## How to apply

Load the aligned feature table with missing intensity values from the prior alignment step. Apply a data recursion algorithm that, for each missing feature intensity, searches through related samples identified by retention time and m/z proximity to locate intensity values in alternate sample batches or replicates. The algorithm exploits the structure of replicate and batch relationships to infer missing values without interpolation. Fill the missing intensities using the recursively retrieved values while maintaining the sample-feature matrix structure. Output the completed feature table to CSV or mzTab format for downstream analysis. Parameter optimization (if enabled) automatically tunes recursion sensitivity and proximity thresholds.

## Related tools

- **Centwave** (Peak picking algorithm that precedes alignment and gap-filling; SLAW wraps it as one of three selectable peak pickers)
- **SLAW** (Complete untargeted LC-MS workflow embedding gap-filling by data recursion as a core processing step) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/mzML:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Completeness metric: percentage of missing cells filled before and after gap-filling (expect >90% recovery for well-replicated cohorts)
- Schema invariant: output feature table has no NA entries in intensity columns (or NA count significantly reduced from input)
- Retention time and m/z consistency: recovered intensities come from samples within user-specified tolerance windows (RT ±seconds, m/z ±ppm)
- Feature abundance distribution: recovered values should follow the distribution of detected values for the same feature (sanity check against extreme outliers)
- Sample coverage: each sample should retain or gain intensity values, not lose them; output matrix dimensions match input (rows=features, cols=samples)

## Limitations

- Gap-filling by data recursion depends on the existence of related samples (replicates, batches) with detectable feature intensities; singletons or poorly structured cohorts may yield limited recovery.
- The algorithm assumes that missing features are true below-detection events rather than biological absences; this may conflate technical absence with true absence in subsequent statistical tests.
- Requires careful parameter tuning (RT and m/z tolerances); overly permissive tolerances may recover intensities from non-matching features, while overly strict tolerances may leave gaps unfilled.
- SLAW only supports DDA (data-dependent acquisition) MS/MS; DIA-MS2 spectra are skipped, so gap-filling applies to MS1 features only.

## Evidence

- [other] SLAW includes gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts.: "SLAW includes gap-filling by data recursion as a processing step within its complete untargeted LC-MS workflow, following peak picking, sample alignment, and grouping of isotopologues and adducts."
- [other] Load aligned feature table with missing intensity values (NA or zero entries) from prior alignment step. Apply data recursion algorithm to identify features present in some samples but absent (below detection) in others. For each missing feature intensity, search recursively through related samples (by retention time and m/z proximity) to locate intensity values in alternate sample batches or replicates.: "For each missing feature intensity, search recursively through related samples (by retention time and m/z proximity) to locate intensity values in alternate sample batches or replicates."
- [readme] Automated parameter optimization for picking, alignment, gap-filling: "Automated parameter optimization for picking, alignment, gap-filling"
- [readme] Scalability: SLAW can process thousands of SAMPLES efficiently: "SLAW can process thousands of samples efficiently"
- [readme] All data must be centroided and of unique polarity: "All data must be centroided and of unique polarity"
