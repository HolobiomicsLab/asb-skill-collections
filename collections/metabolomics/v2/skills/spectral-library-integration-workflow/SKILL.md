---
name: spectral-library-integration-workflow
description: Use when when you have experimental UHPLC-HRMS/MS data targeting lipid species not adequately covered by LipidMatch's built-in library (500,000+ species across 60+ lipid types), or when working with specialized applications requiring custom lipid definitions (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0153
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

# spectral-library-integration-workflow

## Summary

Integration of user-generated lipid spectral libraries into LipidMatch to enable identification of lipid species in specialized or unique lipidomics applications. This workflow extends LipidMatch's built-in library of 500,000+ lipid species by combining it with custom libraries formatted and validated according to LipidMatch schema specifications.

## When to use

When you have experimental UHPLC-HRMS/MS data targeting lipid species not adequately covered by LipidMatch's built-in library (500,000+ species across 60+ lipid types), or when working with specialized applications requiring custom lipid definitions (e.g., non-standard adducts, rare lipid classes, or organism-specific lipidomes). Use this when standard peak-picking and library-matching workflows yield insufficient or incomplete annotations.

## When NOT to use

- Input is already a fully annotated lipid feature table from another lipidomics software; use library combination/consensus instead.
- Your UHPLC-HRMS/MS data were acquired on Waters instruments; LipidMatch does not currently support Waters files.
- Your custom lipid definitions cannot be expressed as molecular formulas, adduct types, and predictable fragment m/z values; rule-based in-silico fragmentation is required.

## Inputs

- User-generated lipid library in .csv format with lipid names, molecular formulas, adduct types, and in-silico fragment m/z values
- Peak-picked feature matrix from UHPLC-HRMS/MS data (from MZmine, XCMS, MS-DIAL, or Compound Discoverer)
- Experimental MS/MS fragment m/z values and retention times
- LipidMatch built-in library (500,000+ lipid species)

## Outputs

- Integrated lipid identification results combining built-in and user-generated library matches
- Annotated feature table with lipid identifications, fragment m/z matches, and confidence scores
- Validated user library metadata confirming schema compliance and integration success

## How to apply

First, create a user-generated lipid library in .csv format following LipidMatch schema specifications, including lipid names, molecular formulas, adduct types, and in-silico fragment m/z values. Validate the .csv structure and content against LipidMatch format requirements to ensure compatibility. Integrate the user library into the LipidMatch workflow using the documented facile integration mechanism. Perform peak picking on your UHPLC-HRMS/MS data using one of the supported tools (MZmine, XCMS, MS-DIAL, or Compound Discoverer) to generate a feature matrix with experimental m/z and retention time values. Run LipidMatch identifications against the combined library (built-in library + user-generated library) by matching experimental fragment m/z values with simulated library m/z values. Finally, validate results by confirming that novel lipids are correctly identified and that built-in library matches remain unchanged.

## Related tools

- **LipidMatch** (Core software for in-silico lipid library matching and spectral integration; performs fragment m/z matching against combined (built-in + user-generated) libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature detection to prepare experimental feature matrix for LipidMatch input)
- **XCMS** (Peak picking and feature detection to prepare experimental feature matrix for LipidMatch input)
- **MS-DIAL** (Peak picking and feature detection to prepare experimental feature matrix for LipidMatch input)
- **Compound Discoverer** (Peak picking and feature detection to prepare experimental feature matrix for LipidMatch input)

## Evaluation signals

- User-generated library .csv file passes LipidMatch schema validation: all required columns (lipid name, molecular formula, adduct type, fragment m/z values) are present and formatted correctly.
- Integrated workflow produces lipid identifications for both built-in and user-generated library entries without duplication or conflicts.
- Experimental fragment m/z values match simulated library m/z values within expected mass accuracy tolerance (as validated in original LipidMatch publications on Q-Exactive and Q-TOF instruments).
- Built-in library matches remain unchanged after user library integration, confirming non-destructive combination of results.
- Novel lipids from user-generated library are correctly annotated in the final output with appropriate confidence metrics, while lipids not in either library remain unidentified.

## Limitations

- LipidMatch does not currently support Waters instrument files; data must be converted or acquired on Q-Exactive orbitrap, Agilent, Bruker, or SCIEX Q-TOF platforms.
- User-generated libraries must be in .csv format and conform strictly to LipidMatch schema specifications; deviations prevent integration.
- Library quality depends on accuracy of in-silico fragment m/z value predictions; incorrect fragmentation rules will produce false identifications.
- Integration mechanism is documented as 'facile' but specific technical details on format specifications and integration API are not detailed in the README.
- LipidMatch is modular and allows combination with various peak-picking tools, but compatibility with all downstream lipidomics software workflows is not guaranteed.

## Evidence

- [other] LipidMatch supports integration of user-generated libraries in .csv format as a documented extension mechanism for specialized lipidomics applications.: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [other] User libraries must follow LipidMatch schema specifications including lipid names, molecular formulas, adduct types, and in-silico fragment m/z values.: "Create a user-generated lipid library in .csv format following LipidMatch schema specifications (lipid names, molecular formulas, adduct types, and in-silico fragment m/z values)"
- [readme] LipidMatch performs lipid identification by matching experimental fragment m/z values with simulated library m/z values.: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [readme] LipidMatch has been validated using Q-Exactive orbitrap and Agilent, Bruker, SCIEX Q-TOF platforms with multiple MS acquisition approaches.: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] LipidMatch does not support Waters instrument files, limiting platform compatibility.: "The software does not currently support Waters files"
- [readme] LipidMatch integrates with multiple peak-picking tools to create modular workflows.: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
