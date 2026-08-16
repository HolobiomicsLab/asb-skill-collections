---
name: feature-count-verification-across-adducts-and-isotopologues
description: Use when after mzRAPP has exported a benchmark CSV file from centroided
  mzML files and you need to confirm the benchmark was constructed correctly before
  using it to evaluate NPP tool performance. Specifically, when you have a reference
  expectation (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - mzRAPP
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

# feature-count-verification-across-adducts-and-isotopologues

## Summary

Validate that a generated LC-HRMS benchmark dataset contains the expected number of unique molecular features (molecules × adducts × isotopologues) by counting distinct feature combinations and comparing against reference values. This skill ensures benchmark integrity before using it to assess non-targeted data pre-processing reliability.

## When to use

After mzRAPP has exported a benchmark CSV file from centroided mzML files and you need to confirm the benchmark was constructed correctly before using it to evaluate NPP tool performance. Specifically, when you have a reference expectation (e.g., 47 molecules, 157 features, 2870 total peaks from 30 mzML files) and want to detect generation errors or data loss.

## When NOT to use

- Benchmark CSV has not yet been exported by mzRAPP (i.e., benchmark generation is still in progress).
- You are validating NPP tool output (e.g., XCMS or MZmine 2 results), not the reference benchmark itself.
- The benchmark was generated with intentionally different parameters or target molecule sets than the reference specification.

## Inputs

- mzRAPP-exported benchmark CSV file
- Reference specification document (molecule count, feature count, peak count expectations)

## Outputs

- Count report: observed unique molecules
- Count report: observed unique features (molecule+adduct+isotopologue combinations)
- Count report: observed total peaks
- Validation summary: match/mismatch against reference

## How to apply

Load the benchmark CSV file exported by mzRAPP after processing all mzML files. Count the unique molecule identifiers to verify the molecular diversity. For each molecule, enumerate all unique feature rows (defined as the combination of molecule ID, adduct type, and isotopologue designation) and sum across all molecules to obtain the total feature count. Count all individual chromatographic peak detections (rows in the benchmark representing single peak observations) to derive the total peak count. Document whether observed counts match expected values (47 molecules, 157 features, 2870 peaks in the reference case); any discrepancy indicates incomplete extraction, filtering, or file corruption. Use R with mzRAPP's data loading functions to programmatically validate structure and schema before manual inspection.

## Related tools

- **mzRAPP** (Generates the benchmark dataset from centroided mzML files; exports CSV containing molecules, features (adduct+isotopologue combinations), and detected peaks) — https://github.com/YasinEl/mzRAPP
- **R** (Programming environment for loading benchmark CSV, performing counts, and comparing against reference values)
- **enviPat** (Underlying tool used by mzRAPP to predict isotopologue patterns for target molecules)

## Examples

```
library(mzRAPP); bm <- read.csv('benchmark_output.csv'); n_molecules <- length(unique(bm$molecule)); n_features <- nrow(unique(bm[,c('molecule','adduct','isotopologue')])); n_peaks <- nrow(bm); cat('Molecules:', n_molecules, '\nFeatures:', n_features, '\nPeaks:', n_peaks)
```

## Evaluation signals

- Observed unique molecule count equals reference count (e.g., 47 molecules detected in benchmark).
- Observed unique feature count (molecule+adduct+isotopologue tuples) equals reference count (e.g., 157 features).
- Observed total peak count (all peak detections across all features) equals reference count (e.g., 2870 peaks).
- No rows in benchmark CSV contain NULL, NaN, or malformed adduct/isotopologue designations for counted molecules.
- Benchmark structure passes schema validation: contains required columns (molecule ID, adduct, isotopologue, peak boundaries, etc.) without duplication errors.

## Limitations

- Discrepancies may arise from incomplete mzML file downloads (e.g., fewer than 30 files processed) or intentional subset processing; reference values are specific to the full MTBLS267 dataset and parameter set.
- mzRAPP filters isotopologues based on peak shape correlation (Pearson r < 0.85) and abundance bias (>30% deviation from predicted isotopologue ratio); peaks failing these criteria are excluded before benchmark export, so observed counts may legitimately differ from raw extraction counts.
- The skill validates row counts and feature cardinality only; it does not verify m/z accuracy, retention time precision, or peak boundary correctness—those are separate quality assessments.
- Benchmark CSV structure and column names depend on mzRAPP version and export options; schema validation must account for optional columns (e.g., FileName, user-defined metadata).

## Evidence

- [methods] A benchmark dataset generated from 30 mzML files should contain 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870 peaks in total.: "If you processed all 30 mzML files, you should have generated a benchmark containing 47 different molecules with 157 different features (including all adducts and isotopologues), resulting in 2870"
- [methods] Isotopologue peaks with criteria violations are removed from the benchmark.: "Isotopologue peaks with an area or height which is more than 30% off the predicted value or a Pearson Correlation coef < 0.85 (as compared to the highest isotopologue) are removed."
- [methods] mzRAPP extracts and validates chromatographic peaks using enviPat-predicted isotopologues.: "mzRAPP extracts and validates chromatographic peaks for which boundaries are provided for all (enviPat predicted) isotopologues"
- [readme] Benchmark dataset generation workflow includes exporting a CSV file.: "Load the generated benchmark CSV file exported by mzRAPP after processing all 30 mzML files from MTBLS267."
- [readme] Features are defined by the combination of molecule, adduct, and isotopologue.: "With 157 different features (including all adducts and isotopologues)"
