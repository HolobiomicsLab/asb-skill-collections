---
name: fragment-ion-library-matching
description: Use when you have peak-picked experimental MS/MS data (m/z, retention time, intensity) from UHPLC-HRMS/MS instruments (Orbitrap or Q-TOF from Agilent, Bruker, SCIEX, or similar vendors) and need to annotate detected features with specific lipid identifications using in-silico fragmentation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Q-Exactive
  techniques:
  - tandem-MS
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

# fragment-ion-library-matching

## Summary

Fragment-ion library matching is a mass spectrometry annotation workflow that identifies lipid species by matching experimental fragment m/z values against simulated library m/z values derived from in-silico fragmentation libraries. This skill is essential for high-throughput lipid annotation in untargeted lipidomics when experimental MS/MS data must be assigned to specific lipid identities.

## When to use

Apply this skill when you have peak-picked experimental MS/MS data (m/z, retention time, intensity) from UHPLC-HRMS/MS instruments (Orbitrap or Q-TOF from Agilent, Bruker, SCIEX, or similar vendors) and need to annotate detected features with specific lipid identifications using in-silico fragmentation reference libraries covering multiple lipid classes.

## When NOT to use

- Input data is already a pre-annotated feature table with lipid identities assigned
- Vendor software (e.g., Waters) is used that is not currently supported by the annotation tool
- Experimental data lacks MS/MS fragmentation information (MS1-only workflows)

## Inputs

- Peak list (m/z, retention time, intensity) from peak-picking software (MZmine, XCMS, MS-DIAL, Compound Discoverer output)
- In-silico fragment ion library with theoretical m/z values for lipid species and their fragments
- MS/MS spectral data in vendor format or converted format compatible with annotation software

## Outputs

- Annotated feature table with assigned lipid identifications
- Lipid identifications ranked by matching score and confidence level
- Fragment matching details (matched fragment m/z values, intensity correlations)

## How to apply

Load the experimental peak list (m/z, retention time, intensity) from peak-picking software output (MZmine, XCMS, MS-DIAL, or Compound Discoverer). Retrieve candidate lipid species from a comprehensive in-silico fragmentation library (e.g., LipidMatch's 500,000+ lipid species across 60+ lipid types) by matching parent ion m/z within a specified mass tolerance threshold (typically 5 ppm or less for high-resolution instruments). For each candidate, compare experimental fragment m/z values against simulated library fragment m/z values using the same mass tolerance. Calculate a matching score based on the number of matched fragments, intensity correlation, or similar metric. Rank candidates by matching score and assign a lipid identification with confidence level. The workflow is modular and can integrate user-generated libraries for unique applications and combine results from complementary lipidomics software.

## Related tools

- **LipidMatch** (Primary tool for performing fragment m/z matching and lipid identification using in-silico fragmentation libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature detection software that produces experimental peak lists consumed by fragment-ion matching)
- **XCMS** (Peak picking and feature detection software that produces experimental peak lists consumed by fragment-ion matching)
- **MS-DIAL** (Peak picking and feature detection software that produces experimental peak lists consumed by fragment-ion matching)
- **Compound Discoverer** (Peak picking and feature detection software that produces experimental peak lists consumed by fragment-ion matching)
- **Q-Exactive** (Orbitrap UHPLC-HRMS/MS instrument used to generate and validate fragment-ion matching on experimental data)

## Evaluation signals

- Feature table contains valid lipid identifications with clear naming conventions (e.g., lipid class and chain composition)
- Matching scores or confidence metrics are calculated and reported for each identification
- Output includes matched fragment m/z values that fall within the specified mass tolerance of library values
- Intensity correlation between experimental and simulated fragment patterns is above a reasonable threshold (e.g., R² > 0.5 or similar metric)
- Identifications can be cross-validated by examining fragment ion patterns manually or comparing against orthogonal annotation methods

## Limitations

- LipidMatch does not currently support Waters instrument file formats
- Matching accuracy depends on mass accuracy of the MS instrument and correctness of the in-silico fragmentation library
- Complex lipid mixtures or isobaric lipid species may produce ambiguous or multiple equally-ranked identifications
- User-generated or non-standard lipid libraries require manual validation and integration

## Evidence

- [readme] Core matching mechanism: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [intro] Library scale and coverage: "in-silico fragmentation libraries containing over 500,000 lipid species across over 60 lipid types"
- [readme] Instrument compatibility and validation scope: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Peak picking software integration: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] Workflow modularity and customization: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [readme] Vendor file format limitations: "The software does not currently support Waters files"
- [intro] Experimental input specification: "Load experimental peak list (m/z, retention time, intensity) from peak-picking software output (MZmine, XCMS, MS-DIAL, or Compound Discoverer)"
