---
name: threshold-based-filtering
description: Use when after computing pairwise similarity scores between query molecular
  embeddings and a reference database, apply this skill when you need to distinguish
  high-confidence candidate matches from spurious matches.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0092
  tools:
  - Convolutional Neural Network (CNN)
  - cosine similarity / Euclidean distance metric
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1101/2025.02.07.637102v1
  title: ChemEmbed
evidence_spans:
- perform predictions using a trained Convolutional Neural Network (CNN) model
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemembed_cq
    doi: 10.1101/2025.02.07.637102v1
    title: ChemEmbed
  dedup_kept_from: coll_chemembed_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.02.07.637102v1
  all_source_dois:
  - 10.1101/2025.02.07.637102v1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# threshold-based-filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Filter candidate molecule matches by applying a similarity score threshold to retain only high-confidence predictions from a CNN-based metabolite identification framework. This skill ensures that only embeddings sufficiently similar to the query meet downstream acceptance criteria.

## When to use

After computing pairwise similarity scores between query molecular embeddings and a reference database, apply this skill when you need to distinguish high-confidence candidate matches from spurious matches. Specifically: when ranked candidate lists contain many low-scoring matches and you require strict evidence thresholds for metabolite identity assignment; or when configuring the framework to balance recall (accepting more candidates) against precision (accepting only strong matches).

## When NOT to use

- Input is already a curated reference database with known high-quality annotations — thresholding is a match-filtering step, not a database curation step.
- Your analysis goal is exploratory or requires all candidate matches (including low-confidence) for rank visualization or ROC analysis — threshold filtering will discard information.
- Reference database embeddings have not yet been computed or ranked against query embeddings — apply this skill only after similarity scoring is complete.

## Inputs

- ranked_candidate_list_with_scores (CSV or DataFrame with reference molecule IDs and cosine similarity scores, sorted descending)
- similarity_threshold (float, typically 0.0–1.0, user-specified in config.yaml or command-line argument)

## Outputs

- filtered_candidate_list (subset of input ranked list; only entries with similarity_score >= threshold)
- match_metadata_with_thresholded_scores (CSV or DataFrame preserving match scores and reference molecule identifiers for accepted candidates only)

## How to apply

After ranking reference database molecules by cosine similarity score in descending order, apply a user-defined similarity threshold to each query–reference pair. Retain only matches whose similarity score meets or exceeds this threshold; discard all below-threshold matches. The threshold value is typically configurable via YAML parameters (e.g., `top_n_candidates` control); practitioners must set this based on their tolerance for false positives versus false negatives in metabolite identification. Rationale: mass spectrometry metabolite identification requires high specificity; a threshold gate prevents low-scoring accidental matches from being propagated to downstream analysis or reporting.

## Related tools

- **Convolutional Neural Network (CNN)** (Generates query and reference molecular embeddings prior to similarity scoring; filtered matches are predictions from this trained model) — https://github.com/faizanurv/ChemEmbed
- **cosine similarity / Euclidean distance metric** (Computes pairwise similarity scores between query and reference embeddings; threshold is applied to these scores) — https://github.com/faizanurv/ChemEmbed

## Examples

```
python main.py --config config.yaml  # where config.yaml includes top_n_candidates: 5 parameter that controls candidate filtering threshold
```

## Evaluation signals

- Verify that all retained candidates have similarity_score >= threshold; spot-check that all filtered-out candidates have similarity_score < threshold.
- Count of retained candidates should be <= total number of reference database molecules and typically << total count if threshold is stringent.
- No duplicates in filtered output; each query–reference pair appears at most once.
- Output schema matches input schema (same columns/fields preserved for accepted matches).
- If threshold is set to 0.0, output should include all candidates; if threshold is 1.0 (or near-perfect similarity), output should be very sparse or empty unless embeddings are identical.

## Limitations

- Threshold value is user-dependent and dataset-specific; no universally optimal threshold is provided by the framework. Practitioners must tune based on validation data or domain knowledge.
- CNN embedding quality directly determines whether similarity scores are meaningful; if the CNN model is poorly trained or reference embeddings are of low quality, thresholding may filter out true positives or retain false positives.
- Cosine similarity ranges 0–1 (or sometimes −1 to 1); Euclidean distance does not; ensure threshold and distance metric are compatible (e.g., do not apply a 0–1 threshold to unbounded Euclidean distances).
- No changelog or versioning mentioned for configuration parameters; if threshold values change across runs, reproducibility may be compromised without explicit tracking.

## Evidence

- [other] Filter candidate matches by applying a similarity threshold to retain only high-confidence matches.: "Filter candidate matches by applying a similarity threshold to retain only high-confidence matches."
- [other] Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance).: "Compute pairwise similarity scores between query embeddings and all reference database embeddings using a distance metric (e.g., cosine similarity or Euclidean distance)."
- [readme] Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity.: "Matches predicted embeddings with a reference database to find top candidate molecules based on cosine similarity."
- [readme] top_n_candidates: Number of top candidate molecules to retrieve from the reference database. (default: 5): "top_n_candidates: Number of top candidate molecules to retrieve from the reference database. (default: 5)"
- [readme] Allows users to adjust parameters like intensity thresholds, resolution, and the number of top candidates via a YAML configuration file.: "Allows users to adjust parameters like intensity thresholds, resolution, and the number of top candidates via a YAML configuration file."
