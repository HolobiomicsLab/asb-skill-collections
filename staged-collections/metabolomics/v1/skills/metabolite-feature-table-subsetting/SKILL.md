---
name: metabolite-feature-table-subsetting
description: "Subset a metabolite feature table to a curated list of annotated metabolites and filter conditionally-dependent taxa based on predictive strength, enabling focused analysis of microbe-metabolite interactions. This skill reduces feature and taxa complexity to only those with high-confidence annotations and strong conditional probability relationships."
when_to_use_negative: |
  - "Input is already a fully annotated, curated interaction table with pre-selected metabolites and taxa."
  - "You require exhaustive exploration of all taxa-metabolite pairs, not prioritization by conditional probability; subsetting discards weak associations."
  - "Conditional probabilities have not yet been computed; mmvec analysis has not been run on your microbiome and metabolite data."
edam_operation: "http://edamontology.org/operation_3695"
edam_topics: |
  - "http://edamontology.org/topic_3172"
  - "http://edamontology.org/topic_3391"
tools: |
  - name: "mmvec"
  role: "Computes conditional probability distributions of metabolites given taxa; output is subsetted by this skill."
  - name: "QIIME2"
  role: "Hosts the microbe-metabolite vectors plugin that produces the conditional probability artifact to be filtered."
  - name: "R"
  role: "Used to perform subsetting operations on conditional probability tables and filter by metabolite identifiers and taxa ranks."
  repo: "https://github.com/jhaffner09/core_metabolome_2021"
provenance: |
  source_task_ids:
  - task_004
  source_papers:
  - doi: "10.1128/msystems.00710-22"
  title: "Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions"
schema_version: "0.2.0"
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/metabolite-feature-table-subsetting@sha256:106aab1ed3b9a9286706aa395c98678757ecd3fb59c97a843d8055791681589f
---

# metabolite-feature-table-subsetting

## Summary

Subset a metabolite feature table to a curated list of annotated metabolites and filter conditionally-dependent taxa based on predictive strength, enabling focused analysis of microbe-metabolite interactions. This skill reduces feature and taxa complexity to only those with high-confidence annotations and strong conditional probability relationships.

## When to use

When you have a full mmvec conditional probability output (microbe-metabolite vectors neural network result) and want to visualize or analyze probable interactions: you have more annotated metabolites and taxa than are interpretable, and you need to prioritize those with compound-level annotations and highest conditional probabilities to reveal key drivers of microbiome-metabolome interactions.

## When NOT to use

- Input is already a fully annotated, curated interaction table with pre-selected metabolites and taxa.
- You require exhaustive exploration of all taxa-metabolite pairs, not prioritization by conditional probability; subsetting discards weak associations.
- Conditional probabilities have not yet been computed; mmvec analysis has not been run on your microbiome and metabolite data.

## Inputs

- mmvec conditional probability matrix (QIIME2 artifact or tabular format)
- list of annotated metabolite identifiers with compound-level annotations
- metabolite feature annotations table

## Outputs

- filtered conditional probability table (CSV or matrix format)
- subset of shared annotated metabolites (67 in article example)
- subset of major predictive taxa ranked by conditional probability (27 in article example)

## How to apply

Load the mmvec conditional probability matrix exported from QIIME2 microbe-metabolite vectors plugin. Subset rows to only the annotated shared metabolites (e.g., 67 in this study) by filtering on metabolite identifiers that have compound-level annotations. Then filter columns (taxa) by ranking conditional probability values across all metabolites and retaining only the top N taxa with the highest conditional probabilities (27 in this case). The rationale is that high conditional probabilities indicate strong predictive relationships; filtering to annotated metabolites ensures chemical interpretability. Export the resulting filtered conditional probability table to CSV for downstream visualization and hypothesis generation about specific metabolite-taxon pairs.

## Related tools

- **mmvec** (Computes conditional probability distributions of metabolites given taxa; output is subsetted by this skill.)
- **QIIME2** (Hosts the microbe-metabolite vectors plugin that produces the conditional probability artifact to be filtered.)
- **R** (Used to perform subsetting operations on conditional probability tables and filter by metabolite identifiers and taxa ranks.) — https://github.com/jhaffner09/core_metabolome_2021

## Evaluation signals

- Subset metabolite list contains only annotated metabolites with compound-level identifications (not unknowns or partial structures); count should match declared annotated list (67 in this study).
- Subset taxa list ranked by conditional probability values in descending order; top N taxa (27 in this study) retained, remainder discarded.
- Exported table has dimensions [number of annotated metabolites] × [number of major taxa], each cell containing a conditional probability value.
- Spot-check: verify that the highest conditional probability values in the filtered matrix are substantially higher than those discarded, confirming that selection prioritized strong associations.
- Output schema: three columns (or rows) minimum — metabolite identifier, taxon identifier, conditional probability value — with no missing or NaN entries in the filtered subset.

## Limitations

- Subsetting discards all weak associations; taxa and metabolites with conditional probabilities below the cutoff are lost and cannot be explored post-hoc without rerunning mmvec.
- The choice of N (27 major taxa in this study) is somewhat arbitrary; no principled statistical threshold is provided; results may be sensitive to this cutoff.
- Filtering to annotated metabolites excludes unknown or partially annotated features, which may harbour important signals if their structures are later identified.
- Conditional probability alone does not imply causation or functional relevance; high probability may reflect co-occurrence in shared environmental niches rather than direct metabolic interaction.

## Evidence

- [results] After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed: "After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed"
- [results] we used the neural network platform microbe-metabolite vectors (mmvec): "we used the neural network platform microbe-metabolite vectors (mmvec)"
- [other] Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa, with N-acetyl-L-phenylalanine showing strong predictive interactions with an unknown Sporobacter species, abrine with another Sporobacter species, and glycyl-tyrosine and N-acetyl-D-mannosamine strongly driven by the Anaeroplasmataceae member.: "Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa, with N-acetyl-L-phenylalanine showing strong predictive interactions with an unknown"
- [results] A total of 163 (43.1%) metabolite features had compound-level annotations: "A total of 163 (43.1%) metabolite features had compound-level annotations"
