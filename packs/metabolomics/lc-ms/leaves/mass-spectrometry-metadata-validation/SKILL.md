---
name: mass-spectrometry-metadata-validation
description: Use when after importing raw LC-MS/MS data files into the SIRIUS Java
  framework, before constructing indexed spectrum objects or submitting data to CSI:FingerID,
  CANOPUS, or MSNovelist web services.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_3520
  tools:
  - SIRIUS
  - CSI:FingerID
  - CANOPUS
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41587-021-01045-9
  title: cosmic
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cosmic
    doi: 10.1038/s41587-021-01045-9
    title: cosmic
  dedup_kept_from: coll_cosmic
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41587-021-01045-9
  all_source_dois:
  - 10.1038/s41587-021-01045-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-metadata-validation

## Summary

Validates and quality-checks spectral metadata extracted from LC-MS/MS data files (mzML, mzXML, vendor formats) to ensure precursor m/z, retention time, collision energy, and fragment ion assignments are complete and within acceptable ranges before downstream analysis in SIRIUS.

## When to use

After importing raw LC-MS/MS data files into the SIRIUS Java framework, before constructing indexed spectrum objects or submitting data to CSI:FingerID, CANOPUS, or MSNovelist web services. Apply this skill when you need to detect incomplete or out-of-range spectral metadata that would corrupt fragmentation tree computation or isotope pattern analysis.

## When NOT to use

- Spectral data already successfully processed through SIRIUS and validated in prior runs; re-validation adds no new information.
- Pre-curated, manually verified spectral libraries (e.g., MoNA, NIST) with known-good metadata; library curation has already ensured completeness.
- Targeted or data-independent acquisition (DIA) workflows where precursor m/z isolation windows and window-specific fragment assignments follow non-standard conventions incompatible with traditional metadata fields.

## Inputs

- Raw LC-MS/MS data files (mzML, mzXML, or vendor-specific binary formats)
- Spectral metadata: precursor m/z, retention time, collision energy, fragment ion m/z and intensity
- Quality thresholds (ion count minima, mass range bounds)

## Outputs

- Validated spectral dataset in SIRIUS serialized format
- Quality control report flagging incomplete or out-of-range metadata
- Structured spectrum objects with indexed MS1 and MS/MS hierarchies

## How to apply

Parse spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from input LC-MS/MS files using SIRIUS's built-in data importer. Perform automated quality checks by validating: (1) non-zero ion counts in both MS1 and MS/MS scans; (2) precursor m/z and fragment masses within physically realistic ranges (e.g., 50–2000 m/z for metabolites); (3) metadata completeness (no null/missing retention time or collision energy fields); (4) isotope pattern consistency with expected natural abundances. Flag or reject spectra failing any criterion and generate a validated spectral dataset in SIRIUS serialized format. This ensures downstream fragmentation tree and molecular formula inference operate on clean, complete data.

## Related tools

- **SIRIUS** (Java framework that ingests LC-MS/MS data, parses and validates spectral metadata, and constructs indexed spectrum objects for downstream fragmentation tree and molecular formula analysis) — https://github.com/sirius-ms/sirius
- **CSI:FingerID** (Receives validated spectra and fragmentation trees from SIRIUS to perform structure database matching and molecular fingerprinting) — https://bio.informatik.uni-jena.de/software/csi-fingerid/
- **CANOPUS** (Accepts validated fragmentation patterns to assign systematic chemical classifications and natural product annotations) — https://bio.informatik.uni-jena.de/software/canopus/

## Evaluation signals

- All imported spectra contain non-zero ion counts in both MS1 and MS/MS scans; no scans dropped due to empty peak lists.
- Precursor m/z and fragment m/z values fall within the expected range (typically 50–2000 m/z for small-molecule metabolites); no outliers detected.
- Spectral metadata fields (retention time, collision energy, precursor charge state) are complete; percentage of missing values is zero or below a pre-defined tolerance (e.g., <1%).
- SIRIUS successfully constructs fragmentation trees and generates molecular formula hypotheses from validated spectra without parsing errors or metadata-related warnings.
- Output serialized spectrum objects can be uploaded to CSI:FingerID or CANOPUS web services without rejection due to malformed or incomplete metadata.

## Limitations

- Validation thresholds (mass range, ion count minima, metadata completeness) are global; tool does not adapt per-spectrum to ion source, ionization mode, or sample-type-specific characteristics.
- Isotope pattern validation relies on theoretical natural abundances; real patterns affected by sample contamination, detector saturation, or non-standard labeling will not be flagged as invalid.
- Vendor-specific binary formats (Thermo .raw, Waters .raw, Bruker .d) require manufacturer-supplied converters or third-party libraries to parse into mzML/mzXML; SIRIUS data importer support may vary by version and platform.
- No changelog provided in repository; validation rule updates or bug fixes in recent versions cannot be cross-referenced, and backward compatibility is unclear.

## Evidence

- [other] Parse and validate spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from the input files.: "Parse and validate spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from the input files."
- [other] Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format.: "Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format."
- [readme] SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other 'small molecules of biological interest'.: "SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other 'small molecules of biological interest'."
- [other] Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer.: "Load raw LC-MS/MS data files (mzML, mzXML, or vendor formats) into the SIRIUS Java framework using the built-in data importer."
- [other] Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation.: "Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation."
