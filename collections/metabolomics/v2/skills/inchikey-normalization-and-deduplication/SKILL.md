---
name: inchikey-normalization-and-deduplication
description: Use when you have an annotated MS/MS spectral dataset with structure metadata (InChI or SMILES records) linked to InChIKey identifiers, and you observe that some InChIKeys are associated with multiple or variant InChI strings due to curation inconsistencies, stereoisomerism notation differences, or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0154
  - http://edamontology.org/topic_0091
  tools:
  - RDKit
  - matchms
  - Python
derived_from:
- doi: 10.1186/s13321-021-00558-4
  title: MS2DeepScore
evidence_spans:
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities.
- Unless noted otherwise, we used Tanimoto scores on RDKit [23] Daylight fingerprints (2048 bits) to compute structural similarities
- Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields
- For each pair of molecular fingerprints Tanimoto scores were calculated, indicating the structural similarity of that pair. (as implemented in matchms [18])
- Our MS2DeepScore Python library offers two types of data generators, one which iterates over all unique InChIKeys (DataGeneratorAllInchikeys) and one which iterates over all spectra and was used for
- Our MS2DeepScore Python library offers two types of data generators
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
---

# InChIKey Normalization and Deduplication

## Summary

Resolve and consolidate multiple chemical structure annotations (InChI/SMILES) assigned to the same 14-character InChIKey, selecting a canonical representative per unique key to enable consistent fingerprint generation and structural similarity computation. This preprocessing step is essential when curating MS/MS spectral libraries where duplicate or redundant structure records must be collapsed before computing machine learning training labels.

## When to use

You have an annotated MS/MS spectral dataset with structure metadata (InChI or SMILES records) linked to InChIKey identifiers, and you observe that some InChIKeys are associated with multiple or variant InChI strings due to curation inconsistencies, stereoisomerism notation differences, or annotation redundancy. Perform this normalization before generating molecular fingerprints or computing pairwise structural similarity matrices for model training.

## When NOT to use

- Your dataset already contains one unique structure record per InChIKey (no duplicates or variants) — normalization is redundant.
- You need to preserve and distinguish stereoisomers or tautomeric variants as separate entities — InChIKey normalization collapses these into one representative.
- Your workflow does not use InChIKey as a structural identifier; you are using full InChI or SMILES strings as your primary keys.

## Inputs

- Annotated MS/MS spectra dataset with InChIKey and SMILES/InChI metadata fields (e.g., GNPS library in MGF or TSV format)
- InChIKey-to-structure mapping table with potential duplicates or variant records per key

## Outputs

- Deduplicated structure dataset: one canonical InChI (or SMILES) per unique 14-character InChIKey
- Mapping of InChIKey → canonical InChI for downstream fingerprint generation
- Report of removed/consolidated redundant records (optional)

## How to apply

For each unique 14-character InChIKey in your dataset, identify all associated InChI records. Select the most frequently occurring InChI (or apply a deterministic tie-breaking rule if frequencies are tied) and designate it as the canonical representative for that key. Discard or flag alternative InChI variants linked to the same key. This consolidation prevents spurious or inconsistent fingerprint generation and ensures that the resulting structural similarity matrix reflects true chemical uniqueness rather than annotation artifacts. The rationale is that InChIKey serves as the primary deduplication index; multiple InChI strings mapped to the same key indicate redundancy to be collapsed, not chemical diversity to preserve.

## Related tools

- **RDKit** (Generates molecular fingerprints from the canonical InChI after deduplication, enabling structural similarity computation) — https://rdkit.org
- **matchms** (Metadata cleaning and structure annotation lookup; used to load and inspect the MS/MS spectral dataset before and after normalization) — https://github.com/matchms/matchms
- **Python** (Scripting language for implementing deduplication logic (dictionary aggregation, frequency counting))

## Examples

```
from collections import Counter; inchikey_to_inchis = {}; [inchikey_to_inchis.setdefault(k, []).append(inchi) for k, inchi in zip(inchikeys, inchis)]; canonical = {k: Counter(inchis_list).most_common(1)[0][0] for k, inchis_list in inchikey_to_inchis.items()}
```

## Evaluation signals

- Output dataset cardinality: count of unique InChIKeys in normalized output should exactly match count of unique InChIKeys in input (no keys lost); total structure records should be ≤ input (no records added, only consolidated).
- Determinism: running the deduplication twice on the same input produces identical output (same canonical InChI selected per key).
- Downstream fingerprint consistency: generating RDKit Daylight fingerprints from deduplicated InChI strings produces one 2048-bit fingerprint vector per InChIKey; no InChIKey maps to multiple distinct fingerprints.
- Inspection of removed records: manually verify that discarded/consolidated records genuinely represent duplicate or variant annotations of the same molecule, not distinct chemicals mis-assigned the same InChIKey.
- Pairwise similarity matrix: resulting Tanimoto score matrix dimensions are (N unique InChIKeys) × (N unique InChIKeys), with no missing or NaN values for valid key pairs.

## Limitations

- InChIKey is a lossy hash (14 characters); it ignores stereoisomerism and some tautomeric forms by design. Deduplication by InChIKey may obscure chemical distinctions important for some applications.
- Tie-breaking rule for InChI selection is arbitrary: if two InChI variants occur with equal frequency for the same InChIKey, the chosen representative may depend on insertion order or random seed, leading to minor non-determinism if no explicit rule is defined.
- The workflow does not validate whether all InChI records truly correspond to the assigned InChIKey; misassignment in the source annotation will not be corrected by this step.
- Large datasets with many InChIKey collisions (e.g., due to annotation errors) may require manual curation; fully automated deduplication assumes annotations are mostly correct.

## Evidence

- [methods] For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint.: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed)"
- [methods] Extract the most common InChI for each unique InChIKey (handling cases where multiple InChI annotations exist for the same InChIKey).: "Extract the most common InChI for each unique InChIKey (handling cases where multiple InChI annotations exist)"
- [methods] The full cleaned dataset (210,407 spectra, 184,698 annotated with InChIKey and SMILES and/or InChI) can be found on zenodo: "The full cleaned dataset (210,407 spectra, 184,698 annotated with InChIKey and SMILES and/or InChI)"
- [results] The dataset contains 15,062 different molecules (disregarding stereoisomerism): "The dataset contains 15,062 different molecules (disregarding stereoisomerism)"
