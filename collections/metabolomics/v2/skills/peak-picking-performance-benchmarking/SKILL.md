---
name: peak-picking-performance-benchmarking
description: Use when when you have completed non-targeted peak picking and alignment with tools such as MZmine 2, XCMS, or MS-DIAL on LC-HRMS mzML data and need to quantify performance metrics (found peaks %, degenerated isotopologue ratio, alignment errors) by comparing against a curated benchmark of known.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0602
  tools:
  - mzRAPP
  - MZmine 2
  - R
  - XCMS
  - enviPat
  - Skyline
  - MSconvert (ProteoWizard)
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioinformatics/btab231/6214530
  all_source_dois:
  - 10.1093/bioinformatics/btab231/6214530
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-picking-performance-benchmarking

## Summary

Quantitatively assess the reliability of non-targeted metabolomics data pre-processing peak detection and alignment using a reference benchmark dataset with known molecules, isotopologues, and retention time boundaries. This skill validates peak detection rate, isotopologue ratio integrity, and alignment accuracy against ground truth extracted from high-resolution mzML files.

## When to use

When you have completed non-targeted peak picking and alignment with tools such as MZmine 2, XCMS, or MS-DIAL on LC-HRMS mzML data and need to quantify performance metrics (found peaks %, degenerated isotopologue ratio, alignment errors) by comparing against a curated benchmark of known molecules with predicted isotopologues and manual retention time boundaries.

## When NOT to use

- Input mzML files are profile (not centroided) mode — requires prior centroiding via MSconvert or equivalent.
- Target molecules lack reliable retention time boundaries — mzRAPP requires user.rtmin and user.rtmax for each compound; manual curation (e.g. via Skyline) is prerequisite.
- Non-targeted output is already a feature matrix or consensus peaks without sample-level peak boundaries — assessment requires sample-level aligned/unaligned CSVs with m/z, retention time, and abundance per sample.

## Inputs

- centroided mzML files (set of 5 or more LC-HRMS data files)
- sample-group CSV file (sample_name, sample_group columns)
- target CSV file (molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax columns)
- instrument resolution list or enviPat instrument name
- aligned peak table CSV from non-targeted processing tool
- unaligned peak table CSV from non-targeted processing tool

## Outputs

- benchmark dataset (CSV with 47+ molecules, 157+ features, 2870+ peaks with validated isotopologues and retention boundaries)
- NPP assessment report with found/not-found peak counts and percentages
- post-alignment performance metrics (peak detection rate 82–99%, degenerated IR 1–53%)
- alignment error rate and BM divergence statistics
- interactive sunburst plot of peak classification (found, split, missing, misaligned)
- line plot of reported peak abundance quality and isotopologue ratio degradation
- diagnostic CSV exports of intermediate performance boxes

## How to apply

First, create a benchmark dataset by providing: (1) centroided mzML files, (2) a sample-group CSV mapping file names to experimental groups, (3) a target CSV listing molecules with molecular formula, main adduct (e.g. M+H), and user-defined retention time boundaries (user.rtmin/user.rtmax in seconds), and (4) instrument resolution parameters. mzRAPP generates extracted ion chromatograms for all enviPat-predicted isotopologues, filters isotopologues with >30% abundance bias or Pearson correlation <0.85 versus the most abundant isotopologue, and outputs a validated benchmark. Next, export aligned and unaligned peak tables (CSV format) from your NPP tool and load them into mzRAPP alongside the benchmark. Execute the NPP assessment module, selecting your tool type (e.g. 'MZmine'), which performs one-to-one matching between benchmark peaks and detected peaks. Extract three key metrics from the assessment output: (a) Post Alignment box: found peaks percentage and degenerated isotopologue ratio (IR) — degradation thresholds typically 1–9% for good performance; (b) Peak Picking box: total detected peaks and split peak count; (c) Alignment Step box: BM divergence and alignment error rate. Validate results using interactive sunburst visualizations (found vs. not-found peak distribution) and line plots of peak abundance quality.

## Related tools

- **mzRAPP** (primary assessment framework: loads benchmark and NPP outputs, performs peak matching, computes reliability metrics, generates visualizations and summary statistics) — https://github.com/YasinEl/mzRAPP
- **MZmine 2** (example non-targeted peak picking and alignment tool whose output (unaligned and aligned CSVs) is evaluated by mzRAPP)
- **XCMS** (alternative non-targeted peak picking and alignment tool; supports export of CSV outputs for mzRAPP assessment)
- **enviPat** (library for predicting isotopologue patterns and relative abundances from molecular formulas and instrument resolution)
- **Skyline** (optional manual peak curation tool for defining and exporting retention time boundaries for target molecules)
- **MSconvert (ProteoWizard)** (preprocessing tool to convert vendor-specific MS data to centroided mzML format required by mzRAPP)

## Examples

```
library(mzRAPP)
callmzRAPP()
# Then: (1) Load 30 _POS.mzML files from MTBLS267; (2) Select SampleGroups_MTBLS267.csv and Target_File_MTBLS267.csv; (3) Select instrument/resolution; (4) Run benchmark generation; (5) Load MZmine_unaligned.csv and MZmine_aligned.csv; (6) Execute NPP assessment module with tool='MZmine'; (7) Export metrics and plots.
```

## Evaluation signals

- Benchmark dataset validation: confirmed detection of all enviPat-predicted isotopologues for ≥47 target molecules with Pearson correlation ≥0.85 and abundance bias ≤30%.
- Post-alignment peak detection rate in expected range (82–99%) and degenerated isotopologue ratio (1–53%) consistent with published performance for the evaluated tool.
- Split peak count and alignment error rate reported in assessment output; sunburst plot shows clear classification of found vs. split vs. missing vs. misaligned peaks without NA or ambiguous assignments.
- Line plot of peak abundance quality shows smooth degradation pattern with no sudden jumps or inversions; isotopologue ratios remain proportional to prediction.
- Exported CSV intermediate performance boxes match numeric summaries in interactive assessment tab; total found + not-found peaks ≤ benchmark peak count.

## Limitations

- Benchmark generation requires manual retention time boundary curation for all target molecules; without accurate user.rtmin/user.rtmax, isotopologues may be rejected even if detected, artificially lowering benchmark completeness.
- Assessment is molecule-centric and requires ≥2 isotopologues per adduct to be valid; singly-charged or low-abundance adducts may not meet detection thresholds, limiting coverage for minor variants.
- Peak matching between benchmark and NPP output relies on m/z and retention time tolerances (user-configurable); misalignment of retention time windows or mass calibration drift between mzML processing and NPP may cause spurious not-found classifications.
- Isotopologue ratio degradation metric (IR bias <30% threshold) is global; localized mass calibration errors or ion suppression in specific compounds are not flagged separately.
- Assessment assumes that aligned/unaligned CSVs from the NPP tool are in the correct format; malformed peak tables (missing columns, inconsistent m/z/RT precision) will cause import failure or silent filtering without explicit error messages.

## Evidence

- [readme] The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN,..) in the realm of liquid chromatography high-resolution mass spectrometry (LC-HRMS).: "mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP; XCMS, XCMS3, MetaboanalystR 3.0, SLAW, XCMS-online, MZmine 2, MZmine 3, MS-DIAL, OpenMS, El-MAVEN,..) in the realm"
- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files. The resulting benchmark dataset is used to extract different performance metrics for NPP performed on the same mzML files.: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files. The resulting"
- [readme] In order to generate a benchmark you need to provide your centroided mzML files. Conversion of files of different vendors to mzML as well as centroiding can be done by Proteowizards MSconvert.: "In order to generate a benchmark you need to provide your centroided mzML files. Conversion of files of different vendors to mzML as well as centroiding can be done by Proteowizards MSconvert."
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] MZmine 2 post-alignment performance on the benchmark detected 82-92% of peaks with 1-9% degenerated isotopologue ratio.: "MZmine 2 post-alignment performance on the benchmark detected 82-92% of peaks with 1-9% degenerated isotopologue ratio."
- [methods] Execute the NPP assessment module in mzRAPP by selecting 'MZmine' as the non-targeted tool and running the comparison between unaligned, aligned, and benchmark data.: "Execute the NPP assessment module in mzRAPP by selecting 'MZmine' as the non-targeted tool and running the comparison between unaligned, aligned, and benchmark data."
- [methods] Extract and validate the three key performance metrics from the View NPP assessment tab: (a) Post Alignment box for found peaks percentage and degenerated isotopologue ratio (IR), (b) Peak Picking box for total peaks detected and split peak count, (c) Alignment Step box for BM divergence and alignment errors.: "Extract and validate the three key performance metrics from the View NPP assessment tab: (a) Post Alignment box for found peaks percentage and degenerated isotopologue ratio (IR), (b) Peak Picking"
