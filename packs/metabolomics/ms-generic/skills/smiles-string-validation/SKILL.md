---
name: smiles-string-validation
description: Use when you have MSBERT-preprocessed spectral datasets (GNPS, MoNA, or MTBLS1572 format) with SMILES annotations before training a spectral embedding or compound identification model.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3307
  - http://edamontology.org/topic_0154
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# SMILES String Validation

## Summary

Validates and removes spectral entries with malformed or syntactically invalid SMILES strings from mass spectrometry datasets (GNPS, MoNA, MTBLS1572) preprocessed by MSBERT. This data-cleaning step improves input quality for downstream spectral embedding model training by ensuring structural and syntactic correctness of chemical notation.

## When to use

Apply this skill when you have MSBERT-preprocessed spectral datasets (GNPS, MoNA, or MTBLS1572 format) with SMILES annotations before training a spectral embedding or compound identification model. Use it if the source spectral library may contain format errors, missing SMILES fields, or entries with improperly formatted chemical strings that could degrade model performance.

## When NOT to use

- Input spectra already validated by a curated high-quality library (e.g., MassBank, MassSpecGym) where SMILES correctness is guaranteed
- Spectral dataset without SMILES annotations or structured chemical identifiers
- Use case requiring retention of all entries for exploratory analysis regardless of SMILES validity

## Inputs

- MSBERT-preprocessed spectral data (MSP or equivalent format from GNPS, MoNA, or MTBLS1572)
- Spectral entries with SMILES string annotations and metadata (precursor m/z, peak lists)

## Outputs

- Cleaned spectral dataset with invalid SMILES entries removed
- Validated spectral entries with retained metadata associations
- Cleaning report documenting removal counts, reasons, and per-dataset retention statistics

## How to apply

Load the MSBERT-preprocessed spectral data using spectral-reading utilities (e.g., read_raw_spectra function). For each entry, validate the SMILES string by checking for valid chemical notation (proper valence, bracket matching, atom symbols) and syntactic correctness (no trailing/leading whitespace, valid bond notation). Flag and remove entries containing malformed SMILES sequences, missing or null SMILES fields, and format errors. Retain all metadata associations (precursor m/z, peak lists, annotations) for valid entries. Write the cleaned dataset to output format, preserving spectral structure and library organization. Generate a cleaning report documenting the count of entries removed, removal reasons (malformed syntax, missing field, format error), and retention statistics per source dataset to quantify data quality improvement.

## Related tools

- **read_raw_spectra** (Loads MSBERT-preprocessed spectral data from MSP format files for SMILES validation) — https://github.com/sword-nan/SpecEmbedding
- **Python 3.12** (Runtime environment for implementing SMILES validation and cleaning scripts)
- **PyTorch 2.6.0** (Optional acceleration framework for large-scale dataset processing if integrated with downstream embedding models)

## Examples

```
from SpecEmbedding.utils.clean import read_raw_spectra
q = read_raw_spectra("./GNPS_preprocessed.msp")
valid_entries = [entry for entry in q if entry.get('smiles') and is_valid_smiles(entry['smiles'])]
print(f"Removed {len(q) - len(valid_entries)} entries with invalid SMILES")
```

## Evaluation signals

- Verify that all remaining entries have non-null, non-empty SMILES strings with valid atomic symbols, bond notations, and balanced brackets
- Confirm that removal count and per-dataset retention statistics reported in cleaning report match independent validation of input/output record counts
- Check that metadata associations (precursor m/z, peak lists, annotations) are preserved without loss or corruption in valid entries
- Validate that downstream spectral embedding model performance improves (e.g., higher hit rate on MassBank/MassSpecGym evaluation sets) compared to unfiltered input
- Cross-check removed entries against a SMILES validation library (e.g., RDKit parse) to confirm false positives are minimal

## Limitations

- Validation relies on syntactic correctness checks; chemically invalid but syntactically valid SMILES (e.g., impossible valence states that pass basic bracket/symbol checks) may not be detected without full structure parsing
- On Windows systems, numerical errors during processing may occur due to @njit decorators from the numba library; workaround requires commenting out @njit decorators in the code
- Removal is irreversible; entries flagged as invalid cannot be recovered; archive original data if reanalysis may be needed

## Evidence

- [other] The data-cleaning step applies removal of entries with malformed or invalid SMILES strings to MSBERT-preprocessed GNPS, MoNA, and MTBLS1572 datasets to improve data quality for spectral embedding model training.: "removal of entries with malformed or invalid SMILES strings to MSBERT-preprocessed GNPS, MoNA, and MTBLS1572 datasets to improve data quality for spectral embedding model training"
- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings: "removed entries with malformed or invalid SMILES strings"
- [other] Validate each SMILES string entry for structural and syntactic correctness by checking for valid chemical notation and proper formatting.: "Validate each SMILES string entry for structural and syntactic correctness by checking for valid chemical notation and proper formatting"
- [other] Flag and remove entries containing malformed SMILES sequences or entries with missing/null SMILES fields.: "Flag and remove entries containing malformed SMILES sequences or entries with missing/null SMILES fields"
- [other] Retain metadata associations (precursor m/z, peak lists, annotations) for all valid entries.: "Retain metadata associations (precursor m/z, peak lists, annotations) for all valid entries"
- [other] Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset.: "Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset"
