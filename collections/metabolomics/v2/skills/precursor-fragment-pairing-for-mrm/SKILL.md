---
name: precursor-fragment-pairing-for-mrm
description: Use when when designing a targeted lipidomics experiment and you have lipid species definitions (including chain composition and adducts) but need to configure precursor–fragment transitions for MRM or PRM acquisition on a Thermo QExactive HF, Agilent QTOF, or compatible high-resolution or.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_0153
  - http://edamontology.org/topic_3375
  tools:
  - Skyline
  - LipidCreator
  - Thermo QExactive HF
  - Agilent QTOF
derived_from:
- doi: 10.1038/s41467-020-15960-z
  title: LipidCreator
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidcreator_cq
    doi: 10.1038/s41467-020-15960-z
    title: LipidCreator
  dedup_kept_from: coll_lipidcreator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-020-15960-z
  all_source_dois:
  - 10.1038/s41467-020-15960-z
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-fragment-pairing-for-mrm

## Summary

Generate precursor–fragment m/z pairs and transition metadata for multiple reaction monitoring (MRM) and parallel reaction monitoring (PRM) targeted experiments from lipid definitions. This skill automates the pairing of precursor ions with expected fragment ions and collision energy settings, producing Skyline-compatible target lists that configure targeted mass spectrometry workflows.

## When to use

When designing a targeted lipidomics experiment and you have lipid species definitions (including chain composition and adducts) but need to configure precursor–fragment transitions for MRM or PRM acquisition on a Thermo QExactive HF, Agilent QTOF, or compatible high-resolution or triple-quadrupole instrument. Use this skill before instrument method setup to ensure transitions are optimized and formatted for Skyline import.

## When NOT to use

- Lipid identities have already been confirmed by experiment and you have empirical fragmentation spectra — use a spectral library search or peak matching tool instead.
- Input is already a complete Skyline document or method file — no pairing step is needed.
- Instrument requires manufacturer-specific transition optimization that is not based on lipid chain structure — consult instrument vendor tools.

## Inputs

- Lipid definitions (species, acyl chain composition, adducts; CSV or text format)
- Lipid class (e.g., PC, PE, TG, SM) and ionization mode (positive/negative)
- Optional: collision energy parameters or energy prediction model

## Outputs

- Tab-delimited or CSV target list file with precursor m/z, fragment m/z, collision energy, polarity, and retention time window (compatible with Skyline import)
- Standalone fragment spectral library (.blib or .msp format) for Skyline integration
- Transition metadata table (precursor, fragment, CE, charge state)

## How to apply

Begin by parsing lipid definitions specifying lipid species, acyl chain composition, and ionization adducts (e.g., [M+H]+, [M+Na]+). Calculate the theoretical precursor m/z for each target lipid. Apply lipid-class-specific fragmentation rules and chain cleavage patterns to predict fragment m/z values (e.g., neutral loss of head group, fatty acid anions, or lyso-species). Assign collision energy values appropriate to the lipid class and mass range, or allow automated energy prediction based on precursor m/z. Assemble each precursor–fragment pair into a transition entry recording precursor m/z, fragment m/z, collision energy, ionization polarity, and retention time window. Export the complete transition set as a tab-delimited or CSV file with metadata columns required by Skyline (precursor m/z, fragment m/z, collision energy, polarity, retention time window), or as a standalone fragment library in .blib or .msp format for Skyline spectral library integration.

## Related tools

- **Skyline** (Import and deploy precursor–fragment transitions, configure acquisition parameters, and integrate fragment libraries into targeted experiment workflows) — https://skyline.ms/project/home/software/Skyline/begin.view
- **LipidCreator** (Standalone or command-line application that generates user-defined target lists and fragment libraries from lipid definitions, with support for collision energy calculation and Skyline-compatible export) — https://github.com/lifs-tools/lipidcreator
- **Thermo QExactive HF** (High-resolution mass spectrometry instrument platform validated for import and execution of LipidCreator-generated transitions in PRM workflows)
- **Agilent QTOF** (High-resolution mass spectrometry instrument platform validated for import and execution of LipidCreator-generated transitions)

## Evaluation signals

- All precursor m/z values fall within the calibrated instrument range and match theoretical calculations (within instrument mass accuracy tolerance, typically 1–5 ppm for QExactive HF or Agilent QTOF).
- Fragment m/z values conform to known lipid fragmentation rules for the specified lipid class (e.g., neutral loss of phosphocholine head group for PC lipids, m/z = 184).
- Collision energy values assigned are physiologically reasonable for the precursor m/z and lipid class (typically 15–50 eV for high-resolution instruments).
- Exported transition list is parseable by Skyline and all required metadata columns (precursor m/z, fragment m/z, CE, polarity, RT window) are populated.
- Fragment library (.blib or .msp) can be imported into Skyline without errors and spectral entries display correct precursor–fragment pairs and retention time annotations.

## Limitations

- LipidCreator has been tested only with Thermo QExactive HF and Agilent QTOF instruments; transitions generated may require manual adjustment for other instrument types.
- Fragmentation rule predictions are based on known lipid cleavage patterns; novel or unusual lipid structures not in the fragmentation rule database may produce suboptimal or incorrect fragments.
- Retention time predictions are not explicitly mentioned in the workflow; users may need to supply or calibrate retention time windows separately for optimal transition selectivity.
- On Linux/Ubuntu, graphical window repainting issues may occur due to incomplete Mono implementation; command-line mode is more reliable.
- The .blib spectral library export requires SQLite 3 libraries; precompiled binaries are provided only for Debian and Ubuntu; other distributions may require custom compilation.

## Evidence

- [other] Parse lipid definitions; generate precursor and fragment m/z; assemble transitions; export Skyline-compatible list: "1. Parse lipid definitions (species, chain composition, adducts) from input specification. 2. Generate precursor m/z values and retention time predictions for each lipid target. 3. Calculate expected"
- [readme] LipidCreator creates target lists and fragment libraries for PRM/MRM in Skyline: "LipidCreator is a plugin for Skyline supporting targeted workflow development in lipidomics. It can be used to create user-defined target lists and fragment libraries for PRM and MRM experiments in"
- [readme] Tested instruments: "It has been tested with Thermo QExactive HF and Agilent QTOF instruments."
- [other] Standalone and library export support: "Optionally generate standalone fragment library file in Skyline-compatible format (.blib or .msp)."
- [readme] Command-line operation and cross-platform support: "It also supports standalone and command-line operation."
