---
name: msms-spectrum-metadata-preservation
description: Use when removing invalid or malformed entries (e.g., SMILES validation, format errors) from large spectral datasets (GNPS, MoNA, MTBLS1572, MassBank).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3071
  tools:
  - Python
  - PyTorch
  - read_raw_spectra
  - Python 3.12
  - PyTorch 2.6.0
  techniques:
  - tandem-MS
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

# MS/MS Spectrum Metadata Preservation

## Summary

Retain and propagate auxiliary annotations (precursor m/z, peak lists, chemical identifiers) linked to each spectrum record throughout filtering and preprocessing workflows. This ensures that cleaned spectral embeddings remain scientifically interpretable and traceable to their original library sources.

## When to use

Apply this skill when removing invalid or malformed entries (e.g., SMILES validation, format errors) from large spectral datasets (GNPS, MoNA, MTBLS1572, MassBank). Without metadata preservation, you lose the ability to retrieve compound identities, precursor masses, or source provenance for downstream retrieval or identification tasks.

## When NOT to use

- Input spectra are already in a reduced feature representation (e.g., fingerprint vectors, pre-computed embeddings) with no original m/z or annotation data—metadata preservation assumes source records exist.
- Workflow goal is rapid anonymization or deidentification; preserving source metadata contradicts privacy requirements.
- Downstream task requires only similarity scores or rankings without needing to report which compound each match corresponds to.

## Inputs

- Raw spectral data in MSP or similar format (precursor m/z, peak intensities, metadata fields)
- SMILES or other chemical structure strings linked to each spectrum
- Spectral library records from GNPS, MoNA, MTBLS1572, MassBank, or MassSpecGym

## Outputs

- Cleaned spectral dataset with valid entries and intact metadata (precursor m/z, peak lists, SMILES, annotations)
- Cleaning report documenting entries removed, removal reasons, retention statistics per source dataset

## How to apply

After filtering spectra for structural validity (e.g., SMILES correctness, format compliance), maintain associations between the spectrum record (m/z peaks, intensities) and its metadata fields: precursor m/z, SMILES string, InChI, common name, library source, and any other annotations present in the original record. Implement this by treating metadata as a parallel data structure—do not strip or re-index it during removal operations. When entries are removed (e.g., flagged for malformed SMILES), delete the entire record pair (spectrum + metadata) together, rather than orphaning metadata. Validate preservation by spot-checking that retained spectra can still retrieve their compound identifiers and precursor masses without additional lookups.

## Related tools

- **read_raw_spectra** (Load spectral records and associated metadata from MSP or library files into structured format for downstream filtering and preservation checks) — https://github.com/sword-nan/SpecEmbedding
- **Python 3.12** (Execute data wrangling, filtering, and metadata-pairing logic during spectral cleaning pipeline)
- **PyTorch 2.6.0** (Compute embeddings and similarity scores for filtered spectra while preserving original metadata links) — https://github.com/sword-nan/SpecEmbedding

## Examples

```
from SpecEmbedding.utils.clean import read_raw_spectra; q = read_raw_spectra('./q.msp'); print(f"Spectrum 0: SMILES={q[0].get('smiles')}, precursor_mz={q[0].get('precursor_mz')}")
```

## Evaluation signals

- Row count: number of retained spectrum–metadata pairs equals number of valid spectra after filtering (no orphaned records).
- Completeness: spot-check 10–20 retained entries; verify each spectrum record has non-null precursor m/z, peak list, and SMILES fields.
- Traceability: confirm retained spectra can be matched back to their original dataset source (GNPS, MoNA, etc.) via preserved metadata field.
- Cleaning report consistency: sum of (removed entries + retained entries) equals original dataset size; removal reasons are documented and reproducible.
- Round-trip validation: pass retained spectra through embedding pipeline (e.g., via load_tanimoto_supcon_aug_model) and confirm cosine similarity retrieval returns correct compound identifiers from preserved metadata.

## Limitations

- Metadata preservation does not validate correctness of annotations themselves—a spectrum may retain invalid or contradictory precursor m/z or SMILES alongside valid peaks.
- If multiple versions of the same compound exist in source libraries with conflicting metadata, preservation copies all versions; downstream deduplication logic must handle this separately.
- Windows platforms may encounter numerical errors during downstream operations (e.g., cosine similarity) due to @njit decorators from numba, affecting metadata-linked similarity computations; solution is to comment out numba decorators.

## Evidence

- [other] Retain metadata associations (precursor m/z, peak lists, annotations) for all valid entries.: "Retain metadata associations (precursor m/z, peak lists, annotations) for all valid entries."
- [other] Write the cleaned spectral dataset to output format, preserving the original spectral structure and library organization.: "Write the cleaned spectral dataset to output format, preserving the original spectral structure and library organization."
- [other] Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset.: "Generate a cleaning report documenting the number of entries removed, removal reasons, and retention statistics per source dataset."
- [readme] To further improve data quality, we removed entries with malformed or invalid SMILES strings.: "To further improve data quality, we removed entries with malformed or invalid SMILES strings."
- [readme] Load query and reference spectra: "Load query and reference spectra"
