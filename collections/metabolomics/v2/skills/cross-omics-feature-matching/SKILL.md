---
name: cross-omics-feature-matching
description: Use when when you have two feature matrices from different omics modalities
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3565
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0092
  - http://edamontology.org/topic_3674
  tools:
  - haCCA
  license_tier: restricted
derived_from:
- doi: 10.1101/2024.08.20.608773v2
  title: haCCA
evidence_spans:
- haCCA, a workflow utilizing high Correlated feature pairs combined with a modified
  spatial morphological alignment
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hacca_cq
    doi: 10.1101/2024.08.20.608773v2
    title: haCCA
  dedup_kept_from: coll_hacca_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2024.08.20.608773v2
  all_source_dois:
  - 10.1101/2024.08.20.608773v2
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# cross-omics-feature-matching

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Identifies and ranks high-correlation feature pairs between two omics datasets (e.g., spatial transcriptome and metabolome) by computing pairwise correlation coefficients and filtering by correlation threshold. This skill forms the foundation for downstream spot-to-spot data integration in multi-modal omics workflows.

## When to use

When you have two feature matrices from different omics modalities (e.g., gene expression and metabolite abundance) collected on the same or aligned spatial coordinates, and you need to discover which features across modalities are most strongly associated before performing joint spatial alignment or integration.

## When NOT to use

- Input feature matrices are missing or have zero overlap in sample coordinates—cross-omics matching assumes spatial or technical co-localization.
- Feature matrices have already been pre-filtered or curated to only highly correlated pairs—applying the skill again risks over-filtering.
- You aim to identify de novo feature relationships across modalities *without* correlation as a criterion (e.g., using causal inference or metabolic pathway databases instead).

## Inputs

- Feature matrix from first omics modality (e.g., spatial transcriptome; np.ndarray or .h5ad X layer)
- Feature matrix from second omics modality (e.g., metabolome; np.ndarray or .h5ad X layer)
- Correlation threshold (numeric; user-defined)

## Outputs

- Ranked list of high-correlation feature pairs
- Correlation scores (Pearson or Spearman coefficients) for each pair
- Pair metadata (feature names, modality labels)

## How to apply

Load the feature matrices from both omics modalities (e.g., transcriptome features and metabolome features from .h5ad files or other formats). Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features. Apply a correlation threshold (exact value depends on dataset; haCCA does not specify a default) to retain only high-correlation feature pairs. Rank the filtered pairs by absolute correlation coefficient in descending order. Output the ranked feature pair list with correlation scores and metadata for downstream use in spatial alignment or network analysis.

## Related tools

- **haCCA** (Multi-module workflow that integrates cross-omics feature pair matching with modified spatial morphological alignment for spot-to-spot data integration) — github.com/LittleLittleCloud/haCCA

## Examples

```
from hacca import Data; import scanpy as sc; a_h5ad = sc.read_h5ad('a.h5ad'); b_h5ad = sc.read_h5ad('b.h5ad'); a = Data(X=a_h5ad.X.toarray(), D=a_h5ad.obsm['spatial']); b = Data(X=b_h5ad.X.toarray(), D=b_h5ad.obsm['spatial'])
```

## Evaluation signals

- Correlation coefficients are in the expected range [−1, 1] with magnitudes reflecting biological association strength.
- Number of retained pairs after thresholding is reasonable relative to dataset size (i.e., not all pairs retained, but not excessively sparse).
- Top-ranked pairs have been visually or statistically validated (e.g., known metabolite–gene regulatory relationships or pathway co-occurrence).
- Downstream spatial alignment using the matched pairs achieves stated metrics (high resolution and accuracy of spot-to-spot integration as reported for haCCA).
- Ranked list is reproducible when re-run on identical input matrices with the same correlation coefficient and threshold.

## Limitations

- Pearson and Spearman correlation assume linear or monotonic associations; non-linear cross-omics relationships may be missed.
- Correlation does not imply causation; high-scoring pairs may be confounded by shared biological or technical factors rather than direct functional links.
- Performance and ranking quality depend critically on the correlation threshold choice, which is not data-adaptively determined in the described workflow.
- No changelog or version control information is provided, limiting reproducibility across tool releases.

## Evidence

- [other] Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features.: "Compute pairwise Pearson or Spearman correlation coefficients between all transcriptome features and all metabolome features."
- [other] Filter feature pairs by correlation threshold to retain only high-correlation pairs.: "Filter feature pairs by correlation threshold to retain only high-correlation pairs."
- [other] Rank filtered pairs by absolute correlation coefficient in descending order.: "Rank filtered pairs by absolute correlation coefficient in descending order."
- [readme] haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration: "haCCA, a workflow utilizing high Correlated feature pairs combined with a modified spatial morphological alignment to ensure high resolution and accuracy of spot-to-spot data integration"
- [intro] High Correlated feature pairs identification: "High Correlated feature pairs identification"
