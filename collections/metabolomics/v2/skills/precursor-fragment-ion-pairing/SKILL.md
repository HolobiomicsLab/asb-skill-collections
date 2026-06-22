---
name: precursor-fragment-ion-pairing
description: Use when you have raw LC-MS/MS data files (mzML/mzXML format from Thermo, Waters, or Bruker instruments) and a list of target compounds defined by precursor m/z values (and optionally retention time windows).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_3520
  tools:
  - meRgeION2
  - MergeION2
  - GNPS
derived_from:
- doi: 10.1021/acs.analchem.2c04343
  title: MeRgeION
evidence_spans:
- github.com__daniellyz__meRgeION2
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mergeion_cq
    doi: 10.1021/acs.analchem.2c04343
    title: MeRgeION
  dedup_kept_from: coll_mergeion_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c04343
  all_source_dois:
  - 10.1021/acs.analchem.2c04343
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# precursor-fragment-ion-pairing

## Summary

Extract and pair MS1 precursor ions with their corresponding MS2 fragment spectra from raw chromatogram files (mzML/mzXML) using user-specified m/z and retention time targets. This skill enables construction of local spectral libraries while preserving data confidentiality by selectively pulling only the scans of interest from DDA or targeted MS/MS acquisition modes.

## When to use

You have raw LC-MS/MS data files (mzML/mzXML format from Thermo, Waters, or Bruker instruments) and a list of target compounds defined by precursor m/z values (and optionally retention time windows). You want to build a confidential local spectral library without uploading raw data to public repositories, or you need to extract specific analytes for focused spectral annotation and library building.

## When NOT to use

- Input data are already in spectral library format (e.g., GNPS .mgf, MassBank records) — this skill targets raw chromatogram extraction.
- You require untargeted, global MS/MS annotation without pre-specified m/z targets — use full-scan spectral library matching instead.
- Data are in proprietary binary formats (e.g., .raw, .d) without prior conversion to mzML/mzXML — a format conversion step must precede this skill.

## Inputs

- mzML or mzXML format mass spectrometry chromatogram file(s)
- User-defined target list with precursor m/z values (required) and retention time ranges (optional)
- Instrument vendor specification (Thermo, Waters, or Bruker)

## Outputs

- Paired MS1–MS2 scan table with columns: precursor m/z, retention time, MS1 scan number, MS2 scan number, fragment ion list, intensity values, and scan metadata
- GNPS-style spectral library entries (when merged with user-provided metadata)

## How to apply

Load the mzML/mzXML file(s) using a mass spectrometry data parser compatible with your instrument vendor. Parse user-provided m/z targets and optional retention time ranges into a query specification. Scan the chromatogram data to identify MS1 scans matching the target m/z values within the instrument's measurement tolerance and any specified retention time bounds. For each matched precursor, extract the corresponding MS2 fragment spectrum (the child scan associated with that precursor ion). Compile the paired MS1–MS2 records into a structured output with scan metadata including m/z, retention time, scan number, and intensity. The pairing step is critical: each MS2 must be validated as originating from its matched precursor (via parent m/z and scan hierarchy), ensuring spectral integrity for downstream library search.

## Related tools

- **MergeION2** (Primary tool implementing MS1/MS2 scan extraction, pairing, and merging into GNPS-style spectral libraries with metadata integration) — https://github.com/daniellyz/MergeION2
- **GNPS** (Reference spectral library format and destination for merged, annotated precursor–fragment ion pairs)

## Examples

```
params.query.sp = list(prec_mz = 369.232, use_prec = TRUE, polarity = "Positive", method = "Cosine", min_frag_match = 6); search_result = library_query(input_library = library1c, query_spectrum = query.sp, params.query.sp = params.query.sp)
```

## Evaluation signals

- Verify that each extracted MS2 spectrum's parent m/z matches the corresponding MS1 precursor m/z within instrument tolerance (e.g., ±0.02 m/z for high-resolution MS).
- Confirm that retention times of extracted scans fall within user-specified windows (if provided), with no orphaned MS2 scans lacking a matched MS1 precursor.
- Check that intensity distributions and fragment peak patterns in the paired spectra are consistent with known chemical structure fragmentation rules for the target compounds.
- Validate that the output library can be successfully queried against test spectra using spectral similarity algorithms (e.g., Cosine ≥ 0.7 for true positives).
- Ensure all metadata (compound names, INCHIKEY, adduct type, polarity) are correctly preserved in the merged library entries.

## Limitations

- Skill is restricted to mzML/mzXML formats; proprietary binary formats (.raw, .d, .ms) require prior vendor-specific conversion tools.
- Performance and accuracy depend on user-provided m/z tolerance and retention time windows; overly narrow windows may miss real peaks due to instrument drift or calibration variation.
- Currently supports ESI-MS/MS spectra in positive ion mode; negative ion mode and alternative ionization methods are mentioned as future work.
- Requires careful manual inspection of metadata (compound names, structures, drug annotations) during library merging to avoid confidentiality leaks or propagation of incorrect annotations.
- DDA and targeted MS/MS modes are both compatible, but targeted mode may yield higher specificity at the cost of untargeted discovery.

## Evidence

- [intro] extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users: "extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users"
- [intro] MergeION is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files in either DDA or targeted MS/MS-mode: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
- [intro] Building a local high quality spectral library is an essential step in metabolomics and pharmaceutical laboratories, often lacking due to data confidentiality concerns: "Building a local high quality spectral library is an essentiel step thus often lacking in metabolomics and pharmaceutical laboratories. This is often due to the data confidentiality (e.g drug"
- [intro] MergeION enables building local spectral libraries without sharing them in public domains: "enables building local spectral libraries without sharing them in public domains"
- [other] Scan the chromatogram data to identify MS1 scans matching the target m/z values within tolerance and retention time bounds, then extract corresponding MS2 fragment spectra: "Scan the chromatogram data to identify MS1 scans matching the target m/z values within tolerance and retention time bounds (if specified). 4. Extract corresponding MS2 fragment spectra for matched"
- [intro] Several library search algorithms are available in MergeION for searching and annotating spectra in local or public databases: "Several library search algorithms are available, allowing users to search and annotate an unknown spectrum in their local database or public databases"
