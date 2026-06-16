---
name: mass-spectrometry-fragment-matching
description: Use when you have experimental fragment m/z peaklists from Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, or SCIEX Q-TOF UHPLC-HRMS/MS instruments (in CSV or mzML-derived table formats) and need to assign lipid identities using untargeted or targeted tandem MS data.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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

# mass-spectrometry-fragment-matching

## Summary

Match experimental fragment m/z values against in-silico fragmentation libraries to identify lipids using tandem mass spectrometry data. This skill applies mass tolerance thresholds to compare high-resolution MS/MS spectra to comprehensive lipid databases containing >500,000 species across 60+ lipid classes.

## When to use

You have experimental fragment m/z peaklists from Q-Exactive orbitrap, Agilent Q-TOF, Bruker Q-TOF, or SCIEX Q-TOF UHPLC-HRMS/MS instruments (in CSV or mzML-derived table formats) and need to assign lipid identities using untargeted or targeted tandem MS data. Apply this skill when you have already performed peak picking (via MZmine, XCMS, MS-DIAL, or Compound Discoverer) and want rule-based lipid annotation without manual spectral curation.

## When NOT to use

- Waters UHPLC-HRMS/MS data: LipidMatch does not currently support Waters file formats.
- Already-annotated feature table: If lipids are already identified by another method, use this skill only for validation or re-annotation.
- Non-lipid small-molecule identification: LipidMatch libraries are optimized for lipids; application to general metabolites may produce false assignments.

## Inputs

- Experimental fragment m/z peaklist (CSV, mzML-derived table, or Q-Exactive / Q-TOF native format)
- Precursor m/z and retention time metadata (optional but recommended)
- LipidMatch in-silico fragmentation library CSV files (500,000+ lipid species across 60+ lipid types)

## Outputs

- Matched lipid identifications table (lipid name, class, matched m/z values, match quality metrics)
- Candidate lipid list ranked by match score

## How to apply

Load your experimental fragment m/z values and associated retention time / precursor m/z information from the peak-picking output. Load the LipidMatch in-silico library CSV files covering the desired lipid classes (60+ types available). Apply the LipidMatch m/z matching algorithm by comparing each experimental fragment m/z against library fragments using a mass tolerance threshold (typically 5–10 ppm for orbitrap, instrument-specific for Q-TOF). Rank candidate matches by the number of matching fragments and their match quality metrics (intensity correlation, fragment count agreement). Output a structured results table containing matched lipid names, lipid class, theoretical m/z, experimental m/z, and match quality scores. Validate results by confirming that high-scoring matches have isotope patterns and fragmentation logic consistent with lipid chemistry.

## Related tools

- **LipidMatch** (Core m/z matching algorithm and in-silico fragmentation library lookup engine) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature extraction upstream of LipidMatch)
- **XCMS** (Peak picking and feature extraction upstream of LipidMatch)
- **MS-DIAL** (Peak picking and feature extraction upstream of LipidMatch)
- **Compound Discoverer** (Peak picking and feature extraction upstream of LipidMatch)
- **Q-Exactive orbitrap** (Validated MS instrument for data collection)
- **Agilent Q-TOF UHPLC-HRMS/MS** (Validated MS instrument for data collection)
- **Bruker Q-TOF UHPLC-HRMS/MS** (Validated MS instrument for data collection)
- **SCIEX Q-TOF UHPLC-HRMS/MS** (Validated MS instrument for data collection)

## Evaluation signals

- Match count: ≥3 matching fragments per candidate lipid is typical for high-confidence identifications; inspect the number of matched vs. predicted fragments.
- Mass accuracy: All matched m/z values fall within the specified tolerance window (e.g., ±5 ppm for orbitrap); verify no systematic m/z drift across the feature list.
- Lipid class consistency: Matched lipids belong to chemically plausible classes for the sample type (e.g., phospholipids in plasma, triacylglycerols in adipose tissue).
- Retention time and precursor m/z plausibility: Matched lipids have precursor m/z and retention time in expected ranges for the separation method.
- Fragmentation pattern agreement: Dominant matched fragments align with known lipid fragmentation rules (e.g., loss of headgroup, acyl chain fragments for glycerolipids).

## Limitations

- Waters file formats are not currently supported; conversion or pre-processing may be required.
- LipidMatch relies on in-silico fragmentation rules and does not account for instrument-specific fragmentation artifacts or non-standard modifications.
- Match quality depends on the completeness of the in-silico library; lipids outside the 500,000-species library will not be identified.
- Mass tolerance thresholds must be tuned per instrument and calibration; improper thresholds reduce specificity or sensitivity.
- No changelog is available, limiting reproducibility and understanding of software updates.

## Evidence

- [readme] LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values using in-silico fragmentation libraries"
- [readme] in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types making it one of the most comprehensive open-source software"
- [readme] tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation (AIF) approaches: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] The software does not currently support Waters files: "The software does not currently support Waters files"
- [readme] LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer): "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [readme] LipidMatch allows for facile integration of user generated libraries for unique applications: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [other] compare each experimental m/z against library fragments using mass tolerance thresholds to identify candidate lipid matches: "Apply LipidMatch m/z matching algorithm: compare each experimental m/z against library fragments using mass tolerance thresholds to identify candidate lipid matches"
