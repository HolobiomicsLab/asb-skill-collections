---
name: matrix-equivalence-validation
description: Use when you have generated gene-level count matrices via two methodologically distinct routes—e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3233
  edam_topics:
  - http://edamontology.org/topic_3170
  - http://edamontology.org/topic_0203
  tools:
  - tximport
  - readr
  - summarizeToGene
  - all.equal
derived_from:
- doi: 10.12688/f1000research.7563.1
  title: tximport
evidence_spans:
- Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages
- Importing transcript abundance with tximport
- While tximport works without any dependencies, it is significantly faster to read in files using the readr package
- significantly faster to read in files using the readr package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/transcriptomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_tximport
    doi: 10.12688/f1000research.7563.1
    title: tximport
  dedup_kept_from: coll_tximport
schema_version: 0.2.0
---

# matrix-equivalence-validation

## Summary

Verify that two alternative computational pathways for generating gene-level count matrices produce identical numerical outputs. This skill validates workflow correctness by confirming that transcript-level summarization followed by gene-level aggregation yields the same result as direct gene-level import.

## When to use

Apply this skill when you have generated gene-level count matrices via two methodologically distinct routes—e.g., (1) importing transcript-level estimates via tximport with txOut=TRUE and then applying summarizeToGene, versus (2) importing directly at gene level via tximport with txOut=FALSE—and need to confirm that downstream statistical analyses will not be affected by which pathway was chosen. This is particularly important when deciding whether to retain transcript-level detail for isoform analysis or compress directly to gene level.

## When NOT to use

- If your analysis requires transcript-level differential expression or isoform quantification—equivalence validation does not address whether transcript-level or gene-level analysis is more appropriate for your biological question.
- If your tx2gene mapping contains errors or misses transcripts present in the quantification files; validation will fail but will not diagnose the root cause of the mapping problem.
- If you are comparing counts matrices from different quantification methods (e.g., salmon vs. kallisto) or different reference annotations; this skill validates consistency within a single workflow, not across disparate sources.

## Inputs

- salmon quantification output files (quant.sf) from multiple samples
- tx2gene data.frame (transcript-to-gene mapping with columns for transcript ID and gene ID)
- tximport object with txOut=TRUE (transcript-level abundance, counts, length matrices)
- tximport object with txOut=FALSE (gene-level abundance, counts, length matrices)

## Outputs

- Boolean equivalence result (TRUE/FALSE from all.equal() comparison)
- Confirmation that gene-level count matrices are identical between two import pathways
- Optionally, summary statistics showing matrix dimensions and sample of count values

## How to apply

Load the same upstream quantification files (e.g., salmon output) using tximport twice: first with txOut=TRUE to capture transcript-level abundance, counts, and length matrices, then apply summarizeToGene with the tx2gene mapping to collapse to gene level; second with txOut=FALSE (default) to generate gene-level matrices in a single operation. Use the all.equal() function to compare the resulting gene-level count matrices element-wise, checking for numerical identity within machine precision. If all.equal() returns TRUE, the two workflows are equivalent and either may be used depending on downstream analysis needs (transcript-level detail vs. computational efficiency). Examine the tx2gene mapping carefully to ensure it correctly associates every transcript ID in your quantification output with a unique gene ID, as mismatched annotations will produce discrepancies.

## Related tools

- **tximport** (Primary tool for importing transcript-level or gene-level quantification matrices from salmon/sailfish/kallisto output with configurable txOut parameter to control summarization level) — https://github.com/thelovelab/tximport
- **summarizeToGene** (Function applied to txOut=TRUE output to collapse transcript-level matrices to gene level using tx2gene mapping) — https://github.com/thelovelab/tximport
- **readr** (Optional but recommended for faster file I/O when reading quantification files prior to tximport)
- **all.equal** (R base function used to test numerical equivalence of two count matrices with tolerance for floating-point precision)

## Examples

```
txi_tx <- tximport(salmon_files, type='salmon', tx2gene=tx2gene, txOut=TRUE); txi_gene_via_summarize <- summarizeToGene(txi_tx, tx2gene); txi_gene_direct <- tximport(salmon_files, type='salmon', tx2gene=tx2gene, txOut=FALSE); all.equal(txi_gene_via_summarize$counts, txi_gene_direct$counts)
```

## Evaluation signals

- all.equal() returns TRUE with no reported differences between the two gene-level count matrices
- Matrix dimensions (genes × samples) are identical between txOut=TRUE + summarizeToGene and txOut=FALSE outputs
- Sample-wise row sums (total counts per gene) are identical or differ only by machine epsilon (< 1e-12 relative difference)
- No NAs or NaNs are introduced in either pathway; missing values occur in the same positions if at all
- Gene IDs and sample names are preserved and match across both outputs, confirming no reordering occurred

## Limitations

- Equivalence validation does not determine which pathway is biologically or statistically appropriate; it only confirms computational consistency. Transcript-level vs. gene-level analysis decisions must be driven by the research question.
- Floating-point rounding may introduce negligible differences (< 1e-12) that all.equal() tolerates by default but could accumulate downstream in iterative statistical algorithms; inspect numeric_tol if higher precision is critical.
- This skill requires a high-quality, comprehensive tx2gene mapping; if transcripts are missing from the mapping or gene assignments are incorrect, the validation will fail silently as a FALSE result rather than diagnosing the annotation error.
- The skill applies only to count matrices; length-based offset matrices (used for correcting differential isoform usage) may differ between txOut=TRUE+summarize and txOut=FALSE paths if isoform composition varies across samples, and separate validation is needed for those matrices.

## Evidence

- [other] Equivalence of two pathways confirmed by all.equal() comparison: "Gene-level count matrices derived from transcript-level tximport output (txOut=TRUE) followed by summarizeToGene are identical to those produced by direct gene-level tximport (txOut=FALSE), as"
- [other] Workflow pathway 1: transcript-level import with summarization: "Load salmon quantification output files and a tx2gene data.frame (transcript-to-gene mapping) using tximport with type='salmon' and txOut=TRUE to retain transcript-level abundance, counts, and length"
- [other] Workflow pathway 2: direct gene-level import: "Load the same salmon files directly using tximport with txOut=FALSE (default) to generate gene-level matrices in a single step."
- [intro] Core purpose of tximport tool: "Imports transcript-level abundance, estimated counts and transcript lengths, and summarizes into matrices for use with downstream statistical analysis packages"
- [intro] Length matrix for downstream offset correction: "Average transcript length, weighted by sample-specific transcript abundance estimates, is provided as a matrix which can be used as an offset for different expression of gene-level counts."
