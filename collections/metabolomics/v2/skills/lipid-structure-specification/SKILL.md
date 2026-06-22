---
name: lipid-structure-specification
description: Use when you have identified lipid species unique to your sample type (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3766
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values
- LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)
- for example MZmine, XCMS, MS-DIAL, and Compound Discoverer
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch_cq
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch_cq
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

# lipid-structure-specification

## Summary

Define and format user-generated lipid libraries in .csv schema to extend LipidMatch's identification capability for specialized or non-standard lipid species. This skill enables researchers to encode lipid nomenclature, molecular formulas, adduct types, and in-silico fragment m/z values for integration into the LipidMatch workflow.

## When to use

You have identified lipid species unique to your sample type (e.g., rare lipid modifications, synthetic lipids, or lipids from non-mammalian organisms) that are not present in LipidMatch's built-in library of 500,000+ lipid species across 60+ lipid types, and you want to augment the identification workflow with your custom entries prior to experimental UHPLC-HRMS/MS data processing.

## When NOT to use

- Your target lipids are already comprehensively covered by LipidMatch's 500,000+ species library — use the built-in library directly.
- You lack validated fragmentation data or molecular formulas for your lipids — this skill requires accurate structure specification; incomplete or uncertain data will produce unreliable identifications.
- Your mass spectrometry data comes from a Waters instrument — LipidMatch does not currently support Waters files, so integration of custom libraries will not improve compatibility.

## Inputs

- Lipid structure information (names, molecular formulas, adduct types, fragmentation patterns)
- Plain-text or spreadsheet template (e.g., .xlsx, .csv) listing lipid metadata
- Representative UHPLC-HRMS/MS data (mzML, netCDF, or vendor format) for validation

## Outputs

- User-generated lipid library in .csv format conforming to LipidMatch schema
- Merged lipid library (built-in + user entries) ready for LipidMatch workflow integration
- Validation report (lipid identifications from test data using extended library)

## How to apply

Create a user-generated lipid library by encoding each lipid entry in .csv format following LipidMatch schema specifications: include lipid names (LIPID MAPS nomenclature preferred), molecular formulas (exact mass), adduct types ([M+H]+, [M+Na]+, etc.), and in-silico fragment m/z values computed from fragmentation rules or validated experimentally. Validate the .csv structure and content against LipidMatch format requirements (column headers, data types, formula syntax) before integration. Use LipidMatch's documented facile integration mechanism to merge the user library with the built-in library. Test the extended workflow by running LipidMatch identifications against representative UHPLC-HRMS/MS data to verify that custom lipid entries are matched correctly and do not introduce false positives or parsing errors.

## Related tools

- **LipidMatch** (Integration point for user-generated libraries; performs lipid identification by matching experimental fragment m/z values with simulated library m/z values) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Upstream peak picking and feature extraction to generate experimental m/z and retention time values for validation against user library)
- **XCMS** (Upstream peak picking and feature extraction to generate experimental m/z and retention time values for validation against user library)
- **MS-DIAL** (Upstream peak picking and feature extraction to generate experimental m/z and retention time values for validation against user library)
- **Compound Discoverer** (Upstream peak picking and feature extraction to generate experimental m/z and retention time values for validation against user library)

## Evaluation signals

- CSV file validates against LipidMatch schema requirements: all required columns (lipid name, molecular formula, adduct type, fragment m/z values) are present and populated; data types match specification (e.g., numeric m/z, valid formula syntax).
- Merged library is successfully loaded by LipidMatch without parsing errors or warnings.
- Test UHPLC-HRMS/MS data processed with extended library yields identifications for custom lipid entries with fragment m/z matches within expected mass accuracy window (typically ±5 ppm for high-resolution orbitrap or Q-TOF instruments).
- No false-positive or off-target identifications of known compounds appear as a result of custom library integration; specificity metrics remain stable relative to built-in library alone.
- Custom lipid identifications are cross-validated against experimental fragmentation patterns or literature MS/MS spectra when available.

## Limitations

- User-generated libraries are only as accurate as their underlying lipid structure definitions and fragmentation rules; incorrect molecular formulas, incomplete fragment annotations, or non-representative in-silico fragmentation will degrade identification quality.
- LipidMatch does not currently support Waters mass spectrometry file formats, so custom libraries cannot extend identification capability for Waters-acquired data.
- The facile integration mechanism assumes standard .csv formatting; non-standard delimiters, encoding, or column ordering may cause integration failures or silent data corruption.
- No built-in validation tool is explicitly mentioned to detect schema violations or inconsistencies in user libraries before integration; manual or external validation is required.
- Large custom libraries may increase computational cost and memory footprint of the LipidMatch matching workflow.

## Evidence

- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [readme] LipidMatch allows for facile integration of user generated libraries for unique applications: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [other] Create a user-generated lipid library in .csv format following LipidMatch schema specifications (lipid names, molecular formulas, adduct types, and in-silico fragment m/z values): "Create a user-generated lipid library in .csv format following LipidMatch schema specifications (lipid names, molecular formulas, adduct types, and in-silico fragment m/z values)"
- [other] Validate the .csv structure and content against LipidMatch format requirements. Integrate the user library into the LipidMatch workflow using the facile integration mechanism provided by the software.: "Validate the .csv structure and content against LipidMatch format requirements. Integrate the user library into the LipidMatch workflow using the facile integration mechanism provided by the software."
- [other] Test the extended workflow by running LipidMatch identifications against experimental UHPLC-HRMS/MS data using the combined library (built-in library + user-generated library): "Test the extended workflow by running LipidMatch identifications against experimental UHPLC-HRMS/MS data using the combined library (built-in library + user-generated library)"
