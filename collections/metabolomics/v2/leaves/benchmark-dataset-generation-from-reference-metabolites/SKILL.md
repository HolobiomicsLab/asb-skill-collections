---
name: benchmark-dataset-generation-from-reference-metabolites
description: Use when you have a set of centroided mzML files from LC-HRMS analysis,
  a list of target metabolites with known molecular formula and retention time windows,
  and you need to create a reference dataset to benchmark the reliability of NPP tools
  (XCMS, MZmine, MS-DIAL, etc.) on the same files.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzRAPP
  - enviPat
  - R
  - Skyline
  - MSconvert
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
- mzRAPP extracts and validates chromatographic peaks for which boundaries are provided
  for all (enviPat predicted) isotopologues
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

# benchmark-dataset-generation-from-reference-metabolites

## Summary

Generate a ground-truth benchmark dataset of known metabolite peaks from centroided mzML files by extracting and validating isotopologue chromatograms for reference molecules with known molecular composition, adducts, and retention time boundaries. The benchmark quantifies peak detection performance and isotopologue ratio fidelity for downstream non-targeted data preprocessing (NPP) method assessment.

## When to use

You have a set of centroided mzML files from LC-HRMS analysis, a list of target metabolites with known molecular formula and retention time windows, and you need to create a reference dataset to benchmark the reliability of NPP tools (XCMS, MZmine, MS-DIAL, etc.) on the same files. Use this skill when you want to measure NPP performance metrics (peak detection rate, isotopologue ratio bias, alignment errors) against a curated truth set rather than relying on putative identifications alone.

## When NOT to use

- Input mzML files are not centroided (non-centroided data will cause peak extraction failure; use MSconvert to centroid first).
- Target molecules lack reliable retention time boundaries or do not have at least two detected isotopologues per adduct (benchmark will be sparse or empty).
- You are benchmarking targeted metabolomics methods that already use internal standards and validated SRM/MRM transitions (benchmark-dataset-generation is for non-targeted methods and discovery workflows).

## Inputs

- centroided mzML files (LC-HRMS data; vendor-agnostic after MSconvert conversion)
- sample-group CSV file (columns: sample_name, sample_group)
- target file CSV (columns: molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax; optional: adduct_c, StartTime.EIC, EndTime.EIC, FileName, additional metadata)
- instrument/resolution specification (enviPat predefined or custom .csv with R and m/z columns)
- list of additional adducts to screen (e.g., M+NH4, M+Na, M+K)

## Outputs

- benchmark dataset CSV file containing validated peaks (one row per detected peak with molecule, adduct, isotopologue, m/z, retention time, intensity, quality metrics)
- performance summary (total molecules, total features, total peaks detected)
- optional Skyline export for manual curation and visualization

## How to apply

First, prepare three input CSV files: (1) sample-group file mapping mzML filenames to group labels, (2) target file with molecule names, molecular composition (SumForm_c), main adduct, and user-defined retention time boundaries (user.rtmin/user.rtmax in seconds), and (3) optional file-specific adduct columns. Launch mzRAPP via R (library(mzRAPP); callmzRAPP()), navigate to Generate Benchmark, and select all mzML files plus the two CSVs. Configure the instrument/resolution (e.g., OrbitrapXL/Velos/VelosPro_R60000@400) and choose additional adducts (e.g., M+NH4, M+Na, M+K). Set extraction parameters: lowest isotopologue ≥0.05 (% relative abundance), minimum 6 scans per peak, 6 ppm mass precision, and 5 ppm mass accuracy. mzRAPP will extract ion chromatograms for all enviPat-predicted isotopologues, apply provided RT boundaries, and automatically filter out isotopologues failing (a) peak-shape correlation ≥0.85 with the most abundant isotopologue or (b) isotopologue-ratio bias >30% relative to predictions. Only isotopologues where both the theoretically most abundant and at least one additional isotopologue are detected are retained. Export the finished benchmark as CSV; evaluate by checking that the detected feature count, peak count, and molecule coverage match expectations (e.g., 47 molecules, 157 features, 2870 peaks for MTBLS267 with all 30 files).

## Related tools

- **mzRAPP** (Primary tool for benchmark generation from mzML files, isotopologue validation, and peak extraction with Shiny GUI and R API) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Isotopologue pattern prediction and adduct mass calculation; used by mzRAPP to predict isotopologue ratios and validate measured isotopologue abundances)
- **R** (Runtime environment for mzRAPP; required for programmatic benchmark generation without GUI)
- **Skyline** (Manual peak curation tool from which RT boundaries can be exported and imported as user.rtmin/user.rtmax for benchmark target file) — https://skyline.ms/project/home/software/Skyline/begin.view
- **MSconvert** (Vendor-neutral conversion and centroiding of raw mass spectrometry files to mzML format prior to benchmark generation) — http://proteowizard.sourceforge.net/tools.shtml

## Examples

```
library(mzRAPP); callmzRAPP()  # Launch interactive Shiny app; then select all 30 *_POS.mzML files, SampleGroups_MTBLS267.csv, Target_File_MTBLS267.csv; set instrument to OrbitrapXL,Velos,VelosPro_R60000@400; select M+NH4, M+Na, M+K adducts; configure lowest_isotopologue=0.05, min_scans=6, mz_precision=6ppm, mz_accuracy=5ppm; execute benchmark generation
```

## Evaluation signals

- Benchmark file contains exactly one row per detected peak; all molecule names, adducts, and isotopologue identifiers match the target file (no truncation, misalignment, or duplicates).
- Peak count matches expected total (e.g., 2870 peaks for MTBLS267 with 30 _POS.mzML files); feature count (unique molecule–adduct–isotopologue combinations) is consistent with input (e.g., 157 features for MTBLS267).
- All retained peaks satisfy isotopologue ratio bias <30% and peak-shape correlation (Pearson r) ≥0.85 with respect to the most abundant isotopologue for that molecule; verify by spot-checking several rows in the exported CSV.
- Retention time (RT) boundaries in benchmark output are within ±user.rtmin/user.rtmax; any narrowing should reflect 5% max-height EIC intersection and be documented.
- All additional adducts and isotopologues are present for molecules where at least two isotopologues of each adduct were detected; absence indicates filtering (check isotopologue-ratio and peak-shape metrics).

## Limitations

- Benchmark quality depends critically on accuracy of user.rtmin/user.rtmax; peaks with incorrect or overlapping RT windows may be rejected or conflated. Manual curation (e.g., via Skyline) is recommended.
- Only isotopologues with sufficient abundance (≥ lowest isotopologue threshold, default 0.05%) and ≥2 scans are included; low-intensity adducts or rare isotopologues may be absent even if present in raw data.
- Isotopologue ratio bias filter (>30%) removes genuine biological or instrumental variation; adduct ratios not matching enviPat predictions (e.g., due to incomplete ionization or salt effects) will be flagged as 'degenerated' and excluded from benchmark.
- Benchmark does not capture NPP-specific artifacts (e.g., background noise, co-eluting unknowns, retention time drift across samples); it is a best-case reference and may overestimate NPP performance in real discovery workflows.
- Different mzML files may have different instrument parameters (resolution, mass accuracy); if pooling files from multiple instruments, ensure instrument/resolution is representative or apply file-specific parameters via FileName column in target file.

## Evidence

- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues of those target molecules directly from mzML files.: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [methods] If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870 peaks in total.: "47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870 peaks in total"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 are removed"
- [other] Remove isotopologues failing peak-shape correlation (with most abundant isotopologue) or isotopologue-ratio bias (>30%) filters using enviPat isotopologue predictions.: "Remove isotopologues failing peak-shape correlation or isotopologue-ratio bias (>30%) filters using enviPat isotopologue predictions"
- [readme] In order to generate a benchmark you need to provide your centroided mzML files. Conversion of files of different vendors to mzML as well as centroiding can be done by Proteowizards MSconvert.: "you need to provide your centroided mzML files. Conversion...can be done by Proteowizards MSconvert"
- [readme] Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark.: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered"
