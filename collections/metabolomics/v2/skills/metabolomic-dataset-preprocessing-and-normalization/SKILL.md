---
name: metabolomic-dataset-preprocessing-and-normalization
description: Use when you have raw or minimally processed FT-ICR MS peak tables in Formularity .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0943
  tools:
  - MetaboDirect
  - Python
  - R
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - Formularity
  - KEGGREST
  - vegan
  - SYNCSA
  - NumPy, pandas
  - R packages vegan, SYNCSA
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- Molecular transformation networks for each sample (mass difference network-based approach) are generated in this step
- The MetaboDirect pipeline consists of 6 major steps/categories (Fig. 1)
- The MetaboDirect pipeline was developed in Python 3.8 [38]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
---

# metabolomic-dataset-preprocessing-and-normalization

## Summary

Preprocessing and normalization of FT-ICR MS metabolomic data by filtering peaks on physicochemical criteria (m/z range, isotopic signature, formula assignment error, sample prevalence) and normalizing intensities to remove technical bias. This foundational step prepares Formularity .csv output (assigned molecular formulas, m/z values, peak intensities) for downstream chemodiversity and statistical analysis.

## When to use

You have raw or minimally processed FT-ICR MS peak tables in Formularity .csv format (columns: m/z, assigned formula, peak intensity across samples) and need to remove spurious peaks, isotopic duplicates, or low-confidence formula assignments before calculating molecular diversity indices or running multivariate statistics. Apply when sample-level presence thresholds or intensity normalization strategies must be decided to reduce noise and ensure robust downstream inference.

## When NOT to use

- Input data are already quality-filtered and intensity-normalized from a prior preprocessing pipeline; re-filtering risks over-processing and loss of true low-abundance features.
- Raw (unprocessed) mass spectrometry data in mzML, netCDF, or vendor-proprietary format; use signal processing and formula assignment tools (e.g., CoreMS, Formularity) first to generate the .csv input required here.
- Study design does not require sample-level comparisons or multivariate statistics (e.g., single-sample molecular characterization); filtering by sample prevalence is unnecessary.

## Inputs

- Formularity .csv file (one or more samples with columns: m/z, assigned molecular formula, peak intensity, isotopic label)
- User-specified m/z range filter (lower and upper bounds)
- Formula assignment error tolerance (ppm threshold, e.g., 0.5 ppm)
- Sample prevalence threshold (minimum number of samples in which a peak must be detected)
- Normalization method choice (e.g., quantile, reference-based, or user-defined)

## Outputs

- Preprocessed and normalized peak intensity table (filtered to peaks passing all criteria, intensities normalized)
- Preprocessing report (number of peaks removed by each filter stage, retention statistics)
- Metadata on filter decisions and normalization parameters applied

## How to apply

In MetaboDirect's preprocessing step, (1) filter detected peaks by m/z value range (user-specified input), (2) remove isotopic peaks (13C duplicates), (3) exclude peaks with formula assignment error exceeding 0.5 ppm, and (4) discard peaks absent in a user-defined minimum number of samples (sample prevalence threshold). After filtering, normalize peak intensities using a user-selected normalization method (options supported by MetaboDirect, including quantile and reference normalization). The rationale is to eliminate technical artifacts and low-confidence assignments that inflate false diversity estimates, while normalizing accounts for run-to-run ion suppression and instrument drift. These decisions directly impact downstream chemodiversity metrics (richness, evenness) and should be documented and tested for sensitivity.

## Related tools

- **MetaboDirect** (Implements the six-step preprocessing, filtering, and normalization pipeline; orchestrates m/z, isotope, ppm error, and sample prevalence filters followed by user-selected intensity normalization) — https://github.com/Coayala/MetaboDirect
- **Formularity** (Upstream signal processing and molecular formula assignment tool; generates the .csv input (m/z, formula, intensity) required by this skill)
- **NumPy, pandas** (Python libraries underlying MetaboDirect data filtering and normalization operations (vectorized filtering, normalization computation))
- **R packages vegan, SYNCSA** (Post-preprocessing diversity metric calculation; presume filtered, normalized input from this skill)

## Examples

```
metabodirect --input bacterium_phage.csv --mz_min 200 --mz_max 900 --ppm_error 0.5 --sample_prevalence 2 --normalization quantile --output preprocessed_normalized
```

## Evaluation signals

- Peak count reduction is monotonic across filter stages (m/z → isotope → ppm error → sample prevalence); document counts at each stage to verify no unexpected reversals.
- Normalized intensity distributions show reduced variance across samples for technical replicates or pooled quality-control samples; compare coefficient of variation before/after.
- Peaks retained after filtering satisfy all four criteria simultaneously: within m/z range, non-isotopic, ≤0.5 ppm formula error, present in ≥user_threshold samples.
- Downstream chemodiversity metrics (observed formula count, DBE distribution) and multivariate ordination (PCA, NMDS) are stable to moderate variations in prevalence threshold (e.g., ±1 sample); sensitivity analysis confirms robustness.
- Preprocessing report is complete and matches article benchmark expectations (e.g., bacterium-phage dataset: 36 samples, 495 avg peaks per sample before filtering; final count after filtering documented).

## Limitations

- Sample prevalence filtering is user-defined; overly stringent thresholds (high sample count requirement) remove rare but real metabolites, while lenient thresholds retain noise. No consensus threshold exists; exploratory threshold scans are recommended.
- Formula assignment error tolerance (0.5 ppm) is fixed in the article's benchmark but may be inappropriate for lower-resolution instruments or non-FT-ICR data; users must adapt.
- Normalization does not account for biological confounders (e.g., biomass differences between samples); intensity normalization is technical only and may require downstream abundance correction (e.g., relative or compositional normalization) before statistical inference.
- Peak presence/absence filtering assumes the underlying data matrix is sparse (many undetected peaks); dense matrices (all peaks detected in most samples) may lose little information and make filtering decisions less critical.
- MetaboDirect requires Cytoscape (3.8+) and multiple R/Python dependencies; installation and environment setup can be labor-intensive and platform-dependent.

## Evidence

- [methods] detected peaks are filtered by their m/z values (based on the user's input): "detected peaks are filtered by their m/z values (based on the user's input)"
- [methods] isotopic presence (13C peaks): "isotopic presence (13C peaks)"
- [methods] error in formula assignment (0.5 ppm): "error in formula assignment (0.5 ppm)"
- [methods] based on the number of samples that they are present in (threshold determined by the user): "based on the number of samples that they are present in (threshold determined by the user)"
- [methods] peak intensities are normalized in this step based on the user's input: "peak intensities are normalized in this step based on the user's input"
- [methods] data pre-processing: "6 major steps/categories (Fig. 1): (i) data pre-processing"
- [intro] Filtering and normalization of data: "Filtering and normalization ✔"
- [readme] MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above): "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"
