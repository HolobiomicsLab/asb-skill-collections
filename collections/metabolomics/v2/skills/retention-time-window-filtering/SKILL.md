---
name: retention-time-window-filtering
description: Use when you have mzML/mzXML chromatogram files from Thermo, Waters, or Bruker instruments and need to extract MS1 and MS2 scans matching both a target m/z value AND a known or suspected retention time range.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3375
  - http://edamontology.org/topic_0091
  tools:
  - meRgeION2
  - MergeION2
  - GNPS
  techniques:
  - LC-MS
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

# retention-time-window-filtering

## Summary

Filter MS1 and MS2 scans from raw chromatogram files by applying user-specified retention time (RT) bounds in addition to m/z targets, enabling targeted extraction of precursor and fragment ions within defined chromatographic windows. This skill is essential when building local spectral libraries from high-volume LC-MS/MS data while maintaining specificity to the intended analyte elution profile.

## When to use

Apply this skill when you have mzML/mzXML chromatogram files from Thermo, Waters, or Bruker instruments and need to extract MS1 and MS2 scans matching both a target m/z value AND a known or suspected retention time range. Use it when building local spectral libraries from DDA or targeted MS/MS acquisitions where RT precision helps disambiguate isobaric compounds, reduces off-target spectral noise, or aligns with method scouting or forced degradation studies where elution timing is experimentally controlled.

## When NOT to use

- Input is already a pre-built spectral library or consensus spectrum—apply deconvolution or spectral merging skills instead.
- Retention time information is unavailable or unreliable (e.g., from older instruments, damaged acquisition logs, or untargeted discovery scans with unknown RT ranges)—use m/z-only filtering.
- The goal is exploratory data mining across a wide, undefined RT range; overly restrictive RT windows will discard valid analyte signal and introduce bias.

## Inputs

- mzML or mzXML format chromatogram file(s) (converted from Thermo, Waters, or Bruker raw data)
- Target m/z value(s) with tolerance threshold (ppm or Da)
- Retention time window specification (min_RT, max_RT in minutes, optional)

## Outputs

- Filtered MS1 scans with matched precursor m/z, retention time, scan number, intensity
- Corresponding MS2 fragment spectra for matched precursors
- Structured output table or spectral library entries with scan metadata (m/z, RT, scan ID, intensity)

## How to apply

Parse the raw mzML/mzXML chromatogram file(s) using a mass spectrometry data parser compatible with your instrument vendor format. Construct a query specification that combines (1) target m/z value(s) with user-defined m/z tolerance (typically instrument-dependent, e.g., 10–50 ppm for high-resolution MS), and (2) optional retention time bounds supplied as a min–max window (in minutes). Scan the chromatogram data and retain only MS1 scans whose precursor m/z matches the target within tolerance AND whose scan timestamp falls within the specified RT window. For each matched MS1 precursor, extract the corresponding MS2 fragment spectrum. Compile results into a structured output (tabular format with columns: m/z, retention time, scan number, intensity, scan metadata) suitable for downstream library merging. The RT window acts as a spatial constraint that reduces false positives from co-eluting isobars and ensures only the chromatographically relevant portion of the acquisition is retained.

## Related tools

- **MergeION2** (Primary tool for parsing mzML/mzXML files and performing MS1/MS2 scan extraction with m/z and retention time filtering; outputs are merged into GNPS-style spectral libraries) — https://github.com/daniellyz/MergeION2
- **GNPS** (Spectral library standard and target format for merged, filtered scan data; provides reference database for library search and annotation)

## Examples

```
# In R, after loading MergeION2 and an mzML file, extract MS1/MS2 scans for m/z 369.232 within RT 5.0–6.5 min; then merge into spectral library
params.query = list(prec_mz = 369.232, min_RT = 5.0, max_RT = 6.5, polarity = "Positive")
filtered_scans = extract_MS_scans(mzml_file = "sample.mzML", params = params.query)
library_merged = merge_to_library(filtered_scans, metadata = user_metadata)
```

## Evaluation signals

- Output scan count is smaller than input scan count and reflects the expected selectivity for the RT window (sanity check: narrow RT windows should yield fewer scans; wide windows should be closer to unfiltered counts).
- All output scans have retention time values within the user-specified min_RT and max_RT bounds (strict boundary check).
- All output precursor m/z values fall within ±tolerance of the target m/z (verification of m/z filter fidelity).
- MS2 scans are properly linked to their parent MS1 precursors (data integrity check: scan hierarchy preserved).
- Metadata fields (scan number, intensity, polarity) are populated and consistent with source mzML/mzXML structure (schema validation).

## Limitations

- Retention time windows must be manually defined by the user; no automated RT prediction is performed. Incorrect or overly narrow windows will result in loss of valid signal.
- Retention time calibration and stability vary across instruments and acquisition methods; clock drift or method changes between runs can shift expected RT ranges.
- MergeION2 is currently limited to ESI-MS/MS spectra in positive ion mode; negative ion mode data will not be usable with the pre-compiled spectral database.
- RT filtering is only optional in MergeION2; if omitted, the tool reverts to m/z-only extraction, which may increase false positives in crowded m/z regions.
- Large chromatogram files or very strict m/z tolerance + narrow RT windows can result in no matching scans if parameters are misaligned with actual data distribution.

## Evidence

- [readme] extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users: "extracting MS1 and MS2 scans from one or multiple raw chromatogram files according to m/z (and retention time) provided by users"
- [readme] compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA or targeted MS/MS-mode: "It is compatible with mzML/mzXML format converted from Thermo, Water or Bruker data files, in either DDA (Data-driven acquisition) or targeted MS/MS-mode"
- [other] Scan the chromatogram data to identify MS1 scans matching the target m/z values within tolerance and retention time bounds: "Scan the chromatogram data to identify MS1 scans matching the target m/z values within tolerance and retention time bounds (if specified)"
- [readme] Building a local high quality spectral library is an essential step thus often lacking in metabolomics and pharmaceutical laboratories: "Building a local high quality spectral library is an essentiel step thus often lacking in metabolomics and pharmaceutical laboratories"
