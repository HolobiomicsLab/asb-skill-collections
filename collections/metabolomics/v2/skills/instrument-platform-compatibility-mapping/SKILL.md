---
name: instrument-platform-compatibility-mapping
description: Use when when adopting a mass spectrometry data processing tool (e.g., LipidMatch) and needing to verify whether your specific instrument platform (vendor + model) and acquisition mode combination (targeted, ddMS2-topN, AIF, direct infusion, imaging) have been formally validated.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3443
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  techniques:
  - direct-infusion-MS
  - tandem-MS
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

# instrument-platform-compatibility-mapping

## Summary

A systematic approach to extract, validate, and document the complete matrix of instrument vendors, models, and acquisition modes for which a lipidomics software tool has been tested and validated. This skill produces a machine-readable compatibility table and identifies explicitly unsupported platforms to guide users toward compatible workflows.

## When to use

When adopting a mass spectrometry data processing tool (e.g., LipidMatch) and needing to verify whether your specific instrument platform (vendor + model) and acquisition mode combination (targeted, ddMS2-topN, AIF, direct infusion, imaging) have been formally validated. Use this skill before investing time in troubleshooting or modifying workflows on potentially unsupported hardware.

## When NOT to use

- Tool documentation explicitly lists all compatible platforms in a single, pre-built compatibility table already provided by the vendor — use that table directly instead.
- User is troubleshooting a specific error on a known-unsupported platform; this skill documents compatibility, it does not enable workarounds.
- The goal is to evaluate instrument performance metrics (e.g., mass accuracy, resolution, sensitivity) rather than to validate software support — use a different comparative benchmarking skill.

## Inputs

- tool GitHub repository (e.g., GarrettLab-UF/LipidMatch)
- tool README documentation
- published manuscript or supplementary materials
- enriched index of tools and validated platforms

## Outputs

- instrument–mode compatibility matrix (CSV format)
- list of supported vendor–model–mode combinations
- list of explicitly unsupported platforms with evidence
- evidence reference table mapping claims to source sections

## How to apply

First, access the tool's primary documentation sources (README, GitHub repository, published paper supplementary materials) and systematically extract all explicit statements about validated and unsupported instruments. Scan for named vendors (Thermo, Agilent, Bruker, SCIEX, Waters) and specific models (e.g., Q-Exactive orbitrap). For each instrument-mode pair identified, record the validation status (supported, unsupported, or untested) and the exact evidence location (section, quote). Cross-reference findings against the published enriched index or supplementary tables to ensure completeness. Construct a tabular CSV with columns for vendor, instrument model, acquisition mode, validation status, and evidence reference. Validate that all named platforms and modes from the documentation appear in the final matrix, and document any negative cases (explicitly unsupported platforms) as separate entries to prevent false inclusion.

## Related tools

- **LipidMatch** (target software tool for which compatibility matrix is being constructed) — https://github.com/GarrettLab-UF/LipidMatch
- **Q-Exactive orbitrap** (validated high-resolution mass spectrometry platform tested with LipidMatch)
- **Agilent Q-TOF UHPLC-HRMS/MS** (validated vendor platform tested with LipidMatch for direct infusion and imaging)
- **Bruker Q-TOF UHPLC-HRMS/MS** (validated vendor platform tested with LipidMatch for direct infusion and imaging)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (validated vendor platform tested with LipidMatch for direct infusion and imaging)

## Evaluation signals

- All named instrument vendors and models from the README and enriched index appear in the final compatibility matrix with no omissions.
- Acquisition modes (targeted, ddMS2-topN, AIF, direct infusion, imaging) are correctly paired with each instrument vendor and documented with appropriate validation status.
- Waters is explicitly listed as unsupported with verbatim evidence ('The software does not currently support Waters files').
- Each row in the compatibility matrix includes a traceable evidence reference (section location and quote) that matches the source documentation.
- Cross-check confirms all pairs mentioned in the enriched index (e.g., 'Q-Exactive orbitrap with targeted, ddMS2-topN, and AIF modes'; 'Agilent, Bruker, and SCIEX Q-TOF with direct infusion and imaging') are present in the output table.

## Limitations

- Documentation may not explicitly name all acquisition modes tested on every instrument; inferences about untested combinations must be flagged as such rather than assumed unsupported.
- The GitHub repository README alone may not capture all validated platforms if supporting evidence is scattered across supplementary materials, method sections, or separate documentation files not provided in this context.
- Negative evidence (explicit unsupported platforms like Waters) is only reliable when stated directly; absence of mention of a platform does not confirm unsupported status.
- Vendor and model names in documentation may use shorthand or variation (e.g., 'Q-TOF' vs. 'QTOF') that must be normalized to avoid duplicate or conflicting entries in the compatibility matrix.

## Evidence

- [readme] LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] LipidMatch has also been applied for the annotation of direct infusion and imaging experiments: "LipidMatch has also been applied for the annotation of direct infusion and imaging experiments"
- [readme] LipidMatch has been tested and validated using Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments: "LipidMatch has been tested and validated using Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
