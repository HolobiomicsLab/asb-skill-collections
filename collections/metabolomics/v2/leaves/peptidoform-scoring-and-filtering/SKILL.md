---
name: peptidoform-scoring-and-filtering
description: Use when after a transformer-based de novo sequencing model (such as
  Casanovo) generates candidate peptide sequences from MS/MS spectra, before exporting
  results or using them in database matching or visualization workflows.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3645
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Casanovo
  - PyTorch
  - DepthCharge
  - CUDA Toolkit
  - limelight-import-casanovo
  - PDV
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

# peptidoform-scoring-and-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Post-hoc validation and ranking of de novo peptide sequence predictions by applying mass tolerance constraints, minimum length thresholds, and per-residue confidence scoring. This skill ensures predicted peptidoforms meet chemical plausibility and quality criteria before downstream interpretation.

## When to use

After a transformer-based de novo sequencing model (such as Casanovo) generates candidate peptide sequences from MS/MS spectra, before exporting results or using them in database matching or visualization workflows. Essential when working with data-dependent acquisition bottom-up tandem mass spectrometry datasets where sequence predictions require post-hoc validation against precursor mass and confidence thresholds.

## When NOT to use

- Input peptides are already identified via database matching and do not need de novo filtering.
- Precursor m/z or charge state information is missing from the dataset.
- Working with closed-search or peptide library matching workflows where mass tolerance is enforced upstream.

## Inputs

- MS/MS spectra (MGF or mzML/mzXML format)
- de novo peptide predictions with per-residue logits and precursor m/z
- configuration parameters: min_peptide_len, precursor_mass_tol (ppm or Da)

## Outputs

- filtered peptidoform predictions (mzTab format)
- ranked candidate sequences with amino acid scores and peptide scores
- sequence and modification annotations in ProForma 2.0 notation

## How to apply

Apply three complementary filters in sequence: (1) reject predictions with sequence length below min_peptide_len threshold to eliminate implausibly short identifications; (2) penalize or exclude predictions whose calculated precursor mass deviates beyond precursor_mass_tol (specified in ppm or Daltons) from the experimental precursor m/z, correcting for charge state; (3) compute amino acid scores as the product of per-residue confidence logits from the model's decoder output, then aggregate into a peptide-level score for ranking. Retain only predictions passing all filters, then export with sequence, modifications (ProForma 2.0 notation), amino acid scores, peptide score, precursor m/z, charge state, and scan metadata to mzTab format for downstream analysis.

## Related tools

- **Casanovo** (transformer-based de novo sequencing model that generates candidate peptide sequences and per-residue confidence logits as input to scoring and filtering) — https://github.com/Noble-Lab/casanovo
- **DepthCharge** (spectrum encoder used upstream in Casanovo pipeline to generate spectral representations fed to the transformer)
- **PyTorch** (deep learning framework underlying Casanovo model inference and logit computation)
- **limelight-import-casanovo** (post-filtering converter that transforms filtered mzTab outputs to Limelight XML for visualization and quality assessment) — https://github.com/yeastrc/limelight-import-casanovo
- **PDV** (graphical viewer for inspecting and validating filtered Casanovo predictions and annotated spectra) — https://github.com/wenbostar/PDV

## Evaluation signals

- All retained peptides meet min_peptide_len threshold (no sequences shorter than configured cutoff).
- Precursor mass deviation for all retained peptides is within ±precursor_mass_tol across all charge states (verifiable by recalculating theoretical mass from sequence).
- Per-residue logit products are non-negative and bounded; peptide-level scores monotonically reflect confidence of highest-confidence residues.
- mzTab export contains all required fields: sequence, ProForma 2.0 modifications, amino acid scores, peptide score, precursor m/z, charge state, scan metadata.
- Filtered prediction count is ≤ unfiltered count; no predictions incorrectly retained or rejected due to parameter misconfiguration.

## Limitations

- Precursor mass tolerance filtering assumes accurate precursor m/z assignment; errors in charge state determination upstream will propagate as false negatives.
- Per-residue logits reflect model confidence, not ground-truth correctness; high logit scores do not guarantee sequence accuracy, especially for post-translational modifications or non-standard amino acids.
- ProForma 2.0 notation support depends on upstream model training; modifications not explicitly modeled during training may be missed or mislocalized.
- Filtering thresholds (min_peptide_len, precursor_mass_tol) are dataset- and instrument-specific; values must be tuned for each LC-MS platform and sample type.

## Evidence

- [other] Apply post-hoc filters: reject predictions failing the minimum peptide length (min_peptide_len), penalize predictions outside precursor mass tolerance (precursor_mass_tol in ppm or Da), and assign amino acid scores as the product of per-residue confidence logits.: "Apply post-hoc filters: reject predictions failing the minimum peptide length (min_peptide_len), penalize predictions outside precursor mass tolerance (precursor_mass_tol in ppm or Da), and assign"
- [other] Export predictions to mzTab format, including sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge state, and scan metadata.: "Export predictions to mzTab format, including sequence, modifications in ProForma 2.0 notation, amino acid scores, peptide score, precursor m/z, charge state, and scan metadata."
- [readme] Casanovo can be used to find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset, and is particularly useful for immunopeptidomics, metaproteomics, paleoproteomics, venomics: "find unexpected peptide sequences in any data-dependent acquisition, bottom-up tandem mass spectrometry dataset"
- [methods] A converter for generating Limelight XML from Casanovo results is available, see the converter documentation: "A converter for generating Limelight XML from Casanovo results is available"
