---
name: lipid-mass-spectral-matching
description: Use when you have peak-picked LC-HRMS/MS or direct infusion MS/MS data (m/z, retention time, intensity) from Q-Exactive, Agilent, Bruker, or SCIEX instruments and need to annotate experimental fragment patterns to known lipid structures.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Q-Exactive (Orbitrap UHPLC-HRMS/MS)
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

# lipid-mass-spectral-matching

## Summary

Match experimental tandem MS fragment m/z values against simulated in-silico lipid fragmentation libraries to assign lipid identifications with confidence scores. This skill enables automated annotation of untargeted lipidomics data across >500,000 lipid species in >60 lipid classes.

## When to use

Apply this skill when you have peak-picked LC-HRMS/MS or direct infusion MS/MS data (m/z, retention time, intensity) from Q-Exactive, Agilent, Bruker, or SCIEX instruments and need to annotate experimental fragment patterns to known lipid structures. Use it when unbiased lipid coverage (not targeted assays) is the goal and you want to leverage comprehensive in-silico libraries rather than manual interpretation.

## When NOT to use

- Input data are from Waters instruments (currently unsupported file formats)
- Only low-resolution or nominal mass MS data are available (method requires high mass accuracy for m/z matching)
- Targeted single-MRM or SRM transitions are already available (use targeted quantitation instead)

## Inputs

- Peak-picked feature list with m/z, retention time, and intensity columns (CSV, mzXML, or native format from MZmine/XCMS/MS-DIAL/Compound Discoverer)
- Experimental MS/MS spectra with parent and fragment m/z values
- LipidMatch in-silico fragmentation library (CSV format, 500,000+ lipid species)

## Outputs

- Annotated feature table with assigned lipid identifications and matching scores
- Confidence levels for each lipid assignment
- Ranked list of candidate lipid identifications per feature

## How to apply

Ingest experimental peak lists from peak-picking software (MZmine, XCMS, MS-DIAL, Compound Discoverer) containing m/z and retention time. For each experimental parent ion, retrieve candidate lipid species from the LipidMatch library using parent m/z within a specified mass tolerance window. Match the experimental fragment m/z values against simulated library fragment m/z values for each candidate, applying a mass tolerance threshold (typically ppm-based). Calculate a matching score based on the number of matched fragments and optionally intensity correlation. Rank candidates by matching score, assign the top-ranked lipid identification, and output a confidence level or score metric alongside the annotated feature table.

## Related tools

- **LipidMatch** (Core matching engine; performs rule-based fragment matching against in-silico fragmentation library and assigns lipid identifications) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Upstream peak-picking and feature detection from raw HRMS data; outputs feature list for LipidMatch input)
- **XCMS** (Upstream peak-picking and feature detection from raw HRMS data; outputs feature list for LipidMatch input)
- **MS-DIAL** (Upstream peak-picking and feature detection from raw HRMS data; outputs feature list for LipidMatch input)
- **Compound Discoverer** (Upstream peak-picking and feature detection from raw HRMS data; outputs feature list for LipidMatch input)
- **Q-Exactive (Orbitrap UHPLC-HRMS/MS)** (Validated instrument platform for data acquisition; LipidMatch has been tested on targeted, ddMS2-topN, and AIF data from this platform)

## Evaluation signals

- Matched fragment count and intensity correlation are above predefined thresholds for accepted identifications
- Mass error (ppm difference) between experimental and library m/z values stays within specified tolerance window for all matched fragments
- Matching score ranks are stable and reproducible across repeated runs with the same input and parameter settings
- Annotated lipid identifications are consistent with known sample composition (e.g., biological or chemical standards)
- Feature annotation rate (number of peaks assigned identifications) is consistent with expected lipid diversity for sample type

## Limitations

- Does not currently support Waters file formats
- Matching accuracy depends on library comprehensiveness; lipids absent from the 500,000+ species library cannot be identified
- Mass tolerance thresholds must be calibrated per instrument platform and ionization method to balance sensitivity and false-positive rate
- Requires high mass accuracy (ppm-level) MS/MS data; nominal mass or low-resolution data will produce low match rates

## Evidence

- [readme] Fragment matching library approach: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [readme] Validated instrument platforms: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Upstream peak-picking software compatibility: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] Workflow integration and modularity: "LipidMatch is modular, allowing it to fit in various workflows you may have in your lab"
- [readme] Waters platform limitation: "The software does not currently support Waters files"
- [readme] User library integration: "LipidMatch allows for facile integration of user generated libraries for unique applications"
