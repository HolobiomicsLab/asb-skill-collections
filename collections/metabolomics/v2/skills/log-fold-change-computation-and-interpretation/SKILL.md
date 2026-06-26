---
name: log-fold-change-computation-and-interpretation
description: Use when when you have completed differential expression analysis (via
  edgeR, DESeq2, or RankProduct) on preprocessed count matrices or abundance tables
  and need to quantify and interpret the magnitude of expression changes between conditions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3223
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0203
  tools:
  - DESeq2
  - RankProd
  - ggplot2
  - ComplexHeatmap
  - edgeR
  - RankProduct
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- 'Differential expression analyss | R packages: DESeq2, edger, RankProd'
- '### DESeq2 [deseq](../modules/local/deseq2)'
- 'Genes, miRNA, isoforms, proteins, lipids | Data preprocessing | R packages: edger,
  limma, sva, ggplot2, ComplexHeatmap'
- 'R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_multiomicsintegrator_cq
    doi: 10.1093/bioadv/vbae175
    title: MultiOmicsIntegrator
  dedup_kept_from: coll_multiomicsintegrator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1093/bioadv/vbae175
  all_source_dois:
  - 10.1093/bioadv/vbae175
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# log-fold-change-computation-and-interpretation

## Summary

Computation and interpretation of log-fold-changes (log₂FC) as a quantitative measure of differential expression magnitude across omics data types (genes, miRNAs, isoforms, proteins, lipids). This skill interprets log₂FC values alongside statistical significance (adjusted p-values) to identify biologically meaningful changes in feature abundance between experimental conditions.

## When to use

When you have completed differential expression analysis (via edgeR, DESeq2, or RankProduct) on preprocessed count matrices or abundance tables and need to quantify and interpret the magnitude of expression changes between conditions. Use this skill when results tables contain raw p-values and adjusted p-values but lack biological interpretation of fold-change magnitude or when you need to generate diagnostic visualizations (volcano plots, MA plots) that combine fold-change and statistical significance.

## When NOT to use

- Input is already a processed set of biologically validated biomarkers with known effect sizes and clinical relevance; re-computation adds no new insight.
- Experimental design lacks proper replication (e.g., n=1 per condition); fold-change estimates are unreliable without variance estimation.
- Count matrices are not normalized to a common scale (e.g., raw read counts without TMM or DESeq2 size factor normalization); fold-changes will be confounded by sequencing depth.
- The research question focuses on presence/absence detection rather than quantitative magnitude of change (binary classification task).

## Inputs

- Differential expression results table (feature identifiers, fold-changes, test statistics, raw p-values, adjusted p-values)
- Preprocessed count matrix or abundance matrix (from edgeR, DESeq2, or RankProduct output)
- Sample metadata with condition/group assignments

## Outputs

- Volcano plot (−log₁₀(adjusted p-value) vs. log₂FC) with significance thresholds highlighted
- MA plot (log₂FC vs. mean log₂ abundance) showing systematic biases
- P-value distribution histogram
- Filtered results table with |log₂FC| and adjusted p-value thresholds applied
- Interpretation summary of upregulated and downregulated features by omics type

## How to apply

Extract log-fold-change (log₂FC) values from the differential expression results table, which quantifies the log₂-scaled ratio of mean abundance in the treatment group relative to the control group. Compute or retrieve adjusted p-values (typically using Benjamini-Hochberg correction) to threshold statistical significance (commonly α = 0.05). Create diagnostic plots using ggplot2 and ComplexHeatmap: (1) volcano plots plot -log₁₀(adjusted p-value) on the y-axis against log₂FC on the x-axis to simultaneously visualize effect size and significance; (2) MA plots (M = log₂(treatment/control), A = mean log₂ abundance) reveal systematic bias in fold-change estimation across abundance ranges. Interpret log₂FC values in biological context: log₂FC > 1 indicates ≥2-fold upregulation, log₂FC < -1 indicates ≥2-fold downregulation, and |log₂FC| near 0 indicates minimal change despite potential statistical significance. Filter results by joint thresholds (e.g., |log₂FC| > 1 AND adjusted p-value < 0.05) to identify robust, biologically relevant differential features.

## Related tools

- **DESeq2** (Computes log₂FC and adjusted p-values for RNA-seq and protein abundance data; outputs results tables with fold-change, test statistics, and significance thresholds.)
- **edgeR** (Estimates log₂FC via generalized linear models with negative binomial dispersion; accepts custom contrasts and formula specifications to define fold-change comparisons.)
- **RankProduct** (Ranks features by fold-change and computes rank-based p-values; used for non-parametric differential expression analysis on small sample sizes or lipid/metabolite data.)
- **ggplot2** (Generates volcano plots and MA plots to visualize log₂FC against statistical significance; enables custom aesthetic mapping and annotation of differential features.)
- **ComplexHeatmap** (Creates annotated heatmaps displaying log₂FC values across conditions and features; supports hierarchical clustering and side annotations for biological metadata.)

## Evaluation signals

- Volcano plot displays expected bimodal distribution of fold-changes: features with |log₂FC| > 1 and adjusted p-value < 0.05 are clearly separated from the background; symmetry or asymmetry matches the experimental hypothesis (upregulation vs. downregulation bias).
- MA plot shows random scatter of residuals (log₂FC) around the zero line across all abundance ranges (A-axis); systematic trend (e.g., decreasing log₂FC with increasing abundance) indicates normalization or batch effect requiring correction.
- P-value distribution is uniformly distributed for non-significant features (histogram tail approaching y=0 for p > 0.1) and shows sharp peaks near p≈0 for significant features; other distributions (e.g., bimodal, strongly right-skewed) indicate model misspecification.
- Filtered results (|log₂FC| > threshold AND adjusted p-value < α) are consistent with prior biological knowledge (e.g., known disease-associated genes, expected pathway members); no spurious high-FC features in negative control samples.
- Fold-change magnitude is concordant across replicates: box plots or scatter plots of log₂FC per replicate show consistency in sign and magnitude; coefficient of variation of log₂FC estimates across replicates is < 20% for robust features.

## Limitations

- Log₂FC estimates are unreliable for features with very low mean abundance; pseudocounts or shrinkage priors (e.g., DESeq2's lfcShrink) are required to reduce noise in fold-change estimates for weakly expressed features.
- Adjusted p-value thresholds (e.g., α = 0.05) assume independent tests and large sample sizes; with small n or correlated tests, Benjamini-Hochberg correction may be conservative, increasing false negatives.
- Joint thresholds (|log₂FC| > 1 AND p < 0.05) prioritize effect size and statistical significance but may miss biologically important features with modest fold-changes in large cohorts or very strong fold-changes in small, noisy samples.
- Log₂FC interpretation as a 2ⁿ-fold linear change assumes log-scale normalization; effects may be compressed in count-scale data and misinterpreted if non-log normalization (e.g., CPM, FPKM without log₂ transformation) is used upstream.
- Fold-change magnitude depends on choice of reference level (control vs. treatment) and scale of abundance measurement (raw counts vs. normalized); results are not directly comparable across studies using different preprocessing or reference definitions.

## Evidence

- [other] The pipeline implements dispatched differential expression analysis where users specify the algorithm via the alg_genes parameter in params_genes.yml (defaulting to 'edger'), with each algorithm (edgeR, DESeq2, RankProduct) requiring specific samplesheet column conventions: "each algorithm (edgeR, DESeq2, RankProduct) requiring specific samplesheet column conventions: edgeR uses 'condition' for grouping and accepts custom formula/contrasts; DESeq2 requires columns named"
- [other] Results include feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values: "Generate a results table containing feature identifiers, fold-changes, test statistics, raw p-values, and adjusted p-values"
- [other] Diagnostic plots are generated using ggplot2 and ComplexHeatmap: "Create diagnostic plots (volcano plot, MA plot, p-value distribution) using ggplot2 and ComplexHeatmap"
- [other] Differential expression analysis is performed on preprocessed count matrices: "Execute the selected algorithm (edgeR, DESeq2, or RankProduct via their R package implementations) using sample group assignments from the required samplesheet column"
- [methods] Pipeline performs differential expression analysis across multiple omics types: "Genes, miRNA, isoforms, proteins, lipids | Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap"
