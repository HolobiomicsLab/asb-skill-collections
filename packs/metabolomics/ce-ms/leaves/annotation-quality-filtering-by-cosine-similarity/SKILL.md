---
name: annotation-quality-filtering-by-cosine-similarity
description: Use when you have in silico annotations (e.g. from GNPS, timaR, or SIRIUS)
  paired with experimental MS/MS spectra and need to select only the highest-confidence
  structural matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - MZmine2
  - MZmine3
  - timaR
  - GNPS
  - Inventa
  techniques:
  - CE-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.3389/fmolb.2022.1028334
  title: Inventa
- doi: 10.1038/s41467-021-23953-9
  title: ''
evidence_spans:
- MZmine output format using only the 'Peak area', 'row m/z' and 'row retention time'
  columns. -Inventa takes input directly from MZmine2
- Inventa takes input directly from MZmine2 or MZmine 3
- -Inventa takes input directly from MZmine2 or [MZmine 3](http://mzmine.github.io/),
  is possible to use other processing sofwares
- 'tima_results_filename: timaR reponderated output format. - for performing in silico
  annotations and taxonomically informed reponderation.'
- 'tima_results_filename: timaR reponderated output format'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_inventa_cq
    doi: 10.3389/fmolb.2022.1028334
    title: Inventa
  dedup_kept_from: coll_inventa_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.3389/fmolb.2022.1028334
  all_source_dois:
  - 10.3389/fmolb.2022.1028334
  - 10.1038/s41467-021-23953-9
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# annotation-quality-filtering-by-cosine-similarity

## Summary

Filter in silico metabolite annotations by applying a minimum cosine similarity threshold to MS/MS spectral matches, retaining only high-confidence structural assignments. This is a critical quality-control step in metabolomics pipelines that reduces false positive annotations before downstream analysis such as feature component or priority scoring.

## When to use

You have in silico annotations (e.g. from GNPS, timaR, or SIRIUS) paired with experimental MS/MS spectra and need to select only the highest-confidence structural matches. Cosine similarity filtering is especially important when integrating multiple annotation sources or when the downstream analysis (e.g. Feature Component calculation, chemical class assignment) depends on reliable annotation status to distinguish annotated from unannotated features.

## When NOT to use

- You have only MS1 (precursor m/z) annotations without MS/MS fragmentation data; cosine similarity requires MS/MS spectra.
- Your annotation source does not provide or report cosine similarity scores (e.g. some database formats or custom in silico tools).
- You are performing exploratory, hypothesis-generating analysis where you want to retain lower-confidence hits; cosine filtering prioritizes specificity over sensitivity.

## Inputs

- Annotation results table with cosine_score column (e.g. from GNPS, timaR, or spectral library matching)
- Reference MS/MS spectra (implied; used to compute cosine scores)
- Experimental MS/MS spectra (implied; basis for annotation matching)

## Outputs

- Filtered annotation table (subset of input where cosine_score >= threshold)
- Annotation retention/rejection statistics (count of passing vs. filtered records)

## How to apply

Load the annotation results table (e.g. timaR output or GNPS library match table) and extract the cosine score column. Apply a minimum cosine threshold (e.g. cosine ≥ 0.7) as a binary filter: retain only rows where cosine_score >= your chosen cutoff, discard the rest. The rationale is that cosine similarity directly measures the overlap between the experimental MS/MS fragmentation pattern and the database reference spectrum; higher values indicate more reliable spectral matches. This filter is typically applied in conjunction with other annotation quality criteria (ppm error, shared peaks count, ionization mode matching) to create a conservative, high-confidence annotation set. Document the threshold you apply and the number of annotations retained versus discarded.

## Related tools

- **GNPS** (Source of library matching results with cosine similarity scores for experimental spectra)
- **timaR** (Performs taxonomically informed in silico annotation with cosine score output for filtering) — https://taxonomicallyinformedannotation.github.io/tima-r/index.html
- **Inventa** (Applies cosine score filtering as part of annotation quality control before Feature Component calculation) — https://github.com/luigiquiros/inventa

## Evaluation signals

- Verify that all retained annotations have cosine_score >= the declared threshold; spot-check a sample of filtered-out records to confirm they fall below threshold.
- Compare the count of annotations before and after filtering; a reasonable retention rate is typically 50–90% depending on data quality and threshold stringency.
- Inspect the distribution of cosine scores in the retained set (e.g. via histogram or summary statistics) to confirm they cluster in the high-confidence range.
- Confirm that retained annotations are used consistently in downstream steps (e.g. Feature Component marking, Chemical Class assignment) with no residual low-cosine records.
- Cross-validate with other annotation metrics (ppm error, shared peaks) to ensure cosine filtering is congruent with and complementary to those filters, not contradictory.

## Limitations

- Cosine similarity is sensitive to spectral noise and database spectrum quality; two chemically identical compounds with poor-quality reference spectra may yield low cosine scores.
- The optimal cosine threshold is context-dependent (instrument type, ionization mode, collision energy) and may require empirical tuning; a threshold of 0.7 is conventional but not universal.
- Cosine filtering alone does not account for m/z accuracy, retention time, or biological plausibility; it should be combined with ppm error, shared peaks count, and other filters.
- Low-abundance features or rare metabolites may have weak MS/MS spectra that fail to achieve high cosine matches even if the annotation is correct; filtering may inadvertently exclude valid discoveries.

## Evidence

- [other] cosine = 0.7 # min cosine score to consider an annotation valable: "cosine = 0.7 # min cosine score to consider an annotation valable"
- [other] Filter ISDB annotations by ppm_error (e.g., 5 ppm), shared_peaks (e.g., 10), cosine score (e.g., 0.7), and min_score_final threshold: "Filter ISDB annotations by ppm_error (e.g., 5 ppm), shared_peaks (e.g., 10), cosine score (e.g., 0.7), and min_score_final threshold"
- [other] For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks: "For cleaning-up annotations from GNPS ppm_error = 5 # min error in ppm to consider an annotation valable shared_peaks = 10 # min number of shared peaks"
