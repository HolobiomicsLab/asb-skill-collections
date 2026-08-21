---
name: tree-based-model-validation
description: Use when after training a decision tree classifier on ChemEcho sparse
  feature vectors (representing tandem mass spectra fragmentation patterns), especially
  when the goal is to deploy predictions as executable queries or to validate that
  learned splits correspond to chemically meaningful.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3432
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0091
  tools:
  - ChemEcho
  - Decision tree classifier (scikit-learn or equivalent tree-based ML framework)
  - scikit-learn (Decision Tree Classifier)
  - Mass Query Language (MassQL)
  - LIME
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c02591
  title: ChemEcho
- doi: 10.1145/2939672.2939778
  title: ''
evidence_spans:
- github.com__biorack__chemecho
- Using ChemEcho vectors, we can train decision trees which are able to be directly
  converted to MassQL
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_chemecho_cq
    doi: 10.1021/acs.analchem.5c02591
    title: ChemEcho
  dedup_kept_from: coll_chemecho_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c02591
  all_source_dois:
  - 10.1021/acs.analchem.5c02591
  - 10.1145/2939672.2939778
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# tree-based-model-validation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Validate and interpret shallow decision trees trained on sparse ChemEcho feature vectors by examining prediction accuracy, decision splits, and convertibility to domain-specific queries (MassQL). This skill ensures that tree-based models on interpretable mass spectrometry features are trustworthy and actionable for fragmentation-pattern prediction.

## When to use

After training a decision tree classifier on ChemEcho sparse feature vectors (representing tandem mass spectra fragmentation patterns), especially when the goal is to deploy predictions as executable queries or to validate that learned splits correspond to chemically meaningful fragmentation criteria. Use this skill when interpretability and reproducibility are essential—e.g., when predicting functional group presence (sulfo groups, etc.) and you need to inspect which peaks or neutral losses drive each prediction.

## When NOT to use

- Input is already a feature table or low-dimensional embedding (latent space); ChemEcho's value lies in sparse, interpretable formulas—if features are already latent vectors, conversion and chemical interpretation are not possible.
- The tree is too deep or complex (>5–10 levels) to inspect manually; at that point, tree-based interpretability loses value and black-box approximation (e.g., LIME) may be more suitable.
- Fragmentation patterns are highly idiosyncratic and do not correspond to known chemical fragmentation rules; tree splits may lack chemical defensibility, making deployment risky.

## Inputs

- Trained decision tree classifier (scikit-learn or equivalent)
- ChemEcho sparse feature vectors (high-dimensional, where each dimension is a peak or neutral loss formula)
- Binary or multiclass labels (e.g., sulfo group presence/absence)
- Test or validation subset of ChemEcho vectors and labels

## Outputs

- Tree structure documentation (node splits, thresholds, leaf predictions)
- Prediction accuracy metrics (e.g., classification accuracy, precision, recall)
- MassQL query strings derived from tree paths
- Validation report documenting alignment between learned splits and fragmentation chemistry
- Interpretability assessment (decision paths convertible to executable queries)

## How to apply

Extract and document the trained tree structure, including node splits, thresholds, and leaf predictions, then validate prediction accuracy on a held-out test set. Examine individual tree paths to confirm that splits align with known fragmentation chemistry (e.g., specific m/z values or neutral loss formulas from ChemEcho). Convert at least one representative path to a MassQL query and verify it can be deployed against raw spectra. Assess interpretability by checking whether the feature thresholds (which represent unique peak or neutral loss formulas) are chemically defensible and whether the tree depth allows human inspection of decision logic. Document any paths that achieve high prediction confidence to enable straightforward deployment.

## Related tools

- **ChemEcho** (Converts tandem mass spectra into sparse feature vectors where each dimension is a unique peak or neutral loss formula; required input for training and validating interpretable tree-based models on fragmentation data.) — https://github.com/biorack/chemecho
- **scikit-learn (Decision Tree Classifier)** (Trains the shallow decision tree classifier on sparse ChemEcho feature vectors; provides tree structure extraction for interpretation and validation.)
- **Mass Query Language (MassQL)** (Domain-specific language for expressing fragmentation patterns; target format for converting validated tree paths into deployable queries against tandem mass spectra.) — https://mwang87.github.io/MassQueryLanguage_Documentation/
- **LIME** (Local interpretable model-agnostic explanations; mentioned as an alternative for approximating black-box predictions when tree-based interpretability is insufficient.) — https://dl.acm.org/doi/10.1145/2939672.2939778

## Evaluation signals

- Prediction accuracy on held-out test set is above a domain-appropriate threshold (e.g., >80% for binary classification of functional group presence) and precision/recall are balanced.
- All node splits correspond to ChemEcho feature indices (peak or neutral loss formulas) and thresholds are within biologically plausible ranges for m/z values or neutral loss masses.
- At least one tree path can be successfully converted to a valid MassQL query string and executed against validation spectra with predictions matching the tree's leaf label.
- Tree depth is ≤5–10 levels, allowing a domain expert to inspect and approve each decision path within a reasonable time; no path requires understanding >3 sequential feature conditions.
- Converted MassQL queries retrieve spectra with fragmentation patterns consistent with the learned splits (e.g., presence of expected peaks or neutral losses in true positives).

## Limitations

- Shallow tree depth is required for interpretability, which may trade off overall predictive accuracy compared to ensembles or deeper models; validation must confirm that accuracy is sufficient for the deployment context.
- ChemEcho feature vectors are sparse and high-dimensional; interpretation relies on access to the original mass spectrometry metadata (peak masses, neutral loss formulas) to map feature indices back to chemistry, which may not always be available.
- Conversion of tree paths to MassQL queries assumes a 1:1 mapping between tree thresholds and query conditions; complex thresholds or unusual feature interactions may not translate cleanly, limiting deployability.
- Tree validation assumes that fragmentation patterns are reproducible and correspond to known chemistry; spectra from novel compounds or unusual ionization conditions may not align with learned splits, causing tree predictions to be unreliable in those domains.

## Evidence

- [other] Extract and document the decision tree structure, including node splits, thresholds, and leaf predictions.: "Extract and document the decision tree structure, including node splits, thresholds, and leaf predictions."
- [intro] ChemEcho converts tandem mass spectra into sparse feature vectors representing unique peak or neutral loss formulas for interpretable ML.: "ChemEcho is a tool for converting tandem mass spectra into sparse feature vectors, enabling the training of interpretable machine learning models. Rather than mapping fragmentation data into a latent"
- [intro] Sparse, high-dimensional feature vectors from ChemEcho are well-suited for tree-based machine learning architectures.: "The resulting sparse, high-dimensional feature vectors are well-suited for models that handle sparse inputs, such as regression and tree-based architectures."
- [intro] Decision trees trained on ChemEcho vectors can be converted directly to MassQL queries for deployment and evaluation.: "Using ChemEcho vectors, we can train decision trees which are able to be directly converted to MassQL for straightforward deployment, and to more easily evaluate the prediction criteria."
- [readme] MassQL is a domain-specific language used to describe fragmentation patterns of tandem mass spectra.: "The Mass Query Language (MassQL) is a domain specific language used to describe fragmentation patterns (and other attributes) of tandem mass spectra."
- [readme] Shallow decision tree trained to predict sulfo group presence can be converted to MassQL queries.: "Shown here is a shallow decision tree trained to predict the presence of a sulfo group, and the resulting query built from one path of the tree."
