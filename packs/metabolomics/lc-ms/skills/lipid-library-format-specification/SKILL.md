---
name: lipid-library-format-specification
description: Use when when you have curated or synthesized a set of custom lipid species (e.g., rare or organism-specific lipids, modified lipids, or synthetic standards) and need to integrate them into LipidMatch for candidate matching against your experimental MS/MS datasets.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - LipidMatch
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-library-format-specification

## Summary

Specification and validation of .csv lipid library file format for integration into LipidMatch, enabling custom lipid entries with annotated m/z fragmentation patterns to be incorporated as matching candidates. This skill ensures that user-authored libraries conform to the format required for successful ingestion and deployment in lipidomics workflows.

## When to use

When you have curated or synthesized a set of custom lipid species (e.g., rare or organism-specific lipids, modified lipids, or synthetic standards) and need to integrate them into LipidMatch for candidate matching against your experimental MS/MS datasets. Use this skill when the built-in in-silico libraries of 500,000+ lipids do not cover your analytes of interest.

## When NOT to use

- Your custom lipids are already available in the built-in 500,000+ species in-silico fragmentation library — use direct matching instead.
- Your input is a vendor-supplied or pre-compiled binary library format (not .csv) — consult tool-specific import/conversion guidance.
- You do not have MS/MS fragmentation data or in-silico fragmentation patterns for your custom lipids — the library cannot be populated.

## Inputs

- .csv file with user-authored lipid library entries conforming to LipidMatch manual format specification
- LipidMatch installation directory with designated library folder
- Optional: sample MS/MS dataset or synthetic fragment m/z list for validation testing

## Outputs

- Registered custom lipid library indexed in LipidMatch active library store
- Matching candidate output list confirming custom lipid entries are available for matching
- Validation report confirming successful integration

## How to apply

Consult the LipidMatch manual to determine the required .csv column schema (e.g., lipid name, m/z, fragmentation patterns, adduct type, etc.). Author your custom library entries following this specification, including at least 3–5 test entries with complete m/z and fragment annotation fields. Place the .csv file in the designated library directory within the LipidMatch installation. Run the LipidMatch library loading/integration step (as documented) to register entries into the active library index. Validate by executing a test matching workflow on a sample MS/MS dataset or synthetic fragment m/z list, then inspect the output candidate list to confirm that custom entries appear among ranked matches.

## Related tools

- **LipidMatch** (Primary software for integration, validation, and deployment of user-generated lipid libraries in .csv format and subsequent matching of custom entries against experimental MS/MS data) — https://github.com/GarrettLab-UF/LipidMatch

## Evaluation signals

- The .csv file adheres to the LipidMatch manual format specification (all required columns present, data types correct, m/z and fragmentation fields populated).
- The library loads without parse errors during the LipidMatch integration/loading step.
- At least one custom library entry appears in the ranked candidate output when queried against a test MS/MS dataset or synthetic fragment m/z list.
- Custom lipid entries are retrievable in the active library index and listed as available matching candidates before and after workflow execution.
- No duplicate or malformed entries in the indexed library; entry counts match the number of rows submitted in the .csv file.

## Limitations

- LipidMatch does not currently support Waters file format, which may limit applicability if your MS/MS data originates from Waters instruments.
- The quality and correctness of custom library entries depend entirely on the accuracy of manually curated or in-silico predicted m/z and fragmentation patterns; incorrect fragmentation annotations will produce false or missed matches.
- Library integration is file-based and manual; there is no built-in version control or rollback mechanism — maintain separate backups of library versions.
- No changelog mechanism documented for tracking modifications to custom libraries over time.

## Evidence

- [other] Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns.: "Author a test .csv lipid library conforming to the LipidMatch manual format specification, including at least 3–5 custom lipid entries with annotated m/z fragmentation patterns."
- [other] Place the .csv library file in the designated library directory within the LipidMatch installation and run LipidMatch library integration/loading step to register custom entries into the active library index.: "Place the .csv library file in the designated library directory within the LipidMatch installation. 4. Run LipidMatch library integration/loading step (as documented in the manual) to register the"
- [other] Execute a test matching workflow on a sample MS/MS dataset with the integrated library active and parse output candidate list to confirm custom library entries appear ranked among matching candidates.: "Execute a test matching workflow on a sample MS/MS dataset (or synthetic fragment m/z list) with the integrated library active. 6. Parse and inspect the output candidate list to confirm that at least"
- [readme] LipidMatch allows for facile integration of user generated libraries for unique applications.: "LipidMatch allows for facile integration of user generated libraries for unique applications."
- [intro] LipidMatch contains in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types.: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
