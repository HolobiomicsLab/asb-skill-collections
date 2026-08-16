---
name: feature-alignment-metabolomics
description: Use when you have detected multiple ion peaks from replicate injections
  of the same sample in untargeted metabolomics and need to consolidate them into
  a single feature table.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3933
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - openNAU
  - MetaQC
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21147/j.issn.1000-9604.2023.05.11
  all_source_dois:
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-alignment-metabolomics

## Summary

Consolidate detected ion peaks from replicate mass-spectrometry injections into unified metabolic features by aligning peaks across the mass-to-charge (m/z) and retention-time dimensions. This skill is essential in untargeted metabolomics workflows to reduce redundancy and generate a quantitative feature abundance matrix suitable for downstream statistical analysis.

## When to use

Apply this skill when you have detected multiple ion peaks from replicate injections of the same sample in untargeted metabolomics and need to consolidate them into a single feature table. Specifically, use it after peak detection has identified candidate signals across m/z and retention-time space but before intensity extraction and statistical comparison.

## When NOT to use

- Input is already a consolidated feature table with unified features across replicates
- Analysis involves targeted metabolomics with predefined m/z and retention-time windows (use targeted extraction instead)
- Peak detection has not been performed or no replicate injections are available

## Inputs

- detected ion peaks (m/z, retention time, intensity) from replicate sample injections
- peak detection output (usually as a feature list with m/z, retention time, and intensity per sample)

## Outputs

- feature abundance matrix (rows = features with m/z, retention time, and identifier; columns = sample intensities)
- unified feature table

## How to apply

After peak detection identifies ion signals across mass-to-charge and retention-time dimensions in replicate samples, perform peak alignment by matching peaks with similar m/z values (typically within a tolerance of 5–10 ppm) and retention-time windows (typically within 0.1–0.5 min). Group aligned peaks into unified features, resolving inconsistencies in m/z or retention time across replicates by computing consensus values (e.g., median m/z, mean retention time). Validate alignment quality by examining the distribution of within-feature m/z and retention-time variation; peaks that deviate significantly from the feature consensus may indicate misalignment or noise. Once grouping is complete, extract intensity values for each feature across all samples to compile into a feature abundance matrix with rows as features (identified by m/z, retention time, and a unique identifier) and columns as sample intensities.

## Related tools

- **openNAU** (performs raw mass data extraction, peak detection, peak alignment, and feature grouping for untargeted metabolomics) — https://github.com/zjuRong/openNAU
- **MetaQC** (quality control module within openNAU for validating peak alignment and feature extraction) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Feature abundance matrix has expected dimensions (number of features × number of samples) with no missing intensity values
- Within-feature m/z variation is below the specified alignment tolerance (typically < 5–10 ppm)
- Within-feature retention-time variation is below the specified alignment window (typically < 0.1–0.5 min)
- Each feature is assigned a unique identifier and possesses a consensus m/z and retention time
- Intensity values are non-negative and show expected sample-to-sample and replicate-to-replicate correlation patterns

## Limitations

- Peak alignment quality depends critically on m/z tolerance and retention-time window parameters; narrow tolerances may fragment true features, while wide tolerances may merge distinct metabolites
- Alignment assumes that retention time is reproducible across replicate injections; significant drift or instrumental variation will degrade feature grouping
- Co-eluting metabolites with similar m/z values may be incorrectly merged into a single feature, compromising quantification and identification
- The method does not distinguish between true metabolic features and instrumental artifacts or noise; quality control filtering is required downstream

## Evidence

- [other] Perform peak alignment and feature grouping to consolidate peaks from replicate injections into unified features.: "Perform peak alignment and feature grouping to consolidate peaks from replicate injections into unified features."
- [other] Extract intensity values for each feature across all samples and compile into a feature abundance matrix.: "Extract intensity values for each feature across all samples and compile into a feature abundance matrix."
- [other] Output the extracted feature table with rows as features (m/z, retention time, identifier) and columns as sample intensities.: "Output the extracted feature table with rows as features (m/z, retention time, identifier) and columns as sample intensities."
- [readme] It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks.: "It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
