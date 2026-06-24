---
name: thermodynamic-molecular-index-calculation-from-elemental-composition
description: 'Use when when you have peak-abundance .csv files with assigned molecular
  formulas (elemental composition: C, H, O, N, P, S) from FT-ICR MS or high-resolution
  MS and need to characterize the redox and structural properties of the molecular
  pool—e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
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
  - vegan (R)
  - SYNCSA (R)
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39]
- develop MetaboDirect, an open‑source, command‑line‑based pipeline for the analysis
  (e.g., chemodiversity analysis, multivariate statistics)
- The MetaboDirect pipeline was developed in Python 3.8
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2
- It requires the Python dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Thermodynamic molecular index calculation from elemental composition

## Summary

Calculate thermodynamic and chemical indices (e.g., nominal oxidation state of carbon, hydrogen deficiency, aromaticity proxies) from assigned molecular formulas in FT-ICR MS datasets to quantify the oxidation state and structural properties of organic molecules. This skill enables rapid assessment of sample chemodiversity and biochemical transformation potential.

## When to use

When you have peak-abundance .csv files with assigned molecular formulas (elemental composition: C, H, O, N, P, S) from FT-ICR MS or high-resolution MS and need to characterize the redox and structural properties of the molecular pool—e.g., to compare chemodiversity between samples, track oxidation states across environmental gradients, or identify potential biochemical transformation networks based on mass differences and oxidation state shifts.

## When NOT to use

- Input peak data lacks assigned molecular formulas (e.g., only m/z and abundance available without elemental composition).
- Raw FT-ICR MS spectra have not yet undergone signal processing and molecular formula assignment.
- You need to separate chemical isomers or infer functional group-level detail; MetaboDirect computes bulk indices only, not full structure elucidation.

## Inputs

- Peak abundance .csv files (rows: peaks/molecular formulas, columns: sample IDs; values: ion abundances)
- Assigned molecular formulas with elemental composition (C, H, O, N, P, S counts per peak)

## Outputs

- Per-peak elemental composition indices (NOSC, DBE, O:C, H:C, aromaticity proxies)
- Per-sample aggregate chemodiversity metrics (mean NOSC, median O:C, etc.)
- Van Krevelen diagrams and elemental/molecular class composition plots
- .csv tables with computed indices for downstream statistical analysis

## How to apply

Starting from peak abundance matrices and their assigned molecular formulas (C, H, O, N, P, S counts), MetaboDirect calculates elemental composition-derived indices for each peak within the data pre-processing and data diagnostics workflow steps. For each assigned formula, compute nominal oxidation state of carbon (NOSC), double-bond equivalence (DBE), oxygen-to-carbon ratio (O:C), hydrogen-to-carbon ratio (H:C), and other aromaticity proxies. These indices are then aggregated per sample (e.g., mean NOSC, median O:C) and visualized in Van Krevelen diagrams and elemental composition plots. Apply no mass-difference filtering at this stage; use the full set of assigned peaks. The indices enable comparison of chemodiversity metrics and ordination analyses (PCA, NMDS) to assess how molecular composition varies across sample conditions. Verify that all assigned formulas have non-null elemental counts and that computed indices fall within expected ranges for natural organic matter (NOSC typically −3 to +1, O:C typically 0 to 1.2).

## Related tools

- **MetaboDirect** (Command-line pipeline that automates elemental composition-based index calculation, chemodiversity analysis, and visualization (Van Krevelen diagrams, composition plots) from peak abundance and assigned formula matrices.) — https://github.com/Coayala/MetaboDirect
- **NumPy** (Numerical computation library for vectorized calculation of indices from elemental count arrays.)
- **pandas** (Data manipulation and tabular I/O for peak-by-sample matrices and formula metadata.)
- **vegan (R)** (R package used by MetaboDirect for multivariate statistical analysis (PERMANOVA, NMDS) of aggregated chemodiversity metrics.)
- **SYNCSA (R)** (R package integrated into MetaboDirect for functional trait-based (trait = elemental composition index) community analysis.)

## Examples

```
metabodirect -i peaks_abundance.csv -f molecular_formulas.csv -o output_dir
```

## Evaluation signals

- All assigned molecular formulas (C, H, O, N, P, S counts) are non-null and yield valid elemental composition indices; no NaN or Inf values in output index tables.
- Computed NOSC values fall within expected range for natural organic matter (−3 to +1); O:C and H:C ratios are non-negative and consistent with stoichiometric constraints (H:C ≤ 2.5 for most organic molecules).
- Van Krevelen diagrams correctly plot O:C (y-axis) vs. H:C (x-axis) for all peaks with assigned formulas; peak densities in diagram match sample-specific molecular diversity patterns.
- Per-sample aggregate metrics (e.g., mean NOSC, median O:C) vary across sample conditions in a biologically plausible manner (e.g., oxidized samples show higher mean NOSC, reduced samples show lower mean NOSC).
- Downstream ordination analyses (PCA, NMDS on sample-level index vectors) produce statistically significant clustering or separation by condition; PERMANOVA p-value < 0.05 when comparing a priori groups.

## Limitations

- MetaboDirect does not perform raw spectra data preprocessing; molecular formula assignment must be completed upstream (e.g., CoreMS, Formularity) before index calculation.
- Elemental composition indices are bulk descriptors; they do not distinguish chemical isomers or provide functional group-level resolution.
- Signal suppression or enhancement in direct injection MS can confound downstream data analysis, skewing relative abundances and thus sample-level aggregate index estimates.
- Index calculations assume no systematic bias in formula assignment accuracy; a uniform ppm error threshold (0.5 ppm) is applied during pre-processing, but extreme outliers or systematic misassignments may distort index distributions.
- Results are limited to molecular formulas with assigned C, H, O, N, P, S; peaks that cannot be assigned are excluded from chemodiversity analysis.

## Evidence

- [intro] MetaboDirect pipeline consists of six main steps for the analysis of FT-ICR MS data: "MetaboDirect pipeline consists of six main steps for the analysis of FT-ICR MS data"
- [methods] Data pre-processing and diagnostics as pipeline steps: "(i) data pre-processing (ii) data diagnostics (iii) data exploration (iv) chemodiversity analysis"
- [methods] Compound classes determination from elemental composition: "Compound classes of each of the filtered peaks are then determined based on the assigned molecular formula"
- [abstract] Van Krevelen diagram visualization: "visualization (e.g., Van Krevelen diagrams, elemental and molecular class composition plots)"
- [abstract] Chemodiversity analysis capability: "for the analysis (e.g., chemodiversity analysis, multivariate statistics)"
- [results] Output format and performance on real datasets: "The main steps of the MetaboDirect pipeline (without KEGG database mapping or calculating transformation networks) took less than 1 min (~36 s)"
- [intro] Input data specification: "The pipeline accepts peak abundance and assigned molecular formula data produced after an initial processing of raw FT-ICR MS spectra or any other high-resolution MS technique"
- [readme] README installation and dependencies: "MetaboDirect requires Python (3.5 and above), R (4 and above) and Cytoscape (3.8 and above)"
