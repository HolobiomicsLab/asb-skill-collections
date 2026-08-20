---
name: mass-accuracy-tolerance-calibration
description: Use when you have experimental fragment m/z values from HRMS/MS instruments
  (Q-Exactive orbitrap, Q-TOF) in CSV or mzML-derived peaklist format, and need to
  match them against a library of 500,000+ in-silico fragmented lipid species.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Q-Exactive orbitrap UHPLC-HRMS/MS
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  - R
  - MetIDfyR
  - MSnbase
  - Rdisop
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
- doi: 10.1021/acs.analchem.0c02281
  title: ''
evidence_spans:
- tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data
- open-source, cross-platform and versatile R script
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  - build: coll_metidfyr_cq
    doi: 10.1021/acs.analchem.0c02281
    title: MetIDfyR
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-017-1744-3
  all_source_dois:
  - 10.1186/s12859-017-1744-3
  - 10.1021/acs.analchem.0c02281
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-accuracy-tolerance-calibration

## Summary

Calibrate and apply mass tolerance thresholds when matching experimental fragment m/z values to in-silico library m/z values in high-resolution tandem mass spectrometry data. This skill ensures that lipid identifications are sensitive to true matches while rejecting spurious hits caused by instrument mass error.

## When to use

You have experimental fragment m/z values from HRMS/MS instruments (Q-Exactive orbitrap, Q-TOF) in CSV or mzML-derived peaklist format, and need to match them against a library of 500,000+ in-silico fragmented lipid species. Mass tolerance calibration is critical when working across different instrument platforms (Thermo, Agilent, Bruker, SCIEX) or when comparing multiple sample types (targeted, ddMS2-topN, AIF) to ensure consistent match quality and avoid false-positive lipid identifications.

## When NOT to use

- Input data is from Waters HRMS/MS instruments — LipidMatch does not currently support Waters files.
- You are comparing pre-annotated lipid identifications rather than performing de novo matching against a library.
- Fragment m/z values have already been matched and filtered by upstream software (e.g., Compound Discoverer already performed m/z matching) — reapplying this skill may introduce redundant or conflicting tolerances.

## Inputs

- Experimental fragment m/z peaklist (CSV, mzML-derived table, or peak picker output from MZmine/XCMS/MS-DIAL/Compound Discoverer)
- LipidMatch in-silico fragmentation library CSV files (500,000+ lipid species across 60+ lipid types)
- Instrument type metadata (e.g., Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, SCIEX Q-TOF)

## Outputs

- Matched lipid identifications table (columns: lipid name, lipid class, matched m/z, match count, match quality metrics)
- Calibrated mass tolerance value(s) applied (ppm or Da)
- Unmatched or low-confidence fragments (optional)

## How to apply

Load experimental m/z values (from peak picking output such as MZmine, XCMS, MS-DIAL, or Compound Discoverer) and the LipidMatch in-silico fragmentation library covering 500,000+ lipid species. Apply mass tolerance thresholds to compare each experimental m/z against library fragments; the tolerance window determines which candidates are considered matches. The tolerance should be tuned based on the instrument's typical mass accuracy (e.g., ppm error range for orbitrap vs. Q-TOF). For each experimental fragment, count matches within the tolerance window and rank or filter candidate lipids by match quality metrics (e.g., number of matched fragments, mass accuracy of top match). Output a structured table with matched lipid names, classes, m/z values, and match quality scores, discarding or flagging low-confidence matches that fall outside the calibrated tolerance.

## Related tools

- **LipidMatch** (Applies m/z matching algorithm with mass tolerance thresholds to compare experimental fragments to in-silico library; outputs matched lipid identifications with quality metrics) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking software to generate experimental m/z peaklists suitable as input to LipidMatch matching)
- **XCMS** (Peak picking software to generate experimental m/z peaklists suitable as input to LipidMatch matching)
- **MS-DIAL** (Peak picking software to generate experimental m/z peaklists suitable as input to LipidMatch matching)
- **Compound Discoverer** (Peak picking software to generate experimental m/z peaklists suitable as input to LipidMatch matching)
- **Q-Exactive orbitrap UHPLC-HRMS/MS** (Source instrument for experimental m/z data; validated platform for LipidMatch matching)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Source instrument for experimental m/z data; validated platform for LipidMatch matching)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Source instrument for experimental m/z data; validated platform for LipidMatch matching)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (Source instrument for experimental m/z data; validated platform for LipidMatch matching)

## Evaluation signals

- Matched lipid identifications are returned as a structured table with populated lipid name, class, m/z, and match quality columns (no missing or null entries in key fields).
- All matched fragments have m/z differences within the applied tolerance threshold; verify by calculating |experimental_m/z − library_m/z| for each match and confirming it falls within the specified tolerance window (e.g., ±5 ppm for orbitrap).
- Match quality metrics (e.g., number of matched fragments per lipid candidate) are consistent across the output; lipids with higher fragment match counts should rank higher in the results.
- Repeated runs with the same input data and tolerance settings produce identical outputs (reproducibility check).
- The number of matched lipids and false-positive rate are reasonable relative to the sample type and instrument (e.g., more matches for AIF mode than targeted mode; lower false-positive rate for validated instrument platforms like Q-Exactive than for less-tested instruments).

## Limitations

- LipidMatch does not currently support Waters file formats, limiting applicability to non-Waters HRMS/MS workflows.
- Mass tolerance thresholds must be manually tuned or calibrated per instrument type; no automatic calibration procedure is provided in the README.
- The in-silico library is fixed at publication (500,000 lipid species across 60+ types); user-generated libraries can be integrated, but new lipid species or classes beyond the library scope cannot be identified.
- Match quality depends on the accuracy and completeness of peak picking upstream (MZmine, XCMS, etc.); poor peak picking will reduce the number of detectable matches even with correct tolerance calibration.

## Evidence

- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [other] Apply mass tolerance thresholds to compare experimental m/z against library fragments: "Apply LipidMatch m/z matching algorithm: compare each experimental m/z against library fragments using mass tolerance thresholds to identify candidate lipid matches."
- [readme] Validated using Q-Exactive orbitrap and Q-TOF instruments across multiple acquisition modes: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] LipidMatch is modular and integrates with peak picking software and user libraries: "LipidMatch allows for facile integration of user generated libraries for unique applications. LipidMatch is modular, allowing it to fit in various workflows you may have in your lab"
