---
name: lipid-retention-time-rule-application
description: Use when you have candidate lipid annotations from spectral library matching
  (e.g., XCMS + CAMERA output) with MS/MS scores, and you need to reduce false positives
  and predict previously unannotated lipids.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - XCMS
  - CAMERA
  - LipidIN (LCI Module)
  - RaMS
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear
  peak alignment, matching and identification.'
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-retention-time-rule-application

## Summary

Apply three relative retention time (RRT) rules from the Lipid Categories Intelligence model to filter and classify candidate lipid annotations, reducing false positive identifications while predicting unannotated lipids. This skill re-evaluates high-scoring spectral matches using retention time relationships across species cohorts to achieve a 5.7% estimated false discovery rate.

## When to use

You have candidate lipid annotations from spectral library matching (e.g., XCMS + CAMERA output) with MS/MS scores, and you need to reduce false positives and predict previously unannotated lipids. Apply this skill when you have retention time measurements across multiple species or cohorts and want to leverage inter-lipid retention time relationships as a secondary validation filter for annotations that passed initial spectral matching.

## When NOT to use

- Retention time data is unavailable or inconsistent across samples/species; RRT rules require reliable RT measurements.
- Input is already a curated, high-confidence lipid feature table without candidate annotations; this skill is for ranking and filtering candidates, not de novo identification.
- Single-sample or single-species analysis with no cross-cohort retention time intervals to compute; RRT rules rely on interval comparisons across groups.

## Inputs

- Spectral query results (CSV or tabular format with candidate lipid annotations, m/z, retention time, spectral match scores from hierarchical fragmentation library matching)
- Retention time measurements per lipid per species/cohort
- Processed mzML mass spectrometry data (or .rda format after preprocessing with XCMS/RaMS)

## Outputs

- Filtered lipid predictions (CSV) with classification (true/false positive)
- False discovery rate (FDR) metric per analysis
- Lipid coverage count (total unique lipids identified)
- Annotated lipid list with predicted unannotated lipids and RRT rule assignments

## How to apply

Load spectral query results containing candidate lipid annotations with their retention times and spectral match scores. Extract relative retention time (RRT) values for each candidate by computing retention time intervals across species cohorts (normalizing to a reference lipid or cohort). Apply the three RRT rules from the Lipid Categories Intelligence model to classify candidates as true or false positives based on whether observed RRT values conform to expected RRT patterns for each lipid class. Aggregate predictions across all species, calculate the false discovery rate (FDR) as a quality metric, and count unique lipid identifications (coverage). Export filtered lipid predictions with FDR and coverage statistics. The RRT rules use heuristic search algorithms with spectral match scores as prior information to re-evaluate high-score matches.

## Related tools

- **XCMS** (Peak alignment, matching, and preprocessing of mass spectrometry data prior to spectral querying and RRT rule application)
- **CAMERA** (Compound spectra extraction and annotation of LC/MS data; provides candidate annotations fed into RRT filtering)
- **LipidIN (LCI Module)** (Implements the three relative retention time rules and heuristic search algorithm for lipid classification and FDR reduction) — https://github.com/LinShuhaiLAB/LipidIN
- **RaMS** (Data preprocessing and format conversion (mzML to .rda) before RRT rule application)

## Examples

```
source('LCI.r'); LCI(filename='QC_POS1.rda')
```

## Evaluation signals

- False discovery rate is reported and ≤5.7% estimated FDR (or meets study-specific threshold); validate by comparing to orthogonal methods (e.g., manual curation, reference standards).
- Lipid coverage (total unique lipid identifications) increases or remains consistent after RRT filtering; document count of true positives retained vs. false positives removed.
- RRT values for retained lipids conform to expected retention time patterns (e.g., longer-chain or more saturated lipids elute later); spot-check a sample of predicted annotations against literature or authenticated standards.
- Output CSV contains required columns: lipid name, m/z, retention time, spectral match score, RRT rule classification, and FDR flag; no missing or malformed entries.
- Cross-species coherence: lipid predictions from the same lipid class should exhibit consistent RRT patterns across species cohorts (within acceptable retention time drift).

## Limitations

- RRT rules assume consistent chromatographic behavior across species and samples; matrix effects, column degradation, or instrument drift can inflate false discovery rate.
- The 5.7% FDR estimate is based on the 168.6 million lipid hierarchical library used in LipidIN; performance may vary with different or smaller libraries, different ionization modes ([M+COOH]⁻ vs [M+CH₃COO]⁻), or non-standard sample types.
- Requires multi-sample or multi-species data to compute meaningful retention time intervals; single-sample analysis cannot leverage cross-cohort RRT patterns.
- Performance depends on quality of prior spectral matching; if spectral library is incomplete or has systematic biases, RRT rules alone cannot overcome poor initial candidates.
- Multitasking environments can cause file accessibility issues in the LCI module; serial or controlled parallel execution is recommended.

## Evidence

- [other] Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence model to filter and classify candidates as true or false positives.: "Extract relative retention time (RRT) values for each candidate lipid and compute retention time intervals across species cohorts. Apply the three RRT rules from the Lipid Categories Intelligence"
- [readme] The Lipid Categories Intelligence (LCI) Module: Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches.: "Based on the relative position of primary information, it conducts heuristic searches using secondary matching scores as prior information to re-evaluate high-score matches."
- [readme] three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate"
- [other] Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications).: "Aggregate predictions across all species and calculate false discovery rate (FDR) and total lipid coverage (count of unique lipid identifications)."
- [readme] When using the negative ion mode, please ensure to extract the neg_ALL.zip file beforehand. ESI: 'p' for positive ionization mode, 'n1' for negative ionization mode [M+COOH]−, 'n2' for negative ionization mode [M+CH3COO]−.: "ESI: 'p' for positive ionization mode, 'n1' for negative ionization mode [M+COOH]−, 'n2' for negative ionization mode [M+CH3COO]−."
