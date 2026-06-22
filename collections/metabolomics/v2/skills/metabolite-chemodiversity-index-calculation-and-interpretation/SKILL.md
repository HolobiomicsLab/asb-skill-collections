---
name: metabolite-chemodiversity-index-calculation-and-interpretation
description: Use when you have peak-abundance data (after molecular formula assignment, peak filtering by m/z, isotope, ppm error, and sample presence thresholds) and you need to quantify and compare the molecular composition diversity across samples or conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
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
  - FT-ICR MS
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect
schema_version: 0.2.0
---

# metabolite-chemodiversity-index-calculation-and-interpretation

## Summary

Compute and interpret chemodiversity indices (e.g., richness, evenness, heterogeneity metrics) on filtered peak-abundance matrices from FT-ICR MS data to quantify the molecular complexity and compositional structure of natural organic matter or metabolite pools. This skill enables researchers to compare chemical diversity across samples, treatments, or environmental conditions.

## When to use

Apply this skill when you have peak-abundance data (after molecular formula assignment, peak filtering by m/z, isotope, ppm error, and sample presence thresholds) and you need to quantify and compare the molecular composition diversity across samples or conditions. Use it to detect how biological systems respond to changes in biotic or abiotic factors by measuring shifts in chemodiversity.

## When NOT to use

- Input peaks have not yet been assigned molecular formulas—chemodiversity requires elemental/structural knowledge.
- Peaks have not been filtered for isotopic presence, formula error tolerance (>0.5 ppm), or sample-presence thresholds—unfiltered noise will inflate apparent diversity artificially.
- Raw FT-ICR MS spectra have not yet undergone signal processing—MetaboDirect does not provide raw spectra preprocessing and requires pre-processed peak tables as input.

## Inputs

- peak-abundance .csv matrix (rows=peaks, columns=samples, values=normalized intensities)
- assigned molecular formula data (.csv with m/z, formula, compound class)
- sample metadata or grouping factors (treatment, environment, time point)

## Outputs

- chemodiversity index values per sample (richness, evenness, heterogeneity)
- PERMANOVA and NMDS/PCA ordination plots showing compositional groupings
- statistical comparison tables (p-values, effect sizes) across treatment groups
- .csv tables of index values and ordination scores for downstream analysis

## How to apply

After executing the MetaboDirect data pre-processing, diagnostics, and filtering steps (which remove peaks by m/z range, 13C isotopes, >0.5 ppm formula error, and user-defined sample-presence thresholds), invoke the chemodiversity analysis module. This step computes diversity indices (richness, evenness, heterogeneity) on the resulting filtered peak-abundance matrix using vegan and SYNCSA R packages. The indices are then used in conjunction with multivariate statistics (PERMANOVA, NMDS, PCA) to interpret patterns in molecular diversity. Key decision: chemodiversity indices are most meaningful when computed on peaks that have been consistently assigned molecular formulas and filtered to remove noise and isotopic duplicates.

## Related tools

- **MetaboDirect** (command-line pipeline for automated chemodiversity analysis module; orchestrates data pre-processing, filtering, and diversity index computation) — https://github.com/Coayala/MetaboDirect
- **vegan** (R package used for ordination (NMDS, PCA) and multivariate statistical testing (PERMANOVA))
- **SYNCSA** (R package for community assembly and diversity calculations on filtered peak-abundance matrices)
- **FT-ICR MS** (high-resolution mass spectrometry instrument providing peak abundance and m/z data as input to chemodiversity workflow)

## Examples

```
metabodirect -i peak_abundance.csv -f assigned_formulas.csv -c sample_metadata.txt --normalize --permanova --nmds --pca --output_dir results/
```

## Evaluation signals

- Chemodiversity indices (richness, evenness, heterogeneity) are computed for all samples without errors and vary appropriately by sample and treatment group.
- PERMANOVA p-values and effect sizes are reported; ordination plots (NMDS, PCA) show expected separation of sample groups if biological or environmental differences exist.
- Index values fall within expected ranges for the sample type (e.g., soil, water, microbial biofilm); extreme values warrant re-inspection of filtering parameters.
- All output .csv files (diversity indices, ordination coordinates) and visualization plots (Van Krevelen diagrams, composition plots) are generated without errors, matching the paper's reported runtime (<1 min for 36 samples, ~2 min for 120 samples).
- Filtering thresholds (m/z range, 0.5 ppm error, sample-presence threshold, 13C removal) are recorded and reproducible; results should be sensitive to these choices.

## Limitations

- MetaboDirect does not provide raw spectra data preprocessing; input must already be peak-abundance matrices with assigned molecular formulas.
- Chemodiversity analysis is restricted to peaks that pass filtering stages (isotopic presence, ppm error threshold ≤0.5, sample-presence thresholds); thresholds are user-determined and affect reproducibility.
- Web-based GUI software (e.g., MetaboAnalyst) provides only restrictive, non-customizable diversity analyses; MetaboDirect command-line approach requires Python/R competence.
- KEGG database querying and transformation network calculation are excluded from runtime benchmarks and may substantially increase total pipeline runtime; these steps are optional and not part of core chemodiversity analysis.
- Direct injection MS cannot separate chemical isomers and lacks fine resolving power relative to chromatographic methods; ion suppression or enhancement may confound downstream interpretation of diversity metrics.

## Evidence

- [intro] MetaboDirect pipeline consists of six main steps for the analysis of FT-ICR MS data: "MetaboDirect pipeline consists of six main steps for the analysis of FT-ICR MS data"
- [abstract] chemodiversity analysis is one of the main workflow steps: "for the analysis (e.g., chemodiversity analysis, multivariate statistics)"
- [methods] peak filtering is performed before chemodiversity analysis: "detected peaks are filtered by their m/z values, isotopic presence (13C peaks), error in formula assignment (0.5 ppm), and based on the number of samples that they are present in"
- [methods] ordination analyses such as NMDS and PCA are core to chemodiversity interpretation: "non-metric multidimensional scaling (NMDS) ordination, Principal Component Analysis (PCA), permutational analysis of variance (PERMANOVA)"
- [intro] environmental conditions influence chemodiversity interpretation: "Environmental conditions such as temperature, and water availability can strongly influence the microbial community structure and function and thus its interaction with NOM"
- [abstract] chemodiversity enables evaluation of FT-ICR MS data in greater depth: "showcase the exploration capabilities of the pipeline that will enable the research community to evaluate and interpret their data in greater depth and in less time"
- [methods] MetaboDirect does not provide raw spectra preprocessing: "MetaboDirect does not provide raw spectra data preprocessing"
- [intro] DI-ICR MS has analytical limitations affecting data interpretation: "drawbacks are its inability to separate chemical isomers, lack of fine resolving power, and most importantly signal suppression or enhancement that can confound downstream data analysis"
