---
name: tandem-mass-spectrometry-metadata-standardization
description: Use when you have raw MS/MS spectra from public repositories (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3314
  tools:
  - matchms
  - pubchempy
  - RDKit
  - Python
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

# Tandem Mass Spectrometry Metadata Standardization

## Summary

Standardize and validate MS/MS spectrum metadata (compound names, adducts, chemical structure annotations) using automated tools to enable downstream structural similarity prediction and machine learning. This skill transforms heterogeneous raw GNPS annotations into a consistent schema suitable for neural network training.

## When to use

You have raw MS/MS spectra from public repositories (e.g., GNPS, MoNA) with inconsistent or incomplete metadata (compound name variations, missing InChI/SMILES, adduct information scattered across fields) and need to prepare them for deep learning model training or large-scale spectral similarity comparisons. Trigger: spectrum collection lacks standardized InChIKey, normalized compound names, or explicit adduct extraction.

## When NOT to use

- Spectra are already in a proprietary curated database with locked structure assignments (e.g., NIST library with peer-reviewed annotations); re-standardization risks losing expert curation.
- Negative ionization mode spectra are the primary target; the workflow explicitly filters to positive mode only.
- Your dataset contains fewer than ~5,000 unique molecules or <50,000 spectra; the automated PubChem lookup and neural network training rationale assumes sufficient molecular and spectral diversity.

## Inputs

- raw MS/MS spectrum collection (e.g., GNPS export with 210,407+ spectra)
- spectrum metadata fields (compound name, adduct, precursor m/z, ionization mode)
- spectra in MGF, MSP, mzML, mzXML, or JSON format

## Outputs

- cleaned spectrum metadata dictionary with normalized compound names, extracted adducts, standardized field locations
- InChIKey–SMILES–InChI mapping table (validated against PubChem)
- filtered spectrum collection (109,734 spectra in this study) with complete 14-character InChIKey and structure annotations
- metadata quality report (% spectra passing each filter, annotation coverage)

## How to apply

Use matchms v0.8.2 to clean and normalize compound names, extract adduct information from raw metadata fields, and standardize field locations. For spectra still lacking InChI or SMILES annotations after cleaning, run automated PubChem lookup via pubchempy to retrieve and map structure data. Filter to retain only spectra in positive ionization mode with valid 14-character InChIKey, explicit SMILES/InChI annotations, and at least 5 peaks in the 10–1000 Da range. This multi-stage approach ensures both structural provenance (InChIKey for deduplication and grouping by unique molecule) and metadata consistency necessary for paired training data generation and reproducible model evaluation.

## Related tools

- **matchms** (Core cleaning and standardization engine; normalizes compound names, extracts and standardizes adduct metadata, maps InChI/SMILES/InChIKey to consistent fields) — https://github.com/matchms/matchms
- **pubchempy** (Automated structure annotation lookup; retrieves InChI and SMILES for spectra lacking structure data via PubChem API)
- **RDKit** (Validates and canonicalizes molecular structures (SMILES/InChI); ensures structural consistency before fingerprint generation)
- **Python** (Orchestration and data I/O; implements filtering logic, peak intensity transformations, binning, and metadata export) — https://github.com/matchms/ms2deepscore

## Examples

```
from matchms.importing_utils import load_from_mgf; from matchms.filtering import default_filters; spectra = [s for s in load_from_mgf('gnps_raw.mgf')]; cleaned = [default_filters.apply_filters(s) for s in spectra]; import pubchempy as pcp; spectra_with_structures = [s for s in cleaned if s.get('inchikey') or pcp.get_compounds(s.get('compound_name'), 'name')[0] if s.get('compound_name')]
```

## Evaluation signals

- 100% of retained spectra have a valid 14-character InChIKey and non-null SMILES or InChI field (no null structure annotations in output)
- Compound name field normalized consistently (e.g., trailing spaces, case, standardized chemical nomenclature applied uniformly)
- Adduct information successfully extracted from raw metadata and stored in dedicated field (e.g., '[M+H]+', '[M-H]-' parseable)
- PubChem lookup success rate reported; proportion of spectra enriched via automated search vs. present in raw metadata
- Filtering step report: number of spectra removed at each stage (ionization mode, InChIKey validity, structure annotation presence, peak count, mass range) totals to expected drop from 210,407 → 109,734

## Limitations

- Automated PubChem lookup may introduce incorrect or ambiguous structure assignments if compound names are non-standard or share aliases; expert manual curation is recommended for mission-critical applications.
- Positive ionization mode filter excludes negative-mode spectra entirely; negative-mode datasets require separate standardization workflow.
- InChIKey-based deduplication assumes InChIKeys are correctly computed; errors in RDKit canonicalization or PubChem data will propagate into the cleaned dataset.
- Spectra with <5 peaks in the 10–1000 Da range are discarded; datasets with many low-energy fragmentation patterns will experience reduced coverage.
- Metadata enrichment relies on external PubChem API availability and current data; stale or deprecated compound records may not be retrieved or may be incorrect.

## Evidence

- [other] Raw GNPS spectra (210,407 total) were processed using matchms for metadata cleaning and automated PubChem searches to obtain chemical structure annotations (InChI/SMILES), yielding 109,734 spectra with annotations representing 15,062 unique molecules for training.: "Raw GNPS spectra (210,407 total) were processed using matchms for metadata cleaning and automated PubChem searches to obtain chemical structure annotations"
- [other] Clean and standardize metadata using matchms v0.8.2, including compound name normalization, adduct extraction, and InChI/SMILES/InChIKey conversion and mapping.: "Clean and standardize metadata using matchms v0.8.2, including compound name normalization, adduct extraction, and InChI/SMILES/InChIKey conversion and mapping"
- [other] Run automated PubChem lookup via pubchempy for spectra lacking InChI or SMILES annotations.: "Run automated PubChem lookup via pubchempy for spectra lacking InChI or SMILES annotations"
- [other] Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation, containing ≥5 peaks in the 10.0–1000.0 Da mass range.: "Filter spectra to retain only those in positive ionization mode with valid 14-character InChIKey and SMILES/InChI annotation, containing ≥5 peaks in the 10.0–1000.0 Da mass range"
- [methods] Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields"
- [methods] We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations: "We then ran an automated search against PubChem using pubchempy for spectra which still missed InChI or SMILES annotations"
- [results] The resulting training data set contains chemical structure annotations for 109,734 spectra: "The resulting training data set contains chemical structure annotations for 109,734 spectra"
- [results] The dataset contains 15,062 different molecules (disregarding stereoisomerism): "The dataset contains 15,062 different molecules (disregarding stereoisomerism)"
- [readme] Installation is expected to take 10-20 minutes.: "Installation is expected to take 10-20 minutes."
