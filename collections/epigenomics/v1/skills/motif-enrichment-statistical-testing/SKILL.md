---
name: motif-enrichment-statistical-testing
description: Use when after identifying a set of differentially accessible peaks (via tl.diff_test or equivalent), when you need to infer which transcription factors may regulate the observed chromatin state changes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0438
  edam_topics:
  - http://edamontology.org/topic_0654
  - http://edamontology.org/topic_0621
  - http://edamontology.org/topic_3169
  tools:
  - SnapATAC2
  - tl.motif_enrichment
  - tl.diff_test
  - datasets.cis_bp
  - Python
  - Scanpy
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

# motif-enrichment-statistical-testing

## Summary

Statistical testing of transcription factor binding motif enrichment in differentially accessible chromatin peaks using position-weight matrices and background models. This skill quantifies whether specific DNA motifs are overrepresented in a peak set relative to a null distribution, producing enrichment scores and p-values to identify functionally relevant regulatory factors.

## When to use

After identifying a set of differentially accessible peaks (via tl.diff_test or equivalent), when you need to infer which transcription factors may regulate the observed chromatin state changes. Apply this skill when you have peak coordinates, a motif database (such as CIS-BP), and seek statistical evidence of motif overrepresentation to guide downstream regulatory network analysis.

## When NOT to use

- Peak set lacks sufficient genomic annotation or quality control filtering—validate peak reproducibility and signal-to-noise ratio before enrichment analysis.
- Motif database is not curated for the target organism or tissue; mismatched PWM libraries will introduce false positives and reduce interpretability.
- Input peaks are already annotated with regulatory elements (e.g., promoters, enhancers from ChIP-seq); use ChIP-seq peaks directly instead for higher resolution.

## Inputs

- Peak coordinate set (GRanges or BED-like object)
- Differentially accessible peaks (output from tl.diff_test)
- Motif position-weight matrix (PWM) database
- Reference genome sequence (FASTA or indexed)

## Outputs

- Motif enrichment table (rows=motifs, columns=motif ID, enrichment score, p-value, FDR)
- Motif occurrence map (motif coordinates within peaks)
- Statistical summary (global false discovery rate, significance threshold)

## How to apply

Load differentially accessible peaks as a feature set into SnapATAC2. Retrieve motif definitions and position-weight matrices from a reference database (e.g., datasets.cis_bp for CIS-BP). Invoke tl.motif_enrichment on the peak set, which scans for motif occurrences within the differential regions and computes enrichment statistics by comparing observed motif counts against a background model (typically peaks from the genome or matched by length/GC content). The function returns a motif enrichment table with motif IDs, enrichment scores (e.g., log-odds or fold-change), and statistical p-values. Validate that all required columns are present and non-null, and interpret p-values as measures of the statistical significance of motif overrepresentation after multiple-hypothesis correction (e.g., Benjamini–Hochberg FDR).

## Related tools

- **SnapATAC2** (Core framework providing tl.motif_enrichment function and AnnData-based data structures for storing peaks and enrichment results) — https://github.com/scverse/SnapATAC2
- **tl.diff_test** (Upstream method for identifying differentially accessible peaks that serve as input to motif enrichment analysis) — https://github.com/scverse/SnapATAC2
- **datasets.cis_bp** (CIS-BP motif database loader providing curated position-weight matrices for enrichment scanning) — https://github.com/scverse/SnapATAC2
- **Python** (Programming language for SnapATAC2 API and motif enrichment computation)
- **Scanpy** (Integrated single-cell analysis package for seamless data handling and visualization of motif enrichment results)

## Examples

```
import snapatac2 as sa; import snapatac2.datasets as datasets; peaks = adata.var[adata.var['diff_significant']]; pwm_db = datasets.cis_bp(); sa.tl.motif_enrichment(peaks=peaks, motif_db=pwm_db, genome='hg38', output_file='motif_enrichment.tsv')
```

## Evaluation signals

- Motif enrichment table contains non-null entries for all required columns (motif ID, enrichment score, p-value, FDR) with no NaN values in statistical columns.
- P-values follow a uniform or enriched distribution; genome-wide significance is confirmed by FDR-corrected p-values (e.g., FDR < 0.05) for top enriched motifs.
- Enrichment scores are consistent with motif occurrence frequency: motifs present in >5% of peaks should show detectable enrichment versus background; absence of enrichment in rare motifs confirms proper background modeling.
- Motif occurrences are spatially localized to peak summits or promoter-proximal regions; randomly distributed motifs within peaks suggest model miscalibration.
- Known regulatory factors for the cell type or condition are present in the top-ranked enriched motifs (e.g., pioneer factors in chromatin remodeling peaks), validating biological plausibility.

## Limitations

- Motif enrichment depends critically on database quality and completeness; orphan or tissue-specific transcription factors absent from CIS-BP will not be detected.
- Background model assumptions (e.g., matched-length or genome-wide nucleotide composition) may not capture local chromatin context; enrichment scores are relative and not absolute.
- Multiple-hypothesis correction (FDR) becomes stringent with large motif databases; borderline significant motifs (FDR 0.05–0.20) may represent true but weak regulatory associations.
- Overlapping or degenerate motif families can inflate apparent enrichment; post-hoc motif deconvolution or clustering may be required to identify the true causal factor.

## Evidence

- [other] Reconstructing motif enrichment analysis using tl.motif_enrichment with CIS-BP dataset: "Reconstruct motif enrichment analysis using tl.motif_enrichment with the CIS-BP dataset"
- [other] What output does the motif enrichment function produce: "What output does the motif enrichment function (tl.motif_enrichment) produce when applied to differentially accessible peaks?"
- [other] How the workflow operates: "Load differentially accessible peaks (output from tl.diff_test) as a feature set into SnapATAC2. Load the CIS-BP motif database using datasets.cis_bp to obtain motif definitions and position-weight"
- [other] Output validation requirements: "Retrieve the resulting motif enrichment table containing motif IDs, enrichment scores, and p-values. Validate that all required columns are present and non-null, and that p-values reflect the"
- [methods] Motif analysis in workflow: "tl.motif_enrichment for motif analysis"
- [intro] End-to-end pipeline scope: "End-to-end analysis pipeline for single-cell ATAC-seq data, including preprocessing, dimension reduction, clustering, data integration, peak calling, differential analysis, motif analysis"
