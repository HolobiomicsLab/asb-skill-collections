---
name: technical-specification-tabulation
description: Use when when you need to verify whether a specific mass spectrometry instrument platform (vendor and model), acquisition mode (e.g., targeted, ddMS2-topN, AIF, direct infusion, imaging), or file format is compatible with a lipidomics or proteomics software tool;
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data
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
---

# technical-specification-tabulation

## Summary

Systematically extract and tabulate validated instrument platforms, vendor models, and acquisition mode combinations from software documentation and repositories to establish a definitive support matrix. This skill produces a CSV-formatted compatibility specification that enables users to determine whether their analytical hardware is supported before committing to a workflow.

## When to use

When you need to verify whether a specific mass spectrometry instrument platform (vendor and model), acquisition mode (e.g., targeted, ddMS2-topN, AIF, direct infusion, imaging), or file format is compatible with a lipidomics or proteomics software tool; or when assembling a methods section that requires explicit enumeration of validated platform/mode combinations to avoid false negative results from unsupported hardware.

## When NOT to use

- Input documentation is silent on instrument compatibility (no explicit validated list) — use general compatibility inference instead.
- You need real-time or benchmarked performance metrics (speed, sensitivity, accuracy per platform) — this skill only enumerates support status, not quantitative validation.
- The software uses dynamic or vendor-specific plugins that alter support matrix per installation — static tabulation will be incomplete.

## Inputs

- GitHub repository (code, README, documentation)
- Supplementary materials or technical documentation
- Publication methods/results sections describing instrument validation

## Outputs

- CSV tabulation file with columns: instrument_vendor, instrument_model, acquisition_mode, validation_status, supporting_reference
- Negative case list (explicitly unsupported platforms/modes)
- Completeness checklist against documented platforms

## How to apply

Clone or download the software repository and systematically scan the README, documentation, and supplementary materials for explicit statements of validated platforms, acquisition modes, and unsupported systems. For LipidMatch, extract confirmed combinations: Q-Exactive orbitrap with targeted, ddMS2-topN, and AIF modes; Agilent, Bruker, and SCIEX Q-TOF platforms with direct infusion and imaging modes; and document negative cases (e.g., Waters instruments explicitly unsupported). Construct a tabular CSV file with columns for instrument vendor, instrument model, acquisition mode, validation status, and supporting reference location (section and evidence). Cross-validate completeness by checking all named platforms and modes mentioned in the documentation against your compiled matrix. Prioritize explicit 'tested and validated' or 'does not support' language over implied support.

## Related tools

- **LipidMatch** (Software tool whose instrument/mode compatibility matrix is being extracted and tabulated) — https://github.com/GarrettLab-UF/LipidMatch
- **Q-Exactive orbitrap** (Validated instrument platform for targeted, ddMS2-topN, and AIF acquisition modes)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging modes)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging modes)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging modes)

## Evaluation signals

- Tabulated CSV contains all instrument vendors/models mentioned in README (completeness check against named platforms).
- Each row in the matrix is backed by an explicit evidence span from documentation (no inferred or assumed support).
- Negative cases (unsupported platforms like Waters) are clearly marked with 'unsupported' status and supporting reference.
- No contradictions between columns: if a vendor is listed as 'supported' for one mode, verify that claim is sourced to a single, consistent evidence statement.
- Cross-check: sum of supported vendor-mode pairs matches the count of distinct supported combinations stated in the README or article.

## Limitations

- The documented support matrix is static and may lag behind actual software capabilities; unsupported platforms may gain support in newer versions (no changelog found in the repository).
- Documentation may list instruments at the vendor level (e.g., 'Q-TOF') without specifying exact models or firmware versions required for validation.
- Implicit support (e.g., mention of 'UHPLC-HRMS/MS' without acquisition mode detail) cannot be assumed equivalent to explicit validation; only 'tested and validated' statements are reliable.
- File format support (e.g., Waters .raw) is a separate axis from instrument hardware support and must be extracted separately.

## Evidence

- [readme] LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] LipidMatch has also been applied for the annotation of direct infusion and imaging experiments: "LipidMatch has also been applied for the annotation of direct infusion and imaging experiments"
- [intro] LipidMatch has been tested and validated using Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments: "LipidMatch has been tested and validated using Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments"
- [intro] The software does not currently support Waters files: "The software does not currently support Waters files"
