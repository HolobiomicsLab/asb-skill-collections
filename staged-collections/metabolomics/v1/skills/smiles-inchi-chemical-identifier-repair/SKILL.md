---
name: smiles-inchi-chemical-identifier-repair
description: Use when metabolomics requires the repair and validation of chemical structure identifiers (SMILES, InChI, InChIKey) through comparison with canonical references and correction of salt-form SMILES to prevent downstream failures in LC-MS and GC-MS untargeted lipidomics.
when_to_use_negative:
- Input records lack any SMILES, InChI, or InChIKey field — use 'Derive annotation from compound name' (via PubChem) first to obtain initial structure identifiers.
- The annotation is already curated and chemically validated externally — skip to 'Require valid annotation' filter instead.
- Your analysis does not require structural metadata or does not perform adduct/parent mass repair — this repair is only necessary when downstream filters depend on chemically consistent SMILES.
edam_operation: http://edamontology.org/operation_3930
edam_topics:
- http://edamontology.org/topic_3407
- http://edamontology.org/topic_0154
tools:
- name: RDKit
  role: Parse, validate, canonicalize, and interconvert SMILES, InChI, and InChIKey; remove ionic counter-ions from salt-form SMILES
- name: matchms
  role: Provide spectrum object framework and filter pipeline; integrate SMILES/InChI repair as a library cleaning filter step
  repo: https://github.com/matchms/matchms
- name: PubChem
  role: Source of canonical SMILES, InChI, and InChIKey when deriving annotations from compound names; used for validation reference
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/smiles-inchi-chemical-identifier-repair@sha256:95009297c7c899c79c658052f912b6553eaa3f84c845a87f673c28344b09cf49
---

# SMILES/InChI Chemical Identifier Repair

## Summary

Repair and validate chemical structure identifiers (SMILES, InChI, InChIKey) by comparing them against each other and canonical references, and correcting salt-form SMILES that would otherwise cause downstream failures. This skill is essential in MS/MS library cleaning to ensure annotations are chemically consistent before requiring them as mandatory metadata.

## When to use

Apply this skill when you have mass spectral library records with SMILES, InChI, or InChIKey annotations that may be incomplete, inconsistent, or incorrectly formatted (e.g., salt-form SMILES that do not represent the neutral parent compound). Specifically, use it when you plan to enforce strict annotation requirements downstream or when you need to compare and harmonize multiple structural representations of the same compound.

## When NOT to use

- Input records lack any SMILES, InChI, or InChIKey field — use 'Derive annotation from compound name' (via PubChem) first to obtain initial structure identifiers.
- The annotation is already curated and chemically validated externally — skip to 'Require valid annotation' filter instead.
- Your analysis does not require structural metadata or does not perform adduct/parent mass repair — this repair is only necessary when downstream filters depend on chemically consistent SMILES.

## Inputs

- Mass spectral library records (MGF format or equivalent) with SMILES, InChI, and/or InChIKey metadata fields
- Parsed spectrum objects from matchms with attached annotation dictionaries containing chemical structure identifiers

## Outputs

- Repaired SMILES field (salt forms removed, canonicalized)
- Regenerated InChI and InChIKey fields (derived from repaired SMILES via RDKit)
- Repair status flag (binary or categorical: repaired, valid, invalid)
- Summary statistics: count of repaired records, count of invalid records, records with structural inconsistencies before repair

## How to apply

Load SMILES, InChI, and InChIKey metadata fields from each spectrum record using RDKit and compare the three identifiers to each other to detect inconsistencies. For records with valid SMILES, use RDKit to canonicalize them and regenerate InChI and InChIKey to ensure all three representations refer to the same 2D structure. Repair salt-form SMILES (e.g., those containing '[Na+]', '[Cl-]', or other counter-ions) by removing the ionic components and retaining only the neutral parent structure; this prevents parent mass and adduct calculations from being corrupted by salt-specific mass values. Flag records where repair succeeds for downstream repair-dependent filters (e.g., 'Repair adduct and parent mass based on SMILES'). Reject records where SMILES cannot be parsed or where InChI/InChIKey derivations fail after repair, as these indicate fundamentally malformed chemical annotations.

## Related tools

- **RDKit** (Parse, validate, canonicalize, and interconvert SMILES, InChI, and InChIKey; remove ionic counter-ions from salt-form SMILES)
- **matchms** (Provide spectrum object framework and filter pipeline; integrate SMILES/InChI repair as a library cleaning filter step) — https://github.com/matchms/matchms
- **PubChem** (Source of canonical SMILES, InChI, and InChIKey when deriving annotations from compound names; used for validation reference)

## Evaluation signals

- All repaired SMILES are canonical (e.g., no alternative atom ordering or bond notation); regenerated InChI/InChIKey match their original values if the original represented the same parent compound
- Salt-form SMILES are successfully converted to neutral parent structures (e.g., '[Na+].[Cl-]' counter-ions removed) and do not introduce parsing errors in downstream tools
- Repair rate and distribution match expected ranges from library cleaning benchmarks (e.g., GNPS library showed 10.4% of spectra benefited from repair functions overall; individual repair function rates vary 0.02–0.024% for adduct correction)
- Consistency check: if a record had SMILES and InChIKey before repair, the repaired SMILES should regenerate an InChIKey identical or equivalent to the original (indicating the repair corrected form, not structure)
- No increase in downstream 'Repair adduct and parent mass based on SMILES' failures after SMILES repair; count of successfully derived adducts should remain ≥99.98% for valid parent spectra

## Limitations

- Salt-form SMILES removal assumes that counter-ions are correctly and unambiguously represented in the input SMILES; malformed salt notation (e.g., mixed representations) may not be detected or may be incorrectly stripped.
- InChI/InChIKey regeneration depends on RDKit's chemical interpretation; some non-standard or ambiguous SMILES may be canonicalized differently than intended, yielding false inconsistency flags.
- The repair does not validate whether the parent structure is chemically sensible or pharmaceutically relevant; it only checks structural consistency across the three identifier formats. Wrong annotations consistent with measured mass will go unnoticed (as noted in the article's discussion).
- Performance scales with library size and RDKit's parsing overhead; on large libraries (e.g., GNPS with 500,569 spectra) this repair step contributes to runtime (matchms pipeline total: 6 h 45 min for full cleaning).

## Evidence

- [methods] SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [methods] Repair SMILES of salts: "Repair SMILES of salts"
- [methods] Library cleaning. Runs all default filters, but in addition repairs errors in the annotations and requires complete annotations after all repairs were run.: "Library cleaning. Runs all default filters, but in addition repairs errors in the annotations and requires complete annotations after all repairs were run."
- [results] a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084: "a total of 83,843 spectra were removed...In the library cleaning pipeline only 31,758 spectra were removed showing that combined the newly introduced repair functions repaired the metadata of 52,084"
- [discussion] Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline.: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline."
