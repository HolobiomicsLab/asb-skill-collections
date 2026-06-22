---
name: mass-spectrometry-feature-detection-validation
description: Use when when you have processed LC-HRMS mzML files through a non-targeted preprocessing tool (e.g., XCMS, MZmine 2, MS-DIAL) and need to assess whether peak detection rates, isotopologue ratio fidelity, and alignment accuracy meet acceptable thresholds before downstream analysis.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3172
  tools:
  - mzRAPP
  - MZmine 2
  - R
  - XCMS
  - enviPat
  - Skyline
  - R (with mzRAPP library)
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
- Below we provided one more example for MZmine2
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
---

# mass-spectrometry-feature-detection-validation

## Summary

Quantitatively validate non-targeted mass spectrometry peak detection and alignment performance against a reference benchmark by comparing detected peaks, isotopologue integrity, and alignment error metrics across unaligned and aligned datasets from different preprocessing tools.

## When to use

When you have processed LC-HRMS mzML files through a non-targeted preprocessing tool (e.g., XCMS, MZmine 2, MS-DIAL) and need to assess whether peak detection rates, isotopologue ratio fidelity, and alignment accuracy meet acceptable thresholds before downstream analysis. Particularly useful when validating performance on metabolomics benchmarks where ground truth peak boundaries and isotopologue predictions are available.

## When NOT to use

- Input peak CSV files lack retention time boundaries or m/z values for isotopologues — benchmark generation and validation cannot proceed without this metadata.
- No reference benchmark dataset exists for your mzML files or target molecules — validation requires ground truth peak boundaries and isotopologue predictions.
- Preprocessing tool outputs are already feature-aggregated or in non-peak-level format (e.g., feature intensity matrix) — mzRAPP requires peak-level CSV data with individual peak boundaries.

## Inputs

- unaligned peak CSV files from non-targeted preprocessing tool (e.g., 30 mzML files exported as MZmine_unaligned folder)
- aligned peak CSV file from preprocessing tool (e.g., MZmine_aligned.csv)
- benchmark CSV file with 47+ target molecules, ≥157 features, known RT boundaries (user.rtmin, user.rtmax in seconds), molecular formulas (SumForm_c), and main adducts
- centroided mzML files (original raw data for benchmark generation)
- sample-group CSV mapping mzML filenames to experimental groups
- target-file CSV with molecule identifiers, composition, RT bounds, and optional per-file retention time ranges

## Outputs

- NPP assessment metrics: found peaks percentage, split peak count, degenerated isotopologue ratio (%), alignment error count, BM divergence
- Interactive NPP assessment plots: sunburst visualization of found/not-found peak distribution, line plot of peak abundance quality across samples
- Performance summary statistics with quality indicators per sample and per molecule
- Diagnostic comparison tables showing peak detection, isotopologue integrity, and alignment performance for each preprocessing tool/run tested

## How to apply

Load unaligned and aligned peak CSV outputs from your preprocessing tool alongside a reference benchmark dataset (containing known molecules with RT boundaries and predicted isotopologues) into mzRAPP. Execute the NPP assessment module, which extracts three key performance metrics from the View NPP assessment tab: (1) post-alignment found peaks percentage and degenerated isotopologue ratio (IR) from the Post Alignment box, (2) split peak count from the Peak Picking box, and (3) alignment error count from the Alignment Step box. Filter peaks by isotopologue quality (peak shape correlation ≥0.85 with most abundant isotopologue, IR bias <30%) before metric calculation. Generate sunburst and line plots showing peak detection distribution and abundance quality. Accept runs if detected peaks exceed 80–90% with <10% degenerated IR; flag runs with >20% degenerated IR or misalignment patterns for parameter retuning.

## Related tools

- **mzRAPP** (Primary assessment platform: loads unaligned/aligned peak CSVs, generates benchmark from mzML files, executes NPP assessment module, computes performance metrics, and generates diagnostic plots and summary statistics.) — https://github.com/YasinEl/mzRAPP
- **MZmine 2** (Example non-targeted preprocessing tool whose peak detection and alignment performance is validated against benchmark using mzRAPP.)
- **XCMS** (Alternative non-targeted preprocessing tool whose peak detection and alignment performance can be assessed via mzRAPP (referenced as comparative example).)
- **enviPat** (Library used by mzRAPP to predict isotopologue mass patterns and predict isotopologue peaks for target molecules during benchmark generation.)
- **Skyline** (Optional tool for manual peak curation and export of peak boundaries (user.rtmin/user.rtmax) to create target file input for mzRAPP benchmark generation.)
- **R (with mzRAPP library)** (Runtime environment; mzRAPP can be invoked programmatically via R scripts for batch assessment or integrated into larger analysis workflows.)

## Examples

```
library(mzRAPP); callmzRAPP() # Launch GUI; then: load 30 unaligned MZmine CSVs from MZmine_unaligned folder, load MZmine_aligned.csv, select benchmark dataset with 47 molecules, run NPP assessment module, export metrics and diagnostic plots from View NPP assessment tab.
```

## Evaluation signals

- Post-alignment detected peaks percentage falls in expected range (80–94% for established tools); values <70% or >99% warrant investigation of parameter drift.
- Degenerated isotopologue ratio (%) is <10% for well-tuned runs; ratio >20% indicates peak abundance distortion or poor peak boundary definition.
- Sunburst plot shows majority of peaks classified as 'found' (not 'split' or 'not found'); >30% missing or split peaks suggests detection failure.
- Peak shape correlation with most abundant isotopologue ≥0.85 for retained peaks; peaks below this threshold are correctly filtered out.
- Alignment error count (from Alignment Step box) is stable across replicates and tool runs; sudden spike indicates misalignment in chromatographic drift correction.

## Limitations

- Benchmark quality depends on accuracy of provided retention time boundaries (user.rtmin/user.rtmax) and target molecule list; missing or misspecified peaks cannot be validated.
- Isotopologue filtering (peak shape correlation ≥0.85, IR bias <30%) may be conservative, potentially discarding low-abundance isotopologues that are genuinely present but noisy.
- Performance metrics assume that the non-targeted tool exports peak-level CSV with individual peak boundaries and m/z values; tools that output only feature-level intensity matrices cannot be assessed.
- mzRAPP currently supports tools exporting peak lists in standard CSV format; proprietary binary formats or vendor-specific outputs may require prior conversion.
- Validation is restricted to molecules and RT ranges covered by the benchmark; tool performance on out-of-benchmark analytes remains unknown.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files."
- [methods] Three key performance metrics: post-alignment found peaks percentage, degenerated isotopologue ratio, and alignment errors: "Extract and validate the three key performance metrics from the View NPP assessment tab: (a) Post Alignment box for found peaks percentage and degenerated isotopologue ratio (IR), (b) Peak Picking"
- [methods] MZmine 2 post-alignment detected 82-92% of peaks with 1-9% degenerated isotopologue ratio: "In the <i>Post Alignment</i> box, we see that now about 82-92% of peaks have been detected, Which is, in our opinion, not bad but improvable. The proportion of degenerated IR is 1-9%"
- [readme] Isotopologue peaks removed if area/height >30% off predicted or Pearson correlation <0.85: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] Benchmark dataset contains 47 molecules with 157 features resulting in 2870 peaks total from MTBLS267: "If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870"
- [readme] NPP assessment inputs require centroided mzML files and exported peak CSV from preprocessing tools: "In order to generate a benchmark you need to provide your <b>centroided</b> mzML files. Conversion of files of different vendors to mzML as well as centroiding can be done by Proteowizards"
