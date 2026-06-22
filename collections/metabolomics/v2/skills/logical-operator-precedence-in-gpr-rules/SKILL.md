---
name: logical-operator-precedence-in-gpr-rules
description: Use when when computing Reaction Activity Scores (RAS) from transcriptomics data linked to a metabolic model via GPR associations, and the model contains reactions governed by mixed AND/OR logical rules (e.g., '(gene_A AND gene_B) OR gene_C').
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_2259
  - http://edamontology.org/topic_0602
  tools:
  - getRASscore
  - getGPRsFromModel
  - COBRApy
derived_from:
- doi: 10.1371/journal.pcbi.1009337
  title: INTEGRATE
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_integrate_cq
    doi: 10.1371/journal.pcbi.1009337
    title: INTEGRATE
  dedup_kept_from: coll_integrate_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1371/journal.pcbi.1009337
  all_source_dois:
  - 10.1371/journal.pcbi.1009337
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Logical operator precedence in GPR rules

## Summary

Correctly resolve Gene-Protein-Reaction (GPR) logical expressions by applying standard operator precedence (AND before OR) to compute reaction activity scores from gene expression data. This skill ensures that complex GPR rules with mixed AND/OR operators are parsed and evaluated consistently, preventing misinterpretation of subunit stoichiometry vs. isoform redundancy.

## When to use

When computing Reaction Activity Scores (RAS) from transcriptomics data linked to a metabolic model via GPR associations, and the model contains reactions governed by mixed AND/OR logical rules (e.g., '(gene_A AND gene_B) OR gene_C'). Standard precedence must be applied to correctly distinguish between co-catalyzing subunits (AND) and alternative isoforms (OR).

## When NOT to use

- Reactions without GPR associations (assign RAS = 1.0 directly without parsing).
- When gene expression data is qualitative (present/absent) rather than quantitative; precedence application requires numeric transcript abundances to compute min/sum operations.
- If the GPR rule format does not use standard Boolean notation (AND/OR); custom operators or non-standard syntax require rule-specific interpretation before precedence rules apply.

## Inputs

- GPR rule file (CSV with reaction IDs and rule column)
- RNA-seq transcript abundance data (FPKM or normalized read counts per gene, per cell line/sample)
- Metabolic model (SBML or COBRApy format) with embedded GPR rules

## Outputs

- RAS file (CSV with reaction IDs and normalized RAS scores per cell line, range [0,1] for GPR-associated reactions, 1.0 for reactions without GPR)
- Resolved GPR expression values per reaction per sample (intermediate, for validation)

## How to apply

For each reaction in the metabolic model, extract its GPR rule and resolve the logical expression using standard precedence: AND operators bind more tightly than OR operators. For AND-linked genes (representing enzyme subunits), compute the reaction activity as the minimum transcript abundance across those genes; for OR-linked genes (isoforms), compute as the sum of transcript abundances. Apply precedence rules consistently across all reactions—for example, in 'gene_A AND (gene_B OR gene_C)', first resolve the OR clause, then apply AND to gene_A. After resolving the GPR for each reaction and cell line using transcript abundance (typically FPKM or normalized RNA-seq counts), normalize the resulting raw RAS by dividing by the maximum RAS observed across all cell lines for that reaction. Validate by spot-checking 5–10 reactions against manually resolved GPR expressions to confirm precedence was applied correctly.

## Related tools

- **getRASscore** (Python script that generates RAS scores by resolving GPR rules against transcriptomics data; implements logical operator precedence to compute min(AND genes) and sum(OR genes).) — https://github.com/qLSLab/integrate
- **getGPRsFromModel** (Python script that extracts GPR rules from a metabolic model and stores them in a CSV file for downstream processing.) — https://github.com/qLSLab/integrate
- **COBRApy** (Python library for constraint-based metabolic modeling; used to parse metabolic models (SBML) and access embedded GPR rules.)

## Examples

```
python pipeline/getRASscore.py --gprRule ENGRO2_GPR.csv --rnaSeqFileName FPKM_Breast_forMarea.tsv --modelId ENGRO2 --regexOrgSpecific '([A-Z0-9.]+)'
```

## Evaluation signals

- All RAS values for GPR-associated reactions fall within [0, 1] after normalization; reactions without GPR rules equal 1.0.
- Spot-check validation: manually resolve GPR expressions for 5–10 representative reactions (at least one mixed AND/OR rule, one pure AND, one pure OR) and confirm computed RAS matches expected min/sum logic.
- For AND-linked genes in a subunit reaction, RAS should be dominated by the lowest-abundance transcript; for OR-linked isoforms, RAS increases with sum of transcripts.
- Reproducibility: running getRASscore.py on the same transcriptomics and GPR files produces identical RAS outputs.
- Logical consistency: if gene X is upregulated in a reaction governed by 'gene_X AND gene_Y', RAS increases only if gene_Y remains non-zero; if governed by 'gene_X OR gene_Z', RAS increases regardless of gene_Z state.

## Limitations

- Precedence resolution assumes standard Boolean algebra (AND > OR); non-standard or ambiguous GPR notation (e.g., bare parentheses without explicit operators, or use of other logical gates) cannot be parsed correctly.
- The min/sum heuristic for AND/OR ignores enzyme kinetics, cofactor availability, allosteric regulation, and product inhibition—RAS is a proxy for expression-level regulation only.
- Transcript abundance data quality and completeness directly affect RAS validity; missing or zero-count genes in the transcriptomics dataset may cause RAS underestimation or invalid results for affected reactions.
- Normalization by the maximum RAS across cell lines may obscure absolute expression differences if cell-line-specific effects are small; relative rankings are preserved, but absolute flux capacity cannot be inferred from RAS alone.
- Complex nested GPR rules or non-canonical Boolean expressions may require custom regex patterns to extract gene identifiers; the default regex (r'([A-Z0-9.]+)') may fail on gene IDs with special characters or lowercase letters.

## Evidence

- [other] RAS computation integrates Gene-Protein-Reaction rules with RNA-seq read counts. For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes (isoforms), RAS equals the sum of transcript values.: "For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes (isoforms), RAS equals the sum of transcript values."
- [other] For each reaction r and each cell line c, resolve the GPR logical expression: for AND-linked genes, take the minimum transcript abundance value; for OR-linked genes, take the sum of transcript abundances; handle mixed AND/OR using standard precedence rules.: "handle mixed AND/OR using standard precedence rules"
- [other] Validation: confirm RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions against manually resolved GPR expressions.: "verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions against manually resolved GPR expressions"
- [readme] Aim: generate RAS starting from GPR rules and transcriptomics data. Users may decided to leave the following inputs associated to their default values or set them as preferred: gprRule: output file of Step 1. Default value: 'ENGRO2_GPR'; rnaSeqFileName = transcriptomics dataset file name. Default value: 'FPKM_Breast_forMarea.tsv': "generate RAS starting from GPR rules and transcriptomics data"
- [other] Set RAS to 1 for reactions not associated with any GPR.: "Set RAS to 1 for reactions not associated with any GPR."
- [other] Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed: RAS^c_r = RAS^c_r,x / max{RAS^c_r} across all c.: "Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed"
