---
name: fragmentation-pattern-annotation
description: Use when you have custom lipid species (not covered by the 500,000+ built-in LipidMatch entries) that you need to match against experimental MS/MS data, or you are extending LipidMatch's coverage for specialized lipid classes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
---

# fragmentation-pattern-annotation

## Summary

Annotate custom lipid entries with m/z fragmentation patterns conforming to LipidMatch format specification, enabling integration into lipidomics matching workflows. This skill bridges user-authored lipid definitions and in-silico fragment matching by structuring experimental or theoretical fragmentation data into machine-readable .csv library entries.

## When to use

You have custom lipid species (not covered by the 500,000+ built-in LipidMatch entries) that you need to match against experimental MS/MS data, or you are extending LipidMatch's coverage for specialized lipid classes. The trigger is the availability of annotated m/z fragmentation patterns for your lipid of interest—either from literature, prior experiments, or in-silico prediction—and a need to incorporate them into an automated matching workflow.

## When NOT to use

- You are using only the built-in 500,000+ lipid species and do not need custom entries.
- Your MS/MS data is from a Waters instrument; LipidMatch does not currently support Waters files.
- You lack annotated m/z fragmentation patterns for your lipids of interest and cannot obtain or predict them.

## Inputs

- annotated m/z fragmentation pattern data (literature, experimental, or in-silico predicted)
- lipid identifier and parent m/z for each custom entry
- LipidMatch manual (format specification document)

## Outputs

- .csv lipid library file conforming to LipidMatch format
- registered custom lipid entries in the active LipidMatch library index

## How to apply

Author a .csv lipid library file following the LipidMatch manual format specification, with each row representing a custom lipid entry including at minimum: lipid name/identifier, parent m/z, and annotated fragment m/z values (and optionally intensities or fragmentation rules). Create 3–5 test entries to verify format compliance. Place the .csv file in the designated library directory within the LipidMatch installation (as documented in the manual). Run the LipidMatch library integration/loading step to register custom entries into the active library index. The rationale is that LipidMatch matches experimental fragment m/z values against simulated library m/z values; conforming to its .csv schema ensures your custom entries are parseable and ranked consistently with built-in library entries during candidate matching.

## Related tools

- **LipidMatch** (primary tool for loading, integrating, and matching custom .csv lipid libraries against experimental MS/MS fragment m/z values) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (upstream peak picking and feature detection; output used as input to LipidMatch matching workflow)
- **XCMS** (upstream peak picking and feature detection; output used as input to LipidMatch matching workflow)
- **MS-DIAL** (upstream peak picking and feature detection; output used as input to LipidMatch matching workflow)

## Evaluation signals

- The .csv file parses without errors when loaded by the LipidMatch integration step (no format schema violations).
- At least one custom library entry appears in the candidate match list when executing a test matching workflow on sample MS/MS data or a synthetic fragment m/z list.
- Custom entries are ranked among candidates with m/z match tolerance consistent with the instrument's mass accuracy (e.g., orbitrap ≤5 ppm as noted in the article).
- Candidate ranking order reflects expected fragmentation intensity patterns (if annotated) or matches within acceptable ppm tolerance windows.
- The registered custom entries persist in the active library index across multiple matching runs without re-loading.

## Limitations

- LipidMatch does not currently support Waters files, limiting applicability to Agilent, Bruker, or SCIEX Q-TOF instruments and Q-Exactive orbitrap platforms.
- Custom fragmentation annotations must be accurate and complete; incomplete or incorrect m/z patterns will produce false negatives or misleading candidate rankings.
- The .csv format specification is fixed by the LipidMatch manual; deviation requires either manual debugging or re-authoring of entries.
- No automatic validation or visualization tool is mentioned to pre-screen .csv entries before integration; format errors may only surface during the matching workflow.

## Evidence

- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [readme] in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] LipidMatch allows for facile integration of user generated libraries for unique applications: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [other] Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns.: "Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
