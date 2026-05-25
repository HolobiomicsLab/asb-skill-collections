---
name: molecular-network-node-annotation-via-library-matching
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics requires annotating spectral nodes in feature-based molecular networks by matching MS/MS fragmentation spectra against curated reference libraries for structural identification of metabolites.
when_to_use_negative:
- Your metabolites are not well-represented in public reference libraries (e.g., novel synthetic compounds or rare plant species); use de novo structure elucidation or alternative annotation strategies instead.
- Your MS/MS data were acquired on a non-standard instrument or under collision energies not represented in the reference library; spectral matching will fail due to fragmentation pattern mismatch.
- You have already performed targeted MS/MS validation with standards and need only to confirm identities; library matching is redundant.
edam_operation: http://edamontology.org/operation_3631
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_3520
tools:
- name: GNPS (Global Natural Products Social Molecular Networking)
  role: Platform hosting feature-based molecular networking workflow, cosine similarity scoring engine, and public MS/MS reference library for library matching
- name: GNPS public library
  role: Curated MS/MS reference spectral database for matching experimental spectra against known metabolite standards
- name: LC-MS/MS
  role: Analytical instrumentation producing high-resolution MS/MS fragmentation spectra used as input for spectral matching
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1073/pnas
    title: Proceedings of the National Academy of Sciences
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_jeong_full/skills/molecular-network-node-annotation-via-library-matching/SKILL.md
    - outputs/audit_jeong_full/skills/molecular-network-node-annotation-via-library-matching/skill.md
    merged_at: '2026-05-25T07:33:56.368020+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/molecular-network-node-annotation-via-library-matching@sha256:0df80f06f53be883ea74dea46f247959d6faa416ecef6772acbca0e17a88d855
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1073/pnas
---

# molecular-network-node-annotation-via-library-matching

## Summary

Annotate spectral nodes in feature-based molecular networks by matching MS/MS fragmentation spectra against curated reference libraries (e.g., GNPS public library), enabling rapid structural identification of metabolites with high spectral coverage. This skill is essential when a molecular network contains hundreds of spectral nodes and manual curation is infeasible.

## When to use

Apply this skill after generating a feature-based molecular network (FBMN) with cosine similarity scoring from untargeted LC-MS/MS data, when you need to assign putative chemical structures to spectral nodes and your instrument, ionization mode, and collision energy match spectra archived in a public reference library. It is most effective when the reference library has high coverage of your compound class of interest (e.g., glycosylated flavonoids in GNPS).

## When NOT to use

- Your metabolites are not well-represented in public reference libraries (e.g., novel synthetic compounds or rare plant species); use de novo structure elucidation or alternative annotation strategies instead.
- Your MS/MS data were acquired on a non-standard instrument or under collision energies not represented in the reference library; spectral matching will fail due to fragmentation pattern mismatch.
- You have already performed targeted MS/MS validation with standards and need only to confirm identities; library matching is redundant.

## Inputs

- Feature-based molecular network (FBMN) node table with precursor m/z and spectral indices
- MS/MS fragmentation spectra from FBMN (in mzML or GNPS-native format)
- Curated MS/MS reference library (e.g., GNPS public library or instrument-specific database)

## Outputs

- Annotated node table with chemical names, InChIKeys, and cosine similarity scores
- Structural assignments for spectral nodes mapped back to the molecular network visualization
- Summary statistics: count and percentage of network nodes with library matches above threshold

## How to apply

After FBMN job completion, retrieve the molecular network node table and MS/MS spectral data from GNPS. Cross-reference each spectral node's precursor m/z and fragmentation pattern against the GNPS public library using cosine similarity scoring (typically cosine ≥ 0.7 indicates a high-confidence match). For each matched node, extract the library hit's chemical name, InChIKey, and structural metadata. Verify matches by visual inspection of the fragmentation pattern alignment and by contextualizing the annotation within the broader metabolic network—e.g., confirming that a node identified as a hexosylated flavonoid clusters with other known glycosides. Document the number of annotated nodes and the proportion of the total network with structural assignments as a quality metric.

## Related tools

- **GNPS (Global Natural Products Social Molecular Networking)** (Platform hosting feature-based molecular networking workflow, cosine similarity scoring engine, and public MS/MS reference library for library matching)
- **GNPS public library** (Curated MS/MS reference spectral database for matching experimental spectra against known metabolite standards)
- **LC-MS/MS** (Analytical instrumentation producing high-resolution MS/MS fragmentation spectra used as input for spectral matching)

## Evaluation signals

- High-confidence matches have cosine similarity ≥ 0.7 and span ≥ 4 matched fragment ions; verify by visual inspection of the MS/MS trace alignment.
- Annotated nodes cluster correctly in the molecular network—e.g., all hexosylated and pentosylated flavonoids map to the same or adjacent network regions, confirming consistency with known structural relationships.
- Coverage metric: >50% of spectral nodes receive library annotations; low coverage (<30%) indicates poor library representation or data quality issues.
- Matched compound class and substitution patterns align with the experimental design—e.g., if baicalein xylosylation is the hypothesis, all library hits should be flavonoids with expected hydroxyl group counts.
- No false-positive annotations: manual spot-checking of 10–20 highest-confidence matches against chemical formulas and MS/MS neutral loss patterns (e.g., 132.04 Da for pentose) confirms plausibility.

## Limitations

- Library matching depends critically on reference library completeness; many natural products and biotransformation metabolites are absent from public repositories, resulting in false negatives.
- Isomeric compounds (e.g., O-β-D-xylosylated vs. O-α-D-xylosylated baicalein) produce nearly identical MS/MS spectra and are difficult to distinguish by library matching alone; NMR or chromatographic standards are required for regioisomer confirmation.
- Spectral similarity scoring assumes that the experimental MS/MS was acquired under conditions (ionization mode, collision energy, instrument type) similar to those of library entries; mismatches degrade sensitivity.
- Promiscuous enzymes (e.g., LbUGT3) produce multiple regioisomeric metabolites that may not all be represented in the library, leading to partial or ambiguous annotations for complex biotransformation mixtures.

## Evidence

- [results] Many spectral nodes could be structurally annotated due to high coverage of the GNPS MS/MS reference library
- [results] An example of the molecular network- and MassQL-based enzymatic reactivity annotation
- [other] Retrieve the molecular network nodes and edges. Apply MassQL queries within GNPS to filter for MS/MS spectra exhibiting neutral losses of 132.0423 Da (pentosylation) or 162.0528 Da (hexosylation). Cross-reference MassQL-annotated spectral nodes with the molecular network to identify clusters corresponding to pentosylated and hexosylated metabolites.
- [other] Configure FBMN to generate a spectral similarity network and cosine similarity scoring.