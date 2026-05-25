---
name: pubchem-structure-lookup-and-retrieval
description: Use when metabolomics involves LC-MS or GC-MS untargeted lipidomics to query PubChem for canonical SMILES, InChI, and InChIKey from compound names for mass spectra annotations.
when_to_use_negative:
- Spectra lack compound names or have ambiguous/multi-part compound identifiers that PubChem cannot resolve uniquely.
- The analysis goal does not require standardized or canonical structure representations (e.g., only peak-level filtering or intensity normalization is needed).
- Spectra already have manually validated, institution-specific structure identifiers that supersede PubChem's canonical forms.
edam_operation: http://edamontology.org/operation_2421
edam_topics:
- http://edamontology.org/topic_0154
- http://edamontology.org/topic_3172
tools:
- name: matchms
  role: Framework for loading, filtering, and applying the 'derive_annotation_from_compound_name' filter to spectral data
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Parses and compares derived SMILES, InChI, and InChIKey to detect structural mismatches between PubChem results and existing annotations
- name: PubChem
  role: External compound database queried by matchms filter to retrieve canonical SMILES, InChI, and InChIKey from compound names
provenance:
  source_task_ids:
  - task_002
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/article_878_full_2026-05-10_v5/skills/pubchem-structure-lookup-and-retrieval/SKILL.md
    - outputs/article_878_full_2026-05-10_v5/skills/pubchem-structure-lookup-and-retrieval/skill.md
    merged_at: '2026-05-25T06:57:01.437551+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/pubchem-structure-lookup-and-retrieval@sha256:caf14e38619145abf86e3bd669f0f084b6232caaa13d1e8c550a5295033f0c5b
derived_from:
- doi: 10.1186/s13321-024-00878-1
---

# PubChem structure lookup and retrieval

## Summary

Query PubChem to derive canonical SMILES, InChI, and InChIKey from compound names for mass spectra annotations. This skill validates and standardizes chemical structure representations in spectral metadata, enabling detection of structural mismatches and unannotated spectra.

## When to use

When you have mass spectra with compound names but missing or potentially incorrect chemical structure identifiers (SMILES, InChI, InChIKey). Apply this skill to standardize structure annotations, identify spectra that cannot be resolved to a unique structure via PubChem, and detect cases where the derived structure differs from the original annotation—critical for library quality control in spectral databases like GNPS.

## When NOT to use

- Spectra lack compound names or have ambiguous/multi-part compound identifiers that PubChem cannot resolve uniquely.
- The analysis goal does not require standardized or canonical structure representations (e.g., only peak-level filtering or intensity normalization is needed).
- Spectra already have manually validated, institution-specific structure identifiers that supersede PubChem's canonical forms.

## Inputs

- Mass spectra with compound name metadata (as matchms Spectrum objects)
- Existing chemical structure annotations (SMILES, InChI, or InChIKey fields)
- Ion mode and adduct information (for validation context)

## Outputs

- Spectrum objects with derived canonical SMILES, InChI, and InChIKey from PubChem
- Comparison table of original vs. derived structures (flagging mismatches)
- Error report documenting spectra with unresolved compound names and structural discrepancies
- Filtered spectrum table excluding or flagging problematic annotations

## How to apply

Load spectra with valid compound names and ion-mode-matching adducts into matchms (version 0.26.4+). Apply the 'derive_annotation_from_compound_name' filter, which queries PubChem to retrieve canonical SMILES, InChI, and InChIKey for each compound name. Use RDKit to compare the derived chemical structures against existing annotations. Calculate two key error rates: (1) the percentage of spectra from which SMILES could not be derived (expected ~27.6% based on the GNPS benchmark), and (2) among successfully annotated spectra, the percentage assigned a structurally different 2D structure than the original (expected ~1.62%). Generate a filtered spectrum table and an error report documenting unannotated and mismatched records for manual review.

## Related tools

- **matchms** (Framework for loading, filtering, and applying the 'derive_annotation_from_compound_name' filter to spectral data) — https://github.com/matchms/matchms
- **RDKit** (Parses and compares derived SMILES, InChI, and InChIKey to detect structural mismatches between PubChem results and existing annotations)
- **PubChem** (External compound database queried by matchms filter to retrieve canonical SMILES, InChI, and InChIKey from compound names)

## Evaluation signals

- Verify that the percentage of spectra with unresolved compound names is approximately 27.6% (or document actual rate if dataset differs from GNPS benchmark).
- Confirm that among successfully annotated spectra, the proportion with structurally different 2D structures is ~1.62% or lower; elevated rates indicate annotation inconsistencies.
- Check that derived SMILES, InChI, and InChIKey conform to canonical formats (e.g., RDKit can parse them without error).
- Validate that all spectra in the filtered output have non-null structure identifiers and either match the original annotation or are flagged as mismatches in the error report.
- Ensure ion-mode and adduct metadata are preserved in the output spectrum objects for downstream repair filters.

## Limitations

- The filter cannot resolve compound names that are ambiguous, misspelled, or absent from PubChem; ~27.6% failure rate is typical for large public libraries.
- Wrong chemical annotations that are consistent with the measured mass will go undetected by this filter; a subsequent fragment-matching step is needed.
- PubChem lookups depend on network connectivity and may be slow for very large spectral libraries (500,569 spectra took 6 h 45 min in the GNPS benchmark).
- The skill does not validate whether the derived structure actually explains the observed fragmentation pattern; it only checks structural identity.

## Evidence

- [abstract] derive_annotation_from_compound_name filter, PubChem lookup, SMILES/InChI/InChIKey derivation: "This filter derives the canonical SMILES, InChI and InChIKey from PubChem"
- [abstract] Error rates: 27.6% unresolved, 1.62% structural mismatches among annotated spectra: "For 27,6% of the spectra, the SMILES could not be derived from the compound name. Of the spectra that were annotated (72,4%), 1,62% were annotated with a different 2D structure"
- [abstract] RDKit is used to compare derived structures: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [discussion] Fragment matching is a missing signal for future work: "Future expansions might include filters that check if the fragments match the given annotation"
