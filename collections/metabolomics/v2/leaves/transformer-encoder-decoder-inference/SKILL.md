---
name: transformer-encoder-decoder-inference
description: Use when when you have preprocessed MS/MS spectra (normalized intensities,
  filtered for quality, with top peaks retained) that have been encoded using a spectral
  representation method (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3092
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0080
  tools:
  - Casanovo
  - PyTorch
  - DepthCharge
  - CUDA Toolkit
  - PDV
  - limelight-import-casanovo
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-024-49731-x
  title: Casanovo
- doi: 10.1093/bib/bbac542
  title: ''
evidence_spans:
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide
  sequencing.
- Casanovo is a state-of-the-art deep learning tool designed for _de novo_ peptide
  sequencing
- Pytorch is installed automatically when installing Casanovo
- Upgraded minimum Lightning version to 2.6.
- Upgraded minimum DepthCharge version to 0.4.10.
- Install the latest version of the NVIDIA drivers using the official CUDA Toolkit
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transformer-encoder-decoder-inference

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Apply a pretrained transformer encoder–decoder model with beam search decoding to convert preprocessed MS/MS spectral data into candidate peptide sequences ranked by confidence score. This skill encapsulates the core inference step of deep learning–based de novo peptide sequencing, where spectral features are translated into amino acid sequences through learned representations.

## When to use

When you have preprocessed MS/MS spectra (normalized intensities, filtered for quality, with top peaks retained) that have been encoded using a spectral representation method (e.g., DepthCharge with sinusoidal positional encoding on m/z and intensity), and you need to generate ranked predictions of peptide sequences without relying on a protein sequence database. This is appropriate for discovery of unexpected peptides in immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any bottom-up tandem mass spectrometry dataset.

## When NOT to use

- When your input spectra have not been preprocessed (normalized, filtered for quality, peak-selected) — preprocessing must occur before encoding and inference.
- When you are trying to identify peptides against a known protein database — use peptide-centric database search tools (e.g., MS-GF+) instead of de novo sequencing.
- When your goal is to train or fine-tune a new transformer model — this skill applies only to inference with a pretrained model.

## Inputs

- Encoded MS/MS spectra (e.g., from DepthCharge encoder with sinusoidal positional encoding)
- Precursor m/z and charge state for each spectrum
- Configuration parameters (beam width, min_peptide_len, precursor_mass_tol)

## Outputs

- Ranked candidate peptide sequences per spectrum
- Per-residue confidence logits (product of transformer decoder logits)
- Peptide-level scores
- mzTab export file with sequence, modifications, scores, and scan metadata

## How to apply

Load the pretrained Casanovo transformer encoder–decoder model (trained on annotated MS/MS spectra) and pass the encoded spectra through it using beam search decoding with a beam width typically set to 10. For each scan, the decoder generates multiple candidate peptide sequences ranked by cumulative score. Apply post-hoc filters to reject predictions below minimum peptide length, penalize sequences outside precursor mass tolerance (specified in ppm or Da), and compute per-residue confidence scores as the product of logits from the transformer decoder. The transformer's attention mechanism learns to align spectral peaks with amino acid transitions, allowing it to handle variable-length sequences and complex fragmentation patterns. Export ranked predictions with sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge state, and scan metadata to mzTab format for downstream analysis and visualization.

## Related tools

- **Casanovo** (Pretrained transformer encoder–decoder model that performs de novo peptide inference from encoded MS/MS spectra using beam search decoding) — https://github.com/Noble-Lab/casanovo
- **DepthCharge** (Spectral encoder that applies sinusoidal positional encoding to m/z values and intensities prior to transformer inference)
- **PyTorch** (Deep learning framework used to instantiate, load, and execute the transformer encoder–decoder model)
- **CUDA Toolkit** (GPU acceleration library for efficient transformer inference on NVIDIA hardware)
- **PDV** (Graphical interface for inspecting and visualizing transformer inference outputs (peptide predictions and annotated spectra)) — https://github.com/wenbostar/PDV
- **limelight-import-casanovo** (Converter that transforms Casanovo inference results from mzTab format to Limelight XML for web-based visualization and validation) — https://github.com/yeastrc/limelight-import-casanovo

## Examples

```
from casanovo import Casanovo; model = Casanovo.load_pretrained(); predictions = model.sequence_datasets(dataset='encoded_spectra.mzML', beam_width=10, min_peptide_len=6, precursor_mass_tol=10); predictions.write_mztab('predictions.mztab')
```

## Evaluation signals

- Beam search decoder generates at least one candidate sequence per spectrum; verify no missing predictions in output.
- All exported peptide sequences meet minimum length threshold (min_peptide_len parameter); check mzTab for sequence lengths.
- Precursor mass of each prediction matches the input precursor m/z ± tolerance window (specified in ppm or Da); validate mass arithmetic in mzTab export.
- Per-residue confidence scores are strictly between 0 and 1 (logit product normalized); spot-check score ranges in output file.
- mzTab export conforms to PSI-defined schema, includes ProForma 2.0 modification notation, and retains scan metadata (precursor m/z, charge, scan ID); parse and validate mzTab structure.

## Limitations

- Transformer inference accuracy is bounded by the quality and diversity of the training dataset; performance may degrade on novel fragmentation patterns or sample types not well-represented in training.
- Beam search with fixed beam width (typically 10) provides approximate decoding; exact sequence ranking may differ from exhaustive search, and rare high-scoring sequences may be pruned during beam construction.
- Post-hoc filters (mass tolerance, min length) are applied after inference; filtering cannot recover sequences rejected by the transformer decoder itself.
- The model is deterministic given fixed inputs; no uncertainty quantification or confidence intervals around predictions beyond per-residue logit products.
- Inference speed and memory footprint scale with spectrum complexity (number of peaks) and batch size; very large datasets may require optimization or batching strategies.

## Evidence

- [methods] Pass encoded spectra through the pretrained Casanovo transformer encoder–decoder with beam search decoding: "Pass encoded spectra through the pretrained Casanovo transformer encoder–decoder with beam search decoding (beam width typically 10) to generate candidate peptide sequences ranked by score."
- [methods] Apply post-hoc filters on predictions: "Apply post-hoc filters: reject predictions failing the minimum peptide length (min_peptide_len), penalize predictions outside precursor mass tolerance (precursor_mass_tol in ppm or Da), and assign"
- [methods] Export results in mzTab format with structured metadata: "Export predictions to mzTab format, including sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge state, and scan metadata."
- [intro] Casanovo translates peaks in MS/MS spectra into amino acid sequences: "Casanovo 'translates' peaks in MS/MS spectra into amino acid sequences with remarkable precision."
- [intro] Application domain for de novo sequencing: "particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics, or any setting in which you are interested in identifying peptides that may not be in your protein database."
- [readme] Transformer architecture for spectral-to-sequence translation: "Powered by a transformer neural network, Casanovo 'translates' peaks in MS/MS spectra into amino acid sequences with remarkable precision."
