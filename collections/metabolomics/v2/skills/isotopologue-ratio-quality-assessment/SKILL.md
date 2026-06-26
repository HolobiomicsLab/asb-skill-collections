---
name: isotopologue-ratio-quality-assessment
description: Use when evaluating the reliability of non-targeted data pre-processing
  (NPP) tools (XCMS, MZmine 2, MS-DIAL, etc.) on known metabolite peaks.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - mzRAPP
  - XCMS
  - R
  - MZmine 2
  - enviPat
  techniques:
  - mass-spectrometry
  license_tier: open
  provenance_tier: literature
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
- Below we provided one more example for MZmine2
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

# isotopologue-ratio-quality-assessment

## Summary

Validate the peak abundance quality and isotopologue ratio (IR) integrity of chromatographic peaks by comparing detected isotopologue abundances against predicted isotopic patterns. This skill assesses whether non-targeted pre-processing tools faithfully preserve isotopologue peak shapes and abundance ratios, which are indicators of data integrity in metabolomics benchmarking.

## When to use

Apply this skill when evaluating the reliability of non-targeted data pre-processing (NPP) tools (XCMS, MZmine 2, MS-DIAL, etc.) on known metabolite peaks. Use it after peak detection and alignment steps to quantify the proportion of peaks exhibiting degraded isotopologue ratios, which indicates either misalignment, peak splitting, or abundance quantification errors that compromise downstream metabolite identification confidence.

## When NOT to use

- Input data consists of single-isotope features only (no isotopologue clusters to compare) — isotopologue-ratio assessment requires at least two resolvable isotopologues per peak
- NPP output lacks reliable peak shape or abundance information — the skill depends on detection of peak boundaries and intensity values for both major and minor isotopologues
- Benchmark peak definitions lack enviPat-predicted isotopologue boundaries or retention-time windows — the matching and filtering logic requires chromatographic boundaries for all predicted isotopologues

## Inputs

- Benchmark dataset CSV containing 47+ target molecules with 157+ features (all adducts and isotopologues) and 2870+ total peaks with m/z, retention time boundaries, and enviPat-predicted isotopologue identifiers
- NPP unaligned feature table CSV (e.g., XCMS_unaligned_run1.csv or MZmine_unaligned folder containing 30 individual feature CSVs)
- NPP aligned feature table CSV (e.g., XCMS_aligned_run1.csv or MZmine_aligned.csv)
- mzML centroided mass spectrometry files from which peaks were originally detected

## Outputs

- Degenerated isotopologue ratio percentage (%) reported separately for peak-picking, alignment, and post-alignment stages
- Matched record table classifying each benchmark peak as 'found', 'split', 'missing', or 'misaligned' with confidence scores and isotopologue validation flags
- Peak-by-peak isotopologue quality report showing Pearson correlation coefficient and abundance bias for each isotopologue cluster
- Interactive sunburst and line-plot visualizations showing distribution of isotopologue quality across benchmark molecules

## How to apply

For each benchmark peak with multiple isotopologues, calculate the Pearson correlation coefficient between the detected peak shape and the theoretically most abundant isotopologue, filtering out isotopologues with correlation < 0.85 or abundance deviation > 30% from predicted values. Classify peaks as 'degenerated IR' if they fail these criteria. Aggregate the proportion of degenerated isotopologue ratios across all benchmark peaks in the pre-alignment, alignment, and post-alignment stages. Compare the degenerated IR percentage across different NPP tools or parameter sets to identify which configurations best preserve isotopic fine structure. mzRAPP automates this calculation by loading benchmark peak definitions (with enviPat-predicted isotopologue abundances and retention-time boundaries), matching them to NPP-detected feature tables using m/z tolerance (typically 6 ppm precision, 5 ppm accuracy) and RT windowing, then reporting the proportion of matched peaks with IR bias exceeding 30%.

## Related tools

- **mzRAPP** (Primary tool for matching benchmark peaks to NPP output and calculating degenerated IR metrics across all three workflow stages) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Generates predicted isotopologue patterns and validates isotopic fine structure for each target molecule)
- **XCMS** (Example non-targeted pre-processing tool whose outputs (unaligned and aligned feature tables) are assessed for IR quality degradation)
- **MZmine 2** (Example non-targeted pre-processing tool whose outputs are assessed for IR quality degradation in post-alignment stage)
- **R** (Statistical and computational environment for running mzRAPP library and performing isotopologue validation calculations)

## Examples

```
library(mzRAPP); callmzRAPP() # then load benchmark CSV, select NPP tool (XCMS or MZmine 2), specify unaligned and aligned feature tables, and inspect View NPP assessment tab for degenerated IR % in Peak Picking, Alignment, and Post Alignment boxes
```

## Evaluation signals

- Degenerated IR percentage reported for XCMS run 1 matches literature range of 28–53%; XCMS run 3 matches 3–20%; MZmine 2 matches 1–9% — confirms correct calculation of isotopologue bias thresholds
- Benchmark peaks are classified consistently across unaligned and aligned stages: a peak matching as 'found' in both stages should show improvement (lower IR degeneration) in post-alignment output if alignment succeeded
- Peak-by-peak Pearson correlation coefficients for isotopologue clusters cluster bimodally (high > 0.85 vs. low < 0.85), indicating clear filtering boundary at correlation threshold
- Total number of 'found' benchmark peaks plus 'split' peaks plus 'missing' peaks equals 2870 (the total benchmark size), confirming exhaustive classification without gaps or double-counting
- Isotopologue abundance bias values (% deviation from predicted) show mean < 15% for high-quality peaks and > 30% for filtered-out isotopologues, confirming 30% threshold discriminates signal from degradation

## Limitations

- Isotopologue-ratio assessment assumes at least two isotopologues are present and chromatographically resolvable; peaks for which only the monoisotopic form is detected or for which isotopologues co-elute cannot be validated using this approach
- The 30% abundance-deviation and 0.85 correlation thresholds are empirically derived from the MTBLS267 benchmark dataset; their generalizability to other instruments, ionization modes, or metabolite classes is not established in the article
- Peak shape correlation calculation requires sufficient chromatographic resolution and scan density; very narrow or under-sampled peaks may yield unreliable Pearson coefficients regardless of true isotopologue quality
- Assessment depends on accurate retention-time boundaries provided in the benchmark target file; if user-provided RT windows are too narrow or too wide, isotopologues may be incorrectly filtered or missed

## Evidence

- [methods] isotopologue ratio (IR)-metric reports 28-53% degenerated IR: "the isotopologue ratio (IR)-metric reports 28-53% degenerated IR"
- [methods] proportion of degenerated IR decreased to 3-20%: "the proportion of degenerated IR decreased to 3-20%"
- [methods] peak shape correlation with most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%: "validate peak shape correlation with the most abundant isotopologue and filter isotopologues where isotopologue ratio bias exceeds 30%"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 are removed: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed"
- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all enviPat-predicted isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
