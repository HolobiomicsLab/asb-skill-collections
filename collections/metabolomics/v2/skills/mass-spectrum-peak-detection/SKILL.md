---
name: mass-spectrum-peak-detection
description: Use when you have raw or processed MS spectrum data (mz/intensity pairs) from direct infusion MS (DI-MS), ASAP-MS, or other high-throughput ambient ionization methods, and need to identify which m/z signals represent true peaks of interest rather than noise or baseline drift.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3215
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  techniques:
  - direct-infusion-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
- supports data from multiple instruments, including DI-MS and ASAP-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-peak-detection

## Summary

Automatic identification of peaks of interest from raw or processed mass spectrometry spectra via algorithmic detection and intensity-based ranking. This skill extracts structured peak annotations (m/z, intensity, confidence scores) from unprocessed spectral data to enable downstream species authentication and sample classification.

## When to use

Apply this skill when you have raw or processed MS spectrum data (mz/intensity pairs) from direct infusion MS (DI-MS), ASAP-MS, or other high-throughput ambient ionization methods, and need to identify which m/z signals represent true peaks of interest rather than noise or baseline drift. Use it as the first analytical step before database scoring or peak annotation.

## When NOT to use

- Input is already a curated feature table or peak list with pre-assigned identities — re-detection would be redundant.
- Spectrum data is severely corrupted, contains extreme instrument artifacts, or lacks sufficient dynamic range to distinguish signal from noise.
- The analysis goal is to perform database matching without intermediate peak annotation — some workflows may skip explicit peak detection.

## Inputs

- raw MS spectrum data (mz/intensity pairs)
- processed MS spectrum data (mz/intensity pairs)
- data from DI-MS, ASAP-MS, or ambient ionization MS instruments

## Outputs

- peak identifier table
- m/z values for detected peaks
- intensity measurements
- confidence scores per peak
- annotated peak list with structured metadata

## How to apply

Load raw or processed MS spectrum data as mz/intensity pairs from the input file. Apply RapidMass's automatic peak detection algorithm to identify peaks of interest from the full spectrum. The algorithm ranks peaks by intensity and m/z values to distinguish genuine signals from background. Assign labels and confidence scores to each detected peak based on its intensity ranking relative to the overall spectrum distribution. Aggregate results into a structured output table with peak identifiers, m/z values, intensity measurements, and confidence scores. The detection rationale is grounded in intensity thresholding and m/z-based filtering to isolate species-characteristic signals from instrument noise.

## Related tools

- **RapidMass** (Provides the automatic peak detection algorithm and integrated workflow for loading spectra, detecting peaks, and generating annotated output tables with m/z, intensity, and confidence scores.) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Direct infusion mass spectrometry instrument supported as a data source for peak detection.)
- **ASAP-MS** (Ambient ionization mass spectrometry instrument supported as a data source for peak detection.)

## Evaluation signals

- All detected peaks have valid m/z values within the expected mass range for the instrument and sample type.
- Confidence scores are monotonically ranked by intensity; the highest-intensity peaks receive the highest confidence scores.
- Peak table schema is complete (peak_id, m/z, intensity, confidence_score) with no missing values.
- Detected peaks are reproducible across multiple runs on the same raw spectrum file (deterministic algorithm output).
- Visual inspection of detected peaks overlaid on the raw spectrum confirms they correspond to true local maxima and not baseline noise or instrument artifacts.

## Limitations

- Peak detection performance depends on the quality and dynamic range of the input spectrum; low-quality or heavily noisy spectra may yield false positives or miss low-abundance species-characteristic signals.
- The algorithm is optimized for high-throughput ambient ionization methods (DI-MS, ASAP-MS) and may require tuning or validation for other MS methodologies.
- Confidence scores are derived from intensity ranking and m/z-based heuristics; they do not incorporate external validation data such as tandem MS fragmentation patterns or database matching scores.

## Evidence

- [intro] The workflow and rationale for automatic peak detection.: "Load raw or processed MS spectrum data (mz/intensity pairs) from input file. 2. Apply RapidMass automatic peak detection algorithm to identify peaks of interest from the spectrum. 3. Assign labels"
- [readme] Software integration and scope of peak detection capability.: "the software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS"
- [readme] User-facing output and accessibility of the peak detection feature.: "RapidMass features a user-friendly, visual interface, making it accessible to users without programming expertise"
- [readme] Supported instrument diversity for peak detection.: "Other high-throughput mass spectrometry such as ambient ionization mass spectrometry (AI-MS), laser desorption/ionization mass spectrometry (LDI-MS), and several modified MS methodologies can also be"
