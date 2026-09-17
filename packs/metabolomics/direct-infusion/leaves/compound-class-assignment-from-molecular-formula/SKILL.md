---
name: compound-class-assignment-from-molecular-formula
description: Use when after peaks have been filtered (by m/z, isotopic presence, and
  formula assignment error) and you have a list of peaks with assigned molecular formulas.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3407
  tools:
  - pandas
  - NumPy
  - Formularity
  - MetaboDirect
  techniques:
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- requires the Python dependencies NumPy [40], pandas [41, 42]
- It requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and
  is available to install through the Python Package Index... It requires the Python
  dependencies NumPy
- it has been designed to work with the output file (in .csv format) generated directly
  by Formularity [24] which uses FT-ICR MS data in .xml format
- it has been designed to work with the output file (in .csv format) generated directly
  by Formularity [24]
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# compound-class-assignment-from-molecular-formula

## Summary

Assigns biochemical compound classes (e.g., lipids, sugars, amino acids, lignin) to FT-ICR MS peaks based on their elemental composition in assigned molecular formulas. This classification is essential for interpreting metabolomic diversity and understanding the functional roles of detected compounds in biogeochemical cycling.

## When to use

Apply this skill after peaks have been filtered (by m/z, isotopic presence, and formula assignment error) and you have a list of peaks with assigned molecular formulas. Use it before calculating thermodynamic indices or performing chemodiversity analysis, as compound class context is required to stratify downstream analyses by biochemical function.

## When NOT to use

- Peaks lack assigned molecular formulas or have formula assignment error exceeding 0.5 ppm — the elemental composition is undefined.
- The analysis goal is structural isomer discrimination or retention time-based characterization — this skill assigns only broad biochemical classes, not stereoisomeric or positional information.
- Input is already a pre-classified feature table from a targeted metabolomics workflow (e.g., with vendor-supplied MRM transitions) — class assignment is redundant.

## Inputs

- CSV file with peak m/z values, assigned molecular formulas (elemental composition C/H/N/O/S/P), and peak intensities
- Predefined compound class classification lookup table (Supplementary Table 1)

## Outputs

- Annotated peak table with compound class labels appended to each peak
- Compound class frequency and abundance distributions across samples
- Class-stratified diversity metrics and composition plots

## How to apply

For each filtered peak with an assigned molecular formula, extract its elemental composition (C, H, N, O, S, P counts). Compare the elemental composition against predefined classification criteria (provided in Supplementary Table 1 of the source article) to determine which biochemical class the compound belongs to. The classification scheme distinguishes among major organic compound families (lipids, carbohydrates, proteins, nucleic acids, lignin, tannins, and others) based on ratios and presence/absence of key heteroelements. This deterministic lookup produces a discrete class label for each peak, enabling stratified analysis of molecular diversity and transformation networks by compound type.

## Related tools

- **Formularity** (Computes elemental composition from assigned molecular formulas prior to class lookup)
- **MetaboDirect** (Orchestrates the full filtering, classification, and downstream analysis pipeline; implements class assignment as Step 4 of data pre-processing) — https://github.com/Coayala/MetaboDirect
- **pandas** (Loads and manipulates the peak table and merges class labels with intensity and formula data)

## Evaluation signals

- Every retained peak (post-filtering) receives exactly one discrete compound class label with no nulls.
- Class distribution matches known biochemical expectations for the sample type (e.g., soil and peat samples typically yield high proportions of lignin and tannin signatures).
- Elemental composition rules are applied consistently: e.g., peaks with N ≥ 1 and C ≥ 3 are classified as amino acids or proteins; peaks with O/C ratio > 0.5 and C < 30 suggest carbohydrates.
- Class-stratified Van Krevelen diagrams and elemental composition plots show expected clustering (e.g., lignin in the upper-left region of H/C vs. O/C space).
- Subsequent thermodynamic index calculations (NOSC, ΔG°C-ox, AImod) agree with known redox and stability trends for each class.

## Limitations

- Classification is deterministic and based solely on elemental composition; it cannot distinguish structural isomers or positional variants within a class.
- FT-ICR MS direct injection lacks chromatographic separation, so compounds that co-ionize or suffer from ion suppression may not be detected, biasing class abundance estimates.
- The predefined classification scheme (Supplementary Table 1) is specific to natural organic matter and may require customization for other sample types (e.g., pharmaceutical or synthetic metabolites).
- Peaks with ambiguous or ambiguous elemental compositions (e.g., from low signal-to-noise detections or high mass errors) may be misclassified or filtered out before reaching this step.

## Evidence

- [other] Determine compound classes for retained peaks based on assigned molecular formula using predefined classification criteria (Supplementary Table 1).: "Compound classes of each of the filtered peaks are then determined based on the assigned molecular formula"
- [intro] FT-ICR MS can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin).: "DI-MS has ample coverage and can detect a wide range of compounds (e.g., lipids, sugars, amino acids, or lignin)"
- [other] Classification occurs as part of data pre-processing before thermodynamic index calculation.: "calculating several thermodynamic and molecular indices based on each peak's elemental composition"
- [abstract] Class assignments enable stratified chemodiversity and downstream analysis workflows.: "the analysis (e.g., chemodiversity analysis, multivariate statistics)"
