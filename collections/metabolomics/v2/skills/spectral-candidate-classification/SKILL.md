---
name: spectral-candidate-classification
description: Use when after performing spectral library matching of mass spectrometry peaks against a fragmentation library (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - XCMS
  - CAMERA
  - LipidIN LCI module
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# spectral-candidate-classification

## Summary

Apply relative retention time (RRT) rules to filter and classify lipid candidates from spectral library matches as true or false positives, reducing false discovery rate while maintaining coverage across multiple species. This skill uses heuristic RRT-based intelligence to re-evaluate high-confidence spectral matches and predict unannotated lipids.

## When to use

After performing spectral library matching of mass spectrometry peaks against a fragmentation library (e.g., via XCMS/CAMERA or the Expeditious Querying module), when you have multiple candidate lipid annotations per MS/MS spectrum and need to distinguish true positives from false positives using relative retention time relationships within and across species cohorts. This skill is especially valuable when working with unannotated lipids or when sample matrices or instrumentation differences introduce false-positive high-scoring matches.

## When NOT to use

- Input candidates lack retention time or chromatographic context (RRT rules require temporal alignment across cohorts).
- Single-species or single-sample analysis where cohort-level RRT intervals cannot be computed reliably.
- Spectral matching has already been validated by orthogonal methods (e.g., standards, MRM confirmation); re-filtering introduces redundant computational cost.

## Inputs

- Candidate lipid annotations from spectral library matching (CSV or RDA format with m/z, RT, MS2 matching scores, lipid class, chain composition)
- Relative retention time (RRT) values per candidate across species or sample cohorts
- Mass spectrometry data preprocessed to mzML or RDA format (for context)

## Outputs

- Classified lipid candidates (true/false positive verdicts)
- False discovery rate (FDR) metric aggregated across all species
- Total lipid coverage (count of unique lipid identifications)
- Filtered lipid predictions exported to CSV with FDR and coverage statistics

## How to apply

Load the output from spectral matching (candidate lipid annotations with MS1 and MS2 matching scores). Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species or sample cohorts. Apply the three RRT classification rules from the Lipid Categories Intelligence model to filter candidates—these rules leverage primary structural information (chain lengths, saturation, lipid class relationships) to heuristically re-evaluate whether high-scoring matches are plausible. Aggregate classifications across all spectra and cohorts to calculate the false discovery rate (FDR) and count of unique identified lipids. The classification output includes binary verdicts (true/false positive), allowing downstream filtering and export of high-confidence lipid identifications with associated FDR metrics.

## Related tools

- **XCMS** (Upstream peak alignment and initial MS1/MS2 feature extraction for generating candidate annotations)
- **CAMERA** (Isotope pattern and adduct annotation to enrich candidate feature tables before RRT-based classification)
- **LipidIN LCI module** (Implementation of the three RRT rules and heuristic classification logic; reads preprocessed RDA files and outputs filtered lipid verdicts) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source('./LCI.R'); LCI(filename='./demo_neg_CH3COO.rda')
```

## Evaluation signals

- False discovery rate remains at or near the reported 5.7% threshold when applied to multi-species cohorts with >100 lipid identifications.
- Lipid coverage (unique lipid count) is ≥8000 identifications across multiple species, confirming breadth of predictions.
- RRT intervals computed from cohorts show statistically significant separation between true and false positive candidates (e.g., Mann–Whitney U or Kolmogorov–Smirnov test p < 0.05).
- Exported filtered lipid table contains no duplicates and all entries have valid chain composition, class, and RRT statistics.
- Re-running the classifier on a held-out species or cohort yields FDR within 1–2% of the training cohort FDR, indicating stability.

## Limitations

- RRT-based classification assumes lipid class and chain-length relationships are conserved across species and sample types; violations (e.g., unusual lipid modifications, species-specific variations) may degrade performance.
- The three RRT rules were developed on a specific set of lipid standards and hierarchical library; transfer to non-covered lipid classes or novel modifications is not validated.
- Performance is sensitive to retention time calibration and alignment quality; poorly aligned or drift-prone chromatography may inflate false discovery rates.
- Multi-species cohorts with <50 spectra per species may yield unreliable RRT interval estimates, leading to unstable classification thresholds.

## Evidence

- [other] Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence model to filter and classify candidates as true or false positives.: "Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence"
- [other] The Lipid Categories Intelligence (LCI) Model achieves prediction of unannotated lipids with a 5.7% estimated false discovery rate, covering 8923 lipids across various species.: "prediction of unannotated lipids with a 5.7% estimated false discovery rate, covering 8923 lipids across various species"
- [readme] three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids"
- [readme] Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches.: "Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches."
- [other] Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications).: "Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications)."
