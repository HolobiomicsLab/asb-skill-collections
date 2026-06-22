---
name: lipid-fragmentation-pattern-recognition
description: Use when you have experimental tandem MS (MS/MS) spectra from lipid samples (in mzML format) and need to assign molecular identities and lipid classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - XCMS
  - CAMERA
  - RaMS
  - LipidIN Expeditious Querying (EQ) Module
  - LipidIN Lipid Categories Intelligence (LCI) Module
  techniques:
  - LC-MS
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

# lipid-fragmentation-pattern-recognition

## Summary

Recognize and match experimental MS/MS spectra against a hierarchical library of theoretical lipid fragmentation patterns to assign lipid identities with high throughput and reduced false discovery. This skill enables rapid annotation of lipids from mass spectrometry data by leveraging pre-computed fragmentation signatures organized by chain composition and double-bond locations.

## When to use

Apply this skill when you have experimental tandem MS (MS/MS) spectra from lipid samples (in mzML format) and need to assign molecular identities and lipid classes. Specifically, use it when: (1) you have processed MS1/MS2 peak data ready for library matching, (2) you need to screen against a large lipid chemical space (>100M potential structures), (3) speed and coverage matter more than de novo structure elucidation, and (4) false positive annotations are a concern (target FDR < 10%).

## When NOT to use

- Input spectra are from non-lipid molecules or organisms with atypical fragmentation patterns not represented in the 168.6M-entry library.
- You need de novo structure elucidation (this skill does pattern matching, not structure solving).
- Your MS/MS data have not been preprocessed (e.g., peaks not aligned, fragment lists not normalized) or are in unsupported formats (not mzML or .rda).

## Inputs

- Preprocessed MS/MS spectral data in .rda format (output from XCMS/RaMS preprocessing on mzML files)
- Hierarchical lipid fragmentation library (e.g., pos_ALL.rda or neg_ALL.rda, 168.6 million entries)
- MS1 and MS2 m/z tolerance parameters (ppm)
- Ionization mode identifier (positive, negative [M+COOH]−, or negative [M+CH3COO]−)

## Outputs

- Matched lipid identifications with scores and confidence metrics (CSV format)
- Reduced candidate lists after LCI false-positive filtering
- Annotated lipid species with assigned chain compositions and double-bond positions
- FDR-controlled lipid annotations covering 8,923+ lipid molecular species

## How to apply

Load the hierarchical lipid fragmentation library (168.6 million entries indexed by chain composition and double-bond locations) into an in-memory data structure optimized for rapid spectral similarity lookup. For each experimental MS/MS spectrum, compute cosine similarity or mass-error-tolerant fragment matching against library entries using MS1 m/z tolerance (typically 5 ppm) and MS2 m/z tolerance (typically 10 ppm). The expeditious querying module performs ~70 billion spectral queries per second by exploiting the hierarchical organization to prune the search space. Record all matches above a primary similarity threshold, then pass high-confidence hits to the Lipid Categories Intelligence (LCI) module, which applies three relative retention time rules to re-evaluate matches and reduce false positives. Filter results to achieve a target false discovery rate (reported as 5.7% for 8,923 lipids across species in the original work).

## Related tools

- **XCMS** (Upstream preprocessing: nonlinear peak alignment, matching, and MS1 feature extraction from raw mzML data before spectral matching)
- **CAMERA** (Compound spectra extraction and annotation strategy for LC/MS data sets, integrated into preprocessing pipeline)
- **RaMS** (Data preprocessing package to convert mzML format to .rda format with fragment normalization and MS2 filtering)
- **LipidIN Expeditious Querying (EQ) Module** (Core spectral matching engine; performs cosine similarity or mass-error-tolerant fragment matching at ~70 billion queries/second) — https://github.com/LinShuhaiLAB/LipidIN
- **LipidIN Lipid Categories Intelligence (LCI) Module** (Post-matching FDR control via heuristic re-evaluation using relative retention time rules; reduces false positives from 5.7% to target threshold) — https://github.com/LinShuhaiLAB/LipidIN

## Examples

```
source(paste(getwd(),'/EQ.r',sep='')); load(paste(getwd(),'/pos_ALL.rda',sep='')); EQ(filename='QC_POS1.rda', ppm1=5, ppm2=10, ESI='p')
```

## Evaluation signals

- Query throughput matches or exceeds ~70 billion spectral matches per second (wall-clock time < 1 sec for large spectra sets).
- False discovery rate on annotated lipids is ≤ 5.7% (validated against known standards or cross-species lipid assignments).
- All matched lipid identities include assigned chain compositions and double-bond location(s); no ambiguous or partial structures.
- Match scores (cosine similarity or normalized fragment match score) and MS1/MS2 m/z error residuals are within specified tolerances (5 ppm MS1, 10 ppm MS2 by default).
- LCI-filtered candidate lists show reduced recall of false positives compared to raw EQ output; validated by orthogonal retention time or tandem MS fragmentation rules.

## Limitations

- The 168.6M-entry library exhaustively covers only lipids with the chain compositions and double-bond isomers it explicitly indexes; novel or highly unusual lipid structures outside this space will not match.
- Performance depends on hierarchical library indexing into RAM; processing time is dominated by data format conversion (LCI module reports ~2 minutes for format conversion on the benchmark system).
- Relative retention time rules assume consistent chromatographic behavior across samples and species; they may fail on non-standard columns or severe matrix effects.
- False positive filtering (LCI) is tuned for an estimated 5.7% FDR across 8,923 lipids; FDR performance may vary on smaller, non-diverse lipid panels or outside the original biomarker discovery context.
- Requires preprocessing with XCMS/RaMS; raw mzML or other formats must be converted to .rda first, introducing a rate-limiting serialization step.

## Evidence

- [readme] LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations: "LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations"
- [readme] expeditious querying module speeds up to around 70 billion times' spectral querying in less than 1 second: "expeditious querying module speeds up to around 70 billion times' spectral querying in less than 1 second"
- [other] Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries: "Implement spectral querying logic using cosine similarity or mass-error-tolerant fragment matching to compare experimental MS/MS spectra against library entries"
- [readme] three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate: "three relative retention time rules to develop lipid categories intelligence model for reducing false positive annotations and predicting unannotated lipids with a 5.7% estimated false discovery rate"
- [other] Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid spectral similarity lookup: "Load the hierarchical lipid fragmentation library (168.6 million entries organized by chain composition and double-bond locations) into an indexed in-memory data structure optimized for rapid"
- [readme] MS2_filter: a value of 0-1, MS2 fragments with intensity lower than the MS2_filter*max intensity will be deleted: "MS2_filter: a value of 0-1, MS2 fragments with intensity lower than the MS2_filter*max intensity will be deleted"
