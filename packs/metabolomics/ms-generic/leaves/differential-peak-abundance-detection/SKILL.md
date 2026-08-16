---
name: differential-peak-abundance-detection
description: Use when after raw mass spectrometry data has been converted to a peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across samples, and you need to reduce noise and identify which peaks show meaningful differential patterns between.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - MetaQC
  - openNAU
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.21147/j.issn.1000-9604.2023.05.11
  title: OpenNAU
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_opennau_cq
    doi: 10.21147/j.issn.1000-9604.2023.05.11
    title: OpenNAU
  dedup_kept_from: coll_opennau_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.21147/j.issn.1000-9604.2023.05.11
  all_source_dois:
  - 10.21147/j.issn.1000-9604.2023.05.11
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# differential-peak-abundance-detection

## Summary

Quality control filtering of extracted mass spectrometry peak features to identify metabolic ion peaks with significant abundance differences between experimental groups. This skill applies signal-to-noise thresholds, feature prevalence criteria, and statistical comparison tests to isolate candidate differential peaks from untargeted metabolomics data.

## When to use

Apply this skill after raw mass spectrometry data has been converted to a peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across samples, and you need to reduce noise and identify which peaks show meaningful differential patterns between experimental conditions (e.g., treatment vs. control groups).

## When NOT to use

- Input is already a fully annotated metabolite identification table (skip directly to pathway or systems analysis)
- Raw mass spectrometry data in vendor formats (mzML, mzXML, NetCDF) — first perform peak extraction and feature alignment

## Inputs

- Extracted peak feature table (CSV or tabular format with mass-to-charge ratios, retention times, intensity values across all samples)

## Outputs

- Quality-control-filtered feature table with differential ion peaks
- QC metadata annotations (filter parameters applied, peaks passing criteria)

## How to apply

Load the extracted peak feature table and apply multi-stage quality control filters in sequence: (1) remove low-abundance or noisy peaks using signal-to-noise thresholds and feature prevalence criteria (e.g., presence in a minimum proportion of samples); (2) compute statistical comparisons between experimental groups such as fold-change or p-value metrics to identify peaks with significant differential intensity patterns; (3) retain only peaks that pass all QC criteria as candidate differential metabolic ion peaks; (4) annotate the filtered feature table with metadata indicating which QC filters were applied and which peaks survived, enabling downstream identification against metabolomics databases. The rationale is that untargeted metabolomics produces thousands of features, most of which are noise or uninformative background; systematic quality control before statistical testing reduces false discoveries and focuses analysis on biologically relevant signals.

## Related tools

- **MetaQC** (Quality control component within openNAU for filtering extracted peak features and identifying differential metabolic ion peaks) — https://github.com/zjuRong/openNAU
- **openNAU** (Complete analysis system platform for untargeted metabolomics that integrates raw mass data extraction and differential peak QC) — https://github.com/zjuRong/openNAU

## Evaluation signals

- Verify that output feature table contains only peaks passing all stated signal-to-noise thresholds and feature prevalence criteria
- Confirm QC metadata annotations list the specific filter thresholds applied (e.g., SNR cutoff, minimum sample prevalence) and report the number of peaks retained vs. removed at each stage
- Check that differential peaks show statistically significant fold-change or p-value differences between experimental groups as specified in the workflow
- Validate that all peaks in the final table can be traced to specific samples and that intensity distributions are plausible (no negative values, values within expected instrument range)
- Confirm reproducibility by re-running with identical QC parameters and comparing peak lists and annotations for exact matches

## Limitations

- QC filter thresholds (signal-to-noise, feature prevalence, p-value cutoff) are user-configurable and must be justified by the experimental design and metabolomics platform; inappropriate thresholds may remove true signals or retain noise
- Statistical comparison methods (fold-change vs. p-value) assume specific distributional properties of feature intensities; violations (e.g., non-normal distributions, extreme outliers) may lead to spurious differential calls
- Quality control is performed only on extracted features; errors in peak picking, alignment, or retention time correction during raw data processing will propagate into filtered results

## Evidence

- [readme] It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks.: "It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
- [other] 1. Load the extracted peak feature table (CSV or tabular format) containing mass-to-charge ratios, retention times, and intensity values across all samples. 2. Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria. 3. Identify peaks with significant differential intensity patterns between experimental groups using statistical comparison (e.g., fold-change or p-value thresholds). 4. Retain only candidate differential metabolic ion peaks that pass all QC criteria.: "Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria."
- [other] Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification.: "Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification."
