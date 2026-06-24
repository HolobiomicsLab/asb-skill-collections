---
name: vocabulary-coverage-validation
description: Use when after merging separate vocabularies for distinct data modalities
  (e.g., spectral tokens for m/z values and intensities, structural tokens for SMILES
  or graphs) and before deploying the unified vocabulary in a language model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_3674
  tools:
  - BART
  - MS-BART
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.48550/arxiv.2510.20615
  title: MS-BART
evidence_spans:
- MS-BART is the first to leverage language model for mass spectra structure elucidation
  by introducing a unified vocabulary
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms_bart_cq
    doi: 10.48550/arxiv.2510.20615
    title: MS-BART
  dedup_kept_from: coll_ms_bart_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.48550/arxiv.2510.20615
  all_source_dois:
  - 10.48550/arxiv.2510.20615
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Vocabulary Coverage Validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validates that a unified token vocabulary correctly encodes representative samples from heterogeneous data domains (e.g., mass spectra and molecular structures) with complete coverage, no collisions, and correct bidirectional mapping. This skill ensures the vocabulary is ready for downstream pretraining and fine-tuning in multimodal sequence models.

## When to use

Apply this skill after merging separate vocabularies for distinct data modalities (e.g., spectral tokens for m/z values and intensities, structural tokens for SMILES or graphs) and before deploying the unified vocabulary in a language model. Use when you need confidence that all data types in your training corpus will tokenize without errors, unknown tokens, or collisions.

## When NOT to use

- Vocabulary is already validated and in production use for an established model — re-validation is redundant unless the vocabulary is being expanded or merged with new data.
- Input data is unimodal (single data type) — vocabulary merging and collision checking are not necessary; standard vocabulary coverage checks suffice.
- Representative sample set is too small or non-representative of the true data distribution — validation results may be unreliable and should be re-run with a larger, stratified sample.

## Inputs

- Spectral token vocabulary (m/z values, intensity ranges)
- Structural token vocabulary (SMILES strings or graph tokens)
- Representative mass spectra (sample set covering typical m/z and intensity distributions)
- Representative molecular structures (sample set covering structural diversity)
- Bidirectional mapping dictionary (raw data ↔ token ID)

## Outputs

- Validated unified token vocabulary (merged, collision-free token set with unique IDs)
- Coverage validation report (vocabulary statistics: total tokens, spectral token count, structural token count, special token assignments)
- Coverage metrics (domain coverage completeness, encoding success rate for representative samples)
- Bidirectional encoding/decoding verification (confirmation of correct mapping in both directions)

## How to apply

Encode representative mass spectra and molecular structures using the unified vocabulary's bidirectional mapping dictionary. Verify that all spectral features (m/z, intensities) and structural elements (SMILES characters, graph nodes) tokenize to valid token IDs without triggering unknown or padding tokens for in-domain data. Check for token ID collisions (no two distinct data elements mapping to the same token) and confirm coverage of the expected data domain range. Generate a summary report documenting total token count, spectral vs. structural token counts, special token assignments (BOS, EOS, PAD, UNK), and domain coverage metrics to confirm the vocabulary is complete and collision-free.

## Related tools

- **MS-BART** (Language model framework that consumes the unified vocabulary for end-to-end pretraining, fine-tuning, and alignment of mass spectra and molecular structures) — https://github.com/OpenDFM/MS-BART

## Examples

```
python -c "from ms_bart import Vocabulary; vocab = Vocabulary.load('vocab.json'); spectra = load_representative_spectra('spectra_sample.mgf'); molecules = load_representative_molecules('molecules_sample.smi'); success = vocab.validate(spectra, molecules); print(vocab.coverage_report())"
```

## Evaluation signals

- All representative mass spectra tokenize without unknown token (UNK) or excessive padding token (PAD) activations; encoding success rate = 100% for in-domain spectral samples.
- All representative molecular structures tokenize correctly; no SMILES characters or graph tokens fall outside the vocabulary or map to collision token IDs.
- Bidirectional mapping is invertible: raw data → token ID → raw data produces identical results (round-trip consistency check).
- Special tokens (BOS, EOS, PAD, UNK) are assigned unique, non-overlapping token IDs and do not conflict with spectral or structural token IDs.
- Coverage metrics report shows vocabulary domain coverage ≥ 95% across the m/z range, intensity quantiles, and structural feature distributions observed in representative samples; no gaps in common data ranges.

## Limitations

- Vocabulary validation is performed on a representative sample set; true coverage of rare or outlier data points (e.g., extreme m/z values, highly unusual molecular structures) may not be fully characterized.
- Token collision detection relies on explicit ID assignment logic; if the mapping function has latent collisions or hash collisions in the implementation, they may not be caught by validation on the representative set alone.
- Vocabulary size and token ID ranges must be large enough to accommodate both spectral and structural domains without overflow or reuse; if the unified vocabulary is undersized, domain coverage will be incomplete even if representative samples validate.

## Evidence

- [other] Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is complete.: "Validate the vocabulary by encoding representative mass spectra and molecular structures to verify all data types tokenize correctly, no token collisions occur, and coverage of the data domain is"
- [other] Generate a summary report documenting vocabulary statistics (total tokens, spectral token count, structural token count, special token assignments) and coverage metrics.: "Generate a summary report documenting vocabulary statistics (total tokens, spectral token count, structural token count, special token assignments) and coverage metrics."
- [other] MS-BART introduces a unified vocabulary as a core mechanism to enable end-to-end pretraining, fine-tuning, and alignment of mass spectra and molecular structures within a language model framework.: "MS-BART introduces a unified vocabulary as a core mechanism to enable end-to-end pretraining, fine-tuning, and alignment of mass spectra and molecular structures within a language model framework."
- [other] Create a bidirectional mapping dictionary between raw spectral/structural data and token IDs for efficient encoding/decoding.: "Create a bidirectional mapping dictionary between raw spectral/structural data and token IDs for efficient encoding/decoding."
