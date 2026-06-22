---
name: chromatographic-peak-detection-validation
description: Use when you have centroided mzML data and a curated set of target molecules with known retention time (RT) boundaries, and you need to establish ground-truth peak detection performance metrics (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - mzRAPP
  - XCMS
  - R
  - MZmine 2
  - enviPat
  - Skyline
  - MSconvert (ProteoWizard)
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
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

# chromatographic-peak-detection-validation

## Summary

Validate the quality and integrity of chromatographic peaks extracted from centroided mzML files by comparing detected isotopologue patterns, peak boundaries, and abundance ratios against theoretically predicted isotopologue envelopes. This skill assesses whether peak detection workflows preserve isotopologue stoichiometry and correctly identify all isotopologues of target molecules.

## When to use

Apply this skill when you have centroided mzML data and a curated set of target molecules with known retention time (RT) boundaries, and you need to establish ground-truth peak detection performance metrics (e.g., detection rate, isotopologue ratio degradation) before benchmarking non-targeted preprocessing tools like XCMS, MZmine 2, or MS-DIAL.

## When NOT to use

- Input mzML files are not centroided; use MSconvert or equivalent centroiding tool first.
- Target molecules lack known retention time boundaries or isotopologue information; peak detection requires provided RT windows and molecular formula.
- Aim is to assess NPP tool output directly without a benchmark; use the benchmark-comparison skill instead.

## Inputs

- Centroided mzML files (LC-HRMS data)
- Target file (CSV with columns: molecule, SumForm_c, main_adduct, user.rtmin, user.rtmax; optional: adduct_c, StartTime.EIC, EndTime.EIC, FileName, additional columns)
- Sample-group file (CSV with columns: sample_name, sample_group)
- Instrument resolution specification (enviPat list or custom .csv with R and m/z columns)
- Optional: Peak boundary curation file exported from manual peak inspection tool (e.g., Skyline)

## Outputs

- Benchmark dataset CSV containing validated peaks with molecule ID, adduct, isotopologue assignments, RT boundaries, area/height, and isotopologue ratio metrics
- Peak detection summary statistics (total peaks detected, split peak count, percentage of peaks with degenerated isotopologue ratio)
- Filtered isotopologue list with quality flags (peak shape correlation, abundance bias, isotopologue ratio bias)

## How to apply

Load centroided mzML files and a target file specifying molecular composition (SumForm_c), main adduct, and RT boundaries (user.rtmin / user.rtmax in seconds) for each molecule. Using the selected instrument's mass resolution, generate extracted ion chromatograms (EICs) for all enviPat-predicted isotopologues of each target. For each molecule, accept only isotopologues where: (1) the theoretically most abundant isotopologue is detected AND at least one additional isotopologue is present; (2) peak shape correlation with the most abundant isotopologue is ≥ 0.85 (Pearson r); (3) peak area or height deviates by < 30% from the predicted isotopologue abundance; (4) isotopologue ratio bias is < 30%. Reject peaks with insufficient isotopologue coverage. Record intermediate counts (total peaks detected, split peaks, isotopologue-ratio quality metrics) and export the resulting benchmark dataset as CSV containing all validated peaks and their boundaries. The benchmark serves as a true-positive reference for downstream tool assessment.

## Related tools

- **mzRAPP** (Performs benchmark generation by extracting and validating chromatographic peaks with quality filters on isotopologue patterns and peak shape; implements isotopologue prediction via enviPat and peak filtering logic) — https://github.com/YasinEl/mzRAPP
- **enviPat** (Predicts isotopologue patterns and m/z values for target molecules given molecular composition and adduct type; enables definition of theoretical isotopologue envelopes)
- **Skyline** (Manual peak curation tool from which RT boundaries and peak limits can be exported for import into mzRAPP target file)
- **MSconvert (ProteoWizard)** (Converts vendor mass spectrometry formats to centroided mzML files required as input to mzRAPP)
- **R** (Runtime environment for mzRAPP library and scripting of benchmark generation workflows)

## Examples

```
library(mzRAPP); callmzRAPP()  # Launch the Shiny interface to: (1) select centroided mzML files; (2) load target file with molecule SumForm_c, main_adduct, user.rtmin, user.rtmax; (3) set mz precision/accuracy and resolution parameters; (4) execute benchmark generation
```

## Evaluation signals

- Benchmark dataset contains expected total peak count (e.g., 2870 peaks for MTBLS267 dataset with 47 molecules and 157 features)
- Isotopologue ratio bias metric falls within expected range (< 30% for accepted peaks); degenerated isotopologue ratio % reported for quality assessment
- Peak shape correlation (Pearson r ≥ 0.85) and area/height deviation (< 30%) thresholds are satisfied for all retained isotopologues
- Split peak count and detection rate (% of benchmark peaks detected in each file) are consistent across replicate mzML files and align with known molecular targets
- RT boundaries in output benchmark match user-provided user.rtmin/user.rtmax, optionally refined to EIC 5% maximum peak height intersections

## Limitations

- Benchmark generation requires manual RT boundary curation beforehand, typically via Skyline or equivalent tool; peaks without accurate boundaries will be rejected.
- Quality filters (peak shape correlation ≥ 0.85, isotopologue ratio bias < 30%, area/height deviation < 30%) are fixed thresholds; atypical peak shapes or unusual isotopologue ratios may be discarded even if valid.
- Only isotopologues with both theoretically most abundant and at least one additional isotopologue detected are included; singleton isotopologues or molecules with poor isotopologue coverage are filtered out.
- Benchmark relies on enviPat's isotopologue prediction; accuracy is dependent on correct molecular formula (SumForm_c) specification and instrument mass resolution calibration.
- Split peaks or peak merging during extraction may inflate or deflate individual peak counts relative to true molecular abundance; post-alignment metrics are required to assess this.

## Evidence

- [methods] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [readme] Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark.: "Only isotopologues for which the theoretically most abundant and at least one additional isotopologue are found are considered for the final benchmark."
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue): "Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue)"
- [methods] removing isotopologues that do not satisfy criteria in peak shape and abundance (Isotopologue ratio bias < 30%): "removing isotopologues that do not satisfy criteria in peak shape and abundance (Isotopologue ratio bias < 30%)"
