---
name: reaction-activity-score-computation
description: Use when you have RNA-seq read count data and a metabolic model with GPR rules, and you need to assess how differential gene expression translates into differential metabolic reaction capacity across multiple biological conditions or cell lines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3674
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3391
  tools:
  - COBRApy
  - optGpSampler
  - Mann-Whitney U test
  - INTEGRATE pipeline
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans:
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72]
- we exploited the implementation of optGpSampler algorithm [71] available in COBRApy [72], and we sampled a million steady state solutions
- we first performed the Mann-Whitney U test [73] (p-value < 0.05) between the FFD distributions of each pair of the five cell lines
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

# Reaction Activity Score (RAS) Computation

## Summary

Computes Reaction Activity Scores (RAS) from RNA-seq read counts and Gene-Protein-Reaction (GPR) associations to quantify the transcriptional regulation of metabolic reactions across biological samples. RAS serves as a proxy for differential enzyme abundance and enables discrimination of transcriptionally-controlled from metabolically-controlled metabolic fluxes.

## When to use

Apply this skill when you have RNA-seq read count data and a metabolic model with GPR rules, and you need to assess how differential gene expression translates into differential metabolic reaction capacity across multiple biological conditions or cell lines. Use RAS as input to constraint-based flux prediction or for concordance analysis with metabolomics-derived reaction propensity scores.

## When NOT to use

- When the metabolic model lacks GPR rules or has sparse gene annotations; RAS cannot be computed for unannotated reactions.
- When RNA-seq data are not normalized to a consistent metric (e.g., FPKM, TPM); raw read counts alone may not be comparable across samples with different sequencing depths.
- When you only have protein abundance data without transcriptomics; use alternative scoring methods (e.g., flux-based impact analysis) instead.

## Inputs

- SBML metabolic model with Gene-Protein-Reaction (GPR) associations
- RNA-seq read count matrix (rows: genes, columns: samples; format: TSV or CSV)
- Gene identifier mapping table (if sample gene IDs differ from model gene symbols)

## Outputs

- RAS score matrix (rows: reactions with GPR rules, columns: samples; CSV format)
- Normalized RAS score matrix with mean and standard deviation per reaction per sample
- Optionally: split RAS scores for reversible reactions represented as forward and reverse irreversible reactions

## How to apply

Extract GPR rules from your metabolic model (SBML or similar format). Map RNA-seq read counts to gene identifiers using a regex pattern (default: r"([A-Z0-9.]+)") that matches gene symbols in your GPR rules. For each reaction, combine the expression values of all genes in its GPR rule using Boolean logic (AND for protein subunits, OR for isoforms) to produce a single RAS value per reaction per sample. Normalize RAS scores by subtracting the mean and dividing by standard deviation to account for differences in absolute expression levels across samples. Reactions without GPR associations will have undefined RAS values and should be handled separately in downstream analyses (e.g., excluded from concordance analysis).

## Related tools

- **COBRApy** (Read, parse, and manipulate metabolic models in SBML format; extract GPR rules and reaction metadata) — https://github.com/opencobra/cobrapy
- **INTEGRATE pipeline** (Complete multi-omics integration workflow; Steps 1–3 specifically implement GPR extraction, RAS computation, and normalization) — https://github.com/qLSLab/integrate

## Examples

```
python pipeline/getRASscore.py --gprRule ENGRO2_GPR --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2 --regexOrgSpecific r"([A-Z0-9.]+)"
```

## Evaluation signals

- RAS matrix dimensions match: (number of reactions with GPR rules) × (number of samples); no NaN values for reactions with valid GPR associations.
- Normalized RAS scores are centered near zero (mean ≈ 0) and have unit variance (std ≈ 1) per reaction, confirming successful z-score normalization.
- RAS values correlate with independent measures of enzyme abundance (e.g., proteomics data when available) or with known transcriptional regulation patterns in the biological system.
- Concordance analysis downstream (Cohen's kappa between RAS directional changes and RPS directional changes) yields kappa coefficients consistent with published results (Fig 4A–B in the original paper).
- Reactions without GPR rules are explicitly marked as missing and excluded from downstream concordance and flux prediction analyses.

## Limitations

- RAS depends on accurate GPR rules; incomplete or incorrect annotations will propagate into RAS scores. Reactions without GPR associations cannot be scored.
- RAS is a relative measure of transcriptional capacity and does not account for post-translational modifications, protein stability, or enzyme kinetic parameters; therefore, RAS alone does not predict absolute metabolic flux.
- Boolean aggregation of gene expression in GPR rules assumes simple AND/OR logic; complex regulatory interactions (feedback, allosteric effects) are not captured.
- When a model contains reversible reactions, they must be split into forward and reverse irreversible versions before RAS computation; the reverse operation requires careful handling of the RAS file format (Step 8: RAS t-test in the pipeline).
- RAS scores are most valid for reactions with well-expressed genes; reactions catalyzed by very lowly expressed genes may show noise or instability across replicates.

## Evidence

- [other] Computation of Reaction Activity Scores (RAS) from transcriptomics data and GPR rules: "INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only)"
- [readme] Gene-to-reaction mapping via Boolean logic in GPR associations: "regexOrgSpecific: define regex to extract genes from GPR rules. Default value: r"([A-Z0-9.]+)" where dot is needed to also extract already computer scores, which are float."
- [readme] Normalization of RAS scores for cross-sample comparability: "File named modelId + 'wNormalizedRAS.csv' containing for each reaction (column *Rxn*) the mean (*mean_XXX* column) and normalized (*norm_XXX* column) RAS for each cell line *XXX*"
- [other] RAS input to flux prediction and concordance analysis: "INTEGRATE exploits constraint-based modeling to predict how the global relative differences in expression are expected to translate into consistent differences in metabolic fluxes"
- [other] Exclusion of reactions without GPR associations from downstream analyses: "Missing RPSvsRAS values occur when a reaction is not associated with a GPR"
