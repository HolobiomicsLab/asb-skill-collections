---
name: sample-metadata-integration-for-qc
description: Use when when you have an aligned MemoMatrix (sample-by-feature occurrence
  matrix where features are MS2 peaks and neutral losses) and corresponding sample
  annotations (especially blank/control sample labels), and you need to exclude background-derived
  peaks and losses before applying visualization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - Python
  - numpy
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.3389/fbinf.2022.842964
  title: memo
evidence_spans:
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra
- MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2
  spectra and converting them into documents.
- conda create --name memo python=3.8
- pip install numpy
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_memo_cq
    doi: 10.3389/fbinf.2022.842964
    title: memo
  dedup_kept_from: coll_memo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fbinf.2022.842964
  all_source_dois:
  - 10.3389/fbinf.2022.842964
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# sample-metadata-integration-for-qc

## Summary

Integrate sample metadata (e.g., blank sample annotations) with aligned MS2 fingerprint matrices to enable selective quality control filtering before downstream visualization. This skill is essential for removing background contamination from MS2 peak and neutral loss occurrence data in metabolomics workflows.

## When to use

When you have an aligned MemoMatrix (sample-by-feature occurrence matrix where features are MS2 peaks and neutral losses) and corresponding sample annotations (especially blank/control sample labels), and you need to exclude background-derived peaks and losses before applying visualization techniques (MDS/PCoA, TMAP, Heatmap) to avoid misleading sample comparisons.

## When NOT to use

- Input MemoMatrix already has blank filtering applied or no blank samples were acquired in the experimental design.
- Blank samples are not clearly labeled or metadata is missing; integration cannot proceed without reliable blank annotations.
- Analysis goal is to study contaminants or background signals themselves; filtering blanks would remove the signal of interest.

## Inputs

- aligned MemoMatrix (sample-by-MS2-feature occurrence matrix in CSV or tabular format)
- sample metadata table with blank sample identifiers/annotations (CSV or TSV)

## Outputs

- filtered MemoMatrix (blank-corrected sample-by-feature occurrence matrix, CSV or tabular format)
- log or report of removed peaks and neutral losses (for QC documentation)

## How to apply

Load the aligned MemoMatrix and blank sample metadata as tabular data (CSV or matchms-compatible format) into Python/numpy. Cross-reference the blank sample metadata with rows in the MemoMatrix to identify all MS2 peaks and neutral losses present in any blank sample. Remove (set to zero or delete columns for) all peaks and losses that occur in blanks, preserving only features that discriminate true sample composition from contamination. This filtering step is rationale because blank samples capture instrumental noise and ambient contamination; removing their peaks ensures downstream sample comparison reflects biological or chemical differences rather than shared background artifacts.

## Related tools

- **matchms** (Python library for loading and handling aligned MS2 fingerprint matrices and metadata in standardized formats) — https://github.com/matchms/matchms
- **Python** (Programming language for scripting the metadata-matrix cross-reference and filtering operations)
- **numpy** (NumPy arrays for efficient column removal and zero-masking of blank-derived features)

## Examples

```
import numpy as np; from matchms import load_spectrum; memo_matrix = np.loadtxt('aligned_memoMatrix.csv', delimiter=',', skiprows=1); blank_mask = [sample_name.startswith('blank') for sample_name in sample_names]; blank_features = memo_matrix[blank_mask].sum(axis=0) > 0; filtered_memo = memo_matrix[:, ~blank_features]; np.savetxt('filtered_memoMatrix.csv', filtered_memo, delimiter=',')
```

## Evaluation signals

- Verify that the number of features (columns) in the filtered matrix is ≤ the original matrix; no features should be added.
- Confirm that all peaks and neutral losses recorded in blank sample rows are absent (zero or deleted) from the final filtered matrix.
- Check that non-blank sample rows retain their feature occurrences (no data loss in target samples).
- Validate that the filtered matrix is compatible with downstream visualization tools (MDS/PCoA, TMAP, Heatmap) by confirming CSV/tabular schema integrity.
- Document and report which peaks/neutral losses were removed and their frequency in blank samples for transparency.

## Limitations

- Filtering assumes blank samples are correctly labeled in metadata; mislabeled or missing blank annotations will result in incomplete or incorrect contamination removal.
- This approach removes all peaks detected in blanks, even if they co-occur at high abundance in true samples; shared contaminants with genuine signals may be inadvertently discarded.
- No quantitative threshold is applied (e.g., 'remove only if blank occurrence > 50%'); the method is binary (present/absent in any blank).
- Requires that blank samples exist and were acquired; workflows without blanks cannot use this skill.

## Evidence

- [other] Identify all MS2 peaks and neutral losses present in blank samples by scanning their rows in the MemoMatrix: "Identify all MS2 peaks and neutral losses present in blank samples by scanning their rows in the MemoMatrix. 3. Remove (set to zero or delete columns corresponding to) all peaks and losses that occur"
- [other] MEMO applies a filtering operation that removes peaks and neutral losses originating from blank samples: "MEMO applies a filtering operation that removes peaks and neutral losses originating from blank samples from the aligned fingerprint matrix, enabling selective exclusion of background contamination"
- [other] Remove peaks/losses from blanks for visualization techniques: "different filtering (remove peaks/losses from blanks for example) and visualization techniques (MDS/PCoA, TMAP, Heatmap, ...) can be used"
- [other] Export filtered matrix compatible with downstream tools: "Export the filtered MemoMatrix as a CSV or tabular format compatible with downstream visualization tools (MDS/PCoA, TMAP, Heatmap)."
- [other] matchms for handling MS2 spectra and fingerprint matrices: "MEMO is mainly built on `matchms`_ and `spec2vec`_ packages for handling the MS2 spectra"
