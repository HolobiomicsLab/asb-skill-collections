---
name: feature-table-annotation-and-provenance-tracking
description: Use when after generating a filtered feature table from raw mass spectrometry data in openNAU.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - openNAU
  - MetaQC
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
---

# feature-table-annotation-and-provenance-tracking

## Summary

This skill documents which quality control filters were applied to a metabolomic peak feature table and which peaks survived each filtering stage, enabling reproducibility and traceability of differential metabolic ion peak identification. It is essential for untargeted metabolomics workflows where QC decisions directly impact downstream metabolite identification and biological interpretation.

## When to use

Apply this skill after generating a filtered feature table from raw mass spectrometry data in openNAU. Specifically, use it when you have applied signal-to-noise thresholds, feature prevalence criteria, and statistical comparison filters (fold-change or p-value thresholds) to identify differential metabolic ion peaks, and you need to document which QC criteria each peak passed or failed for downstream validation and publication.

## When NOT to use

- Input is raw mass spectrometry data (mzML, NetCDF, or vendor format) rather than an extracted peak feature table—use feature extraction first.
- The analysis goal is exploratory and does not require downstream metabolite identification or publication; in such cases, minimal annotation may suffice.
- QC filters have not yet been designed or applied; defer this skill until filter parameters are finalized and justified.

## Inputs

- extracted peak feature table (CSV or tabular format) with mass-to-charge ratios, retention times, and intensity values across all samples
- QC filter parameters (signal-to-noise thresholds, feature prevalence criteria, statistical comparison thresholds)

## Outputs

- QC-filtered feature table with annotations indicating which QC filters were applied
- annotated feature table indicating which peaks survive QC criteria
- QC provenance metadata documenting filter parameters and decision rationale

## How to apply

After applying quality control filters to remove low-abundance or noisy peaks and identify peaks with significant differential intensity patterns between experimental groups, annotate the output feature table to record: (1) which QC filters were applied (e.g., signal-to-noise threshold values, prevalence cutoff, statistical test type and significance level); (2) which peaks survive all QC criteria; (3) for each retained peak, flag which filters it passed. Export this annotated feature table alongside metadata documenting the filter parameters and decision thresholds. This provenance tracking enables expert review of QC stringency and justification of peak retention decisions, and facilitates troubleshooting if downstream metabolite identification yields unexpected or conflicting results.

## Related tools

- **openNAU** (integrated platform for untargeted metabolomics that includes raw mass data extraction and quality control filtering for differential metabolic ion peak identification) — https://github.com/zjuRong/openNAU
- **MetaQC** (component module within openNAU that performs quality control filtering and peak feature processing) — https://github.com/zjuRong/openNAU

## Evaluation signals

- QC-filtered feature table schema is valid: contains all original intensity columns plus annotation columns documenting filter decisions and pass/fail status for each peak.
- Provenance metadata is present and complete: specifies signal-to-noise thresholds, feature prevalence cutoffs, statistical test types, p-value or fold-change cutoffs used.
- Peak retention counts are documented: total peaks in raw table vs. peaks retained after each filter stage should be reported to justify QC stringency.
- Downstream metabolite identification results are reproducible: when the same QC parameters and annotations are applied, the same peak subset is retained and matched to metabolite standards.
- Expert review of retained vs. discarded peaks confirms that QC decisions are biologically plausible (e.g., low-intensity or high-noise peaks are removed, differential peaks across experimental groups are retained).

## Limitations

- The skill does not prescribe optimal QC filter parameter values; these must be determined empirically or justified by domain knowledge and depend on instrument platform, sample matrix, and experimental design.
- Manual expert review is recommended to validate QC filter stringency and confirm that retained peaks represent true biological signals rather than artifacts—automated annotation alone may miss matrix effects or instrument drift.
- Annotation metadata can become complex if multiple QC filters are chained; clear documentation of filter order and interdependencies is essential to avoid confusion.

## Evidence

- [other] Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification.: "Export the QC-filtered feature table with annotations indicating which QC filters were applied and which peaks survive for downstream identification."
- [readme] The software includes extraction of raw mass data and quality control for the identification of differential metabolic ion peaks.: "It includes the extraction of raw mass data and quality control for the identification of differential metabolic ion peaks."
- [other] Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria.: "Apply quality control filters to remove low-abundance or noisy peaks according to signal-to-noise thresholds and feature prevalence criteria."
- [other] Identify peaks with significant differential intensity patterns between experimental groups using statistical comparison (e.g., fold-change or p-value thresholds).: "Identify peaks with significant differential intensity patterns between experimental groups using statistical comparison (e.g., fold-change or p-value thresholds)."
