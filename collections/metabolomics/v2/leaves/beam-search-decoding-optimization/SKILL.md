---
name: beam-search-decoding-optimization
description: Use when using Casanovo for de novo peptide sequencing on high-stakes
  datasets (immunopeptidomics, paleoproteomics, or monoclonal antibody discovery)
  where missing the correct sequence in the top-1 prediction is costly.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3644
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# beam-search-decoding-optimization

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Replace greedy decoding with beam search decoding in Casanovo to generate multiple candidate peptide sequences ranked by confidence score, improving the likelihood of recovering correct sequences that greedy selection might miss. This skill is applied when MS/MS spectral predictions need higher accuracy and you can tolerate increased computational cost.

## When to use

Apply this skill when using Casanovo for de novo peptide sequencing on high-stakes datasets (immunopeptidomics, paleoproteomics, or monoclonal antibody discovery) where missing the correct sequence in the top-1 prediction is costly. Use it if you have access to GPU acceleration and can afford the computational overhead of exploring multiple decoding paths. Do NOT use if you require real-time or single-candidate predictions.

## When NOT to use

- Input is already a single high-confidence peptide sequence (e.g., from database search)—beam search is only beneficial for de novo prediction where multiple candidates must be ranked.
- Computational resources are severely limited (no GPU, low memory)—beam search multiplies inference cost by the beam width factor; greedy decoding is faster for resource-constrained settings.
- Real-time or streaming MS/MS analysis is required—beam search adds latency incompatible with rapid turnaround demands.

## Inputs

- pre-trained Casanovo checkpoint (PyTorch model file)
- annotated MS/MS spectra in MGF format or mzML/mzXML files
- Casanovo configuration YAML with beam search parameters (beam_width, min_peptide_len, precursor_mass_tol, min_peaks, max_peaks)

## Outputs

- ranked peptide sequence predictions (multiple candidates per spectrum, ordered by score)
- per-residue confidence logits and cumulative peptide scores
- mzTab format export with sequence, ProForma 2.0 modifications, amino acid scores, precursor m/z, charge state, and scan metadata
- comparison metrics (precision, recall, F1 score) between beam search and greedy baseline

## How to apply

Load a pre-trained Casanovo checkpoint and reconfigure the decoder from greedy mode to beam search with a beam width (typically 10) to generate multiple ranked sequence candidates per spectrum. Preprocess MS/MS spectra by normalizing intensities, filtering scans below min_peaks threshold, and retaining only top max_peaks peaks. Encode spectra using DepthCharge with sinusoidal positional encoding on m/z and intensity values. Pass encoded spectra through the Casanovo transformer encoder–decoder with beam search enabled to obtain candidate sequences ranked by cumulative log-probability. Apply post-hoc filters: reject predictions below min_peptide_len, penalize predictions outside precursor_mass_tol (in ppm or Da), and compute per-residue confidence scores as the product of logits. Compare beam search predictions against greedy baseline using precision, recall, and F1 score at the amino acid and peptide level to quantify improvement.

## Related tools

- **Casanovo** (transformer-based de novo peptide sequencing engine; configured with beam search decoder instead of greedy decoder) — https://github.com/Noble-Lab/casanovo
- **PyTorch** (deep learning framework for loading and executing the pre-trained Casanovo transformer model)
- **DepthCharge** (spectrum encoding library used to vectorize MS/MS peaks with sinusoidal positional encoding before transformer inference)
- **CUDA Toolkit** (GPU acceleration library required for efficient beam search inference on large spectral datasets)
- **PDV** (visualization tool for inspecting and comparing predicted peptide sequences and confidence scores from beam search output) — https://github.com/wenbostar/PDV
- **limelight-import-casanovo** (converter to export Casanovo beam search results (mzTab) to Limelight XML format for interactive exploration) — https://github.com/yeastrc/limelight-import-casanovo

## Evaluation signals

- Beam search generates multiple candidate sequences per spectrum (beam width > 1) with monotonically decreasing cumulative log-probability scores.
- Comparison metrics (precision, recall, F1) for beam search predictions are equal to or higher than greedy baseline at both amino acid and peptide level.
- Precursor mass tolerance filter rejects sequences deviating > precursor_mass_tol (ppm or Da) from observed precursor m/z; filtered predictions cluster within the specified tolerance window.
- Per-residue confidence scores (product of logits) and peptide scores are properly exported to mzTab format with all required fields: sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge, scan metadata.
- GPU utilization (monitored via nvidia-smi) shows active CUDA kernel execution during beam search inference, confirming acceleration is enabled.

## Limitations

- Beam search increases inference latency and memory consumption proportionally to beam width; full-dataset re-inference may be required to compare against greedy baseline.
- Quality of beam search predictions depends on pre-trained checkpoint quality and preprocessing parameters (min_peaks, max_peaks, normalization); suboptimal spectrum filtering upstream will propagate to poor rankings.
- Beam search does not guarantee globally optimal sequences—it explores a limited search space bounded by beam width; very rare or unexpected sequences may still be missed if they fall outside the top-k candidates.
- Post-hoc filters (precursor_mass_tol, min_peptide_len) may reject valid candidates generated by beam search; threshold tuning is data-dependent and may require empirical validation on a validation set.

## Evidence

- [other] Casanovo uses a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences.: "Casanovo is powered by a transformer neural network that translates peaks in MS/MS spectra into amino acid sequences."
- [other] Beam search decoding configuration and workflow in Casanovo task.: "Reconfigure Casanovo to use beam search decoding with the same checkpoint and dataset, running prediction and recording predicted sequences."
- [other] Spectrum preprocessing and encoding with DepthCharge in Casanovo.: "Preprocess spectra by normalizing intensities, filtering low-quality scans (fewer than min_peaks threshold), and retaining only the top max_peaks peaks per spectrum."
- [other] Encoder-decoder with beam search and post-hoc filtering.: "Pass encoded spectra through the pretrained Casanovo transformer encoder–decoder with beam search decoding (beam width typically 10) to generate candidate peptide sequences ranked by score."
- [other] Post-hoc filtering and score assignment methodology.: "Apply post-hoc filters: reject predictions failing the minimum peptide length (min_peptide_len), penalize predictions outside precursor mass tolerance (precursor_mass_tol in ppm or Da), and assign"
- [other] Comparison metric methodology for beam search vs. greedy.: "Compare predicted sequences from both methods at the amino acid and peptide level, computing precision, recall, and F1 score for each decoding strategy."
- [other] mzTab export format and metadata fields.: "Export predictions to mzTab format, including sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge state, and scan metadata."
- [readme] README statement on Casanovo accuracy and use cases.: "Casanovo 'translates' peaks in MS/MS spectra into amino acid sequences with remarkable precision."
