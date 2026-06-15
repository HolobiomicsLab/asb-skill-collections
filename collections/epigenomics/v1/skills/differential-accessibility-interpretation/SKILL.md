---
name: differential-accessibility-interpretation
description: Use when after identifying differentially accessible peaks (via tl.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0239
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_0202
  - http://edamontology.org/topic_3169
  tools:
  - SnapATAC2
  - tl.diff_test
  - datasets.cis_bp
  - Python
  - tl.motif_enrichment
  - CIS-BP
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- tl.marker_regions, tl.diff_test for differential analysis
- datasets.cis_bp
- A Python/Rust package for single-cell epigenomics analysis
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_snapatac2
    doi: 10.1038/s41592-023-02139-9
    title: snapatac2
  dedup_kept_from: coll_snapatac2
schema_version: 0.2.0
---

# differential-accessibility-interpretation

## Summary

Interpret differentially accessible peaks from single-cell ATAC-seq data by applying motif enrichment analysis to identify overrepresented transcription factor binding motifs in peak regions that distinguish cell types or conditions. This skill bridges differential testing results to regulatory mechanism discovery.

## When to use

After identifying differentially accessible peaks (via tl.diff_test) between cell populations or conditions in single-cell ATAC-seq data, use this skill to uncover which transcription factors may be driving the observed chromatin accessibility differences and to validate that differential regions are biologically meaningful and not artifacts.

## When NOT to use

- Input is a count matrix or raw accessibility matrix rather than a pre-computed set of differentially accessible peaks with significance values.
- Downstream goal is protein-level validation or regulatory network inference without intermediate motif interpretation.
- Peak set is too small (<100 peaks) or filtered by arbitrary thresholds rather than statistical testing; enrichment statistics become unreliable.

## Inputs

- differentially accessible peak set with p-values and test statistics (output from tl.diff_test)
- CIS-BP motif database with position-weight matrices (datasets.cis_bp)
- genome reference for background peak set or accessibility model

## Outputs

- motif enrichment table with columns: motif ID, motif name, enrichment score, p-value, adjusted p-value
- ranked list of overrepresented transcription factor binding motifs
- statistical significance metrics for each motif

## How to apply

Load the set of differentially accessible peaks (output from tl.diff_test, typically with p-values and fold-change statistics) as a feature set into SnapATAC2. Retrieve motif definitions and position-weight matrices from the CIS-BP motif database via datasets.cis_bp. Invoke tl.motif_enrichment on the peak set, which scans for motif occurrences within differential regions and computes enrichment statistics (e.g., enrichment scores, p-values) against a background model derived from accessible chromatin. Retrieve the resulting motif enrichment table and validate that all required columns (motif IDs, enrichment scores, p-values) are present and non-null, with p-values reflecting statistical significance of motif overrepresentation. Sort by adjusted p-value or enrichment score to prioritize candidate regulatory factors for downstream validation.

## Related tools

- **SnapATAC2** (single-cell ATAC-seq analysis framework providing tl.motif_enrichment, tl.diff_test, and CIS-BP dataset access) — https://github.com/scverse/SnapATAC2
- **tl.motif_enrichment** (core function that performs motif scanning and enrichment statistics computation on peak regions)
- **tl.diff_test** (produces differentially accessible peak set with p-values and statistics used as input to motif enrichment)
- **datasets.cis_bp** (provides curated motif database with position-weight matrices required for motif scanning)
- **CIS-BP** (motif definition and position-weight matrix resource referenced by datasets.cis_bp)

## Evaluation signals

- All rows in the output motif enrichment table have non-null values for motif ID, enrichment score, and p-value.
- P-values and adjusted p-values are in the range [0, 1] and follow expected multiple-testing correction (e.g., Benjamini–Hochberg).
- Top-ranked motifs (by p-value or enrichment score) correspond to known transcription factors relevant to the cell types or conditions being compared (cross-check with literature or known regulatory networks).
- Enrichment scores show expected directionality: motifs enriched in accessible peaks from cell type A but depleted in cell type B should have higher enrichment scores in the differential peak set specific to cell type A.
- Background model and foreground peak set are appropriately matched (e.g., same genome reference, same cell type universe) to avoid spurious enrichment from confounding accessibility patterns.

## Limitations

- Motif enrichment reflects motif sequence occurrence, not actual transcription factor binding or activity; false positives can arise if related motif families are overrepresented by chance.
- CIS-BP database covers vertebrate and some plant transcription factors; coverage is incomplete for non-model organisms or poorly annotated species.
- Peak set must be large enough for statistical power; small or highly filtered differential peak sets may yield unreliable p-values.
- Background model assumptions (e.g., uniform nucleotide distribution, independence between motifs) can bias enrichment scores if not validated against the study-specific chromatin landscape.
- Motif enrichment does not account for regulatory context such as 3D chromatin structure, nucleosome positioning, or cofactor availability.

## Evidence

- [other] Invoke tl.motif_enrichment on the peak set, scanning for motif occurrences within differential regions and computing enrichment statistics against a background model.: "Invoke tl.motif_enrichment on the peak set, scanning for motif occurrences within differential regions and computing enrichment statistics against a background model."
- [other] Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight matrices.: "Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight matrices."
- [other] Validate that all required columns are present and non-null, and that p-values reflect the statistical significance of motif overrepresentation.: "Validate that all required columns are present and non-null, and that p-values reflect the statistical significance of motif overrepresentation."
- [methods] tl.motif_enrichment for motif analysis: "tl.motif_enrichment for motif analysis"
- [readme] End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory network analysis.: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory"
