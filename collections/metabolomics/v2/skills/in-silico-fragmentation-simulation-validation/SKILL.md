---
name: in-silico-fragmentation-simulation-validation
description: Use when you have experimental peak lists (m/z, retention time, intensity) from UHPLC-HRMS/MS or direct infusion MS/MS data and need to assign lipid identities with confidence scores. Use it when your instrument produces high-resolution tandem mass spectra (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Q-Exactive orbitrap UHPLC-HRMS/MS
  - Agilent, Bruker, SCIEX Q-TOF
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
---

# in-silico-fragmentation-simulation-validation

## Summary

Validate lipid identifications by matching experimental fragment m/z values against simulated library m/z values derived from in-silico fragmentation of known lipid species. This skill enables systematic, high-throughput annotation of untargeted lipidomics data across diverse instrument platforms and fragmentation modes.

## When to use

Apply this skill when you have experimental peak lists (m/z, retention time, intensity) from UHPLC-HRMS/MS or direct infusion MS/MS data and need to assign lipid identities with confidence scores. Use it when your instrument produces high-resolution tandem mass spectra (e.g., Q-Exactive orbitrap, Q-TOF) and you want to leverage comprehensive in-silico fragmentation libraries (>500,000 lipid species across 60+ lipid types) rather than manual spectral matching or targeted methods alone.

## When NOT to use

- Input data is from Waters instruments — LipidMatch does not currently support Waters files.
- Peak list is already fully annotated with high-confidence identifications and no re-annotation is needed.
- MS/MS data quality is very poor (low fragment intensity or sparse fragmentation patterns) — matching will be unreliable.

## Inputs

- Experimental peak list (m/z, retention time, intensity) from peak-picking software output (MZmine, XCMS, MS-DIAL, or Compound Discoverer formats)
- Tandem mass spectrometry data (MS/MS or MS2 spectra with fragment m/z and intensity values)
- In-silico fragmentation library (LipidMatch library in .csv format containing theoretical fragment m/z values for lipid species)

## Outputs

- Annotated feature table with assigned lipid identifications
- Lipid identifications ranked by matching score
- Confidence levels for each lipid assignment
- Matched fragment ion lists per identification

## How to apply

Load experimental peak lists from peak-picking software (MZmine, XCMS, MS-DIAL, or Compound Discoverer) and the LipidMatch in-silico fragmentation library. For each experimental peak, retrieve candidate lipid species from the library using parent ion m/z with a specified mass tolerance window. Match experimental fragment m/z values against simulated library fragment m/z values for each candidate using a mass tolerance threshold (typically < 5 ppm for high-resolution data). Calculate a matching score based on the number of matched fragments and/or intensity correlation. Rank candidates by score and assign the highest-scoring lipid as the identification with a confidence level reflecting the scoring metric. Output an annotated feature table with lipid assignments. The modular design allows integration with other lipidomics software and user-generated libraries for unique applications.

## Related tools

- **LipidMatch** (Core software that performs fragment m/z matching and lipid identification using in-silico fragmentation libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak-picking and feature detection software; preprocesses raw MS data into peak lists compatible with LipidMatch input)
- **XCMS** (Peak-picking and feature detection software; preprocesses raw MS data into peak lists compatible with LipidMatch input)
- **MS-DIAL** (Peak-picking and feature detection software; preprocesses raw MS data into peak lists compatible with LipidMatch input)
- **Compound Discoverer** (Peak-picking and feature detection software; preprocesses raw MS data into peak lists compatible with LipidMatch input)
- **Q-Exactive orbitrap UHPLC-HRMS/MS** (High-resolution tandem mass spectrometry instrument used to generate experimental MS/MS data for validation)
- **Agilent, Bruker, SCIEX Q-TOF** (Alternative high-resolution mass spectrometry platforms validated with LipidMatch)

## Evaluation signals

- Matching score distribution — candidate lipids should show a clear peak in the score distribution with top candidate(s) separated from lower-scoring hits by a distinct margin.
- Fragment coverage — the top-ranked identification should explain a substantial fraction (typically >50%) of intense experimental fragments within the specified mass tolerance (e.g., 5 ppm).
- Cross-platform consistency — lipid identifications should be reproducible when data from different instrument types (Q-Exactive, Q-TOF, etc.) are processed with the same library and parameters.
- Library containment — verify that assigned lipid identifications are present in the loaded in-silico library (500,000+ species across 60+ lipid classes).
- Isotope and adduct verification — check that the parent ion m/z matches the theoretical m/z of the assigned lipid ± appropriate adduct mass (e.g., [M+H]+ or [M+NH4]+) within the mass tolerance window.

## Limitations

- Waters instrument files are not currently supported; users must export data to compatible formats (mzML, mzXML, or NetCDF) before processing.
- Matching performance depends on fragmentation quality; poor-quality MS/MS data (sparse fragments, low intensity) will reduce the reliability of identifications.
- The library covers 500,000+ lipid species across 60+ lipid types, but less common lipid classes or unusual species may not be represented; user-generated libraries can be integrated for unique applications.
- High-resolution mass spectrometry instruments are required for accurate m/z matching; low-resolution data may exceed the mass tolerance windows and produce false negatives.
- Isomeric lipids (e.g., positional isomers differing only in acyl chain position) may produce nearly identical fragment spectra; the matching score alone may not resolve them.

## Evidence

- [readme] LipidMatch core method: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [readme] Instrument validation: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Application scope: "LipidMatch has also been applied for the annotation of direct infusion and imaging experiments"
- [readme] Workflow integration: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer), and combine results from other lipidomics software"
- [readme] Waters limitation: "The software does not currently support Waters files"
- [readme] Library customization: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [other] Workflow steps from task card: "Match experimental fragment m/z values against simulated library fragment m/z values for each candidate lipid using mass tolerance threshold. Calculate matching score (number of matched fragments,"
