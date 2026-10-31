---
name: kruskal-wallis-group-comparison
description: "Non-parametric Kruskal–Wallis testing (with Dunn's post hoc tests) to determine whether per-sample Hill-number alpha diversity (observed richness, Shannon's Entropy, Simpson's Index) differs among denoising pipelines (DADA2, Deblur, VSEARCH) across basic, standard, and extra filtering regimes on bat guano COI metabarcoding data."
when_to_use_negative:
  - "Input data are taxonomic classification outcomes or classifier completeness (BOLD API, SINTAX, BLAST+LCA) — that is a separate benchmarking question, not alpha diversity group testing"
  - "You are comparing relative-abundance estimates of specific taxa in diets rather than per-sample diversity metrics (that requires the RA-vs-PA transformation analysis instead)"
  - "Feature tables have already been rarefied and diversity tested; applying Kruskal–Wallis again without re-deriving the grouping factors adds no information"
edam_operation: "http://edamontology.org/operation_2945"
edam_topics:
  - "http://edamontology.org/topic_2269"
tools:
  - name: "Phyloseq"
    role: "R package used to rarefy filtered feature tables (5,000 reads) and compute per-sample Hill Numbers 0, 1, 2 for the Kruskal–Wallis tests"
  - name: "Vegan"
    role: "R package for computing alpha diversity estimates on the rarefied feature tables"
  - name: "Tidyverse"
    role: "R framework for reshaping diversity tables and running the Kruskal–Wallis / Dunn's test workflow and plotting"
  - name: "VSEARCH"
    role: "Denominator pipeline whose OTU-clustered samples (98% merge, 97% final clustering) form the third grouping factor shown to contain 2-3x more ASVs per sample"
    repo: "https://github.com/torognes/vsearch"
  - name: "DADA2"
    role: "Default error-model denoising pipeline whose samples form one comparison group in the Kruskal–Wallis tests"
  - name: "Deblur"
    role: "Denoising pipeline run with '--p-min-reads 2' and '--p-min-size 1' whose samples form another comparison group"
provenance:
  source_task_ids:
    - task_004
  source_papers:
    - doi: "10.1002/ece3.6594"
      title: "A total crapshoot? Evaluating bioinformatic decisions in animal diet metabarcoding analyses"
schema_version: "0.2.0"
content_hash: sha256:782fe830bcec61b22ba3a5e643392942c9a558f4eca3b1ef62c89f7c9c950d06
---

# kruskal-wallis-group-comparison

## Summary

Non-parametric Kruskal–Wallis testing (with Dunn's post hoc tests) to determine whether per-sample Hill-number alpha diversity (observed richness, Shannon's Entropy, Simpson's Index) differs among denoising pipelines (DADA2, Deblur, VSEARCH) across basic, standard, and extra filtering regimes on bat guano COI metabarcoding data.

## When to use

Use when comparing per-sample alpha diversity (e.g., Hill Numbers 0/1/2) across multiple independent treatment groups — such as denoising programs or filtering regimes — on non-normally distributed rarefied feature-table-derived diversity values.

## When NOT to use

- Input data are taxonomic classification outcomes or classifier completeness (BOLD API, SINTAX, BLAST+LCA) — that is a separate benchmarking question, not alpha diversity group testing
- You are comparing relative-abundance estimates of specific taxa in diets rather than per-sample diversity metrics (that requires the RA-vs-PA transformation analysis instead)
- Feature tables have already been rarefied and diversity tested; applying Kruskal–Wallis again without re-deriving the grouping factors adds no information

## Inputs

- Rarefied (5,000 reads/sample) filtered feature tables, one per denoising program (DADA2, Deblur, VSEARCH) and filtering regime (basic, standard, extra)
- Per-sample Hill Number diversity values (Hill 0, 1, 2) computed with Phyloseq/Vegan
- Grouping metadata mapping each guano sample to its denoising program and filtering regime

## Outputs

- Kruskal–Wallis test statistics and p-values for each filtering regime x Hill Number combination
- Dunn's post hoc pairwise comparison results identifying which denoising-program pairs differ
- Per-sample richness/diversity plots by denoising program and filtering regime reproducing Figure 3 / Figure S2 patterns

## How to apply

First generate per-sample alpha diversity values: rarefy each filtered feature table to 5,000 reads per sample and compute Hill Numbers 0, 1, and 2 for every guano sample using Phyloseq/Vegan in R. For each filtering regime (basic, standard, extra) and each Hill Number, fit a Kruskal–Wallis rank-sum test with the denoising program (DADA2, Deblur, VSEARCH) as the grouping factor, since diversity estimates are non-normal and group variances are unequal. If the omnibus test is significant, follow with Dunn's post hoc pairwise tests to identify which program pairs differ. Repeat the test in parallel with and without abundance weighting — the article evaluates both RA and PA count transformations — and interpret results alongside per-sample ASV richness, since VSEARCH-processed samples contained 2-3x more ASVs per sample than DADA2 or Deblur. Validate against the reported pattern: significant differences among programs across filtering regimes (except Hill Number 0 for basic-filtered data), matching Figures 3 and S2.

## Related tools

- **Phyloseq** (R package used to rarefy filtered feature tables (5,000 reads) and compute per-sample Hill Numbers 0, 1, 2 for the Kruskal–Wallis tests)
- **Vegan** (R package for computing alpha diversity estimates on the rarefied feature tables)
- **Tidyverse** (R framework for reshaping diversity tables and running the Kruskal–Wallis / Dunn's test workflow and plotting)
- **VSEARCH** (Denominator pipeline whose OTU-clustered samples (98% merge, 97% final clustering) form the third grouping factor shown to contain 2-3x more ASVs per sample) — https://github.com/torognes/vsearch
- **DADA2** (Default error-model denoising pipeline whose samples form one comparison group in the Kruskal–Wallis tests)
- **Deblur** (Denoising pipeline run with '--p-min-reads 2' and '--p-min-size 1' whose samples form another comparison group)

## Examples

```
kruskal.test(Hill1 ~ denoiser, data = guano_standard_rarefied); dunnTest(Hill1 ~ denoiser, data = guano_standard_rarefied, method="bh")
```

## Evaluation signals

- Kruskal–Wallis tests must identify significant differences in Hill-number alpha diversity among DADA2, Deblur, and VSEARCH samples across the filtering regimes (all combinations except Hill Number 0 for basic-filtered data)
- Dunn's post hoc tests should localize significant pairwise differences, consistent with VSEARCH samples repeatedly containing 2-3x more ASVs per sample than DADA2 or Deblur
- Every test must be run on feature tables rarefied to exactly 5,000 reads per sample after removal of host/mock COI sequences
- Results must match the Figure 3 / Figure S2 pattern for both abundance-weighted and presence/absence-based diversity estimates
- Test must be repeated for all three filtering regimes (basic, standard, extra) with the same samples retained under standard filtering (drop single-sample variants, keep samples with ≥5,000 total filtered reads)

## Limitations

- One combination — Hill Number 0 on basic-filtered data — did not differ significantly among groups, so 'significant everywhere' would be a false expectation; unfiltered data with singletons retained dampen the contrast
- Differences between denoising methods are largely mitigated by removing low-abundance sequence variants, so test conclusions depend critically on which filtering regime is applied
- The paper's aim is not to present a single best pathway, so significant Kruskal–Wallis differences indicate sensitivity to bioinformatic choices, not which program is correct

## Evidence

- [methods] a standard filter required (a) dropping any sequence variant observed in just one sample across the entire dataset and (b) retaining only samples with ≥5,000 total filtered reads: "a standard filter required (a) dropping any sequence variant observed in just one sample across the entire dataset and (b) retaining only samples with ≥5,000 total filtered reads"
- [methods] an extra filter incorporated the standard filters, and subtracted a single, fixed integer from each element of the feature table: "an extra filter incorporated the standard filters, and subtracted a single, fixed integer from each element of the feature table"
- [other] all other diversity estimates differed significantly among filtering and denoising groups, and VSEARCH-processed samples repeatedly contained 2-3x more ASVs per sample than DADA2 or Deblur: [evidence span withheld — anchor status: not_found]
- [readme] See [the docs folder of this repo](https://github.com/devonorourke/tidybug/tree/master/docs) for information on how each part of the project was performed: "See [the docs folder of this repo](https://github.com/devonorourke/tidybug/tree/master/docs) for information on how each part of the project was performed"
