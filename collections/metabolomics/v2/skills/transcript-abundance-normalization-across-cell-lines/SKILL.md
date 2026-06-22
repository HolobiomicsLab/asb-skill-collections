---
name: transcript-abundance-normalization-across-cell-lines
description: Use when you have computed raw RAS values for multiple cell lines or samples by resolving Gene-Protein-Reaction (GPR) logical rules against RNA-seq FPKM abundances, and you need to make reaction activity scores comparable across cell lines by removing sample-level abundance differences so that.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3308
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_2259
  tools:
  - getRASscore.py
  - getNormalizedRAS.py
  - rasIntegration.py
  - constraint-based stoichiometric metabolic models (ENGRO2)
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Transcript-Abundance Normalization Across Cell Lines

## Summary

Normalize gene expression transcript abundances across cell lines by dividing each reaction's Reaction Activity Score (RAS) by the maximum RAS value observed across all samples, producing dimensionless scores in [0, 1] that enable cross-sample comparison of relative enzyme activity. This step is essential after computing raw RAS from GPR-resolved transcript data to enable constraint-based metabolic model integration and flux prediction across heterogeneous cell populations.

## When to use

You have computed raw RAS values for multiple cell lines or samples by resolving Gene-Protein-Reaction (GPR) logical rules against RNA-seq FPKM abundances, and you need to make reaction activity scores comparable across cell lines by removing sample-level abundance differences so that downstream constraint-based modeling can account for relative—not absolute—enzyme expression. Normalization is required before integrating RAS as upper bounds in flux balance analysis or concordance analysis with metabolomic/flux data.

## When NOT to use

- Input transcript abundances are already in relative or normalized form (e.g., TPM, z-scores, or DESeq2 log2-fold-change) rather than raw FPKM or read counts — double normalization will distort signal.
- You are comparing expression across different tissues or developmental stages where absolute transcript levels are biologically meaningful and must be preserved (e.g., temporal dynamics or organ-specific flux); max-normalization erases that information.
- The dataset contains outlier cell lines or replicates with extreme RAS values that would disproportionately compress the majority of reactions toward 0 (e.g., a single sample with 100× higher expression); consider outlier detection or robust scaling first.
- Reactions are annotated with alternative GPR rules that encode tissue-specific or condition-specific isoforms; normalization assumes GPR logic is constant across samples, which may not hold for splice variants or post-translational modification.

## Inputs

- Raw RAS scores per reaction and cell line (computed from GPR resolution and transcript abundances)
- List of cell line identifiers and replicate labels (e.g., ['MCF102A_A', 'MCF102A_B', 'MDAMB231_A', ...])
- GPR association table (reaction ID → GPR rule) to identify non-GPR reactions
- FPKM or transcript abundance data (for validation and spot-checking)

## Outputs

- Normalized RAS matrix (reactions × cell lines) with scores in [0, 1]
- Mean and normalized RAS per reaction per cell line (CSV format: columns 'Rxn', 'mean_XXX', 'norm_XXX' for each cell line XXX)
- Metadata flags indicating which reactions have no GPR association (RAS = 1.0)

## How to apply

For each reaction r, identify the maximum raw RAS value across all cell lines (max{RAS^c_r,x} where c ranges over all cell lines and samples). Then divide each cell line's raw RAS by this maximum: RAS^c_r = RAS^c_r,x / max{RAS^c_r}. Average the normalized RAS across biological replicates within each cell line to obtain the final per-reaction, per-cell-line score. Set RAS = 1.0 for reactions with no GPR association (housekeeping reactions). Validate that all GPR-associated reactions fall in [0, 1] and that non-GPR reactions equal exactly 1.0. This linear scaling preserves the rank order of enzyme activity within reactions while collapsing absolute transcript abundance variation, enabling fair comparison when metabolic models are constrained by relative gene expression.

## Related tools

- **getRASscore.py** (Computes raw RAS values from GPR rules and transcript abundances (prerequisite step); normalization is applied to its output) — https://github.com/qLSLab/integrate
- **getNormalizedRAS.py** (Implements the normalization workflow: divides each reaction's RAS by maximum across samples and averages replicates) — https://github.com/qLSLab/integrate
- **rasIntegration.py** (Consumes normalized RAS output to integrate transcript-derived constraints into cell-line-specific metabolic models) — https://github.com/qLSLab/integrate
- **constraint-based stoichiometric metabolic models (ENGRO2)** (Provides the GPR rules and reaction network structure necessary to interpret and validate normalized RAS before flux optimization)

## Examples

```
python pipeline/getNormalizedRAS.py --inputFileName ENGRO2_RAS.csv --outputFileName ENGRO2_wNormalizedRAS.csv
```

## Evaluation signals

- All RAS values for GPR-associated reactions fall within [0, 1] after normalization; non-GPR reactions equal exactly 1.0.
- The maximum RAS value per reaction is exactly 1.0 (at least one cell line achieves the peak for each reaction).
- Spot-check 5–10 reactions by manually resolving their GPR expressions from the RNA-seq data and verifying that the normalized RAS rank order matches the raw transcript abundance rank order.
- Mean RAS values per cell line across all reactions are consistent (e.g., no cell line has mean RAS < 0.3 or > 0.9), indicating balanced normalization without pathological collapse.
- Replicate variance within each cell line is small relative to variance across cell lines (coefficient of variation of replicate means < 0.15), confirming that averaging across replicates reduces noise.

## Limitations

- Max-normalization assumes that at least one cell line expresses each reaction at a measurable level; reactions absent from all transcriptomics samples will have raw RAS = 0 and remain 0 after normalization, potentially excluding biologically relevant but lowly-expressed enzymes from downstream analysis.
- The method does not account for post-translational modifications, protein degradation rates, or allosteric regulation; normalized RAS reflects mRNA abundance only and may not correlate with actual enzyme activity in vivo.
- Reactions with complex mixed AND/OR GPR logic (e.g., isoforms with sub-unit requirements) depend critically on correct GPR parsing; regex errors or incomplete gene annotation can propagate through raw RAS computation and distort normalized scores.
- Limited metabolite coverage in metabolomics datasets constrains the number of reactions that can be validated by concordance analysis; reactions with unmeasured substrates cannot be cross-validated against flux predictions.
- Normalization is sensitive to the quality of the RNA-seq input; low coverage, batch effects, or systematic bias in FPKM estimation will compress or expand the RAS distribution before normalization, affecting the interpretability of downstream constraint-based predictions.

## Evidence

- [other] RAS computation integrates Gene-Protein-Reaction rules with RNA-seq read counts. For reactions with AND-linked genes (subunits), RAS equals the minimum transcript level; for OR-linked genes (isoforms), RAS equals the sum of transcript values. RAS values are then normalized by dividing each cell line's RAS by the maximum RAS across all cell lines.: "RAS values are then normalized by dividing each cell line's RAS by the maximum RAS across all cell lines. Reactions without GPR associations are assigned RAS = 1."
- [other] Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed: RAS^c_r = RAS^c_r,x / max{RAS^c_r} across all c. Set RAS to 1 for reactions not associated with any GPR. Average normalized RAS across biological replicates within each cell line to obtain the final RAS^c_r score per reaction per cell line.: "Normalize each reaction's RAS across all cell lines by dividing by the maximum RAS value observed: RAS^c_r = RAS^c_r,x / max{RAS^c_r} across all c. Set RAS to 1 for reactions not associated with any"
- [other] Validation of normalization requires confirming RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions against manually resolved GPR expressions.: "Validation: confirm RAS values are in [0, 1] for GPR-associated reactions and equal to 1.0 for non-GPR reactions; verify RAS computation matches expected GPR logic by spot-checking 5–10 reactions"
- [readme] Step 3: getNormalizedRAS script normalizes RAS scores by dividing by maximum and averages replicates.: "**Step 3: getNormalizedRAS** * Aim: normalize RAS scores * Usage: `python pipeline/getNormalizedRAS.py` * Output: File named modelId + 'wNormalizedRAS.csv' containing for each reaction (column *Rxn*)"
- [intro] INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only). Then, INTEGRATE exploits constraint-based modeling to predict how the global relative differences in expression are expected to translate into consistent differences in metabolic fluxes.: "INTEGRATE first computes differential expression of reactions from transcriptomics data (transcriptional regulation only). Then, INTEGRATE exploits constraint-based modeling to predict how the global"
