---
name: p-value-cutoff-threshold-filtering
description: Use when after differential expression analysis (DEA) has produced p-values
  and log fold-change values for multiple omics layers (genes, miRNA, proteins, lipids),
  and you need to select only statistically significant features for pathway enrichment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0203
  - http://edamontology.org/topic_3391
  - http://edamontology.org/topic_0602
  tools:
  - clusterProfiler
  - biotranslator
  - ggplot2
  - ComplexHeatmap
  - DESeq2
  - edgeR
  - limma
  license_tier: open
derived_from:
- doi: 10.1093/bioadv/vbae175
  title: MultiOmicsIntegrator
evidence_spans:
- Pathway enrichment analysis | Clusterprofiler, Biotranslator
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

# p-value-cutoff-threshold-filtering

## Summary

Apply configurable p-value thresholds to filter statistically significant features (genes, miRNA, proteins, lipids) before pathway enrichment analysis in multi-omics workflows. This skill ensures only features meeting study-specific significance criteria are forwarded to downstream annotation tools.

## When to use

After differential expression analysis (DEA) has produced p-values and log fold-change values for multiple omics layers (genes, miRNA, proteins, lipids), and you need to select only statistically significant features for pathway enrichment. Use this skill when different omics layers require different significance thresholds (e.g., genes at p < 1.0, lipids at p < 0.5) as configured in the pipeline parameters.

## When NOT to use

- Input is already a pre-filtered or curated feature set (e.g., from a prior study or manually validated list)—apply this skill only to raw DEA output.
- P-value thresholds have not been defined or justified for your omics layer or biological context—defer filtering until appropriate cutoffs are established by domain experts or prior literature.
- You intend to perform unsupervised pathway analysis or machine-learning-based feature selection that explicitly requires unfiltered feature ranks—this skill is for significance-based filtering only.

## Inputs

- DEA results table (genes, miRNA, proteins, or lipids) with p-value and log fold-change columns
- Pipeline parameter file (params.yml) containing omics-layer-specific p-value cutoff thresholds
- Feature identifier list (gene symbols, miRNA accessions, protein IDs, or lipid names)

## Outputs

- Filtered feature list (subset of input features meeting p-value threshold)
- Feature identifiers formatted for downstream enrichment tool input
- Count of retained vs. filtered features (summary statistics)

## How to apply

Load the DEA output table containing p-values and log fold-change values for each feature layer. Read the omics-specific p-value cutoff thresholds from the pipeline configuration file (params.yml), which stores separate thresholds for genes_genespval, mirna_genespval, proteins_genespval, and lipids_genespval. For each feature layer, apply a row-wise filter retaining only rows where the p-value column is less than or equal to the corresponding configured threshold. Pass the filtered feature lists (gene IDs, miRNA IDs, protein IDs, or lipid identifiers) to the downstream pathway enrichment tool (clusterProfiler or biotranslator). The filtering acts as a mandatory quality gate: features not meeting the threshold are excluded before enrichment computation, reducing false-positive pathway associations and focusing analysis on statistically robust signals.

## Related tools

- **clusterProfiler** (Downstream pathway enrichment tool that receives filtered feature identifiers)
- **biotranslator** (Alternative downstream pathway enrichment tool that receives filtered feature identifiers)
- **DESeq2** (Upstream tool that produces p-values and log fold-change values for filtering)
- **edgeR** (Upstream tool that produces p-values and log fold-change values for filtering)
- **limma** (Upstream tool for differential expression analysis that produces p-values for filtering)

## Evaluation signals

- Filtered feature counts match expected retention rates given the p-value threshold and the distribution of raw p-values (sanity check: typically 10–50% of features retained at p < 0.05).
- All retained features have p-value ≤ configured threshold; all discarded features have p-value > threshold (no violations of filter logic).
- Filtered feature identifiers are correctly formatted for the selected enrichment tool (gene symbols, miRNA accessions, or protein/lipid IDs match tool expectations).
- Downstream enrichment results show enriched pathways with adjusted p-values and effect sizes consistent with the statistical power of the retained feature set.
- Output directory hierarchy correctly separates results by omics layer and tool (e.g., /genes/clusterprofiler/ vs. /lipids/biotranslator/), confirming layer-specific threshold application.

## Limitations

- Fixed p-value thresholds do not account for multiple-hypothesis correction across omics layers; users should consider Bonferroni or FDR-adjusted thresholds if comparing enrichment results across layers.
- Threshold values configured in params.yml are not adaptive to data characteristics (e.g., sample size, effect size distribution); users must manually validate thresholds are appropriate for their study design.
- Filtering on p-value alone ignores effect size (log fold-change); features with small effect sizes may pass the threshold but have weak biological relevance. Consider adding log fold-change filters as an additional QC step.
- If a feature layer has no features passing the threshold, the downstream enrichment tool may fail or produce uninformative results; implement a check for empty filtered sets before tool execution.

## Evidence

- [methods] The pipeline performs pathway enrichment analysis by allowing users to specify either clusterprofiler or biotranslator via the pea_genes parameter, with separate p-value cutoffs configurable for genes, miRNA, proteins, and lipids (genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5).: "separate p-value cutoffs configurable for genes, miRNA, proteins, and lipids (genes_genespval=1, mirna_genespval=1, proteins_genespval=0.5, lipids_genespval=0.5)"
- [methods] If pea_genes selects clusterProfiler, format gene identifiers and apply the configured p-value cutoff threshold to filter significant results.: "apply the configured p-value cutoff threshold to filter significant results"
- [methods] Load DEA output (gene list with p-values and log fold-change values) and read the pea_genes parameter from params.yml to determine tool selection.: "Load DEA output (gene list with p-values and log fold-change values) and read the pea_genes parameter from params.yml"
- [methods] Differential expression analyss | R packages: DESeq2, edger, RankProd, ggplot2 ComplexHeatmap: "Differential expression analyss | R packages: DESeq2, edger, RankProd"
