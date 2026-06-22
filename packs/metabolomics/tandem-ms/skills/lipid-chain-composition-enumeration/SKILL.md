---
name: lipid-chain-composition-enumeration
description: Use when constructing a de novo or expanded lipid spectral library that must cover all theoretically possible chain compositions and double-bond positional isomers for one or more lipid classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3800
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  tools:
  - XCMS
  - CAMERA
  - LipidIN
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1038/s41467-025-59683-5
  title: LipidIN
evidence_spans:
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification'
- 'XCMS: Processing mass spectrometry data for metabolite profiling using nonlinear peak alignment, matching and identification.'
- 'CAMERA: an'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidin_cq
    doi: 10.1038/s41467-025-59683-5
    title: LipidIN
  dedup_kept_from: coll_lipidin_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-025-59683-5
  all_source_dois:
  - 10.1038/s41467-025-59683-5
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-chain-composition-enumeration

## Summary

Systematically enumerate all valid acyl chain structures for a lipid class by iterating over carbon count and unsaturation constraints, then generate regioisomeric variants for each composition to populate a hierarchical fragmentation library. This skill enables comprehensive coverage of lipid structural diversity needed for sensitive and specific mass spectrometry-based annotation.

## When to use

Apply this skill when constructing a de novo or expanded lipid spectral library that must cover all theoretically possible chain compositions and double-bond positional isomers for one or more lipid classes. Use it specifically when traditional spectral matching has limited coverage and you need to enumerate chains within defined carbon count ranges (e.g., C8–C24) and unsaturation constraints (e.g., 0–6 degrees of unsaturation) to avoid missing lipid species during annotation.

## When NOT to use

- When only a small, curated set of known lipids is needed (e.g., targeted assay of <100 lipids); enumeration is overkill for targeted workflows.
- When lipid standards or fragmentation rules for your lipid class are unavailable or unreliable; enumeration requires validated fragmentation patterns.
- When computational resources are severely constrained; enumerating 168+ million entries and organizing them hierarchically requires substantial memory and disk I/O.

## Inputs

- Lipid class definition and taxonomy
- Acyl chain composition rules (carbon count range, unsaturation constraints)
- Lipid fragmentation rule set (neutral loss masses, characteristic ion patterns)
- Known lipid standards for validation (optional)

## Outputs

- Hierarchical lipid fragmentation library indexed by class, composition, and positional isomer
- Enumerated chain structures with all regioisomeric double-bond variants
- Theoretical fragment ion m/z values for each chain composition
- Validation report confirming library completeness and entry count

## How to apply

First, define the lipid class taxonomy and establish acyl chain composition rules by specifying the allowable carbon count range and degree of unsaturation constraints (e.g., chains with 8–24 carbons and 0–6 double bonds). Second, iterate over all valid carbon counts and unsaturation levels, generating all possible regioisomeric double-bond position variants for each composition using combinatorial or graph-based enumeration. Third, compute theoretical fragment ion m/z values for each enumerated chain composition using established lipid fragmentation rules (neutral losses, characteristic ion masses). Fourth, organize the resulting entries into a hierarchical index structure (lipid class → chain composition → positional isomer) to enable rapid lookup during spectral matching. Finally, validate library completeness by spot-checking fragment patterns against known lipid standards and verifying the total entry count matches the expected magnitude (e.g., 168.6 million entries for comprehensive coverage).

## Related tools

- **XCMS** (Processes mzML mass spectrometry data for metabolite profiling and peak alignment, preparing data for spectral matching against the enumerated library)
- **CAMERA** (Performs compound spectra extraction and annotation of LC–MS/MS datasets, used in conjunction with enumerated libraries for lipid feature annotation)
- **LipidIN** (Reference implementation providing the 168.6 million entry hierarchical library and spectral querying module that consumes enumerated chain compositions) — https://github.com/LinShuhaiLAB/LipidIN

## Evaluation signals

- Total entry count in the hierarchical library matches the expected magnitude (e.g., 168.6 million) for the defined lipid classes and composition rules.
- All theoretically valid acyl chain structures within the specified carbon and unsaturation ranges are present; no missing compositions can be identified by manual spot-checks.
- Fragment ion m/z values computed for enumerated chains match those of known lipid standards, confirming fragmentation rules were correctly applied.
- Hierarchical index structure (class → composition → isomer) is traversable and query lookup time is sublinear (e.g., <1 second for 70 billion queries as reported).
- Validation against a reference set of authentic lipid spectra shows no systematic gaps in coverage or mismatches in predicted vs. observed fragments.

## Limitations

- Enumeration assumes lipid fragmentation rules are complete and accurate; missing or incorrect rules will produce incomplete or incorrect entries.
- Storage and indexing of 168+ million entries requires substantial computational infrastructure; practical deployment may require optimization or tiering (e.g., storing a lightweight subset on disk and the full library in cloud storage).
- Regioisomeric enumeration can produce combinatorial explosion if unsaturation constraints are very loose (e.g., many degrees of unsaturation per chain); pragmatic limits on chain length and unsaturation must be applied.
- The enumerated library is static; addition of newly characterized lipid classes or updated fragmentation rules requires re-enumeration and re-indexing.

## Evidence

- [other] 1. Define the lipid class taxonomy and acyl chain composition rules (carbon count range, degree of unsaturation constraints). 2. Enumerate all valid acyl chain structures by iterating over carbon counts and unsaturation levels, generating all regioisomeric double-bond position variants for each composition.: "Define the lipid class taxonomy and acyl chain composition rules (carbon count range, degree of unsaturation constraints). 2. Enumerate all valid acyl chain structures by iterating over carbon counts"
- [other] 3. Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation). 4. Organize the 168.6 million entries into a hierarchical index structure (lipid class → chain composition → positional isomer) for efficient lookup.: "Generate fragment ion theoretical m/z values for each chain composition using lipid fragmentation rules (neutral loss, characteristic ion generation). 4. Organize the 168.6 million entries into a"
- [readme] LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations.: "LipidIN features 168.6 million lipid fragmentation hierarchical library that encompass all potential chain compositions and carbon-carbon double bond locations"
- [other] 5. Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million.: "Validate the library completeness and correctness by spot-checking fragment patterns against known lipid standards and verifying entry count matches the target 168.6 million"
