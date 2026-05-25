---
name: microbe-metabolite-conditional-probability-filtering
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to filter mmvec neural-network conditional probability outputs, retaining only the highest-confidence microbe–metabolite co-occurrence predictions by subsetting to annotated metabolites and the most predictive microbial taxa.
when_to_use_negative:
- Input mmvec output has not been generated or is missing; run mmvec first on your 16S ASVs and metabolite features.
- Metabolites are not yet annotated at compound level; filtering by annotation requires prior MS/MS spectral matching and chemical database searches (e.g., MASST, GNPS, HFMDB).
- Goal is exploratory and you wish to retain all possible taxa–metabolite associations; this filtering technique is selective and will discard low-probability interactions.
edam_operation: http://edamontology.org/operation_3695
edam_topics:
- http://edamontology.org/topic_0602
- http://edamontology.org/topic_0637
- http://edamontology.org/topic_3391
tools:
- name: mmvec
  role: neural network platform that generates conditional probability estimates of metabolite co-occurrence given microbial taxa; output is filtered by this skill
- name: QIIME2
  role: framework for exporting mmvec conditional probability results and managing microbiome-metabolome data
- name: R
  role: used for scripting the subsetting, filtering, and ranking operations on conditional probability matrices
  repo: https://github.com/jhaffner09/core_metabolome_2021
- name: MASST / GNPS
  role: upstream tools for MS/MS spectral matching and metabolite annotation, needed to generate the list of annotated metabolites used in filtering
provenance:
  source_task_ids:
  - task_004
  source_papers:
  - doi: 10.1128/msystems.00710-22
    title: Untargeted Fecal Metabolomic Analyses across an Industrialization Gradient Reveal Shared Metabolites and Impact of Industrialization on Fecal Microbiome-Metabolome Interactions
schema_version: 0.2.0
metadata:
  merge_audit:
    n_source_runs: 2
    source_files:
    - outputs/audit_haffner_v2/skills/microbe-metabolite-conditional-probability-filtering/SKILL.md
    - outputs/audit_haffner_v2/skills/microbe-metabolite-conditional-probability-filtering/skill.md
    merged_at: '2026-05-25T07:33:56.357655+00:00'
    merge_kind: slug_match_union
  iri: https://w3id.org/holobiomicslab/asb-skill/microbe-metabolite-conditional-probability-filtering@sha256:bd57ce4a21ca83058df43ec5f8b5407c93ede24b92428f3b0f9e3e21ab8b6e77
  related_workflows:
  - benchmark/tasks/audit_haffner_v2/workflow.smk
  - benchmark/tasks/audit_jeong_full/workflow.smk
  - benchmark/tasks/article_878_full_2026-05-10_v5/workflow.smk
  - benchmark/tasks/pesticide_full_2026-05-10_v2/workflow.smk
  - benchmark/tasks/audit_s41592_full/workflow.smk
derived_from:
- doi: 10.1128/msystems.00710-22
---

# microbe-metabolite-conditional-probability-filtering

## Summary

Filter mmvec neural-network conditional probability outputs to retain only the highest-confidence microbe–metabolite co-occurrence predictions by subsetting to annotated metabolites and the most predictive microbial taxa. This reduces noise and identifies the strongest probable interactions for downstream interpretation.

## When to use

After running mmvec (microbe-metabolite vectors) on 16S ASVs and untargeted LC-MS/MS metabolite features, when you have a full conditional-probability matrix and wish to focus on biologically interpretable and statistically robust interactions. Apply this when you have a curated list of annotated shared metabolites (e.g., 67 compound-level identifications) and want to rank microbial taxa by the magnitude and consistency of their conditional probabilities across all metabolites.

## When NOT to use

- Input mmvec output has not been generated or is missing; run mmvec first on your 16S ASVs and metabolite features.
- Metabolites are not yet annotated at compound level; filtering by annotation requires prior MS/MS spectral matching and chemical database searches (e.g., MASST, GNPS, HFMDB).
- Goal is exploratory and you wish to retain all possible taxa–metabolite associations; this filtering technique is selective and will discard low-probability interactions.

## Inputs

- mmvec conditional probability matrix (QIIME2 export, tab-delimited or HDF5)
- list of annotated metabolite identifiers (compound names or feature IDs with MS/MS annotations)
- microbial ASV table or taxonomic assignments from 16S rRNA gene sequencing

## Outputs

- filtered conditional probability submatrix (annotated metabolites × major predictive taxa, CSV or tab-delimited)
- ranked list of microbial taxa by conditional probability magnitude
- interaction strength summary table (metabolite–taxon pairs with conditional probability values)

## How to apply

Load the mmvec conditional probability output (exported from QIIME2 plugin) as a matrix with metabolites as rows and microbial taxa as columns. Filter rows to retain only the subset of annotated metabolites matching your compound-level identifications. Rank all microbial taxa by the magnitude of their conditional probabilities across metabolites, then select the top-ranked taxa (e.g., the 27 most predictive) by exploring the distribution of conditional probability values and choosing a threshold that captures substantial interactions. Export the filtered conditional probability submatrix (67 metabolites × 27 taxa) to CSV for visualization and interpretation of individual microbe–metabolite pairs with the highest predicted co-occurrence.

## Related tools

- **mmvec** (neural network platform that generates conditional probability estimates of metabolite co-occurrence given microbial taxa; output is filtered by this skill)
- **QIIME2** (framework for exporting mmvec conditional probability results and managing microbiome-metabolome data)
- **R** (used for scripting the subsetting, filtering, and ranking operations on conditional probability matrices) — https://github.com/jhaffner09/core_metabolome_2021
- **MASST / GNPS** (upstream tools for MS/MS spectral matching and metabolite annotation, needed to generate the list of annotated metabolites used in filtering)

## Evaluation signals

- Filtered output matrix has exactly the expected dimensions (67 annotated metabolites × 27 ranked taxa) with no missing values in the conditional probability cells.
- Conditional probability values in the filtered submatrix span a narrower, higher range than the full mmvec output, indicating successful removal of low-confidence associations.
- Each retained microbial taxon shows non-zero conditional probability for at least one metabolite, confirming taxa were selected based on actual predictive signal.
- Metabolite–taxon pairs with highest conditional probabilities match biological expectations (e.g., known producer–substrate pairs or documented fermentation pathways).
- Filtered CSV rows and columns are identifiable by metabolite name and ASV/taxon ID, enabling verification against source mmvec output and metabolite annotation database.

## Limitations

- Threshold choice for 'major predictive taxa' (e.g., top 27) is somewhat arbitrary; results are sensitive to this cutoff and should be justified post-hoc by inspection of the conditional probability distribution or domain knowledge.
- Filtering to annotated metabolites only (43% of detected features in this study) excludes unknown compounds that may have strong interactions; complementary analysis of unannotated metabolites is needed for complete coverage.
- Conditional probability does not imply causation or biochemical mechanism; high probability indicates co-occurrence in the feature space, not direct metabolic production or consumption.
- mmvec performance depends on sample size, sequencing depth, metabolomic completeness, and neural network hyperparameters; weak or absent signals for some taxa–metabolite pairs may reflect insufficient data or method limitations rather than true absence of interaction.

## Evidence

- [results] After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions between key gut metabolite features and microbes were observed: "After subsetting results to our 67 shared annotated metabolites and their major predictive taxa (27 total), several probable interactions"
- [results] we used the neural network platform microbe-metabolite vectors (mmvec) (69) to identify potential metabolite-microbe interactions by training on amplicon sequencing variants (ASVs) and metabolite feature data: "we used the neural network platform microbe-metabolite vectors (mmvec) (69)"
- [results] Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa, with N-acetyl-L-phenylalanine showing strong predictive interactions with an unknown Sporobacter species, abrine with another Sporobacter species, and glycyl-tyrosine and N-acetyl-D-mannosamine strongly driven by the Anaeroplasmataceae member: "Five Sporobacter species and one unknown Anaeroplasmataceae member were identified as the most influential taxa"
- [methods] Instructions for recreating data analyses in R and Python are available as Jupyter Notebook (85) links at: https://github.com/jhaffner09/core_metabolome_2021: "Instructions for recreating data analyses in R and Python are available as Jupyter Notebook"
