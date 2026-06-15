---
name: ft-icr-ms-data-preprocessing-and-quality-control
description: Use when when you have raw or processed FT-ICR MS peak-abundance .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3375
  tools:
  - MetaboDirect
  - Python 3.8
  - R 4.0.2
  - NumPy
  - pandas
  - seaborn
  - matplotlib
  - vegan
  - SYNCSA
  - R vegan
  - Cytoscape FileTransfer
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis (e.g., chemodiversity analysis, multivariate statistics)
- The MetaboDirect pipeline was developed in Python 3.8
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2
- It requires the Python dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
---

# ft-icr-ms-data-preprocessing-and-quality-control

## Summary

Automated preprocessing and quality control of direct injection FT-ICR MS data prior to downstream analysis, involving peak detection filtering, isotope removal, mass accuracy validation, and intensity normalization to produce analysis-ready molecular abundance matrices.

## When to use

When you have raw or processed FT-ICR MS peak-abundance .csv files with assigned molecular formulas (m/z values, elemental composition, measured abundance across samples) and need to remove noise, isotopic artifacts, and low-confidence assignments before multivariate or chemodiversity analysis.

## When NOT to use

- Input is raw FT-ICR MS spectral data (uncalibrated .raw or .ms files): MetaboDirect requires pre-processed peak lists with assigned molecular formulas; it does not provide raw spectra preprocessing.
- Peak abundance matrix already curated, normalized, and validated by external QC software: applying redundant filtering may remove true biological signal.
- Analysis goal requires retention of isotopic ratios (13C/12C) for abundance quantitation: isotope filtering will eliminate needed data.

## Inputs

- peak-abundance .csv files (rows=peaks/m/z values, columns=samples, values=measured abundance)
- assigned molecular formula data (elemental composition C/H/O/N/S counts, calculated m/z, assignment error)
- sample metadata (optional: for threshold-based filtering)
- user-defined filtering parameters (m/z range, isotope filter flag, ppm error threshold, sample presence minimum)

## Outputs

- filtered peak-by-sample abundance matrix (.csv)
- peak metadata table with compound class assignments (.csv)
- data quality diagnostic plots (distribution of peaks retained/removed, mass accuracy histogram)
- normalized intensity matrix ready for multivariate analysis

## How to apply

The MetaboDirect pipeline applies sequential filtering to detected peaks: (1) filter by m/z range to exclude out-of-range ions; (2) remove 13C isotopic peaks to reduce redundancy; (3) apply strict mass accuracy threshold (0.5 ppm error in formula assignment) to exclude poor-quality assignments; (4) filter peaks by sample presence using a user-defined threshold (e.g., present in ≥ N samples) to remove rare, likely spurious peaks; (5) determine compound classes (e.g., CHO, CHON, CHONS) for each retained peak based on assigned molecular formula; (6) normalize peak intensities across samples using appropriate normalization method. These steps are executed automatically via a single command-line invocation, producing a curated peak-by-sample abundance matrix and metadata table ready for downstream analysis.

## Related tools

- **MetaboDirect** (Command-line pipeline orchestrating automated peak filtering, isotope removal, formula validation, normalization, and compound class assignment) — https://github.com/Coayala/MetaboDirect
- **NumPy** (Underlying numerical array operations for peak intensity normalization and matrix manipulation)
- **pandas** (Tabular data manipulation and filtering by sample presence, m/z range, and error thresholds)
- **R vegan** (Statistical normalization methods (e.g., Hellinger, log-ratio) applied during intensity normalization step)
- **Cytoscape FileTransfer** (Optional: export and visualization of filtered molecular networks for quality assessment)

## Examples

```
metabodirect -i peak_abundance.csv -mf molecular_formulas.csv -o output_dir --m_z_min 100 --m_z_max 900 --ppm_error 0.5 --remove_isotopes --sample_presence_min 2 --normalization_method hellinger
```

## Evaluation signals

- Output abundance matrix dimensions (rows × samples) match expected retained peak count after filtering thresholds applied; no NaN or negative values present.
- Mass accuracy distribution of retained peaks is centered near 0 ppm with all peaks within ±0.5 ppm error threshold; no peaks from rejected formula assignments appear in output.
- Isotope removal verified: 13C peaks absent from output; 12C counterparts present with expected natural abundance ratios in independent validation dataset.
- Normalized intensities scale consistently across samples (e.g., sum of intensities per sample should be similar or follow expected distributional assumption such as lognormal); before-and-after histograms show transition from skewed to normalized distribution.
- Diagnostic QC plots (e.g., peak retention counts, ppm error distribution, sample presence histogram) match user-supplied filter parameters and show expected filtering outcomes.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; input must be pre-processed by external signal-processing software (e.g., CoreMS, Formularity) to produce peak lists and assigned molecular formulas.
- Filtering thresholds (m/z range, ppm error, sample presence minimum, normalization method) are user-defined; no guidance provided for threshold selection specific to instrument, ionization mode, or biological context; suboptimal thresholds may remove true signal or retain noise.
- Isotope filtering assumes clean 13C peak assignment; if formula assignment errors are high, 13C filtering may incorrectly retain artifacts or remove true 13C isotopologues.
- Single-sample datasets or datasets with highly sparse peaks across samples may be adversely affected by stringent 'sample presence' filtering; no automatic adaptive threshold suggested.
- No explicit handling of ion suppression artifacts or signal enhancement bias documented in the article; filtering operates on post-ionization peaks without chemical context correction.

## Evidence

- [methods] detected peaks are filtered by their m/z values: "detected peaks are filtered by their m/z values"
- [methods] isotopic presence (13C peaks): "isotopic presence (13C peaks)"
- [methods] error in formula assignment (0.5 ppm): "error in formula assignment (0.5 ppm)"
- [methods] filtering by number of samples present: "based on the number of samples that they are present in (threshold determined by the user)"
- [methods] Compound classes determination and peak intensity normalization: "Compound classes of each of the filtered peaks are then determined based on the assigned molecular formula. ... peak intensities are normalized in this step"
- [abstract] Single command-line invocation: "MetaboDirect is superior in that it requires a single line of code to launch a fully automated framework"
- [intro] Pipeline accepts processed peak and formula data, not raw spectra: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra"
- [methods] MetaboDirect does not provide raw spectra preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [intro] Signal processing background: ion suppression and enhancement confound analysis: "signal suppression or enhancement that can confound downstream data analysis due to ion suppression"
