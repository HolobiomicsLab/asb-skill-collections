---
name: retention-time-alignment-evaluation
description: Use when you have run an NPP tool (XCMS, MZmine 2, etc.) on mzML files
  and need to assess whether the alignment stage preserved peak detection fidelity
  and isotopologue abundance ratios.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3373
  - http://edamontology.org/topic_0092
  tools:
  - mzRAPP
  - XCMS
  - R
  - enviPat
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing
  (NPP)
- You can then assess the performance of NPP runs we have performed via XCMS
- Download the XCMS- and MZmine 2-output files from [ucloud]
- library(mzRAPP)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mzrapp_cq
    doi: 10.1093/bioinformatics/btab231/6214530
    title: mzRAPP
  dedup_kept_from: coll_mzrapp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# retention-time-alignment-evaluation

## Summary

Evaluate the accuracy of retention-time (RT) alignment in non-targeted preprocessing (NPP) tools by comparing aligned feature tables against a benchmark of known RT boundaries. This skill quantifies alignment losses, peak retention rates, and isotopologue ratio (IR) degeneration post-alignment.

## When to use

Apply this skill when you have run an NPP tool (XCMS, MZmine 2, etc.) on mzML files and need to assess whether the alignment stage preserved peak detection fidelity and isotopologue abundance ratios. Use it when you have both unaligned and aligned feature tables from the same NPP run and a benchmark CSV with known m/z, RT boundaries, and isotopologue identifiers for 2870+ target peaks.

## When NOT to use

- Isotopologue ratio bias filtering has already been applied (filtering removes isotopologues with >30% ratio deviation before comparison)
- Input NPP output lacks distinct unaligned and aligned feature tables, or alignment was not performed as a separate step
- Target molecules in the benchmark do not have retention-time boundaries defined for all predicted isotopologues

## Inputs

- Benchmark CSV file with columns: m/z, retention-time boundaries (user.rtmin, user.rtmax), isotopologue identifiers, adduct types, and optional sample-specific RT overrides
- NPP unaligned feature table (CSV) with detected m/z values, retention times, and peak identifiers
- NPP aligned feature table (CSV) with aligned m/z values, aligned retention times, and peak identifiers

## Outputs

- Matched record CSV table containing benchmark peak identifier, matching status ('found', 'split', 'missing', 'misaligned'), matched NPP feature ID (if found), confidence scores, and isotopologue validation flags
- Peak Picking box output: count of found peaks vs. 2870 benchmark total, split-peak count, isotopologue-ratio quality percentage
- Alignment box output: peak retention rate percentage, IR degeneration percentage, alignment-induced losses
- Post Alignment box output: final peak detection percentage, final IR degeneration percentage

## How to apply

Load the benchmark CSV (containing m/z, retention-time boundaries, isotopologue IDs, and adduct types) and both unaligned and aligned NPP feature tables into mzRAPP. Apply m/z matching at 6 ppm precision and 5 ppm accuracy tolerance, then narrow candidates using RT windowing to the expected chromatographic boundaries. For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter isotopologues with isotopologue ratio bias exceeding 30%. Classify each benchmark peak as 'found', 'split', 'missing', or 'misaligned' by comparing matches across unaligned and aligned tables. Extract three metrics from the Alignment and Post Alignment boxes: peak retention rate (peaks found post-alignment / peaks found pre-alignment), IR degeneration percentage (peaks with >30% ratio bias), and alignment-induced losses (discrepancy between unaligned and aligned detection %). Record intermediate and final metrics to validate performance against expected ranges (e.g., 83–94% post-alignment detection, 28–53% IR degeneration for XCMS run 1).

## Related tools

- **mzRAPP** (Performs m/z and RT matching, isotopologue validation, and generates alignment performance metrics via the Setup NPP assessment and View NPP assessment tabs) — https://github.com/YasinEl/mzRAPP
- **XCMS** (Produces unaligned and aligned feature tables that are evaluated for alignment fidelity and isotopologue ratio preservation)
- **enviPat** (Predicts isotopologue patterns and boundaries for target molecules; mzRAPP uses enviPat-predicted isotopologues to validate benchmark peaks)
- **R** (Scripting environment for programmatic benchmark generation and NPP assessment when not using the mzRAPP Shiny interface)

## Examples

```
library(mzRAPP); callmzRAPP() # Then: Load Benchmark.csv → Setup NPP assessment tab → select XCMS_unaligned_run1.csv and XCMS_aligned_run1.csv → Execute → View NPP assessment tab → extract Alignment box (peak retention rate, IR degeneration %) and Post Alignment box (final detection %, IR degeneration %)
```

## Evaluation signals

- Matched record table contains no null matching statuses; all 2870 benchmark peaks are classified as 'found', 'split', 'missing', or 'misaligned'
- Post-alignment detection percentage is within expected range for the tool (e.g., 83–94% for XCMS run 1, 93–99% for XCMS run 3, 82–92% for MZmine 2)
- IR degeneration percentage post-alignment matches expected range (e.g., 28–53% for XCMS run 1, 3–20% for XCMS run 3, 1–9% for MZmine 2)
- Alignment-induced losses (decrease in peak retention from unaligned to aligned) are ≤ 12% for well-performing tools; losses >20% signal misalignment failure
- All filtered isotopologues (removed due to peak shape correlation <0.85 or ratio bias >30%) are explicitly flagged in the matched record table

## Limitations

- Benchmark generation requires manual RT boundary curation for each target molecule; boundaries must intersect with extracted ion chromatogram at ≥5% of maximum peak height or peaks will be rejected
- Isotopologue filtering removes peaks with Pearson correlation <0.85 to the most abundant isotopologue, which may discard true low-abundance isotopologues if peak detection is poor
- m/z matching tolerance (6 ppm precision, 5 ppm accuracy) is instrument-dependent and may require calibration for lower-resolution or poorly tuned instruments
- Alignment evaluation is only as reliable as the benchmark; missing or incorrectly bounded target peaks in the benchmark will cause false negatives in NPP tool assessment
- Split-peak classification (one benchmark peak matched to multiple NPP features) may indicate genuine co-elution in NPP output rather than alignment failure

## Evidence

- [other] For each benchmark peak, apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features.: "For each benchmark peak, apply m/z matching with specified precision tolerance (6 ppm) and accuracy threshold (5 ppm) to candidate NPP features."
- [other] Apply retention-time windowing to narrow candidate matches to the expected chromatographic boundaries provided in the benchmark.: "Apply retention-time windowing to narrow candidate matches to the expected chromatographic boundaries provided in the benchmark."
- [other] For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%.: "For isotopologue clusters, validate peak shape correlation with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%."
- [methods] In the Post Alignment box, we see that now about 93-99% of peaks have been detected, which is quite some improvement. Also, the proportion of degenerated IR decreased to 3-20%.: "In the Post Alignment box, we see that now about 93-99% of peaks have been detected, which is quite some improvement. Also, the proportion of degenerated IR decreased to 3-20%."
- [other] Inspect the View NPP assessment tab outputs: Peak Picking box (found peaks vs. 2870 benchmark total, split-peak count, isotopologue-ratio quality), Alignment box (peak retention rate, IR degeneration), and Post Alignment box (final peak detection %, IR degeneration %): "Inspect the View NPP assessment tab outputs: Peak Picking box (found peaks vs. 2870 benchmark total, split-peak count, isotopologue-ratio quality), Alignment box (peak retention rate, IR"
