---
name: mass-track-extraction-and-binning
description: 'Use when when you have centroid mzML files from LC-MS metabolomics acquisition
  and need to construct sample-level mass tracks before cross-sample alignment. Specifically:
  you are starting fresh with vendor-converted or pre-processed mzML input;'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0769
  tools:
  - Python
  - pymzml
  - mass_functions.nn_cluster_by_mz_seeds
  - chromatograms.get_thousandth_bins
  - chromatograms.extract_massTracks_
  - ThermoRawFileParser
  - ProteoWizard msconvert
  techniques:
  - LC-MS
  - direct-infusion-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- nearest neighbor (NN) clustering is performed to establish the number of mass tracks.
  The NN clustering assigns each data point to its nearest 'peak mz value'.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari_cq
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-track-extraction-and-binning

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Extract and bin mass tracks (extracted ion chromatograms, EICs) from individual LC-MS samples by parsing mzML files, binning m/z values at high resolution (0.001 amu), and clustering overlapping m/z traces using nearest-neighbor methods. This foundational step produces raw mass tracks that serve as input to cross-sample alignment.

## When to use

When you have centroid mzML files from LC-MS metabolomics acquisition and need to construct sample-level mass tracks before cross-sample alignment. Specifically: you are starting fresh with vendor-converted or pre-processed mzML input; you have not yet built a unified m/z grid across samples; and you need to preserve individual sample m/z calibration and chromatographic resolution for later anchor-track detection and MassGrid construction.

## When NOT to use

- Input is already a feature table or pre-aligned MassGrid—skip to feature detection.
- Profile-mode (not centroid) mzML files—requires different peak-picking strategy.
- Raw vendor files (.RAW, .d) without prior mzML conversion—first convert using ThermoRawFileParser or ProteoWizard msconvert.

## Inputs

- centroid mzML file (single sample)
- m/z binning resolution parameter (default 0.001 amu)
- nearest-neighbor clustering seed set (m/z values)

## Outputs

- mass tracks (EICs) per sample: list of (m/z_bin_id, chromatogram_vector, rt_values)
- per-sample m/z inventory: mapping of binned m/z to track identifiers
- sample-level metadata: acquisition parameters, scan count, m/z range

## How to apply

Parse each mzML file using pymzml to extract m/z and intensity pairs across all scans. Bin m/z values at 0.001 amu resolution (thousandth_bins) by merging adjacent bins within tolerance and resolving overlapping m/z values using nearest-neighbor clustering by m/z seeds (nn_cluster_by_mz_seeds). This produces a set of mass tracks per sample, each representing a distinct m/z value and its full retention-time intensity profile. The 0.001 amu binning leverages high mass resolution to prioritize mass separation; the clustering step removes redundant or near-duplicate tracks that would later complicate anchor detection and alignment. Store each mass track as a vector of (m/z, intensity, rt) tuples, indexed by m/z identifier and sample.

## Related tools

- **pymzml** (Parse mzML files and extract m/z and intensity scan data)
- **mass_functions.nn_cluster_by_mz_seeds** (Cluster overlapping m/z values by nearest-neighbor algorithm to resolve redundant traces) — https://github.com/shuzhao-li/asari
- **chromatograms.get_thousandth_bins** (Bin m/z values at 0.001 amu resolution and merge adjacent bins within tolerance) — https://github.com/shuzhao-li/asari
- **chromatograms.extract_massTracks_** (Extract full retention-time intensity profiles for each binned m/z across all scans) — https://github.com/shuzhao-li/asari
- **ThermoRawFileParser** (Convert Thermo .RAW files to centroid mzML prior to mass-track extraction) — https://github.com/compomics/ThermoRawFileParser
- **ProteoWizard msconvert** (Convert vendor data formats (e.g., .d, .raw, .mzXML) to centroid mzML) — https://proteowizard.sourceforge.io/tools.shtml

## Examples

```
from asari.chromatograms import get_thousandth_bins, extract_massTracks_; mass_tracks = extract_massTracks_(mzml_file='sample_001.mzML', binning_resolution=0.001)
```

## Evaluation signals

- Each sample produces ≥1 mass track; median track count scales with sample complexity and m/z range.
- No duplicate or near-identical m/z bins within a sample—clustering has resolved overlaps.
- Each mass track chromatogram vector length matches total scan count in the mzML file.
- m/z values in each bin are within ±0.0005 amu (half the binning tolerance) of the bin center.
- Mass tracks with median intensity below min_intensity_threshold (default 1e3 for Orbitrap) are flagged or removed in downstream QC.

## Limitations

- High-resolution instruments (Orbitrap, Q-TOF) yield better mass separation at 0.001 amu; lower-resolution instruments may produce artificially merged or split tracks.
- Binning resolution is fixed (0.001 amu); compounds with m/z differences < 0.001 amu cannot be resolved at this step.
- Centroid mode is required; profile-mode data must be centroided first (e.g., by vendor software or ProteoWizard).
- Nearest-neighbor clustering is sensitive to seed selection; poor seed placement may result in incomplete clustering of true duplicates.

## Evidence

- [other] Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve overlapping m/z values: "Extract mass tracks from each sample using pymzml and bin m/z values at 0.001 amu resolution, merging adjacent bins within tolerance and applying nearest-neighbor clustering by m/z seeds to resolve"
- [intro] Taking advantage of high mass resolution to prioritize mass separation and alignment: "Taking advantage of high mass resolution to prioritize mass separation and alignment"
- [other] The default method uses `pymzml` to parse mzML files.: "The default method uses `pymzml` to parse mzML files."
- [other] We use ThermoRawFileParser to convert Thermo .RAW files to .mzML. Msconvert in ProteoWizard can handle the conversion of most vendor data formats.: "We use ThermoRawFileParser (https://github.com/compomics/ThermoRawFileParser) to convert Thermo .RAW files to .mzML. Msconvert in ProteoWizard (https://proteowizard.sourceforge.io/tools.shtml) can"
- [readme] Input data are centroid mzML files from LC, GC or DI-MS metabolomics.: "Input data are centroid mzML files from LC, GC or DI-MS metabolomics."
