---
name: lipid-library-annotation-from-mz
description: Use when you have experimental peaklist data (CSV or mzML-derived tables) from UHPLC-HRMS/MS instruments (Q-Exactive, Agilent/Bruker/SCIEX Q-TOF) with fragment m/z values and want to annotate them to known lipid identities.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
  - Agilent Q-TOF UHPLC-HRMS/MS
  - Bruker Q-TOF UHPLC-HRMS/MS
  - SCIEX Q-TOF UHPLC-HRMS/MS
  techniques:
  - LC-MS
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

# lipid-library-annotation-from-mz

## Summary

Match experimental fragment m/z values from high-resolution tandem MS data against in-silico fragmentation libraries to identify lipid species. This skill applies LipidMatch's rule-based matching algorithm to annotate lipids across >500,000 species spanning >60 lipid classes using mass tolerance thresholds.

## When to use

You have experimental peaklist data (CSV or mzML-derived tables) from UHPLC-HRMS/MS instruments (Q-Exactive, Agilent/Bruker/SCIEX Q-TOF) with fragment m/z values and want to annotate them to known lipid identities. Apply this skill after peak-picking (via MZmine, XCMS, MS-DIAL, or Compound Discoverer) when you need comprehensive lipid class assignments with match quality metrics.

## When NOT to use

- Input is from Waters instruments (software does not currently support Waters files)
- You have only precursor m/z data without fragment ion information (LipidMatch requires fragment-level m/z matching)
- Your lipid species of interest are not represented in the 500,000-species library and you do not have a user-generated library available

## Inputs

- Experimental peaklist file (CSV or mzML-derived table format) containing fragment m/z values from UHPLC-HRMS/MS data
- LipidMatch in-silico fragmentation library CSV files
- Mass tolerance threshold (instrument-dependent, e.g., 5 ppm for Q-Exactive)
- Peak-picked intensity/abundance data (optional, for match quality filtering)

## Outputs

- Lipid annotation table with columns: lipid name, lipid class, matched m/z, match quality metrics
- Candidate lipid matches ranked by fragment ion match count and mass accuracy
- Structured identifications compatible with downstream lipidomics analysis and visualization

## How to apply

Load your experimental fragment m/z peaklist and the LipidMatch in-silico fragmentation library CSV files covering the 500,000+ lipid species across 60+ lipid types. Apply the LipidMatch m/z matching algorithm by comparing each experimental m/z against library fragments using mass tolerance thresholds appropriate to your instrument's resolution (e.g., 5 ppm for Q-Exactive orbitrap, tighter for higher-resolution data). The algorithm ranks candidate lipid matches based on the number of fragment ions matched and their mass accuracy. Output matched identifications as a structured table with lipid name, class, m/z, and match quality metrics. Use the modularity of LipidMatch to integrate results with other lipidomics software or user-generated libraries for specialized lipid classes.

## Related tools

- **LipidMatch** (Core matching engine; performs m/z-based fragment ion annotation against in-silico fragmentation libraries) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and peaklist generation upstream of LipidMatch)
- **XCMS** (Peak picking and peaklist generation upstream of LipidMatch)
- **MS-DIAL** (Peak picking and peaklist generation upstream of LipidMatch)
- **Compound Discoverer** (Peak picking and peaklist generation upstream of LipidMatch)
- **Q-Exactive orbitrap** (UHPLC-HRMS/MS instrument; validated platform for LipidMatch annotation)
- **Agilent Q-TOF UHPLC-HRMS/MS** (UHPLC-HRMS/MS instrument; validated platform for LipidMatch annotation)
- **Bruker Q-TOF UHPLC-HRMS/MS** (UHPLC-HRMS/MS instrument; validated platform for LipidMatch annotation)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (UHPLC-HRMS/MS instrument; validated platform for LipidMatch annotation)

## Evaluation signals

- Output table contains non-empty lipid name and class columns for matched peaks, with one row per unique lipid annotation
- Match quality metrics are present and reasonable (e.g., number of matched fragments >0, mass error within defined tolerance)
- No lipid identifications are assigned to experimental m/z values with zero matching library fragments
- Matched lipid annotations are consistent with lipid class structure rules (e.g., fragmentation patterns match known lipid class behavior)
- Mass error distribution of matched fragments is centered near zero and does not exceed the specified m/z tolerance threshold

## Limitations

- Software does not currently support Waters file formats
- Annotation coverage is limited to the 500,000+ lipid species in the library; novel or rare lipids outside this set cannot be identified without user-generated library extension
- Match quality depends critically on appropriate mass tolerance threshold selection; mismatched instrument resolution or calibration will degrade accuracy
- Fragment ion matching alone may not distinguish between lipid isomers with identical fragmentation patterns; retention time or additional orthogonal data may be needed for disambiguation

## Evidence

- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries of over 500,000 lipid species across"
- [other] Compare each experimental m/z against library fragments using mass tolerance thresholds: "Apply LipidMatch m/z matching algorithm: compare each experimental m/z against library fragments using mass tolerance thresholds to identify candidate lipid matches"
- [other] Load experimental fragment m/z values from peaklist file and load LipidMatch library CSV files: "Load experimental fragment m/z values from a peaklist file (Q-Exactive or Q-TOF format, e.g., CSV or mzML-derived table). 2. Load LipidMatch in-silico fragmentation library CSV files covering the"
- [readme] Tested and validated using Q-Exactive orbitrap and Agilent, Bruker, SCIEX Q-TOF UHPLC-HRMS/MS: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] LipidMatch can be used with various peak picking software: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] Software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] LipidMatch allows integration of user-generated libraries for unique applications: "LipidMatch allows for facile integration of user generated libraries for unique applications"
