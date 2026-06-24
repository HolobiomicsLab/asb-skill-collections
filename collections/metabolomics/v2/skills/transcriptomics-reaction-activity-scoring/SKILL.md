---
name: transcriptomics-reaction-activity-scoring
description: Use when you have RNA-seq read counts (FPKM or similar) for multiple
  cell lines or biological samples, a genome-scale metabolic model with GPR associations,
  and you need to constrain or weight metabolic reactions based on transcriptional
  regulation.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3792
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0821
  - http://edamontology.org/topic_3407
  tools:
  - eFlux
  - TRFBA
  - GX-FBA
  - scFBA
  - STAR aligner (v.2.6.1d)
  - HTSeq (v.0.6.1)
  - YSI2950 bioanalyzer
  - Agilent 1290 Infinity UHPLC system
  - optGpSampler algorithm
  - t-SNE (t-distributed Stochastic Neighbor Embedding)
  - COBRApy
  license_tier: restricted
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36]
- we set flux boundaries as a function of gene expression as done, among others, by
  eFlux [36] and TRFBA
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in GX-FBA [26]
- We scaled metabolic fluxes relative to the maximum flux identified using Flux Variability
  Analysis, as in scFBA [38]
- raw reads were mapped with STAR aligner (v.2.6.1d) to human reference genome (hg38)
- gene counts were calculated by HTSeq (v.0.6.1), using the hg38 Encode-Gencode GTF
  file (v28)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# transcriptomics-reaction-activity-scoring

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute Reaction Activity Scores (RAS) from RNA-seq read counts and Gene-Protein-Reaction (GPR) rules to quantify the transcriptional capacity of metabolic reactions. This bridges gene expression data to metabolic network models by assigning each reaction a normalized score that reflects the abundance of its encoding enzymes.

## When to use

You have RNA-seq read counts (FPKM or similar) for multiple cell lines or biological samples, a genome-scale metabolic model with GPR associations, and you need to constrain or weight metabolic reactions based on transcriptional regulation. Specifically, use this skill when discriminating whether flux differences originate from gene expression changes versus substrate availability—the RAS score quantifies the upper bound imposed by transcriptional control.

## When NOT to use

- Metabolic model lacks GPR associations—reactions without gene links cannot receive meaningful RAS scores.
- RNA-seq data is already aggregated or summarized at reaction level; RAS requires gene-level expression values and explicit GPR logic to compute.
- You need to predict metabolic fluxes without accounting for transcriptional regulation (e.g., purely substrate-availability-driven constraints).

## Inputs

- metabolic model in SBML format with GPR rules attached to each reaction
- RNA-seq read counts (FPKM, TPM, or raw counts) as a tabular file with gene IDs and sample columns

## Outputs

- RAS scores table (reactions × samples) with raw and normalized values
- GPR rule extraction file (reaction IDs and their associated GPR strings)

## How to apply

First, extract GPR rules from the metabolic model (one rule per reaction, defining the logical relationship between genes and reaction catalysis). Then, for each reaction in each sample, compute the RAS by evaluating the GPR rule against RNA-seq read counts: use the minimum expression level for AND-linked genes (all must be present) and the sum for OR-linked genes (any can catalyze). Finally, normalize each reaction's RAS by dividing by the maximum RAS value observed for that reaction across all samples, yielding a per-sample, per-reaction score in [0, 1]. This normalized score reflects relative transcriptional capacity and can then be used to scale flux bounds in the metabolic model during constraint-based analysis.

## Related tools

- **COBRApy** (Metabolic model I/O, GPR rule parsing and metabolic network manipulation) — https://github.com/opencobra/cobrapy
- **STAR aligner (v.2.6.1d)** (RNA-seq read mapping to reference genome to generate count matrices upstream of RAS computation)
- **HTSeq (v.0.6.1)** (Gene-level read quantification from aligned BAM files, producing read counts for RAS input)

## Examples

```
python pipeline/getRASscore.py --gprRule ENGRO2_GPR --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2 --regexOrgSpecific r"([A-Z0-9.]+)"
```

## Evaluation signals

- RAS scores lie in [0, 1] after normalization; verify no missing or NaN values for reactions with valid GPR rules.
- Cross-sample RAS values for a single reaction reflect expected transcriptional differences (e.g., overexpressed genes in cancer lines should yield higher RAS for their encoded reactions).
- Reactions with no GPR association are excluded; confirm that the count of excluded reactions matches the count of orphan reactions in the input model.
- RAS ranks concordantly with raw expression levels of rate-limiting enzymes in well-characterized pathways (e.g., LDHA should rank high in lactate-producing cell lines).
- Downstream constraint-based model predictions (flux distributions, viability) using RAS-scaled flux bounds show improved discrimination between cell lines compared to unconstrained models.

## Limitations

- RAS assumes GPR rules are complete and accurate; missing or incorrect gene assignments lead to biased scores.
- Reactions governed only by AND logic require all encoding genes to be expressed; a single lowly-expressed isoform can artificially suppress RAS even if other isoforms are abundant—consider using maximum instead of minimum for multi-gene AND rules if functional redundancy is suspected.
- RAS captures transcriptional capacity but not post-translational regulation (phosphorylation, allosteric control, protein stability), so a high RAS does not guarantee high flux.
- Normalization by maximum RAS across samples is relative; absolute expression levels are lost, making cross-study comparisons difficult.
- If RNA-seq data quality varies widely between samples (e.g., different sequencing depth), read counts must be normalized (e.g., by library size or FPKM) before RAS computation.

## Evidence

- [methods] Compute Reaction Activity Scores (RAS) from RNA-seq read counts using GPR rules (minimum for AND-linked genes, sum for OR-linked genes) and normalize by maximum RAS across cell lines.: "Compute Reaction Activity Scores (RAS) from RNA-seq read counts using GPR rules (minimum for AND-linked genes, sum for OR-linked genes) and normalize by maximum RAS across cell lines."
- [intro] INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only): "INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only)"
- [readme] getRASscore: generate RAS starting from GPR rules and transcriptomics data ... outputs File named modelId + '_RAS.csv' containing a column including the reactions ID (column *Rxn*), and a column for each cell line in the input transcriptomics dataset corresponding to the computer RAS score.: "getRASscore: generate RAS starting from GPR rules and transcriptomics data ... outputs File named modelId + '_RAS.csv' containing a column including the reactions ID (column *Rxn*), and a column for"
- [results] This dataset includes a RAS score for each input model reaction and for each sample. The score is based on the expression value (RNA-seq read counts) of the genes encoding for catalyzing enzymes: "This dataset includes a RAS score for each input model reaction and for each sample. The score is based on the expression value (RNA-seq read counts) of the genes encoding for catalyzing enzymes"
- [readme] getNormalizedRAS: normalize RAS scores ... output File named modelId + 'wNormalizedRAS.csv' containing for each reaction (column *Rxn*) the mean (*mean_XXX* column) and normalized (*norm_XXX* column) RAS for each cell line *XXX*: "getNormalizedRAS: normalize RAS scores ... output File named modelId + 'wNormalizedRAS.csv' containing for each reaction (column *Rxn*) the mean (*mean_XXX* column) and normalized (*norm_XXX* column)"
- [results] Missing RPSvsRAS values occur when a reaction is not associated with a GPR: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
