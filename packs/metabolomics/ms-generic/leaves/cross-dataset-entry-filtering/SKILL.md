---
name: cross-dataset-entry-filtering
description: Use when you have received MSBERT-preprocessed spectral data from GNPS, MoNA, or MTBLS1572 and need to ensure data integrity before training a spectral embedding model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_3172
  tools:
  - Python
  - PyTorch
  - read_raw_spectra
  - Python 3.12
  - PyTorch 2.6.0
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-dataset-entry-filtering

## Summary

Remove entries with malformed or invalid SMILES strings from MSBERT-preprocessed spectral datasets (GNPS, MoNA, MTBLS1572) to improve data quality before model training. This filtering step ensures that only chemically valid and syntactically correct molecular identifiers are retained in the training corpus.

## When to use

Apply this skill when you have received MSBERT-preprocessed spectral data from GNPS, MoNA, or MTBLS1572 and need to ensure data integrity before training a spectral embedding model. Specifically, use it when you observe that the raw spectral library contains entries with missing, null, or malformed SMILES fields that would cause errors or degrade model performance during embedding training.

## When NOT to use

- Input data is already from a curated spectral library (MassBank, MassSpecGym) with pre-validated SMILES — these are high-quality and filtering may remove valuable edge cases.
- SMILES strings are not available or are intentionally sparse — filtering would remove most entries without a valid alternative chemical identifier.
- Downstream analysis requires retaining raw data with known errors for error analysis or method comparison — filtering removes the evidence needed for such studies.

## Inputs

- MSBERT-preprocessed spectral data from GNPS, MoNA, or MTBLS1572 datasets
- Raw spectrum records in MSP or similar format with SMILES field
- Spectral metadata: precursor m/z, peak lists, library annotations

## Outputs

- Cleaned spectral dataset with valid entries retained
- Filtered spectra with malformed SMILES entries removed
- Preservation of spectral metadata and library structure
- Data cleaning report with removal statistics and retention rates per source dataset

## How to apply

Load the MSBERT-preprocessed spectral dataset using spectral-reading utilities (e.g., read_raw_spectra function). For each spectrum entry, validate the associated SMILES string by checking for valid chemical notation (proper atom symbols, bond notation, charge states) and well-formed syntax (balanced parentheses, valid ring closures). Flag entries with null/missing SMILES fields or those that fail structural validation. Remove flagged entries while preserving metadata associations (precursor m/z, peak lists, spectral annotations, original library organization) for all retained entries. Generate a cleaning report documenting the number of entries removed, categorized by removal reason (missing SMILES, format error, invalid sequence), and retention statistics per source dataset to assess impact and reproducibility.

## Related tools

- **read_raw_spectra** (Loads MSBERT-preprocessed spectral data from GNPS, MoNA, and MTBLS1572 in MSP format into memory) — https://github.com/sword-nan/SpecEmbedding
- **Python 3.12** (Execution environment for implementing SMILES validation logic and data processing workflows)
- **PyTorch 2.6.0** (Backend for downstream spectral embedding model training after data cleaning)

## Examples

```
from SpecEmbedding.utils.clean import read_raw_spectra; spectra = read_raw_spectra('./gnps_data.msp'); cleaned_spectra = [s for s in spectra if s.get('smiles') and is_valid_smiles(s.get('smiles'))]; print(f'Removed {len(spectra) - len(cleaned_spectra)} invalid entries')
```

## Evaluation signals

- Entries with null or missing SMILES fields are completely removed; no null values remain in the retained dataset
- All retained SMILES strings pass structural validation (valid atom symbols, balanced charges, correct ring closure notation, no orphaned bonds)
- Metadata associations (precursor m/z, peak annotations) are perfectly preserved for all retained entries; no data loss in secondary fields
- Cleaning report statistics are internally consistent: (original entries – removed entries) = retained entries
- Retention rates per dataset (GNPS, MoNA, MTBLS1572) are documented; anomalously high removal rates (>50%) warrant manual inspection for validation rule overfitting

## Limitations

- SMILES validation rules are syntactic and structural only; chemically nonsensical but syntactically valid SMILES (e.g., disconnected fragments) will not be detected or removed.
- No canonical SMILES transformation is applied; isomeric ambiguity or non-standard notation may pass validation but still represent poor-quality identifiers.
- Filtering is irreversible; once malformed entries are removed, they cannot be recovered from the output dataset without re-running on the original input.
- On Windows systems, @njit decorators from numba library may cause numerical errors during processing and should be commented out before execution.

## Evidence

- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings: "To further improve data quality, we removed entries with malformed or invalid SMILES strings"
- [other] Validate each SMILES string entry for structural and syntactic correctness by checking for valid chemical notation and proper formatting: "Validate each SMILES string entry for structural and syntactic correctness by checking for valid chemical notation and proper formatting"
- [other] Flag and remove entries containing malformed SMILES sequences or entries with missing/null SMILES fields: "Flag and remove entries containing malformed SMILES sequences or entries with missing/null SMILES fields"
- [other] Retain metadata associations (precursor m/z, peak lists, annotations) for all valid entries: "Retain metadata associations (precursor m/z, peak lists, annotations) for all valid entries"
- [other] Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset: "Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset"
- [readme] All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare: "All cleaned data, along with the preprocessing scripts and 10-fold query/reference splits used for evaluation, are available on figshare"
- [readme] Load query and reference spectra ... Initialize tokenizer and device ... Define the SiameseModel architecture: "Load query and reference spectra ... Initialize tokenizer and device ... Define the SiameseModel architecture"
