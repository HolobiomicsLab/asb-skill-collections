---
name: de-novo-peptide-sequencing
description: Use when you have annotated MS/MS spectra in MGF format and need to identify peptide sequences that may not exist in reference protein databases—such as in immunopeptidomics, metaproteomics, paleoproteomics, venomics, or monoclonal antibody assembly workflows.
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
  - limelight-import-casanovo
  - CUDA Toolkit
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

# de-novo-peptide-sequencing

## Summary

Apply a transformer neural network (Casanovo) to predict amino acid sequences directly from MS/MS spectral peaks without requiring a protein database. This skill is essential for identifying unexpected or novel peptides in bottom-up tandem mass spectrometry datasets, particularly in immunopeptidomics, metaproteomics, and other applications where database searching is insufficient.

## When to use

Use this skill when you have annotated MS/MS spectra in MGF format and need to identify peptide sequences that may not exist in reference protein databases—such as in immunopeptidomics, metaproteomics, paleoproteomics, venomics, or monoclonal antibody assembly workflows. Apply it particularly when greedy decoding produces low-confidence predictions and you want to compare alternative decoding strategies (e.g., beam search) to improve sequence accuracy.

## When NOT to use

- When you have high-quality database search results already; de novo sequencing is best suited for novel or unexpected peptides not in existing databases.
- When your input spectra are not in data-dependent acquisition (DDA) bottom-up MS/MS format; Casanovo is specifically designed for this acquisition mode.
- When you lack sufficient computational resources (GPU with CUDA support); transformer inference on large datasets can be memory-intensive and benefits from GPU acceleration.

## Inputs

- Pre-trained Casanovo checkpoint file
- Annotated MS/MS spectra in MGF format
- Casanovo configuration file (YAML) specifying decoding strategy (greedy or beam search)

## Outputs

- Predicted peptide sequences per spectrum
- Confidence scores for each prediction
- Amino acid-level precision, recall, and F1 scores
- Peptide-level precision, recall, and F1 scores
- Summary table comparing predictions from different decoding strategies

## How to apply

Load a pre-trained Casanovo checkpoint and your MS/MS dataset in MGF format into PyTorch. Configure the model for an initial decoding strategy (e.g., greedy decoding as a baseline), run peptide prediction on the spectra, and record predicted sequences with their confidence scores. Then reconfigure the model with an alternative strategy (e.g., beam search decoding) and repeat prediction on the same dataset. Compare predicted sequences at both amino acid and peptide levels, computing precision, recall, and F1 score for each strategy. Generate a summary table with side-by-side predictions and accuracy metrics to assess whether the alternative decoding strategy yields higher-quality predictions. The choice between greedy and beam search should reflect the trade-off between inference speed and prediction accuracy for your specific application.

## Related tools

- **Casanovo** (Core transformer-based model for translating MS/MS spectral peaks into amino acid sequences with configurable decoding strategies) — https://github.com/Noble-Lab/casanovo
- **PyTorch** (Deep learning framework for loading checkpoints and executing model inference)
- **PDV** (Lightweight visualization tool for inspecting Casanovo predictions and generating annotated spectra) — https://github.com/wenbostar/PDV
- **limelight-import-casanovo** (Converter for transforming Casanovo results (mzTab format) into Limelight XML for downstream visualization and analysis) — https://github.com/yeastrc/limelight-import-casanovo
- **CUDA Toolkit** (Enables GPU acceleration for Casanovo inference on NVIDIA-compatible hardware)

## Evaluation signals

- Predicted sequences are produced for all spectra in the validation dataset with valid confidence scores in the expected range.
- Amino acid-level and peptide-level F1 scores are computed without errors, and beam search decoding produces F1 scores ≥ greedy decoding baseline.
- Side-by-side comparison table shows matching predictions between strategies and clearly identifies divergent predictions where beam search improves accuracy.
- Summary metrics (precision, recall, F1) are calculated per decoding strategy and demonstrate statistical or practical improvement when beam search is used.
- No GPU memory errors or NaN values appear in confidence scores; predictions are logged and reproducible with the same checkpoint and configuration.

## Limitations

- Casanovo's accuracy depends on the quality and composition of the training data; performance may vary on datasets with unusual amino acid modifications or non-standard ionization patterns.
- Beam search decoding increases computational cost and inference time compared to greedy decoding, so trade-offs between speed and accuracy must be evaluated per use case.
- The tool is optimized for bottom-up, data-dependent acquisition MS/MS spectra; performance on other acquisition modes (e.g., data-independent acquisition) is not guaranteed.
- Confidence scores reflect model predictions but do not directly validate against ground truth; independent mass accuracy or retention time validation is recommended for high-stakes identifications.

## Evidence

- [other] Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences.: "Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences."
- [readme] Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset: "Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset"
- [readme] particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any setting in which you are interested in identifying peptides that may not be in your protein database.: "particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any setting in which you are interested in identifying peptides that may not be in your protein database."
- [other] Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score for each decoding strategy.: "Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score for each decoding strategy."
- [readme] Pytorch is installed automatically when installing Casanovo: "Pytorch is installed automatically when installing Casanovo"
- [readme] A converter for generating Limelight XML from Casanovo results is available: "A converter for generating Limelight XML from Casanovo results is available"
