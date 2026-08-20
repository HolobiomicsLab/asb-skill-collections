---
name: metabolite-benchmark-peak-matching
description: Use when you have LC-HRMS mzML files processed by a non-targeted peak-detection
  tool (XCMS, MZmine 2/3, MS-DIAL, OpenMS, etc.) and want to quantify how many of
  a known set of target molecules (47+ compounds with isotopologues) were correctly
  detected, aligned, and preserved with intact isotopologue.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzRAPP
  - XCMS
  - R
  - MZmine 2
  - enviPat
  - Skyline
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

# metabolite-benchmark-peak-matching

## Summary

Quantitatively assess non-targeted metabolomics data pre-processing (peak detection, alignment, isotopologue integrity) by matching detected peaks against a curated benchmark dataset of known molecules with defined retention-time boundaries. This skill enables reliability metrics for tools like XCMS, MZmine, and MS-DIAL.

## When to use

You have LC-HRMS mzML files processed by a non-targeted peak-detection tool (XCMS, MZmine 2/3, MS-DIAL, OpenMS, etc.) and want to quantify how many of a known set of target molecules (47+ compounds with isotopologues) were correctly detected, aligned, and preserved with intact isotopologue ratios. Use this when you need to audit peak-picking sensitivity, alignment fidelity, and isotopologue degeneration across runs or compare performance of different NPP pipelines.

## When NOT to use

- You do not have a pre-curated target molecule list with known retention boundaries and isotopologue definitions; benchmark generation is a prerequisite.
- Your input peaks are already in a consolidated feature table (e.g., intensity matrix ready for multivariate analysis); this skill is for pre-processing QC, not downstream statistics.
- You are assessing untargeted discovery performance where ground truth is unknown; mzRAPP requires known reference molecules.

## Inputs

- Benchmark.csv (curated peak list with 2870 peaks, molecular identities, retention boundaries, isotopologue definitions)
- Unaligned peak list from NPP tool (e.g., XCMS_unaligned_run1.csv)
- Aligned peak list from NPP tool (e.g., XCMS_aligned_run1.csv)
- mzML file(s) used for NPP (optional, for Skyline export or manual inspection)

## Outputs

- Peak Picking metrics (found peaks count, split-peak count, isotopologue-ratio quality %)
- Alignment metrics (peak retention rate %, IR degeneration %)
- Post-Alignment metrics (final peak detection %, IR degeneration %)
- Intermediate stage losses (19–35% alignment losses example)
- Comparative performance summary (e.g., XCMS run 1 vs. run 3 vs. MZmine 2)

## How to apply

Load a pre-generated benchmark CSV (containing 2870 peaks from 47 molecules with 157 features) into mzRAPP alongside unaligned and aligned peak lists (e.g., XCMS_unaligned_run1.csv, XCMS_aligned_run1.csv). In the Setup NPP assessment tab, specify the tool, benchmark file, and aligned/unaligned outputs, then execute mzRAPP's matching algorithm. Extract metrics from three assessment boxes: Peak Picking (detected vs. 2870 benchmark, split-peak count, isotopologue-ratio quality), Alignment (retention-time losses, IR degeneration %), and Post-Alignment (final detection %, IR degeneration %). Validate that reported ranges fall within expected tolerance (e.g., 83–94% post-alignment detection, 28–53% IR degeneration for XCMS run 1; 93–99% and 3–20% for run 3). Record intermediate values to diagnose whether losses occur at peak-picking, alignment, or post-alignment stages.

## Related tools

- **mzRAPP** (Provides the Shiny UI and R backend for benchmark generation, peak matching, and NPP reliability assessment; orchestrates comparison of detected peaks against curated benchmark.) — https://github.com/YasinEl/mzRAPP
- **XCMS** (Example non-targeted peak-detection and alignment tool whose outputs (unaligned and aligned CSV) are assessed against the benchmark; source of run 1 and run 3 results in the workflow.)
- **MZmine 2** (Alternative non-targeted NPP tool; example outputs are compared against the same benchmark to show isotopologue ratio quality (1–9% degeneration).)
- **enviPat** (R package used by mzRAPP to predict isotopologue masses and adduct forms for target molecules during benchmark generation.)
- **Skyline** (External tool for manual peak curation and retention-time boundary export; generates the target file (user.rtmin/user.rtmax) that seed the benchmark.) — https://skyline.ms/project/home/software/Skyline/begin.view
- **R** (Execution environment for mzRAPP library; can run assessment via library(mzRAPP) and callmzRAPP() UI or R-script interface.)

## Examples

```
library(mzRAPP); callmzRAPP() # Load UI, then in Setup NPP assessment tab: select benchmark='Benchmark.csv', unaligned='XCMS_unaligned_run1.csv', aligned='XCMS_aligned_run1.csv', click Assess; read metrics from Peak Picking / Alignment / Post Alignment boxes.
```

## Evaluation signals

- Post-alignment peak detection % reported in the Post Alignment box matches the expected range (e.g., 83–94% for XCMS run 1, 93–99% for run 3).
- Isotopologue ratio (IR) degeneration % at post-alignment stage is within expected tolerance (28–53% for XCMS run 1; 3–20% for run 3; 1–9% for MZmine 2).
- Intermediate losses (Peak Picking, Alignment stages) sum approximately to final post-alignment metrics, with no unexplained discrepancies.
- Split-peak counts and missing-peak classifications are consistent with known isotopologue complexity (157 features × 47 molecules = 2870 peaks total).
- Degenerated IR isotopologues show Pearson correlation <0.85 or >30% area/height bias vs. theoretical, confirming filter logic was applied.

## Limitations

- Benchmark quality depends on accurate curation of retention-time boundaries (user.rtmin/user.rtmax) and target file composition; incorrect boundaries will systematically underestimate NPP performance.
- Filtering criteria (peak shape correlation <0.85, isotopologue ratio bias >30%, lowest isotopologue abundance threshold ≥0.05) are fixed in benchmark generation; tool does not yet support per-molecule or per-file tuning of these thresholds.
- Only molecules with at least two isotopologues detected are retained in the benchmark; singly-charged or rare-isotope features may be excluded, biasing reliability metrics toward abundant, multi-isotope peaks.
- Comparison is valid only between NPP tools applied to the same mzML file set; different source data invalidates cross-tool benchmarking.
- mzRAPP requires centroided mzML files; vendor-specific raw formats must be converted (e.g., via ProteoWizard MSconvert) before use.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files. The resulting benchmark dataset is used to extract different performance metrics for NPP performed on the same mzML files.: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files. The resulting"
- [methods] XCMS run 1 detected 83-94% of peaks post-alignment with 28-53% degenerated isotopologue ratio, while XCMS run 3 improved detection to 93-99% of peaks with 3-20% degenerated isotopologue ratio.: "There we can see that about 83-94% of peaks have been detected, which is ok. However, the isotopologue ratio (IR)-metric reports 28-53% degenerated IR"
- [other] In the Setup NPP assessment tab, select mzRAPP as the non-targeted tool and specify XCMS_unaligned_run1.csv as the unaligned file and XCMS_aligned_run1.csv as the aligned file. Execute the assessment by clicking the blue button, which will apply mzRAPP's matching algorithm to compare detected peaks against the benchmark.: "In the Setup NPP assessment tab, select mzRAPP as the non-targeted tool and specify XCMS_unaligned_run1.csv as the unaligned file and XCMS_aligned_run1.csv as the aligned file. Execute the assessment"
- [other] Inspect the View NPP assessment tab outputs: Peak Picking box (found peaks vs. 2870 benchmark total, split-peak count, isotopologue-ratio quality), Alignment box (peak retention rate, IR degeneration), and Post Alignment box (final peak detection %, IR degeneration %), extracting reported percentage ranges.: "Inspect the View NPP assessment tab outputs: Peak Picking box (found peaks vs. 2870 benchmark total, split-peak count, isotopologue-ratio quality), Alignment box (peak retention rate, IR"
- [readme] If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870 peaks in total.: "If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
