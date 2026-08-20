---
name: chemical-structure-annotation-retrieval
description: Use when you have MS/MS spectra from public repositories (e.g., GNPS) that lack chemical structure annotations (InChI/SMILES), or have incomplete/inconsistent annotations.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3282
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-structure-annotation-retrieval

## Summary

Retrieve and assign chemical structure annotations (InChI, SMILES, InChIKey) to unannotated or partially annotated MS/MS spectra using automated database lookups. This skill is essential for preparing spectral datasets for machine learning by ensuring complete structural metadata coverage.

## When to use

Apply this skill when you have MS/MS spectra from public repositories (e.g., GNPS) that lack chemical structure annotations (InChI/SMILES), or have incomplete/inconsistent annotations. Use it as a preprocessing step before training machine learning models that require paired spectra-to-structure relationships, such as deep learning similarity predictors.

## When NOT to use

- Spectra already contain validated chemical structure annotations from a trusted source (e.g., manually curated library) — annotation retrieval adds redundancy and potential corruption risk.
- Working with proprietary or confidential spectra where external database lookups are not permitted.
- Real-time or streaming applications where automated database queries introduce unacceptable latency.

## Inputs

- Raw MS/MS spectral data with partial or missing structure annotations (e.g., compound names only)
- Spectrum metadata (compound name, neutral mass, ionization mode)
- Access to PubChem or similar chemical structure database

## Outputs

- Spectra with complete chemical structure annotations (InChI, SMILES, InChIKey)
- Standardized metadata fields (InChIKey validated to 14 characters, consistent annotation format)
- Quality-controlled spectral dataset filtered to retain only successfully annotated spectra

## How to apply

For spectra lacking InChI or SMILES annotations, run an automated lookup against PubChem using tools like pubchempy. Standardize and validate all retrieved annotations: ensure 14-character InChIKeys are valid format, verify that InChI and SMILES fields are populated consistently, and reject spectra where annotation retrieval fails. Clean and normalize compound names before lookup to improve match rates. Filter the final annotated set to retain only spectra in positive ionization mode with valid structural metadata, removing those that fail annotation retrieval entirely.

## Related tools

- **pubchempy** (Automated lookup tool to retrieve InChI and SMILES annotations from PubChem for spectra lacking structure metadata)
- **matchms** (Standardize and validate chemical structure annotations (InChI/SMILES/InChIKey conversion and normalization) and manage spectrum metadata fields) — https://github.com/matchms/matchms
- **RDKit** (Validate chemical structure strings (SMILES/InChI) and generate canonical fingerprints for structural comparison)
- **PubChem** (Public chemical structure database queried for InChI and SMILES annotations) — https://pubchem.ncbi.nlm.nih.gov/

## Examples

```
from pubchempy import get_compounds; from matchms import Spectrum; annotated = []; for s in raw_spectra:
  if not s.get('inchi'): cmpd = get_compounds(s['compound_name'], 'name'); s['inchi'] = cmpd[0].inchi if cmpd else None
  if s.get('inchi'): annotated.append(s)
```

## Evaluation signals

- Fraction of input spectra successfully annotated with valid 14-character InChIKey and non-empty SMILES/InChI fields (target: >90% of spectra with initial metadata)
- Verification that all output InChIKeys are exactly 14 characters and follow InChIKey format (e.g., start with 'INCHIKEY=')
- Cross-validation: for a random sample of retrieved annotations, manually verify that the compound name or neutral mass matches the PubChem record
- Consistency check: for spectra with multiple InChI values per InChIKey, confirm that the most common InChI was consistently selected
- Retention rate: compare input vs. output dataset size; ensure filtering decisions (e.g., positive ionization mode only) are documented and intentional

## Limitations

- PubChem lookup success depends on quality and specificity of compound names in the original metadata; incomplete or misspelled names will fail to retrieve annotations.
- Automated annotation retrieval cannot distinguish between isomers or stereoisomers; multiple valid structure records for the same compound name may exist in PubChem, requiring a tie-breaking rule (the study used 'most common InChI' per InChIKey).
- The skill filters spectra to positive ionization mode only, excluding negative ionization spectra; this is suitable for the MS2DeepScore training pipeline but may not generalize to datasets requiring multi-ionization coverage.
- Spectra without valid compound names or neutral masses cannot be reliably annotated; orphan or highly ambiguous entries will be discarded.
- Database coverage limitations: compounds not in PubChem (e.g., novel or proprietary molecules) will not receive annotations, resulting in permanent loss of those spectra from the training set.

## Evidence

- [methods] We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations: "We then ran an automated search against PubChem using pubchempy for spectra which still missed InChI or SMILES annotations"
- [methods] Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms version 0.8.2, which included cleaning compound names, extracting adduct information"
- [other] Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation, containing ≥5 peaks in the 10.0–1000.0 Da mass range.: "Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation"
- [methods] For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint.: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed)"
- [results] The resulting training data set contains chemical structure annotations for 109,734 spectra. The dataset contains 15,062 different molecules: "The resulting training data set contains chemical structure annotations for 109,734 spectra with annotations representing 15,062 unique molecules"
