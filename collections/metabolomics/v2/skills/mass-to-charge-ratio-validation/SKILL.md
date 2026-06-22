---
name: mass-to-charge-ratio-validation
description: Use when after loading MS-Dial feature tables (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) and before sample-level filtering or imputation, whenever the feature abundance matrix contains m/z values acquired across multiple chromatographic runs or polarities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - margheRita
  - R
  - MS-Dial
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1101/2024.06.20.599545v1
  title: MargheRita
- doi: 10.1101/2024.06.20.599545
  title: ''
evidence_spans:
- The R package margheRita addresses the complete workflow for metabolomic profiling in untargeted studies based on liquid chromatography (LC) coupled with tandem mass spectrometry (MS/MS)
- The R package margheRita addresses the complete workflow for metabolomic profiling
- The R package margheRita addresses the complete workflow
- The R package margheRita
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_margherita_cq
    doi: 10.1101/2024.06.20.599545v1
    title: MargheRita
  dedup_kept_from: coll_margherita_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.06.20.599545v1
  all_source_dois:
  - 10.1101/2024.06.20.599545v1
  - 10.1101/2024.06.20.599545
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-to-charge-ratio-validation

## Summary

Excludes metabolomic features with implausible or instrument-artifact m/z values by filtering based on mass defect thresholds. This preprocessing step removes spurious signals that arise from instrument noise or acquisition artifacts before downstream statistical and identification analysis.

## When to use

Apply this skill after loading MS-Dial feature tables (e.g., Urine_RP_NEG_norm.txt or Urine_RP_POS_norm.txt) and before sample-level filtering or imputation, whenever the feature abundance matrix contains m/z values acquired across multiple chromatographic runs or polarities. Use it if your dataset exhibits features with m/z decimal components that are biologically implausible or fall within known instrumental artifact ranges.

## When NOT to use

- Input is already a curated feature table from a commercial or vendor-validated preprocessing pipeline that has already removed m/z artifacts.
- Your study uses only a single, well-characterized instrument run with known stable calibration; instrumental artifacts are negligible.
- You are analyzing targeted metabolomics data where features have been pre-selected by expert knowledge and validated against authentic standards; mass defect filtering may remove valid low-abundance metabolites.

## Inputs

- MS-Dial feature table (text file: e.g., Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt)
- margheRita data structure (after loading MS-Dial output)
- Feature abundance matrix with m/z and feature annotations

## Outputs

- Filtered feature abundance matrix (features with artifact m/z values removed)
- Retained feature count and exclusion report (e.g., 548/604 features retained)
- Feature metadata with m/z validation flags

## How to apply

The filtering() function in margheRita applies mass defect validation by removing features whose m/z decimal values fall within the range [4, 8] by default. This range captures common acquisition artifacts. Load the MS-Dial output as a margheRita data structure, then invoke the filtering function with the m/z filtering step enabled. The rationale is that true metabolites have m/z values distributed across the full decimal range; clustering within [4, 8] signals instrumental or chemical noise. On the Urine dataset, this step reduced features from 604 to 548 (56 features removed, ~9% of total), confirming artifact removal without excessive feature loss. Verify the threshold is appropriate for your instrument and polarity by inspecting the m/z distribution histogram before and after filtering.

## Related tools

- **margheRita** (Provides the filtering() function that implements mass defect-based m/z validation on MS-Dial output feature tables) — https://github.com/emosca-cnr/margheRita
- **MS-Dial** (Peak picking software that generates the input feature tables (Urine_RP_NEG_norm.txt, Urine_RP_POS_norm.txt) subject to m/z validation)
- **R** (Runtime environment for executing margheRita filtering functions)

## Examples

```
filtered_data <- filtering(urine_data, mass_defect_range = c(4, 8))
```

## Evaluation signals

- Feature count before and after m/z filtering matches reported retention (e.g., 604 → 548 features on Urine dataset implies ~56 features removed).
- Histogram of m/z decimal values shows gap or depletion in the [4, 8] range post-filtering, confirming artifact removal.
- No features with m/z decimal values in [4, 8] remain in the output feature table.
- Sample count is unchanged (filtering is feature-level only; e.g., 243/243 samples retained on Urine dataset).
- Downstream statistical tests and metabolite identification show improved specificity or reduced false-positive annotations compared to unfiltered data.

## Limitations

- The default m/z decimal range threshold [4, 8] is empirically determined from the Urine dataset and may not generalize to other instrument types, chromatographic methods, or polarities; validation on your own data is recommended.
- Mass defect filtering alone cannot distinguish between true low-abundance metabolites and instrument noise; it is most effective when combined with sample-level and feature-level missing-value filtering.
- Features with valid metabolite annotations that happen to fall within [4, 8] m/z decimal range risk false-positive exclusion; inspection of removed features against spectral libraries is prudent.
- The skill assumes m/z values are properly calibrated by MS-Dial; miscalibration will render this filtering step ineffective.

## Evidence

- [other] removes features with m/z decimal values within the range [4, 8] by default: "removes features with m/z decimal values within the range [4, 8] by default, and (3) imputes remaining NA values"
- [other] On the Urine dataset, this retained 243/243 samples, 604/604 features after NA filtering, and 548/604 features after m/z filtering: "On the Urine dataset, this retained 243/243 samples, 604/604 features after NA filtering, and 548/604 features after m/z filtering."
- [intro] runs filters to exclude features/sample with many missing values, features with wrong m/z values: "runs filters to exclude features/sample with many missing values, features with wrong m/z values"
- [intro] filtering by mass defects, filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization: "filtering by mass defects, filtering by coefficient of variation (samples vs QCs) and probabilistic quotient normalization"
- [intro] margheRita is intended to be used after having done a number of data acquisition steps through MS-Dial: "margheRita is intended to be used after having done a number of data acquisition steps through MS-Dial"
