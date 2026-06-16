---
name: lipid-identification-scoring
description: Use when after peak picking has generated a peaklist of experimental fragment m/z values (from Q-Exactive orbitrap, Agilent/Bruker/SCIEX Q-TOF UHPLC-HRMS/MS, or direct infusion/imaging experiments) and you need to compare those fragments against the LipidMatch in-silico fragmentation library.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3520
  tools:
  - Q-Exactive orbitrap
  - LipidMatch
  - MZmine
  - XCMS
  - MS-DIAL
  - Compound Discoverer
derived_from:
- doi: 10.1186/s12859-017-1744-3
  title: lipidmatch
evidence_spans:
- tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidmatch
    doi: 10.1186/s12859-017-1744-3
    title: lipidmatch
  dedup_kept_from: coll_lipidmatch
schema_version: 0.2.0
---

# lipid-identification-scoring

## Summary

Score and rank candidate lipid matches by comparing experimental fragment m/z values against in-silico fragmentation library values using mass tolerance thresholds and match quality metrics. This skill filters and prioritizes lipid identifications from high-resolution tandem mass spectrometry data to assign confidence to putative lipid assignments.

## When to use

Apply this skill after peak picking has generated a peaklist of experimental fragment m/z values (from Q-Exactive orbitrap, Agilent/Bruker/SCIEX Q-TOF UHPLC-HRMS/MS, or direct infusion/imaging experiments) and you need to compare those fragments against the LipidMatch in-silico fragmentation library (500,000+ lipid species across 60+ lipid types) to rank candidate lipid identifications by match quality and filter for high-confidence assignments.

## When NOT to use

- Input peaklist is from Waters UHPLC-HRMS/MS instruments — LipidMatch does not currently support Waters files
- Experimental data has not undergone peak picking or m/z extraction — apply peak picking software (MZmine, XCMS, MS-DIAL, Compound Discoverer) first
- You are working with low-resolution MS data (e.g., unit mass accuracy) where mass tolerance windows would encompass too many library fragments to score meaningfully

## Inputs

- experimental fragment m/z peaklist (CSV or mzML-derived table)
- LipidMatch in-silico fragmentation library CSV files (covering 500,000+ lipid species across 60+ lipid types)
- mass tolerance threshold parameter (instrument-specific, e.g., ppm or Da)

## Outputs

- ranked candidate lipid identifications table (lipid name, class, m/z, match quality metrics)
- matched fragment annotations (experimental m/z paired with library m/z and assignment confidence)

## How to apply

Load the experimental fragment m/z values from a peaklist file (CSV or mzML-derived table format compatible with MZmine, XCMS, MS-DIAL, or Compound Discoverer output). Load the corresponding LipidMatch in-silico fragmentation library CSV files for the lipid classes of interest. Apply the LipidMatch m/z matching algorithm: for each experimental m/z, compare it against library fragment m/z values using a mass tolerance threshold (typically instrument-dependent; e.g., orbitrap vs. Q-TOF tolerance specifications) to identify candidate lipid matches. Score each match using quality metrics that quantify agreement between experimental and simulated fragments (e.g., number of matched fragments, m/z error distribution, fragment abundance patterns). Rank candidates by match quality and output a structured table containing lipid name, lipid class, m/z, and match quality metrics for downstream validation or reporting.

## Related tools

- **LipidMatch** (primary m/z matching engine and in-silico fragmentation library for scoring experimental fragments against simulated lipid fragments) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (peak picking software to generate experimental fragment m/z peaklists compatible with LipidMatch input)
- **XCMS** (peak picking software to generate experimental fragment m/z peaklists compatible with LipidMatch input)
- **MS-DIAL** (peak picking software to generate experimental fragment m/z peaklists compatible with LipidMatch input)
- **Compound Discoverer** (peak picking software to generate experimental fragment m/z peaklists compatible with LipidMatch input)

## Evaluation signals

- Output table contains no null or malformed entries in lipid name, class, m/z, or match quality metric columns
- Match quality metrics (e.g., number of matched fragments, m/z error in ppm/Da) fall within expected ranges for the mass spectrometer used (Q-Exactive orbitrap tolerance vs. Q-TOF tolerance)
- Candidate lipids are ranked consistently by match quality; top-ranked candidates have higher fragment match counts and lower m/z errors than lower-ranked candidates
- All matched experimental m/z values fall within the specified mass tolerance threshold of their assigned library m/z values
- Output lipid classes match the lipid types present in the loaded LipidMatch library CSV files (e.g., no TG matches if only PE/PC libraries were loaded)

## Limitations

- LipidMatch does not currently support Waters instrument files; users of Waters UHPLC-HRMS/MS systems must export or convert data to a supported format
- Match quality depends critically on the choice of mass tolerance threshold; too large a tolerance produces false positives, too strict produces false negatives; threshold must be tuned for the specific instrument's mass accuracy
- Library coverage is limited to the 500,000+ lipid species and 60+ lipid classes included in the pre-built LipidMatch libraries; novel or unannotated lipid species outside these classes will not be identified unless custom user-generated libraries are integrated
- Fragment abundance patterns and isotope distributions are not explicitly modeled; scoring relies on m/z matching alone, which may miss or misrank identifications when multiple lipids share similar fragment patterns

## Evidence

- [intro] how m/z matching algorithm works: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [readme] library scale and composition: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] instrument compatibility: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Waters file limitation: "The software does not currently support Waters files"
- [readme] workflow modularity and peak picking compatibility: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] user library integration capability: "LipidMatch allows for facile integration of user generated libraries for unique applications"
