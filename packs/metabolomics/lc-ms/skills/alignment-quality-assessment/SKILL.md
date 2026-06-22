---
name: alignment-quality-assessment
description: Use when after retention time and m/z-based clustering have been applied to group features across samples in a multi-sample metabolomics study.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - JPA
  - R
  - XCMS
  techniques:
  - LC-MS
  - tandem-MS
derived_from:
- doi: 10.3390/metabo12030212
  title: JPA
evidence_spans:
- JPA is a comprehensive and integrated metabolomics data processing software.
- JPA is a comprehensive and integrated metabolomics data processing software
- '''JPA'' is written in R and its source code is publicly available'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_jpa_cq
    doi: 10.3390/metabo12030212
    title: JPA
  dedup_kept_from: coll_jpa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3390/metabo12030212
  all_source_dois:
  - 10.3390/metabo12030212
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# alignment-quality-assessment

## Summary

Evaluating the quality and consistency of metabolic feature alignment across multiple LC-MS samples by computing alignment statistics, coverage metrics, and cluster homogeneity. This skill is essential for validating that retention time and m/z-based consolidation of putative features has succeeded before downstream annotation.

## When to use

After retention time and m/z-based clustering have been applied to group features across samples in a multi-sample metabolomics study. Use this skill when you need to verify that the unified aligned feature table is reliable before proceeding to adduct and metabolite annotation, or when investigating why certain samples show unexpectedly low feature overlap.

## When NOT to use

- Input is already a pre-aligned feature table from external software (e.g. MS-DIAL, XCMS Online) — you would skip alignment entirely
- Single-sample analysis where no cross-sample consolidation is needed
- Data acquired in DIA (data-independent acquisition) or full-scan mode where MS2 recognition was explicitly avoided, as alignment assumptions may not hold

## Inputs

- feature table from individual samples (MS1 peak picking output)
- feature table from individual samples (MS2 recognition output)
- feature table from individual samples (targeted list extraction output)
- retention time tolerance window specification (seconds)
- m/z tolerance window specification (ppm or Da)

## Outputs

- aligned feature table in standardized format
- sample-to-feature coverage matrix
- alignment statistics (number of aligned features)
- alignment quality metrics

## How to apply

After the JPA alignment workflow (Part 5) applies retention time-based clustering within specified tolerance windows and m/z-based clustering to refine feature grouping, compute alignment statistics including (1) total number of aligned features retained post-clustering, (2) sample-to-feature coverage matrix showing which features appear in which samples and their frequency, and (3) alignment quality metrics that measure cluster homogeneity and consistency. Evaluate whether coverage is balanced across samples (indicating successful alignment) or whether particular samples show anomalous patterns (suggesting acquisition or preprocessing problems). The decision to proceed to annotation depends on whether quality metrics meet acceptable thresholds for your experimental design and instrument reproducibility.

## Related tools

- **JPA** (Performs retention time-based and m/z-based clustering to consolidate metabolic features across samples and computes alignment statistics and quality metrics) — https://github.com/HuanLab/JPA.git
- **XCMS** (Embedded within JPA; provides underlying peak picking and feature alignment algorithms) — https://rdrr.io/bioc/xcms/man/
- **R** (Programming environment in which JPA is written and executed for alignment and quality assessment)

## Evaluation signals

- Number of aligned features is consistent with prior knowledge of sample complexity and instrument performance for your compound class
- Sample-to-feature coverage matrix shows no extreme outliers (e.g., one sample with <50% feature detection while others have >90%), which would indicate acquisition or data quality issues
- Alignment statistics show stable clustering: features in the same cluster do not scatter beyond the specified retention time or m/z tolerance windows
- Aligned feature table exports successfully in standardized format compatible with downstream CAMERA annotation module
- Cross-sample comparison of the same metabolite standard(s) shows alignment of their expected m/z and retention time within the tolerance parameters

## Limitations

- Alignment quality depends critically on retention time reproducibility; retention time drift across samples (e.g., from column degradation or temperature variation) can inflate false negatives even within specified tolerance
- m/z-based clustering alone may conflate isobars or features differing by <1 Da; tolerance specification must balance sensitivity against specificity
- Coverage matrix may be skewed if samples have unequal biomass, extraction efficiency, or ionization efficiency — biological vs. technical reasons for missing features cannot be distinguished by alignment metrics alone
- The README notes that MS2 recognition should not be used on full-scan or DIA data; alignment behavior is not validated for those modalities

## Evidence

- [full_text] JPA includes an alignment workflow step (Part 5: Alignment) as part of its comprehensive metabolomics data processing pipeline that operates after feature extraction and before annotation.: "JPA includes an alignment workflow step (Part 5: Alignment) as part of its comprehensive metabolomics data processing pipeline that operates after feature extraction and before annotation"
- [full_text] Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows. 3. Apply m/z-based clustering to refine grouping and merge features with matching mass-to-charge ratios. 4. Generate alignment statistics including number of aligned features, sample-to-feature coverage matrix, and alignment quality metrics.: "Apply retention time-based clustering to group putatively identical features across samples within specified tolerance windows. Apply m/z-based clustering to refine grouping and merge features with"
- [readme] for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5.: "for multi-sample analysis, sample alignment is performed after feature extraction. It will be discussed in section 5"
- [readme] It also performs sample alignment, adduct and metabolite annotations.: "It also performs sample alignment, adduct and metabolite annotations"
- [readme] Please do not use this function when processing full-scan or DIA data set!: "Please do not use this function when processing full-scan or DIA data set"
