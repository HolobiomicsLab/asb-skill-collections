---
name: rt-uncertainty-quantification-and-filtering
description: Use when you have a set of metabolite candidates with observed retention
  times and access to a trained DNN retention time predictor (MAE 39.2±1.2 s) or meta-learned
  projections between chromatographic methods.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0602
  tools:
  - alvaDesc
  - CMM-RT (cmmrt package)
  - CEU Mass Mediator
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1186/s13321-022-00613-8
  title: cmmrt
evidence_spans:
- 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity,
  and Path Fingerprints fingerprints) were generated with the alvaDesc software
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_cmmrt_cq
    doi: 10.1186/s13321-022-00613-8
    title: cmmrt
  dedup_kept_from: coll_cmmrt_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s13321-022-00613-8
  all_source_dois:
  - 10.1186/s13321-022-00613-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# RT Uncertainty Quantification and Filtering

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Compute confidence intervals around predicted retention times and use them to filter and rank metabolite annotation candidates by comparing observed versus predicted RT values. This probabilistic approach enables metabolite annotation workflows to prioritize candidates with high RT prediction confidence while excluding those falling outside expected uncertainty bounds.

## When to use

You have a set of metabolite candidates with observed retention times and access to a trained DNN retention time predictor (MAE 39.2±1.2 s) or meta-learned projections between chromatographic methods. Apply this skill when you need to rank annotation candidates by RT prediction reliability or filter out candidates whose observed RT is inconsistent with the model's projected uncertainty.

## When NOT to use

- No pre-trained DNN model or meta-learned projections are available for your chromatographic method
- Fewer than 10 calibration molecules are available for meta-learning the cross-method projection
- Observed retention times are missing or unreliable for the candidate set

## Inputs

- Molecular structures (SMILES, mol, SDF formats)
- Observed retention time values for candidate metabolites
- Pre-trained DNN retention time predictor weights
- Calibration molecules with known retention times in both source and target chromatographic methods (≥10 molecules)
- Meta-learned Gaussian Process prior for chromatographic method projection

## Outputs

- Ranked metabolite annotation candidate table with descending confidence scores
- Per-candidate RT prediction error and confidence interval bounds
- Boolean filtering flags indicating whether observed RT falls within projected uncertainty

## How to apply

Load molecular structures and predicted retention times from the pre-trained DNN model. Apply meta-learned Bayesian RT projection to map retention times between source and target chromatographic methods using available calibration molecules (minimum 10 molecules). For each candidate, compute RT prediction confidence intervals and compare the observed RT against the projected RT distribution. Score candidates by evaluating whether their observed RT falls within the confidence bounds; candidates inside the bounds receive higher scores. Rank annotation candidates by descending score (highest confidence first), outputting ranked tables that pair each candidate with its annotation score and RT prediction error. This filtering leverages the model's uncertainty quantification to prioritize chemically plausible matches.

## Related tools

- **alvaDesc** (Generates 5,666 molecular descriptors and 2,214 fingerprints (MACCS166, Extended Connectivity, Path Fingerprints) used as input features for the DNN retention time predictor) — https://www.alvascience.com/alvadesc/
- **CMM-RT (cmmrt package)** (Implements state-of-the-art DNN retention time prediction with cosine annealing warm restarts and stochastic weight averaging, plus Bayesian meta-learned GP for chromatographic method projection) — https://github.com/constantino-garcia/cmmrt
- **CEU Mass Mediator** (Target platform for integrating DNN+meta-learned projections into metabolite annotation workflow) — http://ceumass.eps.uspceu.es/

## Examples

```
from cmmrt.rt.build_data_cmm import generate_vector_fingerprints; fingerprints = generate_vector_fingerprints(aDesc, smiles='CC(C)Cc1ccc(cc1)C(C)C(=O)O'); # then score via trained DNN model and meta-learned projections to rank candidates and filter by RT confidence bounds
```

## Evaluation signals

- Confidence interval width should reflect model uncertainty: narrower intervals for predictions in high-density regions of the training set, wider for extrapolated regions
- Ranked candidates with observed RT inside confidence bounds should achieve higher annotation accuracy than those outside bounds (measurable via reference standard compounds)
- Mean absolute error between observed and projected RT for in-bounds candidates should not exceed 39.2±1.2 s (the base DNN error rate)
- Filtering should reduce the median number of candidates per query while preserving the true metabolite in the retained set
- Projection performance should remain competitive (error rates consistent with prior approaches) when meta-trained on exactly 10 calibration molecules

## Limitations

- Requires pre-trained DNN model and meta-learned GP; performance degrades significantly if models are trained on different molecular descriptor sets or chromatographic conditions
- Meta-learning requires ≥10 calibration molecules; fewer molecules may lead to overfit projections or unreliable confidence intervals
- Confidence intervals assume calibration molecules are representative of the target chromatographic method; systematic biases (e.g., column degradation, temperature drift) are not modeled
- The approach is specialized for small-molecule metabolites in METLIN-like datasets; applicability to other compound classes (peptides, polymers) is not demonstrated

## Evidence

- [other] Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected uncertainty bounds.: "Score candidate metabolites by computing RT prediction confidence intervals and comparing observed versus predicted RT values, filtering candidates where observed RT falls within the projected"
- [other] A Bayesian meta-learning approach enables RT projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous approaches.: "A Bayesian meta-learning approach enables RT projection between chromatographic methods from as few as 10 molecules while obtaining competitive error rates compared with previous approaches."
- [readme] The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and 17.2 ± 0.9 s, respectively: "The best results were obtained by a heavily regularized DNN trained with cosine annealing warm restarts and stochastic weight averaging, achieving a mean and median absolute errors of 39.2±1.2 s and"
- [other] Rank annotation candidates by descending score (highest confidence first) and output ranked candidate tables with annotation scores and RT prediction errors.: "Rank annotation candidates by descending score (highest confidence first) and output ranked candidate tables with annotation scores and RT prediction errors."
- [readme] We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotation workflow.: "We illustrate how the proposed DNN+meta-learned projections can be integrated into a metabolite annotation workflow."
