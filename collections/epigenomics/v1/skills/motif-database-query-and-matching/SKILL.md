---
name: motif-database-query-and-matching
description: Use when you have a set of differentially accessible peaks (output from differential accessibility testing, e.g., tl.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0239
  edam_topics:
  - http://edamontology.org/topic_0749
  - http://edamontology.org/topic_3674
  tools:
  - SnapATAC2
  - tl.motif_enrichment
  - tl.diff_test
  - datasets.cis_bp
  - Python
derived_from:
- doi: 10.1038/s41592-023-02139-9
  title: snapatac2
evidence_spans:
- 'SnapATAC2: A Python/Rust package for single-cell epigenomics analysis'
- tl.motif_enrichment for motif analysis
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

# motif-database-query-and-matching

## Summary

Query a curated motif database (e.g., CIS-BP) and match motif position-weight matrices (PWMs) against a set of DNA sequences (typically differentially accessible peaks from single-cell ATAC-seq). This skill produces motif occurrence calls and enrichment statistics that identify transcription factor binding sites overrepresented in the input peak set.

## When to use

You have a set of differentially accessible peaks (output from differential accessibility testing, e.g., tl.diff_test) from single-cell ATAC-seq data and want to identify which transcription factor motifs are overrepresented in those peaks relative to a background model, to infer regulatory drivers of chromatin accessibility changes.

## When NOT to use

- Input peaks have not been validated for reproducibility or consistency; enrichment results on noisy peak sets will be unreliable.
- Background model or motif database is not appropriate for the organism or cell type (e.g., using a vertebrate motif database on plant ATAC-seq data).
- You are interested only in de novo motif discovery rather than matching against known databases.

## Inputs

- Differentially accessible peak set (BED-like format or genomic interval set)
- Motif position-weight matrix (PWM) library from CIS-BP or equivalent curated database

## Outputs

- Motif enrichment table (columns: motif ID, TF name, enrichment score, p-value, q-value)
- Peak-motif match annotation (which motifs occur in which peaks)

## How to apply

Load differentially accessible peaks as a feature set into SnapATAC2. Retrieve motif position-weight matrices from a curated motif database (datasets.cis_bp provides the CIS-BP dataset). Invoke tl.motif_enrichment on the peak set; the function scans for motif occurrences within the differential regions and computes enrichment statistics (typically log-odds ratios or similar) against a background model. Validate the output motif enrichment table for required columns (motif IDs, enrichment scores, p-values), non-null values, and statistical significance thresholds (typically p < 0.05). The resulting table ranks motifs by overrepresentation, allowing prioritization of candidate regulatory transcription factors.

## Related tools

- **SnapATAC2** (Provides tl.motif_enrichment function, datasets.cis_bp database loader, and integration with tl.diff_test for differential peak analysis) — https://github.com/scverse/SnapATAC2
- **tl.motif_enrichment** (Core function that performs motif occurrence scanning and enrichment statistic computation against background model) — https://github.com/scverse/SnapATAC2
- **datasets.cis_bp** (Loads CIS-BP motif database with position-weight matrices and motif definitions) — https://github.com/scverse/SnapATAC2
- **tl.diff_test** (Identifies differentially accessible peaks that serve as input to motif enrichment) — https://github.com/scverse/SnapATAC2

## Examples

```
import snapatac2 as snap; peaks = snap.tl.diff_test(adata, groupby='cell_type'); motifs = snap.datasets.cis_bp(); enrichment = snap.tl.motif_enrichment(peaks, motif_matrix=motifs)
```

## Evaluation signals

- Motif enrichment table contains all expected columns (motif ID, enrichment score, p-value) with non-null values.
- P-values are in valid range [0, 1] and reflect expected statistical distribution under null hypothesis.
- Top-ranked motifs correspond to known regulators of chromatin accessibility in the cell type or biological context (literature validation).
- Enrichment scores are interpretable (e.g., log-odds ratio or z-score) and correlate with motif frequency in the peak set.
- Results are reproducible across independent runs and consistent with complementary differential analysis (e.g., tl.marker_regions on the same peaks).

## Limitations

- Motif enrichment depends on quality and completeness of the reference PWM database; missing or poorly-annotated motifs will not be detected.
- Background model assumptions (e.g., uniform nucleotide distribution, motif independence) may not hold for all genomic regions; peak set-specific background may yield different results.
- Motif matching is sequence-based only; does not account for chromatin accessibility, cofactor binding, or 3D chromatin structure that may modulate actual TF occupancy.
- Multiple hypothesis testing correction (q-value computation) assumes independence of motif tests, which may be violated for similar or degenerate motif PWMs.

## Evidence

- [other] Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight matrices: "Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight matrices."
- [other] Invoke tl.motif_enrichment on the peak set, scanning for motif occurrences within differential regions and computing enrichment statistics: "Invoke tl.motif_enrichment on the peak set, scanning for motif occurrences within differential regions and computing enrichment statistics against a background model."
- [other] Retrieve the resulting motif enrichment table containing motif IDs, enrichment scores, and p-values: "Retrieve the resulting motif enrichment table containing motif IDs, enrichment scores, and p-values."
- [methods] tl.motif_enrichment for motif analysis: "tl.motif_enrichment for motif analysis"
- [readme] End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory network analysis: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis, regulatory"
