---
name: spectral-peak-filtering-by-mass-accuracy
description: Use when after molecular formula assignment has been performed on FT-ICR MS peaks (e.g., by Formularity or CoreMS), and before calculating thermodynamic indices, compound class assignments, or statistical analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3172
  tools:
  - pandas
  - NumPy
  - Formularity
  - CoreMS
  - MetaboDirect
  techniques:
  - mass-spectrometry
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

# spectral-peak-filtering-by-mass-accuracy

## Summary

Filter FT-ICR MS peaks by rejecting those with formula assignment errors exceeding a mass accuracy threshold (typically 0.5 ppm), ensuring only high-confidence molecular formula assignments are retained for downstream analysis. This step removes ambiguous or spurious peaks that would compromise metabolomic interpretation.

## When to use

After molecular formula assignment has been performed on FT-ICR MS peaks (e.g., by Formularity or CoreMS), and before calculating thermodynamic indices, compound class assignments, or statistical analysis. Use this skill when you have a peak abundance matrix with m/z values, assigned molecular formulas, and associated mass assignment error values, and you need to ensure formula quality before proceeding to chemodiversity or transformation network analysis.

## When NOT to use

- Input peaks lack assigned molecular formulas or mass error values—apply formula assignment first (e.g., Formularity).
- Mass accuracy threshold is unknown or instrument-specific calibration differs substantially from 0.5 ppm—consult instrument calibration before filtering.
- You need to retain all peaks for exploratory visualization regardless of assignment quality—consider filtering only for downstream statistical or network analysis, not visualization.

## Inputs

- Peak abundance CSV table with columns: m/z (observed), assigned molecular formula, mass assignment error (ppm)
- User-defined mass accuracy threshold (ppm)

## Outputs

- Filtered peak abundance matrix (subset of input, peaks with error > threshold removed)
- Summary statistics: count of peaks retained vs. rejected, error distribution

## How to apply

Load the peak abundance CSV containing m/z values, assigned formulas, and mass assignment error columns using pandas. Define a maximum allowable formula assignment error threshold (the article demonstrates 0.5 ppm as standard for FT-ICR MS). Retain only peaks where the absolute error between observed and theoretical m/z for the assigned formula is ≤ threshold. Remove all peaks exceeding this error cutoff. The rationale is that FT-ICR MS formula assignment relies on ultra-high mass accuracy; peaks with large errors indicate either misassignment or unresolvable ambiguity, and including them introduces systematic noise into downstream chemodiversity, statistical, and transformation network analyses. Document the number of peaks removed and the distribution of errors pre- and post-filtering.

## Related tools

- **pandas** (Load and filter peak abundance CSV tables by mass error threshold)
- **Formularity** (Upstream tool that assigns molecular formulas and generates mass assignment error values for filtering)
- **CoreMS** (Alternative upstream tool for signal processing and molecular formula assignment prior to error-based filtering)
- **MetaboDirect** (Complete FT-ICR MS pipeline that integrates this filtering step in its data pre-processing stage) — https://github.com/Coayala/MetaboDirect

## Examples

```
peaks_df = pd.read_csv('peaks_with_formulas.csv'); filtered_df = peaks_df[peaks_df['mass_error_ppm'].abs() <= 0.5]; filtered_df.to_csv('filtered_peaks.csv', index=False)
```

## Evaluation signals

- Verify output peak count is strictly ≤ input peak count and > 0; document number of peaks removed.
- Check that all retained peaks have mass assignment error ≤ specified threshold; spot-check a sample of rejected peaks to confirm error > threshold.
- Compare error distribution (mean, median, max) before and after filtering; post-filter distribution should show tighter clustering near zero.
- Confirm downstream analysis outputs (chemodiversity indices, Van Krevelen diagrams, transformation networks) are stable and show expected chemical class distributions, not artifacts from low-quality formula assignments.
- Verify that the filtered matrix is a true subset (all retained peaks exist in input) and that no duplicates were introduced.

## Limitations

- Threshold is instrument- and calibration-dependent; 0.5 ppm is standard for FT-ICR MS but may vary with tuning and sample complexity.
- Filtering by error alone does not resolve structural isomers with identical m/z; these will pass the filter but remain chemically ambiguous.
- Peaks near instrument detection limit may have larger errors and be preferentially removed, potentially biasing toward abundant species.
- Mass error is reported post-assignment; incorrect formula assignments (due to unresolved isobars or co-eluting isomers) may have low reported errors but be chemically wrong—this filter addresses error magnitude, not assignment correctness.

## Evidence

- [methods] Remove peaks with formula assignment error exceeding 0.5 ppm and peaks absent in fewer samples than the user-defined threshold.: "Remove peaks with formula assignment error exceeding 0.5 ppm and peaks absent in fewer samples than the user-defined threshold."
- [methods] Filter peaks by m/z range (user-defined) and remove isotopic peaks (13C).: "Filter peaks by m/z range (user-defined) and remove isotopic peaks (13C)."
- [methods] error in formula assignment (0.5 ppm): "error in formula assignment (0.5 ppm)"
- [intro] advances in analytical mass spectrometry techniques and in particular the introduction of high-resolution mass spectrometry (HR-MS) in the last 20 years have allowed for high-precision formula: "advances in analytical mass spectrometry techniques and in particular the introduction of high-resolution mass spectrometry (HR-MS) in the last 20 years have allowed for high-precision formula"
- [methods] Load the input CSV file containing detected peaks, m/z values, molecular formulas, and peak intensities using pandas.: "Load the input CSV file containing detected peaks, m/z values, molecular formulas, and peak intensities using pandas."
