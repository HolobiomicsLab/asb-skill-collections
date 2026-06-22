---
name: inchikey-smiles-standardization
description: Use when when you have raw MS/MS spectra from repositories like GNPS that lack or have inconsistent chemical structure annotations (InChI/SMILES), and you need to produce a curated dataset with uniform 14-character InChIKey and SMILES/InChI annotations for downstream machine learning or similarity.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3280
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - matchms
  - pubchempy
  - RDKit
  - Python
  - PubChem
  techniques:
  - LC-MS
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields
- For each pair of molecular fingerprints Tanimoto scores were calculated, indicating the structural similarity of that pair. (as implemented in matchms [18])
- We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2deepscore_cq
    doi: 10.1186/s13321-021-00558-4
    title: MS2DeepScore
  dedup_kept_from: coll_ms2deepscore_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-021-00558-4
  all_source_dois:
  - 10.1186/s13321-021-00558-4
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# inchikey-smiles-standardization

## Summary

Standardize chemical structure annotations (InChI, SMILES, InChIKey) for mass spectrometry spectra using automated PubChem lookups and metadata normalization. This skill ensures consistent, machine-readable chemical identifiers suitable for training deep learning models on spectral data.

## When to use

When you have raw MS/MS spectra from repositories like GNPS that lack or have inconsistent chemical structure annotations (InChI/SMILES), and you need to produce a curated dataset with uniform 14-character InChIKey and SMILES/InChI annotations for downstream machine learning or similarity scoring tasks.

## When NOT to use

- Input spectra already have uniform, validated InChIKey and SMILES annotations — standardization is redundant.
- Chemical structure is unknown or cannot be resolved via PubChem (e.g., novel synthesized compounds, proprietary structures without public database entries).
- Downstream analysis does not require structural similarity or chemical fingerprint generation; metadata standardization adds computational overhead without benefit.

## Inputs

- Raw MS/MS spectra dataset (e.g., GNPS format with variable metadata completeness)
- Compound name and adduct metadata (variable format and completeness)
- Spectra with missing or incomplete InChI/SMILES annotations

## Outputs

- Standardized metadata table with 14-character InChIKey, SMILES, and InChI for each spectrum
- Cleaned compound name field
- Extracted and normalized adduct information
- Filtered spectrum set retaining only annotated spectra

## How to apply

First, clean and normalize compound name metadata using matchms v0.8.2, extracting adduct information and moving metadata to consistent fields. For spectra still lacking InChI or SMILES annotations after initial cleaning, run automated PubChem lookup via pubchempy to retrieve structure data. Validate that all retained spectra have valid 14-character InChIKeys paired with SMILES and/or InChI strings. Use RDKit to standardize SMILES representations and verify structural consistency where multiple InChI exist for the same InChIKey (selecting the most common InChI variant). This produces a standardized metadata table suitable for training structural similarity models.

## Related tools

- **matchms** (Cleans and normalizes compound name metadata, extracts adduct information, and converts/maps InChI/SMILES/InChIKey strings to consistent fields) — https://github.com/matchms/matchms
- **pubchempy** (Performs automated PubChem lookups to retrieve InChI and SMILES annotations for spectra lacking these structure annotations)
- **RDKit** (Generates molecular fingerprints and standardizes SMILES representations for structural validation and consistency checking)
- **PubChem** (Public chemical database providing authoritative InChI and SMILES data for compound lookup and annotation recovery)

## Examples

```
from matchms.importing_utils import load_from_json; from matchms.filtering.default_pipelines import LOADS; from pubchempy import get_compounds; spectra = load_from_json('gnps_raw.json'); spectra = [LOADS.normalize_compound_name(s) for s in spectra]; spectra = [LOADS.extract_adduct_from_metadata(s) for s in spectra]; spectra_annotated = [s if s.get('smiles') and s.get('inchikey') else get_compounds(s.get('compound_name'), 'name')[0] for s in spectra]
```

## Evaluation signals

- All retained spectra have valid 14-character InChIKey strings with no missing or truncated values.
- 100% of retained spectra possess both SMILES and/or InChI annotations (no nulls in either field).
- Compound names are normalized (e.g., duplicates resolved, special characters handled, case standardized).
- Adduct information is extracted into a dedicated, consistently formatted field (e.g., '[M+H]+', '[M-H]-').
- Cross-validation: RDKit can parse all SMILES strings without error and generate matching molecular fingerprints for corresponding InChIKeys.

## Limitations

- PubChem lookups fail for novel compounds, proprietary structures, or metabolites not yet indexed in public databases; such spectra are excluded from the final dataset.
- Automated annotation retrieval may return multiple InChI strings for a single InChIKey due to stereoisomerism or historical duplicate entries in PubChem; the selection of 'most common' variant is heuristic and may lose chemical detail.
- Standardization is dependent on the quality and completeness of PubChem annotations; systematic errors or gaps in the public database propagate into the curated dataset.
- Metadata normalization (e.g., compound name cleaning) can be ambiguous for malformed or context-dependent entries; manual review of edge cases is recommended for critical applications.

## Evidence

- [methods] Clean and standardize metadata using matchms v0.8.2, including compound name normalization, adduct extraction, and InChI/SMILES/InChIKey conversion and mapping.: "Clean and standardize metadata using matchms v0.8.2, including compound name normalization, adduct extraction, and InChI/SMILES/InChIKey conversion and mapping"
- [methods] Run automated PubChem lookup via pubchempy for spectra lacking InChI or SMILES annotations.: "Run automated PubChem lookup via pubchempy for spectra lacking InChI or SMILES annotations"
- [methods] Filter spectra to retain only those with valid 14-character InChIKey and SMILES/InChI annotation.: "Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation"
- [other] Metadata was cleaned and checked using matchms version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields"
- [methods] For every unique 14-character InChIKey the most common InChI was selected if different InChI existed and used to generate a molecular fingerprint.: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint"
- [results] The resulting training data set contains chemical structure annotations for 109,734 spectra representing 15,062 unique molecules.: "The resulting training data set contains chemical structure annotations for 109,734 spectra... The dataset contains 15,062 different molecules (disregarding stereoisomerism)"
