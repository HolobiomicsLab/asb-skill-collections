---
name: amino-acid-level-accuracy-evaluation
description: Use when you have predicted peptide sequences from a de novo sequencing tool (e.g., Casanovo) and want to understand the fine-grained accuracy of the predictions beyond exact-match peptide-level scoring.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0154
  tools:
  - Casanovo
  - PyTorch
  - PDV
  - limelight-import-casanovo
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-024-49731-x
  title: Casanovo
- doi: 10.1093/bib/bbac542
  title: ''
evidence_spans:
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing.
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide sequencing
- Pytorch is installed automatically when installing Casanovo
- Upgraded minimum Lightning version to 2.6.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_casanovo_cq
    doi: 10.1038/s41467-024-49731-x
    title: Casanovo
  dedup_kept_from: coll_casanovo_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-024-49731-x
  all_source_dois:
  - 10.1038/s41467-024-49731-x
  - 10.1093/bib/bbac542
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Amino-acid-level accuracy evaluation

## Summary

Evaluate peptide sequence predictions at the individual amino acid level by comparing predicted sequences against ground truth annotations, computing residue-wise precision, recall, and F1 scores. This skill is essential for assessing whether decoding strategies (e.g., greedy vs. beam search) or different de novo sequencing tools produce higher-quality predictions even when full-length peptide sequences differ.

## When to use

Apply this skill when you have predicted peptide sequences from a de novo sequencing tool (e.g., Casanovo) and want to understand the fine-grained accuracy of the predictions beyond exact-match peptide-level scoring. Use it specifically to distinguish between different algorithmic configurations (greedy vs. beam search decoding) or to identify which amino acid positions are most prone to misidentification, particularly in applications like monoclonal antibody characterization or immunopeptidomics where partial sequence correctness may still inform downstream analysis.

## When NOT to use

- When you only have unannotated, experimental MS/MS spectra with no ground-truth peptide sequences available—amino acid-level evaluation requires high-confidence reference sequences.
- When your goal is database-dependent peptide identification (matching against a protein sequence database) rather than de novo sequencing; use database search scoring metrics instead.
- When the predicted and ground-truth sequences cannot be meaningfully aligned (e.g., completely different lengths with no homology); consider sequence alignment tools or peptide spectral matching first.

## Inputs

- Predicted peptide sequences (text strings or records from de novo sequencing tool output, e.g., Casanovo predictions)
- Ground-truth annotated peptide sequences (from MGF file annotations or manual curation)
- Casanovo checkpoint file (pre-trained model weights)
- Validation dataset in MGF format with annotated MS/MS spectra

## Outputs

- Position-wise amino acid comparison table (predicted vs. ground truth for each peptide)
- Amino acid-level precision, recall, and F1 scores (per decoding strategy or tool)
- Summary statistics table showing side-by-side predictions, confidence scores, and accuracy metrics
- Per-position error frequency matrix (identifying hotspots of misidentification)

## How to apply

Load the predicted peptide sequences and the annotated/ground-truth sequences from your validation dataset (typically as MGF-format MS/MS spectra with annotations). Align each predicted sequence to its corresponding ground-truth sequence at the amino acid level, position by position. For each position, record whether the predicted amino acid matches the true amino acid (TP), is absent from predictions (FN), or is incorrectly predicted (FP). Aggregate these position-level classifications across all peptides to compute precision (TP / (TP + FP)), recall (TP / (TP + FN)), and F1 score (2 × (precision × recall) / (precision + recall)). Compare these metrics side-by-side across different decoding strategies or tools to identify which approach achieves higher amino acid-level accuracy. The rationale is that amino acid-level metrics reveal partial correctness and systematic errors that peptide-level metrics (exact match only) would miss, guiding refinement of the sequencing pipeline.

## Related tools

- **Casanovo** (De novo peptide sequencing tool powered by transformer neural network; generates predicted sequences from MS/MS spectra that are then evaluated at amino acid level) — https://github.com/Noble-Lab/casanovo
- **PyTorch** (Deep learning framework used to implement and run Casanovo inference for generating predictions to be evaluated)
- **PDV** (Proteomics data visualization tool for inspecting and comparing Casanovo predictions against MS/MS spectra; useful for visual validation of amino acid-level correctness) — https://github.com/wenbostar/PDV
- **limelight-import-casanovo** (Converter that transforms Casanovo results (mztab format) into Limelight XML for integrated visualization and comparative analysis of predictions) — https://github.com/yeastrc/limelight-import-casanovo

## Examples

```
Load pre-trained Casanovo checkpoint and validation MGF dataset; run inference with greedy decoding and beam search decoding; for each predicted peptide, align to ground-truth sequence and compute per-position TP/FP/FN counts; aggregate precision = sum(TP) / (sum(TP) + sum(FP)), recall = sum(TP) / (sum(TP) + sum(FN)), F1 = 2 × (precision × recall) / (precision + recall); output comparison table.
```

## Evaluation signals

- Amino acid-level precision and recall are computed correctly: TP / (TP + FP) and TP / (TP + FN), with F1 score balancing both metrics.
- Metrics are stratified by decoding strategy or tool and show clear, interpretable differences (e.g., beam search ≥ greedy across most metrics).
- Position-wise error frequencies are plausible and concentrated at difficult regions (e.g., low-abundance or ambiguous peaks in the MS/MS spectrum).
- Summary table includes per-peptide predictions, confidence scores, and computed metrics aligned side-by-side for manual spot-checking.
- No NaN or division-by-zero errors in metric calculation; edge cases (e.g., predictions of length 0) are handled explicitly.

## Limitations

- Amino acid-level evaluation assumes high-quality ground-truth annotations; errors or ambiguities in reference sequences will be misattributed to the prediction method.
- Sequence alignment for comparison can be ambiguous when predicted and true sequences differ significantly in length or contain repeated motifs; a simple position-wise comparison may not capture biological similarity.
- Metrics do not account for modifications (e.g., phosphorylation, oxidation) or non-standard amino acids unless explicitly handled in the alignment logic.
- Performance depends on the representativeness of the validation dataset; datasets biased toward specific peptide properties (length, charge, fragmentation patterns) may not generalize to real-world MS/MS data.
- Confidence scores from Casanovo are not formally calibrated; high confidence predictions with low amino acid-level accuracy may indicate miscalibration rather than true performance gain.

## Evidence

- [other] Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score for each decoding strategy.: "Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score"
- [other] Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences.: "Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences"
- [other] Generate a summary table with side-by-side predictions, scores, and accuracy metrics to identify differences and assess whether beam search yields higher-quality predictions.: "Generate a summary table with side-by-side predictions, scores, and accuracy metrics to identify differences"
- [readme] Casanovo 'translates' peaks in MS/MS spectra into amino acid sequences with remarkable precision.: "Casanovo 'translates' peaks in MS/MS spectra into amino acid sequences with remarkable precision"
- [readme] Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset, and is particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics: "particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any setting in which you are interested in identifying peptides that may not be in your protein database"
