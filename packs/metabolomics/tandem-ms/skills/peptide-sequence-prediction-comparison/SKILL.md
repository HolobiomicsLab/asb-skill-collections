---
name: peptide-sequence-prediction-comparison
description: Use when when you have a pre-trained Casanovo model, annotated MS/MS spectra in MGF format, and want to benchmark whether beam search decoding improves peptide prediction quality over the default greedy decoding strategy.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3646
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Casanovo
  - PyTorch
  - PDV
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

# peptide-sequence-prediction-comparison

## Summary

Compare de novo peptide sequences predicted by Casanovo using different decoding strategies (greedy vs. beam search) to assess whether alternative inference methods yield higher-quality predictions on MS/MS spectra. This skill quantifies prediction accuracy differences at both amino acid and peptide levels using precision, recall, and F1 scores.

## When to use

When you have a pre-trained Casanovo model, annotated MS/MS spectra in MGF format, and want to benchmark whether beam search decoding improves peptide prediction quality over the default greedy decoding strategy. Use this skill if your goal is to validate whether a more computationally expensive inference method produces measurably better de novo peptide identifications.

## When NOT to use

- Input spectra lack ground-truth peptide annotations (cannot compute precision/recall without reference sequences)
- Casanovo model has not been trained or validated; use only pre-trained, evaluated checkpoints to ensure baseline reliability
- Your goal is rapid annotation of large spectra sets; beam search is computationally more expensive and unsuitable if inference speed is the primary constraint

## Inputs

- Pre-trained Casanovo transformer model checkpoint
- Annotated MS/MS spectra in MGF format with ground-truth peptide sequences
- Configuration parameters for greedy and beam search decoding

## Outputs

- Predicted peptide sequences from greedy decoding with confidence scores
- Predicted peptide sequences from beam search decoding with confidence scores
- Precision, recall, and F1 scores computed at amino acid level
- Precision, recall, and F1 scores computed at peptide level
- Summary table comparing predictions and accuracy metrics between decoding methods

## How to apply

Load a pre-trained Casanovo checkpoint and a validation dataset of annotated MS/MS spectra in MGF format. Configure Casanovo to perform peptide sequence prediction using greedy decoding (baseline), recording predicted sequences and confidence scores for each spectrum. Reconfigure Casanovo to use beam search decoding with identical model and dataset, running prediction and recording the resulting sequences. For each predicted sequence, compute precision, recall, and F1 score by comparing predicted amino acids and full peptide sequences against ground-truth annotations. Generate a summary table with side-by-side predictions from both methods, their confidence scores, and accuracy metrics to identify differences and quantify whether beam search yields higher-quality predictions.

## Related tools

- **Casanovo** (Transformer-based de novo peptide sequencing engine; loads pre-trained checkpoint and performs greedy and beam search decoding on MS/MS spectra) — https://github.com/Noble-Lab/casanovo
- **PyTorch** (Deep learning framework required for loading and executing the pre-trained Casanovo transformer model)
- **PDV** (Graphical interface for visual inspection and validation of Casanovo predictions to verify correctness of sequences) — https://github.com/wenbostar/PDV

## Evaluation signals

- Precision, recall, and F1 scores at amino acid level should be ≥0 and ≤1.0; beam search scores should be equal to or higher than greedy baseline
- Precision, recall, and F1 scores at peptide level should show consistent ordering (e.g., if beam search improves one metric, peptide-level metrics should reflect this improvement or neutral stability)
- Summary table row counts must match the number of spectra in the validation dataset; no predictions should be dropped or duplicated
- Confidence scores from both methods should be in valid range (typically [0, 1] or log-probability scale); scores must be recorded alongside each sequence prediction
- Visual inspection using PDV should confirm that higher-confidence predictions align with ground-truth sequences and that beam search selections differ qualitatively from greedy selections in expected ways

## Limitations

- Beam search decoding is computationally more expensive than greedy decoding, which may limit practical application to large-scale screening workflows
- Comparison is specific to the MGF format and requires ground-truth peptide annotations; comparison cannot be performed on unlabeled spectra
- Casanovo transformer accuracy is trained on specific MS/MS fragmentation patterns and proteases; performance may degrade on spectra from non-standard experimental conditions, enzymes, or modifications not well-represented in training data
- F1 score, precision, and recall assume exact amino acid sequence matches; similar sequences differing by single substitutions are scored as incorrect, which may underestimate practical similarity

## Evidence

- [other] Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences.: "Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences."
- [other] Load a pre-trained Casanovo checkpoint and a validation dataset of annotated MS/MS spectra in MGF format.: "Load a pre-trained Casanovo checkpoint and a validation dataset of annotated MS/MS spectra in MGF format."
- [other] Configure Casanovo to use greedy decoding (baseline) and run peptide sequence prediction on the spectra, recording predicted sequences and confidence scores.: "Configure Casanovo to use greedy decoding (baseline) and run peptide sequence prediction on the spectra, recording predicted sequences and confidence scores."
- [other] Reconfigure Casanovo to use beam search decoding with the same checkpoint and dataset, running prediction and recording predicted sequences.: "Reconfigure Casanovo to use beam search decoding with the same checkpoint and dataset, running prediction and recording predicted sequences."
- [other] Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score for each decoding strategy.: "Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score for each decoding strategy."
- [readme] Casanovo "translates" peaks in MS/MS spectra into amino acid sequences with remarkable precision.: "Casanovo "translates" peaks in MS/MS spectra into amino acid sequences with remarkable precision."
- [methods] PDV provides a graphical interface for inspecting Casanovo outputs.: "PDV provides a graphical interface for inspecting Casanovo outputs."
