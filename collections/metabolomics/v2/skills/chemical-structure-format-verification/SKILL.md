---
name: chemical-structure-format-verification
description: Use when working with mass spectrometry spectral libraries (GNPS, MoNA, MTBLS1572, MassBank) that have been preprocessed by prior teams but may contain formatting errors or entries with missing/null SMILES fields.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3375
  tools:
  - Python
  - PyTorch
  - read_raw_spectra
  - SpecEmbedding.utils.clean module
  - Python 3.12
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.1021/acs.analchem.5c02655
  title: SpecEmbedding
evidence_spans:
- Python：3.12
- PyTorch：2.6.0 + CUDA 12.4
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_specembedding_cq
    doi: 10.1021/acs.analchem.5c02655
    title: SpecEmbedding
  dedup_kept_from: coll_specembedding_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02655
  all_source_dois:
  - 10.1021/acs.analchem.5c02655
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-format-verification

## Summary

Validates SMILES strings for structural and syntactic correctness to remove malformed entries from spectral datasets before embedding model training. This filtering step ensures data quality and prevents invalid chemical notation from corrupting downstream spectral embeddings.

## When to use

Apply this skill when working with mass spectrometry spectral libraries (GNPS, MoNA, MTBLS1572, MassBank) that have been preprocessed by prior teams but may contain formatting errors or entries with missing/null SMILES fields. Use it as a mandatory pre-training data-cleaning step for deep learning models that depend on valid chemical structure representations, such as supervised contrastive learning frameworks for spectral embedding.

## When NOT to use

- Input spectra are from high-quality curated libraries (MassBank, MassSpecGym) where SMILES have already been validated by expert curation.
- The downstream task requires preservation of all entries including those with missing or ambiguous structures (e.g., for imputation or recovery studies).
- SMILES strings are not available or are not the primary chemical identifier in the dataset.

## Inputs

- MSBERT-preprocessed spectral datasets (GNPS, MoNA, MTBLS1572, or equivalent in .msp format)
- Spectrum entries with SMILES string fields and associated metadata (precursor m/z, peak lists, annotations)

## Outputs

- Cleaned spectral dataset with malformed/invalid SMILES entries removed
- Retention mapping (original entry ID → kept or removed status)
- Cleaning report with per-source statistics (entries removed, reasons, retention rate)

## How to apply

Load MSBERT-preprocessed spectral data using spectral-reading utilities (e.g., read_raw_spectra function from SpecEmbedding.utils.clean). For each spectrum entry, validate its SMILES string by checking for valid chemical notation and proper formatting; entries with malformed SMILES sequences or null/missing SMILES fields are flagged for removal. Retain all metadata associations (precursor m/z, peak lists, annotations) for valid entries. Write the cleaned spectral dataset to output format, preserving the original spectral structure and library organization. Generate a cleaning report documenting the count of entries removed, reasons for removal (format error vs. missing SMILES), and retention statistics stratified by source dataset (GNPS, MoNA, MTBLS1572).

## Related tools

- **read_raw_spectra** (Loads spectral data from .msp or other spectral file formats into memory for validation) — https://github.com/sword-nan/SpecEmbedding
- **SpecEmbedding.utils.clean module** (Provides spectral reading and SMILES validation utilities) — https://github.com/sword-nan/SpecEmbedding
- **Python 3.12** (Primary language for implementing SMILES validation logic and spectral data processing)

## Examples

```
from SpecEmbedding.utils.clean import read_raw_spectra; q = read_raw_spectra('./q.msp'); print(f'Loaded {len(q)} spectra with valid SMILES fields')
```

## Evaluation signals

- Total number of entries removed matches the count reported in the cleaning report, stratified by removal reason (format error vs. missing SMILES).
- All remaining spectrum entries have non-null, syntactically valid SMILES strings that can be parsed by standard cheminformatics libraries (e.g., RDKit).
- Metadata associations (precursor m/z, peak lists, annotations) are preserved for all retained entries without loss or scrambling.
- Retention rate per source dataset (GNPS, MoNA, MTBLS1572) is reasonable and consistent with the distribution of malformed entries reported in the MSBERT preprocessing paper.
- Downstream spectral embedding model training converges without errors related to invalid SMILES tokens or null chemical identifiers.

## Limitations

- SMILES validation is format-based only; syntactically valid SMILES may still represent chemically impossible or ambiguous structures not caught by this skill.
- Does not perform structural deduplication or tautomeric/stereoisomeric normalization; valid but chemically equivalent variants remain as separate entries.
- Windows environment may encounter numerical errors during downstream similarity computation due to numba @njit decorators, requiring manual code modification.
- Removal is irreversible; no recovery mechanism is provided for entries flagged as invalid without external archival.

## Evidence

- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings: "To further improve data quality, we removed entries with malformed or invalid SMILES strings"
- [other] The data-cleaning step applies removal of entries with malformed or invalid SMILES strings to MSBERT-preprocessed GNPS, MoNA, and MTBLS1572 datasets to improve data quality for spectral embedding model training.: "removal of entries with malformed or invalid SMILES strings to MSBERT-preprocessed GNPS, MoNA, and MTBLS1572 datasets to improve data quality"
- [other] Validate each SMILES string entry for structural and syntactic correctness by checking for valid chemical notation and proper formatting. 3. Flag and remove entries containing malformed SMILES sequences or entries with missing/null SMILES fields.: "Validate each SMILES string entry for structural and syntactic correctness by checking for valid chemical notation and proper formatting. Flag and remove entries containing malformed SMILES sequences"
- [other] Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset.: "Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset"
- [readme] All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
