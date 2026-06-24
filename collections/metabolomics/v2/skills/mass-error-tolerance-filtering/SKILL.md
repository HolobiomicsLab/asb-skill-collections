---
name: mass-error-tolerance-filtering
description: 'Use when when annotating full-scan MS or MS imaging data against a metabolite
  database (e.g., LipidMaps, HMDB) and you need to control the stringency of m/z matching.
  Use this filter to balance annotation sensitivity against specificity: tighter ppm
  tolerances (e.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - SpaMTP
  - R
  - Seurat
  - Cardinal
  techniques:
  - MS-imaging
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.10.31.621429v1
  title: SpaMTP
- doi: 10.1101/2024.10.14.618269
  title: ''
evidence_spans:
- Install SpaMTP if not previously installed devtools::install_github("GenomicsMachineLearning/SpaMTP")
- For plotting + DE plots
- '## Install and Import *R* Libraries'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_spamtp_cq
    doi: 10.1101/2024.10.31.621429v1
    title: SpaMTP
  dedup_kept_from: coll_spamtp_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.10.31.621429v1
  all_source_dois:
  - 10.1101/2024.10.31.621429v1
  - 10.1101/2024.10.14.618269
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-error-tolerance-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Applies a parts-per-million (ppm) error threshold during metabolite annotation to match experimental m/z values against a reference database, accepting only matches within the specified mass tolerance. This filter reduces false-positive annotations by rejecting candidates whose theoretical m/z deviates beyond the tolerance window.

## When to use

When annotating full-scan MS or MS imaging data against a metabolite database (e.g., LipidMaps, HMDB) and you need to control the stringency of m/z matching. Use this filter to balance annotation sensitivity against specificity: tighter ppm tolerances (e.g., 5 ppm for high-resolution instruments) reduce spurious matches but may miss real metabolites; looser tolerances (e.g., 15 ppm) capture more candidates but increase false positives. The choice depends on your instrument's mass accuracy and the annotation database's depth.

## When NOT to use

- Input data has already been annotated and you are only refining results post hoc (use RefineLipids or SearchAnnotations instead).
- You lack instrument-specific mass accuracy information and cannot justify a ppm threshold; consider running multiple thresholds and comparing results.
- Your reference database is known to have large systematic m/z offsets or calibration errors; recalibrate the database first.

## Inputs

- SpaMTP Seurat object with m/z features loaded from intensity matrix
- reference metabolite database (e.g., Lipidmaps_db, HMDB_db) with theoretical m/z values
- numeric ppm_error parameter (e.g., 5, 10, 15)

## Outputs

- SpaMTP Seurat object with feature metadata slot populated with filtered metabolite annotations
- annotation summary table containing m/z values and corresponding metabolite names/IDs within the ppm window

## How to apply

Before or during the AnnotateSM function call in SpaMTP, specify the ppm_error parameter as a numeric value representing the maximum acceptable mass deviation in parts per million. The function calculates the ppm error as |observed_mz − theoretical_mz| / theoretical_mz × 10^6 for each m/z feature against all database entries. Only metabolites whose theoretical m/z falls within ±ppm_error of the observed m/z are retained as candidates. Combine with adduct specification (e.g., 'M+K', 'M+H') to account for ionization mode. The rationale is that modern high-resolution MS instruments (e.g., Orbitrap, TOF) achieve typical mass accuracies of 2–5 ppm, while lower-resolution instruments may require 10–15 ppm; the threshold should reflect your hardware's capability and your annotation goal (discovery vs. validation).

## Related tools

- **SpaMTP** (primary R package housing the AnnotateSM function and ppm_error parameter; applies the mass-error filter during metabolite annotation workflow) — https://github.com/GenomicsMachineLearning/SpaMTP
- **Seurat** (underlying class object (Seurat) used to store m/z features, annotations, and metadata; ppm filtering results are stored in feature metadata slot)
- **Cardinal** (complementary mass spectrometry imaging R package; SpaMTP inherits imaging data structures and can interoperate with Cardinal for MS imaging workflows) — https://github.com/Vitek-Lab/Cardinal3-vignettes

## Examples

```
bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15, adducts = 'M+K')
```

## Evaluation signals

- Count of successfully annotated m/z features increases monotonically as ppm_error tolerance widens (e.g., ppm=5 yields fewer annotations than ppm=15).
- All retained annotations have calculated ppm error ≤ the specified ppm_error threshold; verify by inspecting feature metadata.
- No m/z features are lost from the input object; annotation simply adds or witholds metadata for each feature depending on whether a match exists within the tolerance.
- Annotation coverage and specificity trade-off is sensible: very tight ppm (e.g., 2 ppm) on a lower-resolution instrument may yield zero or very few annotations, while very loose ppm (e.g., 50 ppm) may produce multi-match ambiguities.
- Results are reproducible and stable across repeated runs with identical ppm_error and adduct parameters.

## Limitations

- ppm tolerance is a one-dimensional filter; does not account for adduct complexity, isotopologue overlap, or in-source fragmentation—may require downstream refinement via MS/MS matching (noted as 'To come!' in the article) or paired targeted metabolic data.
- Database-dependent: if the reference database lacks an entry for a metabolite present in the sample, no annotation will occur regardless of ppm threshold.
- Instrument-specific mass accuracy assumptions may not hold across different sample matrices or ionization conditions; ppm threshold should be validated empirically for each new dataset or instrument configuration.
- Multiple metabolites may share the same theoretical m/z within the ppm window, creating ambiguous assignments; disambiguation requires additional orthogonal data (tandem MS, retention time, pathway context).

## Evidence

- [methods] ppm_error = 15, adducts = "M+K": "ppm_error = 15, adducts = "M+K""
- [methods] bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15: "bladder_annotated <- AnnotateSM(bladder, db = Lipidmaps_db, ppm_error = 15"
- [other] AnnotateSM function with parameters: db=Lipidmaps_db, ppm_error=15, adducts='M+K', polarity='positive': "AnnotateSM function with parameters: db=Lipidmaps_db, ppm_error=15, adducts='M+K', polarity='positive'"
- [readme] mass-to-charge ratio (m/z) metabolite annotation: "mass-to-charge ratio (m/z) metabolite annotation"
- [other] Extract the count of successfully annotated m/z features from the returned SpaMTP object: "Extract the count of successfully annotated m/z features from the returned SpaMTP object"
