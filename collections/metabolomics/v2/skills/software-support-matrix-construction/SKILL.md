---
name: software-support-matrix-construction
description: Use when you need to determine the full scope of hardware and methodological compatibility for a bioinformatics tool before designing an analytical workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_3050
  - http://edamontology.org/topic_0121
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  - Waters instruments
  techniques:
  - direct-infusion-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# software-support-matrix-construction

## Summary

Systematically extract and tabulate the complete matrix of instrument vendors, models, acquisition modes, and validation status for a research software tool by mining repository documentation, GitHub materials, and published validation reports. This skill produces a definitive compatibility reference that distinguishes validated, untested, and explicitly unsupported platform combinations.

## When to use

Apply this skill when you need to determine the full scope of hardware and methodological compatibility for a bioinformatics tool before designing an analytical workflow. Specifically, use it when you have access to a software repository and its documentation but lack a pre-compiled compatibility matrix, or when you must audit whether a specific instrument/vendor/acquisition-mode triple is supported before committing to a tool.

## When NOT to use

- Input material is already a pre-compiled compatibility matrix or feature table — skip to validation step instead.
- Tool documentation is absent or inaccessible (e.g., closed-source software with no public README) — this skill requires written statements of support.
- You only need to check whether ONE specific instrument/mode combination is supported; use targeted documentation search instead of full matrix construction.

## Inputs

- GitHub repository source code and README (text)
- Tool manual or supplementary documentation (PDF/text)
- Published validation paper or technical report (text)
- EnrichedIndex of tool mentions and capabilities (structured)

## Outputs

- Instrument-acquisition-mode compatibility matrix (CSV with vendor, model, mode, status, reference columns)
- List of explicitly unsupported platforms (text)
- Validation evidence map (platform → evidence location in source materials)

## How to apply

Begin by accessing the tool's GitHub repository README and any supplementary documentation (manuals, guides, validation papers). Extract all explicit statements naming specific instrument vendors (e.g., Thermo, Agilent, Bruker, SCIEX, Waters), instrument models (e.g., Q-Exactive orbitrap), and acquisition modes (e.g., targeted, ddMS2-topN, AIF, direct infusion, imaging). Separately document positive cases (validated combinations with supporting evidence location) and negative cases (explicitly unsupported platforms). Cross-reference findings against any EnrichedIndex or supplementary materials that may list additional validated configurations. Construct a tabular CSV with columns: instrument_vendor, instrument_model, acquisition_mode, validation_status (validated/unsupported/untested), and supporting_reference (section/line in README or paper). Validate completeness by confirming all named platforms and modes from the documentation appear in your matrix.

## Related tools

- **LipidMatch** (Subject tool under compatibility assessment; validates lipid identifications using Q-Exactive orbitrap, Agilent/Bruker/SCIEX Q-TOF UHPLC-HRMS/MS in targeted, ddMS2-topN, AIF, direct infusion, and imaging modes) — https://github.com/GarrettLab-UF/LipidMatch
- **Q-Exactive orbitrap** (Reference instrument model for which LipidMatch validation is documented across multiple acquisition modes)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging experiments with LipidMatch)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging experiments with LipidMatch)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (Validated instrument platform for direct infusion and imaging experiments with LipidMatch)
- **Waters instruments** (Explicitly unsupported platform for LipidMatch; reference negative case in compatibility matrix)

## Evaluation signals

- CSV matrix contains no blank cells in the vendor, model, mode, and status columns; all rows are complete.
- Every validated entry includes a reference to a specific source location (README section, paper section, line number, or evidence quote).
- Cross-check: sum of validated + unsupported + untested rows equals total number of distinct platform combinations named in source materials.
- Negative validation cases (unsupported platforms like Waters) are explicitly listed with supporting evidence quotes.
- Matrix structure conforms to expected schema: at least one row per validated instrument model, at minimum one row per explicitly unsupported vendor, and one row per documented acquisition mode per instrument.

## Limitations

- This skill reconstructs only what is explicitly stated in public documentation; undocumented but functional support/incompatibility will be missed.
- Acquisition mode support is often validated only on a subset of sample types or tissues; the matrix reflects tested cases only, not all theoretically possible applications.
- LipidMatch explicitly does not support Waters files; compatibility matrix is contingent on tool version and any future updates not yet reflected in current README.
- The matrix captures platform support at the time of documentation; newer instrument models released after the last README update will not appear in the matrix.

## Evidence

- [readme] LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] LipidMatch has also been applied for the annotation of direct infusion and imaging experiments: "LipidMatch has also been applied for the annotation of direct infusion and imaging experiments"
- [readme] as well as Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments: "as well as Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] LipidMatch is modular, allowing it to fit in various workflows you may have in your lab: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab"
