---
name: chemical-metadata-harmonization
description: Use when when aggregating MS/MS spectra from multiple public repositories (GNPS, MassBank, Mona) or in-house sources with inconsistent metadata naming conventions, missing or malformed adduct annotations, or incomplete chemical structure annotations (SMILES/InChI/InChIKey).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0092
  tools:
  - RDKit
  - matchms
  - Python
  - pubchempy
  techniques:
  - LC-MS
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

# chemical-metadata-harmonization

## Summary

Standardize and enrich MS/MS spectra metadata by cleaning compound names, extracting adduct information, consolidating metadata fields, and automating missing structure annotation lookups against PubChem. This ensures consistent metadata representation across heterogeneous spectral datasets before structural similarity computation or model training.

## When to use

When aggregating MS/MS spectra from multiple public repositories (GNPS, MassBank, Mona) or in-house sources with inconsistent metadata naming conventions, missing or malformed adduct annotations, or incomplete chemical structure annotations (SMILES/InChI/InChIKey). Essential before computing molecular fingerprints or training neural networks on spectral pairs.

## When NOT to use

- Input spectra already have curated, consistent metadata from a single well-managed repository with complete structural annotations.
- The analysis does not require structural similarity computation or fingerprint generation (e.g., spectral library matching using only fragmentation patterns).
- PubChem lookup would be inappropriate (e.g., proprietary or novel compounds not in public databases).

## Inputs

- MS/MS spectral dataset (raw, from GNPS/MassBank/Mona or local repository)
- Spectrum metadata: compound names, adduct annotations, InChI/SMILES/InChIKey annotations (incomplete or inconsistent)
- Optional: PubChem compound database (for automated lookup)

## Outputs

- Cleaned MS/MS spectral dataset with standardized metadata
- Deduplicated structure annotations (one InChI per unique 14-character InChIKey)
- Populated InChI/SMILES fields for previously unannotated spectra
- Normalized adduct field
- Consistent metadata field mapping

## How to apply

Use matchms v0.8.2+ to apply automated metadata cleaning: (1) standardize and normalize compound names by removing ambiguous characters and prefixes; (2) extract adduct information (e.g., [M+H]+, [M-H]-) from freeform metadata fields into dedicated adduct fields; (3) move related metadata into consistent, canonical field names. (4) For spectra still lacking InChI or SMILES annotations after cleaning, run automated PubChem lookup via pubchempy by querying the compound name or InChIKey; accept matches only when confident structural mapping is established. Store the resulting cleaned dataset with deduplicated InChI per InChIKey before fingerprint generation. This preprocessing step is critical because inconsistent metadata directly impacts downstream label generation and model generalization.

## Related tools

- **matchms** (Apply automated metadata cleaning pipeline: standardize compound names, extract adduct information, consolidate metadata fields into canonical formats) — https://github.com/matchms/matchms
- **pubchempy** (Automated chemical structure lookup for spectra with missing InChI or SMILES annotations; query PubChem database by compound name)
- **RDKit** (Validate chemical structure annotations and generate molecular fingerprints from cleaned InChI/SMILES for downstream similarity computation) — https://www.rdkit.org

## Examples

```
from matchms.importing_utils import load_from_mgf; from matchms.filtering.default_pipelines import DEFAULT_FILTERS; from matchms.Pipeline import Pipeline, create_workflow; pipeline = Pipeline(create_workflow(query_filters=DEFAULT_FILTERS)); spectra = pipeline.run('raw_spectra.mgf'); print(f'Cleaned {len(spectra)} spectra with harmonized metadata')
```

## Evaluation signals

- All spectra have non-null, consistently formatted metadata fields (compound name, adduct, InChIKey, InChI/SMILES).
- Adduct information is correctly extracted and matches expected ionization modes; validation: check that extracted adducts align with precursor m/z values.
- For each unique 14-character InChIKey, exactly one canonical InChI is retained; no duplicate or conflicting structure annotations remain.
- PubChem lookup success rate documented (number of spectra enriched / number queried); newly annotated structures validate against expected chemical families.
- Downstream fingerprint generation (RDKit) succeeds without parse errors for ≥ 99% of cleaned structures; any failures logged with InChIKey for manual review.

## Limitations

- Automated PubChem lookup may fail or return incorrect structures for ambiguous compound names, proprietary compounds, or novel structures not yet in PubChem.
- Metadata standardization rules are heuristic and repository-specific; some edge cases (e.g., non-standard adduct notations, mixed-case compound names) may not normalize correctly.
- For spectra with multiple conflicting InChI annotations for the same InChIKey, the cleaning step selects the most common InChI, which may discard valid but less frequent structures.
- Metadata harmonization does not validate chemical correctness (e.g., that SMILES/InChI are chemically sound); downstream fingerprint generation may reveal invalid structures.

## Evidence

- [methods] Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "Metadata was cleaned and checked using matchms [18] version 0.8.2, which included cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields"
- [methods] We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations: "We then ran an automated search against PubChem [42] using pubchempy [43] for spectra which still missed InChI or SMILES annotations"
- [methods] For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed) and used to generate a molecular fingerprint.: "For every unique 14-character InChIKey the most common InChI was selected (if different InChI existed)"
- [intro] The dataset was retrieved from GNPS (25/01/2021) and contains a total of 210,407 MS/MS spectra, which was built through curating and cleaning spectra obtained from GNPS: "dataset of 109,734 MS/MS spectra, which was built through curating and cleaning spectra obtained from GNPS"
- [methods] matchms includes cleaning compound names, extracting adduct information from the given metadata, moving metadata to consistent fields: "extracting adduct information from the given metadata, moving metadata to consistent fields"
