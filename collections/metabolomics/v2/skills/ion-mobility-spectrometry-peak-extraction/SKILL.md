---
name: ion-mobility-spectrometry-peak-extraction
description: Use when after peaks have been detected in aligned GCIMS samples using findPeaks with CWT parameters and peaks have been clustered across samples, and you need to integrate peak signals into a matrix format where each entry represents the intensity of a peak cluster in a specific sample for.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3197
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - R
  - GCIMS
derived_from:
- doi: 10.1016/j.chemolab.2023.104938
  title: GCIMS
evidence_spans:
- library(ggplot2) library(cowplot) library(GCIMS)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_gcims_cq
    doi: 10.1016/j.chemolab.2023.104938
    title: GCIMS
  dedup_kept_from: coll_gcims_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1016/j.chemolab.2023.104938
  all_source_dois:
  - 10.1016/j.chemolab.2023.104938
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-mobility-spectrometry-peak-extraction

## Summary

Extraction of intensity values for detected peaks across Gas Chromatography–Ion Mobility Spectrometry samples into a peak intensity matrix suitable for downstream analysis. This skill bridges peak detection and clustering to produce a quantitative feature table where rows represent peaks/clusters and columns represent samples.

## When to use

After peaks have been detected in aligned GCIMS samples using findPeaks with CWT parameters and peaks have been clustered across samples, and you need to integrate peak signals into a matrix format where each entry represents the intensity of a peak cluster in a specific sample for statistical analysis or metabolite identification.

## When NOT to use

- Input GCIMS dataset has not been aligned in retention time and drift time — alignment must precede peak detection and extraction.
- Peak detection has not yet been performed or peaks have not been clustered across samples — the skill requires pre-detected and clustered peak structures.
- You require raw peak coordinates (retention time, drift time, m/z) rather than quantitative intensity values — use the peak_list object directly instead.

## Inputs

- aligned GCIMSDataset object (post-alignment, baseline-corrected)
- peak_list object from findPeaks with CWT parameters
- clustered peaks object (from clusterPeaks)

## Outputs

- peak_table_matrix (rows=peaks/clusters, columns=samples, values=intensity)
- integration result object (intermediate, from integratePeaks)

## How to apply

Load the preprocessed and aligned GCIMS dataset into R using library(GCIMS). Execute the integratePeaks function on the detected peak list, specifying the integration_size_method parameter (e.g., 'fixed_size') and rip_saturation_threshold (typically 0.1 to control saturation artifacts). This step computes integrated intensity values for each detected peak across all samples. Then call the peakTable function on the integration result to extract and format these intensities into a matrix table. The resulting peak_table_matrix will have rows representing peaks or peak clusters and columns representing individual samples, with some entries marked as NA where peaks were not detected or integration failed; these missing values typically require imputation before downstream statistical analysis.

## Related tools

- **GCIMS** (R package providing integratePeaks and peakTable functions to perform fixed-size peak integration and extract intensity matrix from aligned and clustered GCIMS peaks) — https://github.com/sipss/GCIMS
- **R** (Execution environment for GCIMS functions and data manipulation)

## Examples

```
library(GCIMS); integration_result <- integratePeaks(peak_list, integration_size_method='fixed_size', rip_saturation_threshold=0.1); peak_table_matrix <- peakTable(integration_result)
```

## Evaluation signals

- peak_table_matrix has dimensions matching the number of detected peak clusters (rows) × number of samples (columns).
- All intensity values are numeric or marked as NA; no infinite or non-numeric entries present.
- Each column (sample) contains at least one non-NA intensity value, indicating successful integration across samples.
- NA entries are distributed plausibly (not concentrated in a single sample, suggesting systematic failure) and indicate peaks undetected in specific samples rather than integration errors.
- Intensity ranges are consistent with instrument saturation and noise thresholds applied during integration (e.g., RIP saturation threshold of 0.1 excludes oversaturated signals).

## Limitations

- Missing values (NA) in the peak_table_matrix require imputation before statistical analysis; the extraction skill does not handle missing data resolution.
- Fixed-size integration method assumes uniform peak width across retention and drift time dimensions, which may not hold for compounds with varying peak shapes or under different chromatographic conditions.
- Peak clustering quality directly affects the final matrix structure; poor clustering (incorrect merging or splitting of peaks across samples) will result in incorrect intensity estimates.
- RIP (Reactant Ion Peak) saturation threshold (e.g., 0.1) is a tuning parameter that must be optimized per instrument and dataset; incorrect settings may exclude true signals or include artifacts.

## Evidence

- [intro] integratePeaks and peakTable outputs: "Execute integratePeaks function with integration_size_method set to 'fixed_size' and rip_saturation_threshold parameter set to 0.1 to integrate detected peaks across all samples. Call peakTable"
- [intro] NA handling in peak_table_matrix: "The peakTable function produces a peak_table_matrix with rows representing clusters and columns representing samples, containing intensity values with some entries as NA that require imputation."
- [intro] Prerequisite: peak detection with CWT parameters: "Peak detection in the aligned GCIMS dataset is performed using findPeaks with CWT parameters including exclude0scaleAmpThresh=TRUE for both drift time and retention time dimensions, extension factors"
- [readme] GCIMS package scope: "GCIMS is an R package implementing a preprocessing pipeline for Gas Chromatography – Ion Mobility Spectrometry samples."
