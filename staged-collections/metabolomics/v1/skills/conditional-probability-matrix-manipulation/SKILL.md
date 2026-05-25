---
name: conditional-probability-matrix-manipulation
description: Use when extracting and filtering conditional probability matrices from mmvec neural network output to identify high-confidence microbe–metabolite interaction pairs by retaining rows for annotated metabolites and columns for taxa with the highest conditional probabilities.
when_to_use_negative:
- Input is already a curated set of interactions (e.g., from literature or validated databases); filtering would redundantly remove signals.
- All metabolites are unannotated or lack compound-level identifications; filtering to annotated metabolites would leave an empty or uninformative result.
- The goal is to identify rare or low-probability associations; this skill prioritizes high-confidence pairs and will mask weak but real interactions.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_3172
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_0154
tools:
- name: mmvec
  role: generates conditional probability matrices of metabolite abundance given taxon abundance via neural network; output is the primary input to this skill
- name: QIIME2
  role: wraps mmvec and exports conditional probability matrices; provides the export format and framework for this skill
- name: R
  role: used for subsetting matrix rows/columns, ranking taxa by conditional probability, and exporting filtered results
  repo: https://github.com/jhaffner09/core_metabolome_2021
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/conditional-probability-matrix-manipulation@sha256:715291234b0fb35338ab0631c65a87d78205327b8179f49faec5dde385539c2d
---

# conditional-probability-matrix-manipulation

## Summary

Extract and filter conditional probability matrices from mmvec (microbe-metabolite vectors) neural network output to identify high-confidence microbe–metabolite interaction pairs. This skill isolates the most predictive taxa–metabolite associations by retaining rows corresponding to annotated metabolites and columns corresponding to taxa with the highest conditional probabilities.

## When to use

Apply this skill when you have mmvec conditional probability output exported from QIIME2 and need to identify the subset of microbe–metabolite interactions most likely to drive metabolomic variation. Specifically, use it when you have >100 metabolite features or >50 taxa but want to focus on the most interpretable and statistically robust interactions—e.g., when you have 67 annotated shared metabolites and wish to isolate the 27 most influential taxa based on their predictive power across all metabolites.

## When NOT to use

- Input is already a curated set of interactions (e.g., from literature or validated databases); filtering would redundantly remove signals.
- All metabolites are unannotated or lack compound-level identifications; filtering to annotated metabolites would leave an empty or uninformative result.
- The goal is to identify rare or low-probability associations; this skill prioritizes high-confidence pairs and will mask weak but real interactions.

## Inputs

- mmvec conditional probability matrix (QIIME2 format, rows = metabolites, columns = taxa)
- list of annotated metabolite identifiers (compound names or m/z-RT pairs)
- taxon names or ASV identifiers

## Outputs

- filtered conditional probability matrix (CSV or table format)
- interaction table mapping metabolites to their top predictive taxa

## How to apply

Load the mmvec conditional probability matrix (rows = metabolites, columns = taxa, values = P(metabolite|taxon)) exported from QIIME2. First, subset rows to the set of metabolites with compound-level annotations (e.g., via GNPS or ClassyFire identifiers), discarding unannotated features. Next, rank taxa by the maximum conditional probability they exhibit across all retained metabolites, or by the sum of conditional probabilities; select the top N taxa (e.g., 27) meeting a significance threshold. This focuses the interaction network on the most probable and interpretable associations. Export the filtered matrix (67 metabolites × 27 taxa in the source article's case) to CSV, preserving metabolite identifiers and taxon names for downstream visualization and biological interpretation.

## Related tools

- **mmvec** (generates conditional probability matrices of metabolite abundance given taxon abundance via neural network; output is the primary input to this skill)
- **QIIME2** (wraps mmvec and exports conditional probability matrices; provides the export format and framework for this skill)
- **R** (used for subsetting matrix rows/columns, ranking taxa by conditional probability, and exporting filtered results) — https://github.com/jhaffner09/core_metabolome_2021

## Examples

```
# Pseudocode in R: mmvec_cond <- read.csv('mmvec_conditional_prob.csv', row.names=1); annotated_mets <- read.csv('metabolite_annotations.csv')$metabolite_id; mmvec_filtered <- mmvec_cond[rownames(mmvec_cond) %in% annotated_mets, ]; taxa_max_prob <- apply(mmvec_filtered, 2, max); top_taxa <- names(sort(taxa_max_prob, decreasing=TRUE)[1:27]); mmvec_final <- mmvec_filtered[, top_taxa]; write.csv(mmvec_final, 'filtered_mmvec_67met_27taxa.csv')
```

## Evaluation signals

- Filtered matrix dimensions match the expected retain count (e.g., 67 metabolites × 27 taxa); no spurious rows or columns remain.
- All metabolite identifiers in the filtered matrix are present in the original annotated metabolite list; no unannotated features leak through.
- Conditional probability values in retained columns are among the highest in the original matrix (e.g., top decile per taxon); confirm via summary statistics (min, median, max) before/after filtering.
- CSV export is parseable and contains no missing values or malformed identifiers; row and column headers are preserved.
- Biological plausibility: the top taxa (e.g., Sporobacter species, Anaeroplasmataceae) match prior knowledge of dominant fecal microbes, and metabolites (e.g., N-acetyl-L-phenylalanine, abrine) are consistent with known fecal metabolomic profiles.

## Limitations

- Filtering to annotated metabolites discards potentially real but unmapped metabolite–taxon associations; compound-level annotation quality (e.g., confidence level in GNPS) should be transparent.
- Ranking taxa by maximum or summed conditional probability may favor broadly predictive taxa over metabolite-specific specialists; no single ranking criterion is universally optimal.
- mmvec assumes linear latent-variable relationships and requires sufficient sample size to train the neural network; small cohorts or unbalanced designs may yield unstable or overfitted conditional probabilities.
- The filtered matrix is a snapshot at a single cutoff; results are sensitive to the choice of N (number of retained taxa) and may not generalize to independent cohorts.

## Evidence

- [results] After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed: "After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed"
- [results] we used the neural network platform microbe-metabolite vectors (mmvec): "we used the neural network platform microbe-metabolite vectors (mmvec)"
- [results] Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa, with N-acetyl-L-phenylalanine showing strong predictive interactions with an unknown Sporobacter species: "Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa, with N-acetyl-L-phenylalanine showing strong predictive interactions with an unknown"
- [other] 1. Load mmvec conditional probability output exported from QIIME2 microbe-metabolite vectors plugin. 2. Subset conditionals to the 67 annotated shared metabolites by filtering rows to metabolite identifiers. 3. Filter major taxa by exploring high conditional probability values and retain the 27 most predictive microbial taxa by selecting those with the highest conditional probabilities across all metabolites. 4. Export filtered conditional probability results to CSV format as the final interaction table.: "Load mmvec conditional probability output exported from QIIME2 microbe-metabolite vectors plugin. Subset conditionals to the 67 annotated shared metabolites by filtering rows to metabolite"
