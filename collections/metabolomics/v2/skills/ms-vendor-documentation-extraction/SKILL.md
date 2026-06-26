---
name: ms-vendor-documentation-extraction
description: Use when you need to determine the complete set of validated instrument/vendor
  and acquisition mode combinations for a mass spectrometry analysis tool, when assessing
  whether your specific instrument platform (vendor, model, acquisition method) is
  supported before committing to a workflow, or when.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3763
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - Q-Exactive orbitrap UHPLC-HRMS/MS
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  techniques:
  - direct-infusion-MS
  license_tier: open
  provenance_tier: literature
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

# MS vendor documentation extraction

## Summary

Extract and tabulate instrument vendor, model, acquisition mode, and validation status from mass spectrometry software documentation and README files to build a comprehensive support matrix. This skill is used to answer questions about which instrument platforms and data acquisition methods a lipidomics or proteomics tool officially supports or explicitly does not support.

## When to use

Use this skill when you need to determine the complete set of validated instrument/vendor and acquisition mode combinations for a mass spectrometry analysis tool, when assessing whether your specific instrument platform (vendor, model, acquisition method) is supported before committing to a workflow, or when building an instrument compatibility matrix to guide instrument selection or method development decisions.

## When NOT to use

- When the software documentation provides only generic claims ('works with most instruments') without naming specific platforms or vendors — extraction requires explicit naming of supported/unsupported combinations
- When you need to verify instrument compatibility experimentally or in-house; this skill documents claimed support, not runtime validation
- When instrument compatibility information is scattered across multiple blog posts, forum discussions, or undated GitHub issues rather than consolidated in official README or publication

## Inputs

- GitHub repository README or documentation file for mass spectrometry analysis software
- Published article or supplementary materials describing software validation
- Software manual or user guide section detailing supported instruments

## Outputs

- Tabular CSV file with columns: instrument vendor, instrument model, acquisition mode, validation status, evidence location
- Structured list of validated instrument/vendor and acquisition mode combinations
- List of explicitly unsupported platforms (negative cases)

## How to apply

First, clone or download the target software repository and scan the README, documentation, and supplementary materials for explicit statements of validated instrument platforms and acquisition modes. Extract named vendors (e.g., Thermo, Agilent, Bruker, SCIEX, Waters), instrument models (e.g., Q-Exactive orbitrap, Q-TOF), and acquisition methods (e.g., targeted, ddMS2-topN, AIF, direct infusion, imaging). Record both positive cases (validated combinations with supporting evidence location) and negative cases (explicitly unsupported platforms or methods, such as 'Waters files not supported'). Construct a tabular format with columns for instrument vendor, instrument model, acquisition mode, validation status, and supporting evidence location (section of README or documentation). Validate completeness by cross-checking all named platforms and modes mentioned in the documentation against your extracted matrix to ensure no combinations are missed.

## Related tools

- **LipidMatch** (Target software whose instrument support matrix is being extracted) — https://github.com/GarrettLab-UF/LipidMatch
- **Q-Exactive orbitrap UHPLC-HRMS/MS** (Example validated instrument platform; used to identify and classify supported hardware)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Example validated vendor/model combination; used to identify and classify supported hardware)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Example validated vendor/model combination; used to identify and classify supported hardware)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (Example validated vendor/model combination; used to identify and classify supported hardware)

## Evaluation signals

- Completeness check: All instrument vendors, models, and acquisition modes mentioned anywhere in the README, article text, or supplementary materials appear exactly once in the final matrix
- Negative case coverage: Explicitly unsupported platforms (e.g., 'Waters files not supported') are documented with validation status 'not supported' and evidence location cited
- Evidence traceability: Every row in the matrix references a specific section (intro, methods, README) and a verbatim quote or clear evidence span from the source
- Consistency of acquisition mode classification: All acquisition modes are consistently named (e.g., 'ddMS2-topN' or 'data-dependent top-N', not mixed; 'AIF' or 'all ion fragmentation', not both)
- No orphaned claims: If the documentation mentions a vendor or model name, it appears in the matrix with a validation status (supported, unsupported, or unclear)

## Limitations

- Documentation may not list all vendor/instrument/mode combinations tested in-house; absence from README does not prove unsupported status — only explicit negative statements count as confirmed unsupported
- Acquisition mode naming and classification may vary across vendors (e.g., 'AIF' vs. 'all ion fragmentation') — standardization across a matrix requires manual interpretation
- No changelog found in the LipidMatch repository, so the matrix captures only the current documented state; historical changes in support status are not available
- The extracted matrix reflects claimed support as documented; runtime compatibility, file format parsing, or edge cases in actual data processing may reveal undocumented limitations

## Evidence

- [readme] LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] as well as Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments. LipidMatch has also been applied for the annotation of direct infusion and imaging experiments: "as well as Agilent, Bruker and SCIEX Q-TOF UHPLC-HRMS/MS experiments. LipidMatch has also been applied for the annotation of direct infusion and imaging experiments"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] the GitHub page for LipidMatch is: https://github.com/GarrettLab-UF/LipidMatch: "the GitHub page for LipidMatch is: https://github.com/GarrettLab-UF/LipidMatch"
