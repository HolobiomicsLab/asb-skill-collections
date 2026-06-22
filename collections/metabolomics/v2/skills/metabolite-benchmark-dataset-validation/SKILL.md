---
name: metabolite-benchmark-dataset-validation
description: Use when after mzRAPP has exported a benchmark CSV file from processing a batch of centroided mzML files (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_2409
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - mzRAPP
  - R
  - enviPat
derived_from:
- doi: 10.1093/bioinformatics/btab231/6214530
  title: mzRAPP
evidence_spans:
- 'You can now start mzRAPP using: library(mzRAPP); callmzRAPP()'
- The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing (NPP)
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

# metabolite-benchmark-dataset-validation

## Summary

Validate that a generated benchmark dataset from centroided mzML files contains the expected number of target molecules, isotopologue-adduct features, and detected chromatographic peaks. This skill ensures the integrity of the reference dataset used for downstream non-targeted metabolomics preprocessing assessment.

## When to use

After mzRAPP has exported a benchmark CSV file from processing a batch of centroided mzML files (e.g., MTBLS267 with 30 POS-mode files), and you need to confirm that the benchmark composition matches the theoretical expectation before using it to assess non-targeted preprocessing tool performance.

## When NOT to use

- Benchmark CSV has not yet been generated from mzML files (run mzRAPP benchmark generation first).
- Input mzML files are profile-mode rather than centroided (mzRAPP requires centroided data).
- You are validating NPP (non-targeted preprocessing) tool output rather than the ground-truth benchmark itself — use different assessment metrics for that.

## Inputs

- mzRAPP-exported benchmark CSV file (post-processed from 30 centroided mzML files)
- expected reference composition (molecule count, feature count, peak count)

## Outputs

- validation report with observed molecule, feature, and peak counts
- comparison table: observed vs. expected counts with discrepancy flags

## How to apply

Load the exported benchmark CSV file into R and programmatically count: (1) unique molecule identifiers; (2) unique feature records (each combination of molecule, adduct, and isotopologue); and (3) total peak detections across all features. Compare each observed count against the known reference values (e.g., 47 molecules, 157 features, 2870 peaks for MTBLS267). Discrepancies indicate either incomplete mzML processing, filtering thresholds that removed valid isotopologues (those failing peak shape correlation ≥0.85 or isotopologue ratio bias ≥30%), or incorrect file input. Report all three counts and flag any deviation with magnitude and likely cause.

## Related tools

- **mzRAPP** (Generates and exports the benchmark dataset CSV from centroided mzML files; validates isotopologue peak quality (shape, ratio bias) during benchmark creation) — https://github.com/YasinEl/mzRAPP
- **R** (Environment for loading benchmark CSV and performing counts and comparisons)
- **enviPat** (Predicts isotopologue patterns and masses for target molecules; used by mzRAPP to generate expected isotope boundaries)

## Examples

```
library(mzRAPP); benchmark <- read.csv('benchmark_MTBLS267.csv'); cat('Molecules:', length(unique(benchmark$molecule)), '\nFeatures:', nrow(benchmark), '\nPeaks:', sum(benchmark$peak_count))
```

## Evaluation signals

- Observed molecule count equals expected count (e.g., 47 for MTBLS267).
- Observed feature count equals expected count (e.g., 157 for MTBLS267), confirming all adducts and isotopologues were retained post-filtering.
- Observed peak count equals expected count (e.g., 2870 for MTBLS267), indicating no spurious or missing detections.
- No NA or null values in molecule, adduct, or isotopologue columns of the benchmark CSV.
- All retained isotopologue peaks satisfy mzRAPP's quality criteria: Pearson correlation ≥0.85 vs. most abundant isotopologue and isotopologue ratio bias <30%.

## Limitations

- Validation checks composition only; does not assess accuracy of retention time boundaries, m/z accuracy, or peak shape quality — those are evaluated separately via NPP performance metrics.
- Expected reference counts must be known in advance or derived from the input target file and mzML metadata; the skill does not infer ground truth independently.
- Filtering thresholds (peak shape correlation ≥0.85, isotopologue ratio bias <30%) are hard-coded in mzRAPP and cannot be adjusted post-generation; mismatches may require re-running benchmark generation with different parameters.
- Benchmark is specific to the provided mzML files, sample groups, and target molecule list; cannot be directly transferred to different datasets or instrument configurations.

## Evidence

- [methods] If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870: "If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870"
- [readme] mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [methods] Sufficient quality of low peaks was ensured by removing isotopologues that do not satisfy criteria in peak shape (peak shape correlation with most abundant isotopologue) and abundance (Isotopologue ratio bias < 30%): "removing isotopologues that do not satisfy criteria in peak shape and abundance (Isotopologue ratio bias < 30%)"
- [readme] Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing: "The goal of mzRAPP is to allow reliability assessment of non-targeted data pre-processing"
