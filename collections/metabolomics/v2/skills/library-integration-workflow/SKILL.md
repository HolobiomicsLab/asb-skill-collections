---
name: library-integration-workflow
description: Use when you have custom lipid entries (e.g., synthetic lipids, rare
  natural variants, or isotopically labeled standards) not covered by LipidMatch's
  default in-silico library, and you want to include them as matching candidates in
  your UHPLC-HRMS/MS fragment m/z matching workflow without modifying.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3778
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# library-integration-workflow

## Summary

Integration of user-authored .csv lipid libraries into LipidMatch to enable custom lipid entries as matching candidates in subsequent lipidomics analyses. This skill extends LipidMatch's in-silico fragmentation library (>500,000 lipid species across >60 types) with domain-specific or experimental lipid definitions.

## When to use

You have custom lipid entries (e.g., synthetic lipids, rare natural variants, or isotopically labeled standards) not covered by LipidMatch's default in-silico library, and you want to include them as matching candidates in your UHPLC-HRMS/MS fragment m/z matching workflow without modifying the core LipidMatch codebase.

## When NOT to use

- Your custom lipids are already well-represented in LipidMatch's default in-silico libraries (>500,000 species across >60 types) — direct matching without integration is more efficient.
- Your input mass spectrometry data is from Waters instruments — LipidMatch does not currently support Waters files.
- You need to modify fragmentation rules or scoring algorithms themselves — this skill integrates pre-defined libraries only; algorithmic changes require developer-level access.

## Inputs

- LipidMatch software installation (GarrettLab-UF/LipidMatch from GitHub)
- .csv lipid library file with custom lipid entries and annotated m/z fragmentation patterns
- MS/MS dataset or synthetic fragment m/z list for validation testing

## Outputs

- Registered custom lipid library entries in LipidMatch active library index
- Output candidate list from test matching workflow showing custom library entries ranked as matching candidates

## How to apply

Obtain the LipidMatch software and manual from the GarrettLab-UF/LipidMatch GitHub repository. Author a test .csv lipid library file conforming to the manual's format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns. Place the .csv file in the designated library directory within the LipidMatch installation. Run the library integration/loading step (as documented in the manual) to register the custom entries into the active library index. Execute a test matching workflow on a sample MS/MS dataset (or synthetic fragment m/z list) with the integrated library active. Parse and inspect the output candidate list to confirm that custom library entries appear ranked among the matching candidates, validating successful incorporation.

## Related tools

- **LipidMatch** (Core software for matching experimental fragment m/z values with simulated library m/z values; accepts integrated user-generated .csv libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature extraction upstream of LipidMatch matching)
- **XCMS** (Peak picking and feature extraction upstream of LipidMatch matching)
- **MS-DIAL** (Peak picking and feature extraction upstream of LipidMatch matching)
- **Compound Discoverer** (Peak picking and feature extraction upstream of LipidMatch matching)

## Evaluation signals

- Custom .csv library file conforms to LipidMatch manual format specification (includes valid lipid structure descriptors and m/z fragmentation patterns).
- Library integration/loading step completes without errors in the LipidMatch log or console output.
- At least one custom library entry appears in the output candidate list from test matching workflow, ranked by matching score.
- Custom entries' m/z values and fragmentation patterns match the input .csv file entries without truncation or corruption.
- Test workflow produces deterministic results: re-running with the same integrated library on the same MS/MS dataset yields identical candidate lists.

## Limitations

- LipidMatch does not currently support Waters instrument files, limiting integration to data from Q-Exactive, Agilent, Bruker, or SCIEX Q-TOF platforms.
- Custom library entries must be manually authored to conform to LipidMatch's .csv format; no automated validation or format conversion tool is provided in the public release.
- Integration is file-based; there is no documented GUI or interactive builder for custom library entries — all authoring is manual or script-driven.
- No changelog is documented in the README, making version compatibility and library format stability unclear across LipidMatch releases.

## Evidence

- [readme] User-generated library integration capability: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [readme] Comprehensive in-silico library baseline: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] Supported MS platforms for integration: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Waters platform limitation: "The software does not currently support Waters files"
- [other] Workflow task specification: "Run LipidMatch library integration/loading step (as documented in the manual) to register the custom entries into the active library index"
