---
name: hierarchical-spectrum-object-construction
description: Use when immediately after parsing and validating raw LC-MS/MS data files (mzML, mzXML, or vendor formats) when you need to prepare spectral data for fragmentation tree computation, isotope pattern analysis, or molecular formula ranking within the SIRIUS framework.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0599
  tools:
  - SIRIUS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# hierarchical-spectrum-object-construction

## Summary

Construct validated, hierarchically organized spectrum objects from parsed LC-MS/MS data by indexing MS1 and MS/MS peaks into in-memory data structures suitable for fragmentation analysis. This skill ensures spectral metadata (precursor m/z, retention time, collision energy, fragment assignments) and mass accuracy are preserved in a format ready for downstream molecular formula and structure inference.

## When to use

Apply this skill immediately after parsing and validating raw LC-MS/MS data files (mzML, mzXML, or vendor formats) when you need to prepare spectral data for fragmentation tree computation, isotope pattern analysis, or molecular formula ranking within the SIRIUS framework. Use it when input spectral records have been quality-checked for non-zero ion counts and valid mass ranges, but have not yet been indexed into SIRIUS's internal representation.

## When NOT to use

- Input spectral data have not been quality-checked for non-zero ion counts or valid mass ranges; apply quality checks first.
- LC-MS/MS data are already in a validated, indexed format (e.g., already deserialized SIRIUS objects); skip to downstream analysis.
- Input is low-resolution mass spectrometry data lacking accurate isotope pattern information; isotope-based molecular formula ranking will not be reliable.

## Inputs

- Parsed LC-MS/MS spectral records (precursor m/z, retention time, collision energy, fragment ion peaks with m/z and intensity)
- Spectral metadata validated for non-zero ion counts and valid mass ranges
- High-resolution mass spectra with isotope pattern information

## Outputs

- Hierarchically indexed spectrum objects with MS1 and MS/MS data organized into parent–child relationships
- SIRIUS-serialized spectrum dataset ready for fragmentation tree and molecular formula analysis
- Validated spectrum objects with annotated neutral losses and fragment assignments

## How to apply

After loading and parsing spectral metadata from the LC-MS/MS input files, construct hierarchical spectrum objects by: (1) Creating a parent MS1 spectrum node indexed by precursor m/z and retention time, populated with accurate monoisotopic mass and isotope pattern peaks. (2) Attaching child MS/MS spectrum nodes to the parent, each indexed by collision energy and tagged with fragment ion assignments (loss annotations). (3) For each fragment peak, storing the measured m/z, intensity, and—if available—the hypothetical neutral loss mass relative to the precursor. (4) Validating that MS1 and MS/MS hierarchies are internally consistent: parent precursor m/z matches the neutral mass of all MS/MS fragments within the specified mass tolerance (typically 5 ppm for high-resolution instruments), and peak intensities are non-negative. (5) Serializing the validated structure into SIRIUS's native format for subsequent analysis. The rationale is that fragmentation tree algorithms and isotope pattern analysis rely on correct parent–child relationships and accurate mass assignments; misconstrued hierarchies lead to spurious molecular formula candidates and unreliable structure predictions.

## Related tools

- **SIRIUS** (Java framework for ingesting, parsing, and internally representing LC-MS/MS data; provides the serialization format and hierarchical object model for spectrum construction) — https://github.com/sirius-ms/sirius

## Evaluation signals

- Verify that every MS/MS spectrum is linked to exactly one parent MS1 spectrum by precursor m/z (within 5 ppm tolerance).
- Confirm that all fragment peaks in MS/MS spectra have m/z ≤ precursor m/z and that neutral loss masses (precursor m/z – fragment m/z) are non-negative.
- Check that isotope pattern peaks in the MS1 spectrum follow expected relative abundance ratios (e.g., 13C isotopologue ≈ 1% of monoisotopic peak for typical organic molecules).
- Validate that the serialized spectrum object can be deserialized by SIRIUS without errors and that hierarchical indices are intact after round-trip serialization.
- Ensure that spectrum objects contain no missing critical metadata fields (precursor m/z, retention time, collision energy) and that metadata values are within physically plausible ranges (m/z > 0, retention time ≥ 0, collision energy in instrument range).

## Limitations

- Spectrum object construction assumes input LC-MS/MS data have been correctly aligned to a single precursor ion; co-isolation of multiple precursors will result in ambiguous fragment assignments.
- The method relies on accurate mass measurements and high mass resolution (typically 5 ppm or better); low-resolution data may not support reliable isotope pattern analysis or precise neutral loss annotation.
- Metadata such as collision energy and instrument type may be missing or non-standard in vendor formats; partial metadata may reduce the utility of downstream fragmentation tree analysis.
- No changelog or version-specific guidance is publicly available for SIRIUS spectrum object schema evolution; compatibility between versions is not explicitly documented.

## Evidence

- [other] Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation: "Construct structured spectrum objects with properly indexed MS1 and MS/MS data hierarchies within the SIRIUS in-memory representation."
- [other] Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format: "Perform basic quality checks (non-zero ion counts, valid mass ranges, metadata completeness) and output the validated spectral dataset in SIRIUS serialized format."
- [other] Parse and validate spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from the input files: "Parse and validate spectral metadata (precursor m/z, retention time, collision energy, fragment ion assignments) from the input files."
- [readme] SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other small molecules of biological interest: "SIRIUS is a java-based software framework for the analysis of LC-MS/MS data of metabolites and other "small molecules of biological interest"."
- [readme] High resolution mass spectrometry allows us to determine the isotope pattern of sample molecule with outstanding accuracy and apply this information to identify the elemental composition of the sample molecule: "High resolution mass spectrometry allows us to determine the isotope pattern of sample molecule with outstanding accuracy and apply this information to identify the elemental composition of the"
