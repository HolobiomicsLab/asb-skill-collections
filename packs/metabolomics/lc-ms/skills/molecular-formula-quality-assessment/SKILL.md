---
name: molecular-formula-quality-assessment
description: Use when immediately after formula assignment from raw FT-ICR MS peak detection, when you have a peak intensity matrix with assigned molecular formulas and need to remove spurious or low-confidence assignments before calculating thermodynamic indices, determining compound classes, or performing.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - pandas
  - NumPy
  - Formularity
  - MetaboDirect
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- requires the Python dependencies NumPy [40], pandas [41, 42]
- It requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and is available to install through the Python Package Index... It requires the Python dependencies NumPy
- it has been designed to work with the output file (in .csv format) generated directly by Formularity [24] which uses FT-ICR MS data in .xml format
- it has been designed to work with the output file (in .csv format) generated directly by Formularity [24]
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# molecular-formula-quality-assessment

## Summary

Quality assessment and filtering of molecular formula assignments from FT-ICR MS data using error thresholds and presence criteria. This skill removes unreliable formula assignments and low-confidence peaks before downstream analysis, ensuring that only high-quality molecular identifications are retained for metabolomic characterization.

## When to use

Apply this skill immediately after formula assignment from raw FT-ICR MS peak detection, when you have a peak intensity matrix with assigned molecular formulas and need to remove spurious or low-confidence assignments before calculating thermodynamic indices, determining compound classes, or performing statistical analysis. Specifically, use it when formula assignment error or peak prevalence (number of samples containing each peak) is available and variability in data quality across peaks is expected.

## When NOT to use

- Input peaks already have validated formula assignments from orthogonal methods (e.g., MS/MS fragmentation or reference standards); additional mass-error-based filtering may be redundant or overconservative.
- All peaks in the dataset are known to be genuine (e.g., spiked standards or synthetic mixtures); prevalence filtering is unnecessary.
- Formula assignment error information is not available or is unreliable (e.g., calibration failed for portions of the m/z range); do not force-apply a threshold without justification.

## Inputs

- CSV file with detected peaks: m/z values, assigned molecular formulas, formula assignment error (ppm), peak intensities (columns = samples)
- User-defined formula error threshold (ppm; default 0.5)
- User-defined sample prevalence threshold (minimum number of samples peak must appear in)

## Outputs

- Filtered peak abundance matrix (CSV): peaks meeting both error and prevalence criteria, with intensities
- Filtered molecular formula list (CSV): assigned formulas for retained peaks
- Quality report: count of peaks removed at each filter stage, count of peaks retained

## How to apply

Load the detected peaks CSV containing m/z values, assigned molecular formulas, formula assignment errors, and peak intensities across samples using pandas. Remove peaks whose formula assignment error exceeds 0.5 ppm—the threshold that balances ultra-high mass accuracy of FT-ICR MS against realistic calibration drift. Then filter by sample prevalence: exclude peaks absent in fewer samples than a user-defined threshold (e.g., ≥2 samples), removing singleton or near-singleton detections that may reflect noise or instrument artifacts. The rationale is that mass error filtering removes chemically implausible assignments, while prevalence filtering removes sporadic detections unlikely to represent true metabolites. Document the number of peaks retained at each filtering stage for quality control reporting.

## Related tools

- **pandas** (Load, filter, and manipulate peak intensity and formula CSV matrices; apply row-wise filtering logic for error threshold and sample presence criteria) — https://pandas.pydata.org/
- **NumPy** (Vectorized filtering operations on error arrays and presence matrices) — https://numpy.org/
- **Formularity** (Upstream tool that performs initial molecular formula assignment; outputs assignment error values consumed by this filtering skill)
- **MetaboDirect** (Encapsulating pipeline; filtering and normalization step implemented as part of data pre-processing phase before downstream chemodiversity and statistical analysis) — https://github.com/Coayala/MetaboDirect

## Examples

```
import pandas as pd; peaks = pd.read_csv('detected_peaks.csv'); filtered = peaks[peaks['formula_error_ppm'] <= 0.5]; filtered = filtered[filtered.drop(columns=['m/z', 'formula', 'formula_error_ppm']).gt(0).sum(axis=1) >= 2]; filtered.to_csv('filtered_peaks.csv', index=False)
```

## Evaluation signals

- Peak count decreases in two discrete steps: first after applying 0.5 ppm error threshold, then further after applying sample prevalence threshold; no negative peak counts or unexpected jumps.
- All remaining peaks have formula assignment error ≤ 0.5 ppm (verify via histogram or summary statistics).
- All remaining peaks appear in ≥ user-defined sample threshold; verify via row-wise 'number of non-zero entries' count.
- Intensity matrix dimensions are consistent before and after filtering (same number of sample columns; fewer rows after filtering).
- Filtered formula list is subset of original formula list; no new formulas introduced, no formula values altered.

## Limitations

- The 0.5 ppm error threshold is empirically chosen for FT-ICR MS but may not apply to other mass spectrometry platforms (e.g., Orbitrap, Q-TOF) which have different mass accuracy characteristics.
- Sample prevalence threshold is user-defined and dataset-specific; no universal rule exists. Low thresholds (e.g., 1 sample) retain rare metabolites but risk noise; high thresholds (e.g., >50% samples) enforce consistency but discard conditionally-expressed compounds.
- Filtering does not account for peak intensity magnitude or signal-to-noise ratio; high-intensity noise peaks with good mass accuracy may pass filters incorrectly.
- Mass error alone does not guarantee chemical validity; isobaric compounds or non-metabolite contaminants may have valid formula assignments and pass filtering. Subsequent compound class validation and thermodynamic index checks are needed.

## Evidence

- [methods] Remove peaks with formula assignment error exceeding 0.5 ppm and peaks absent in fewer samples than the user-defined threshold.: "Remove peaks with formula assignment error exceeding 0.5 ppm and peaks absent in fewer samples than the user-defined threshold."
- [methods] Filter peaks by m/z range (user-defined) and remove isotopic peaks (13C). Remove peaks with formula assignment error exceeding 0.5 ppm and peaks absent in fewer samples than the user-defined threshold.: "Filter peaks by m/z range (user-defined) and remove isotopic peaks (13C). Remove peaks with formula assignment error exceeding 0.5 ppm and peaks absent in fewer samples than the user-defined"
- [methods] error in formula assignment (0.5 ppm): "error in formula assignment (0.5 ppm)"
- [other] MetaboDirect's filtering and normalization step applies multiple sequential filters (isotopic carbon removal, m/z-based filtering, formula assignment error thresholds) and uses SPANS to select an appropriate normalization method: "MetaboDirect's filtering and normalization step applies multiple sequential filters (isotopic carbon removal, m/z-based filtering, formula assignment error thresholds) and uses SPANS to select an"
- [methods] Load the input CSV file containing detected peaks, m/z values, molecular formulas, and peak intensities using pandas.: "Load the input CSV file containing detected peaks, m/z values, molecular formulas, and peak intensities using pandas."
