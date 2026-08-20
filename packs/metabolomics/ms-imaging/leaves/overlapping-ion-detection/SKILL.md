---
name: overlapping-ion-detection
description: Use when when annotating matrix-related ions in MSI datasets where two or more ions share identical or near-identical m/z values (isobaric ions) or exhibit overlapping spatial distributions across imaging pixels.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - rMSIcleanup
  - rMSI
  - rMSIproc
  - R
  - devtools
  techniques:
  - MS-imaging
derived_from:
- doi: 10.1186/s13321-020-00449-0
  title: ''
evidence_spans:
- rMSIcleanup is an open-source R package to annotate matrix-related signals in MSI data
- devtools::install_github("prafols/rMSI", ref = "0.8")
- devtools::install_github("prafols/rMSIproc", ref = "0.2")
- rMSIcleanup is an open-source R package
- install.packages("devtools")
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
    doi: 10.1186/s13321-020-00449-0
    title: ''
  dedup_kept_from: coll_rmsicleanup_ms_imaging_matrix_peak_annot_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-020-00449-0
  all_source_dois:
  - 10.1186/s13321-020-00449-0
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# overlapping-ion-detection

## Summary

Detect and flag isobaric or co-localized ions that may confound matrix/non-matrix classification in mass spectrometry imaging (MSI) data. This step prevents misclassification of chemically indistinguishable or spatially overlapped peaks during automated matrix annotation.

## When to use

When annotating matrix-related ions in MSI datasets where two or more ions share identical or near-identical m/z values (isobaric ions) or exhibit overlapping spatial distributions across imaging pixels. Critical before binary matrix/non-matrix labeling to avoid false positives that would conflate distinct chemical species or compromise downstream matrix removal.

## When NOT to use

- Input peak matrix already has pre-curated, non-overlapping ions from manual or external curation — overlap detection is redundant.
- MSI dataset has very high mass resolution (>100 kDa resolving power) where isobaric overlap is negligible — chemical formula alone suffices.
- Spatial resolution is so low or sample heterogeneity so high that all ions are diffusely distributed; co-localization becomes non-informative.

## Inputs

- Peak matrix (rMSIproc format .zip file containing m/z and intensity values for each pixel)
- Chemical formula annotations for candidate ions
- Processed MSI dataset (.tar file with spatial coordinates and pixel-level metadata)
- Ion m/z values and spatial distribution patterns extracted from the peak matrix

## Outputs

- Overlap-flagged ion list (binary overlap flag or confidence score for each ion)
- Isobaric/co-localized ion pairs or groups (edges or clusters of ambiguous ions)
- Visual annotation report justifying overlap decisions
- Filtered peak matrix with overlapping ions marked or excluded

## How to apply

After loading peak matrix and chemical formula data into rMSI, extract the spatial distribution patterns for each ion candidate across all imaging pixels. Compare m/z values to identify isobaric or near-isobaric peaks; simultaneously assess spatial coherence by examining whether ions co-localize within the same image regions. Flag ions that share both high m/z similarity and spatial overlap as ambiguous. The overlapping peak detection feature in rMSIcleanup integrates these two signals to generate a confidence score or binary overlap flag for each ion. Ions with detected overlaps are marked during annotation so they are either withheld from classification, assigned lower confidence, or examined manually before final matrix labeling. The rationale is that overlapped ions cannot be reliably distinguished by formula and space alone, so their true identity remains uncertain and they should be excluded or downweighted in downstream matrix removal to avoid introducing false negatives.

## Related tools

- **rMSIcleanup** (Primary tool that integrates overlapping peak detection into matrix annotation workflow; generates overlap flags and visual justification report) — https://github.com/gbaquer/rMSIcleanup
- **rMSI** (Loads and manages MSI data (spatial coordinates, peak intensities); supports extraction of spatial distribution patterns needed for overlap assessment) — https://github.com/prafols/rMSI
- **rMSIproc** (Loads and stores peak matrices in standardized format; preprocesses raw imzML into rMSI-compatible data structures) — https://github.com/prafols/rMSIproc
- **R** (Execution environment and dependency manager for rMSIcleanup, rMSI, and rMSIproc)
- **devtools** (Package installation utility; facilitates GitHub-based installation of rMSIcleanup and dependencies)

## Examples

```
results <- rMSIcleanup::annotate_matrix(pks, "Ag1", full); rMSIcleanup::generate_pdf_report(results, pks, full, "test", folder="/home/user/")
```

## Evaluation signals

- All isobaric ion pairs (same m/z within instrument resolution) are identified and flagged; no isobaric ions slip through without overlap annotation.
- Spatial co-localization is detected: ions whose pixel-wise intensity patterns exhibit Pearson correlation or Euclidean distance above a defined threshold are consistently marked.
- Overlap-flagged ions do not appear in the final cleaned peak matrix (or appear with explicit 'uncertain' status in the visual report); manual inspection confirms these were genuine ambiguities.
- Visual annotation report cross-references each overlap flag with supporting evidence (m/z proximity, spatial correlation coefficient, heatmap overlay); justifications are transparent and auditable.
- Performance on positive controls: if sample data includes known isobaric pairs or synthetic co-localized ions, 100% detection rate is achieved.

## Limitations

- Overlap detection relies on chemical formula completeness; ions without annotated formulas cannot be assessed for isobaric conflicts.
- Spatial coherence assessment assumes uniform sampling across the imaging grid; sparse or non-contiguous pixels may yield spurious co-localization metrics.
- Method does not resolve true chemical identity of overlapping ions—only flags ambiguity; manual tandem MS, high-resolution MS/MS fragmentation, or external standards are required to disambiguate.
- In complex matrices (e.g., biological tissues), many non-matrix ions may also co-localize due to common metabolic compartments, leading to high false-positive overlap flags if spatial threshold is not carefully tuned.
- isobaric detection is limited by instrument mass resolution; time-of-flight (TOF) or lower-resolution instruments may conflate structurally distinct ions as isobaric when they are actually resolved.

## Evidence

- [intro] The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The package incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions"
- [other] Perform overlapping peak detection to identify and flag isobaric or co-localized ions that may confound classification.: "Perform overlapping peak detection to identify and flag isobaric or co-localized ions that may confound classification."
- [readme] overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions: "The algorithm incorporates an overlapping peak detection feature to prevent misclassification of overlapped or isobaric ions."
- [intro] The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related: "The algorithm takes into account the chemical formula and the spatial distribution to determine which ions are matrix-related"
