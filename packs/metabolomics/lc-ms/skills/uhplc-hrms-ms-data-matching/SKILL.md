---
name: uhplc-hrms-ms-data-matching
description: Use when you have peak-picked UHPLC-HRMS/MS data (from Q-Exactive orbitrap, Agilent, Bruker, or SCIEX Q-TOF instruments) with both MS1 and MS/MS fragment spectra, and you need to assign lipid identities to detected features using in-silico fragmentation patterns.
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
  - Q-Exactive orbitrap
  - Agilent Q-TOF
  - Bruker Q-TOF
  - SCIEX Q-TOF
  techniques:
  - LC-MS
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

# uhplc-hrms-ms-data-matching

## Summary

Match experimental fragment m/z values from UHPLC-HRMS/MS data against in-silico fragmentation libraries to enable high-confidence lipid identification across diverse ionization and acquisition modes. This skill is essential when you need to annotate thousands of detected peaks in untargeted lipidomics workflows and have access to comprehensive lipid reference libraries.

## When to use

You have peak-picked UHPLC-HRMS/MS data (from Q-Exactive orbitrap, Agilent, Bruker, or SCIEX Q-TOF instruments) with both MS1 and MS/MS fragment spectra, and you need to assign lipid identities to detected features using in-silico fragmentation patterns. This is especially appropriate when analyzing targeted, data-dependent top-N (ddMS2-topN), or all-ion fragmentation (AIF) acquisition modes, or when extending beyond the built-in library to specialized lipid classes via user-generated libraries.

## When NOT to use

- Input is Waters instrument data — LipidMatch does not currently support Waters file formats
- You are working with direct MS1 data only (no MS/MS fragmentation spectra available) — the matching relies on fragment m/z patterns and cannot function on precursor ion data alone
- Raw, unprocessed instrument files have not yet been peak-picked — run peak picking first before matching

## Inputs

- Peak-picked feature table with m/z, retention time, and intensity (from MZmine, XCMS, MS-DIAL, or Compound Discoverer)
- MS/MS fragment m/z spectra for detected features
- Instrument metadata (instrument type: Q-Exactive, Agilent Q-TOF, Bruker Q-TOF, or SCIEX Q-TOF)
- Acquisition mode metadata (targeted, ddMS2-topN, or AIF)
- Optional: user-generated lipid library in .csv format with lipid names, molecular formulas, adduct types, and fragment m/z values

## Outputs

- Annotated feature table with assigned lipid identities and lipid class assignments
- Matching scores or confidence metrics linking experimental fragments to library entries
- Combined identification results if integrated with other lipidomics software outputs

## How to apply

First, obtain peak-picked feature tables and MS/MS spectra from your UHPLC-HRMS/MS raw data using one of the supported peak picking tools (MZmine, XCMS, MS-DIAL, or Compound Discoverer). Prepare your input in the format LipidMatch expects, containing detected m/z values, retention times, and associated MS/MS fragment m/z values. LipidMatch then matches experimental fragment m/z patterns against its in-silico library of over 500,000 lipid species across 60+ lipid types by comparing observed fragments to simulated fragmentation patterns. If your application requires lipid classes not well-represented in the built-in library, create a user-generated lipid library in .csv format following LipidMatch's schema specifications (lipid names, molecular formulas, adduct types, and simulated fragment m/z values), validate the .csv structure against format requirements, and integrate it into the workflow using LipidMatch's facile integration mechanism. Finally, combine results with other lipidomics software outputs if desired. Success is indicated by confident lipid assignments for features across your sample set with traceable matching scores between experimental and simulated fragments.

## Related tools

- **LipidMatch** (Primary in-silico fragmentation matching engine; performs experimental–library fragment m/z comparison and lipid assignment) — https://github.com/GarrettLab-UF/LipidMatch
- **MZmine** (Peak picking and feature detection upstream of LipidMatch matching)
- **XCMS** (Peak picking and feature detection upstream of LipidMatch matching)
- **MS-DIAL** (Peak picking and feature detection upstream of LipidMatch matching)
- **Compound Discoverer** (Peak picking and feature detection upstream of LipidMatch matching)
- **Q-Exactive orbitrap** (UHPLC-HRMS/MS instrument on which LipidMatch has been validated)
- **Agilent Q-TOF** (UHPLC-HRMS/MS instrument on which LipidMatch has been validated)
- **Bruker Q-TOF** (UHPLC-HRMS/MS instrument on which LipidMatch has been validated)
- **SCIEX Q-TOF** (UHPLC-HRMS/MS instrument on which LipidMatch has been validated)

## Evaluation signals

- Experimental fragment m/z values align with simulated library fragments within expected mass accuracy (instrument-dependent, typically <5 ppm for Orbitrap, <20 ppm for Q-TOF)
- Assigned lipid identities are consistent with known biochemistry for the sample type (e.g., expected lipid classes and chain lengths present in mammalian cells, plant tissues, etc.)
- User-generated .csv libraries pass schema validation (correct column headers: lipid names, molecular formulas, adduct types, fragment m/z values) before integration
- Feature coverage improves when user libraries are added, indicating specialized lipids are now being detected
- Reproducibility across replicates: same lipid identities and matching scores assigned to equivalent features in replicate injections

## Limitations

- Software does not currently support Waters instrument files, limiting applicability to Waters-based UHPLC-HRMS/MS workflows
- Library is comprehensive (500,000+ lipid species across 60+ lipid types) but may not cover all lipids in highly specialized or xenobiotic applications — user-generated library creation required for these cases
- Matching performance depends on MS/MS fragmentation quality and consistency; poor fragmentation or instrument drift can reduce confidence of assignments
- Integration with user-generated libraries requires manual validation of .csv format and fragmentation patterns; incorrectly formatted libraries will not integrate or will produce erroneous matches

## Evidence

- [readme] Fragment m/z matching principle: "LipidMatch identifications are obtained by matching experimental fragment m/z values with simulated library m/z values"
- [readme] Instrument validation scope: "LipidMatch has been tested and validated using Q-Exactive orbitrap UHPLC-HRMS/MS data obtained from multiple sample types using targeted, data-dependent top-N (ddMS2-topN), and all ion fragmentation"
- [readme] Library composition: "in-silico fragmentation libraries of over 500,000 lipid species across over 60 lipid types"
- [readme] User library integration capability: "LipidMatch allows for facile integration of user generated libraries for unique applications"
- [readme] Waters file limitation: "The software does not currently support Waters files"
- [readme] Peak picking tool compatibility: "LipidMatch can be used with various peak picking software (for example MZmine, XCMS, MS-DIAL, and Compound Discoverer)"
- [other] User library format and workflow: "Create a user-generated lipid library in .csv format following LipidMatch schema specifications (lipid names, molecular formulas, adduct types, and in-silico fragment m/z values). 2. Validate the"
