---
name: mass2motif-parameter-optimization
description: Use when when you have a preprocessed bag-of-fragments corpus from tandem mass spectrometry spectra and need to train an MS2LDA model to discover Mass2Motifs.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - MS2LDA
  - Latent Dirichlet Allocation (LDA)
  - Python
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1073/pnas.1608041113
  title: MS2LDA
evidence_spans:
- MS2LDA (Mass Spectrometry–Latent Dirichlet Allocation) is a framework
- MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns
- Apply LDA to the processed spectra
- Configure the Python environment (set PYTHONPATH, activate conda, etc.)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_ms2lda
    doi: 10.1073/pnas.1608041113
    title: MS2LDA
  dedup_kept_from: coll_ms2lda
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1073/pnas.1608041113
  all_source_dois:
  - 10.1073/pnas.1608041113
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass2motif-parameter-optimization

## Summary

Optimize MS2LDA hyperparameters (alpha, beta, n_motifs, n_iterations) to produce a well-trained Mass2Motif model that accurately infers recurring fragmentation patterns from a bag-of-fragments corpus. This skill ensures the LDA model converges reliably and recovers interpretable, high-quality motifs.

## When to use

When you have a preprocessed bag-of-fragments corpus from tandem mass spectrometry spectra and need to train an MS2LDA model to discover Mass2Motifs. Use this skill before model training to select hyperparameters that balance convergence speed, motif interpretability, and computational cost. Particularly important when the number of expected fragmentation patterns or spectral complexity is unknown or when previous model runs produced unstable or non-convergent results.

## When NOT to use

- Input is not a bag-of-fragments corpus — preprocessing (neutral loss extraction, noise filtering) must precede parameter optimization.
- You already have a trained, validated MS2LDA model from a previous run on the same corpus — reuse existing hyperparameters rather than re-optimizing.
- The dataset is very small (<100 spectra) or very large (>1M spectra) — extreme scales may require custom guidance outside standard parameter ranges.

## Inputs

- bag-of-fragments corpus (from Preprocessing module, in MS2LDA.modeling format)
- candidate hyperparameter ranges (alpha, beta, n_motifs, n_iterations)

## Outputs

- convergence_curve.png (LDA objective/likelihood vs. iteration)
- hyperparameter_selection_report (summary of tested values and chosen parameters)
- convergence_metrics (final objective, variance, iteration count)

## How to apply

Initialize an MS2LDA LDA model with candidate hyperparameters: Dirichlet priors alpha and beta control topic sparsity and word-topic sparsity respectively; n_motifs sets the number of topics (Mass2Motifs) to infer; n_iterations determines training duration. Train the model on the corpus and monitor convergence by recording the LDA objective or likelihood across iterations. Plot the convergence curve to visually inspect whether the model has stabilized; a plateau indicates sufficient iterations. Evaluate each parameter set by assessing motif coherence (whether fragment/loss associations are chemically meaningful) and discriminative power (whether motifs capture distinct fragmentation behavior). Select the parameter combination that minimizes objective function variance in later iterations while keeping n_iterations computationally feasible (typically 50–200 iterations for production use). Document the chosen hyperparameters and convergence curve as quality assurance artifacts before final model serialization.

## Related tools

- **MS2LDA** (Primary LDA modeling framework; implements Latent Dirichlet Allocation for fragmentation pattern inference) — https://github.com/vdhooftcompmet/MS2LDA
- **Latent Dirichlet Allocation (LDA)** (Core topic-modeling algorithm; optimized via hyperparameter tuning to learn Mass2Motifs)
- **Python** (Environment for running MS2LDA.modeling, logging convergence metrics, and plotting convergence curves)

## Examples

```
from MS2LDA.modeling import LDAModel; model = LDAModel(n_motifs=20, n_iterations=100, alpha=0.01, beta=0.01); model.train(corpus); model.plot_convergence('convergence_curve.png')
```

## Evaluation signals

- Convergence curve (convergence_curve.png) shows monotonic or near-monotonic decrease in LDA objective/likelihood, with plateau by iteration ~50–150 indicating model stability.
- Final model achieves reasonable predictive log-likelihood or perplexity on held-out test set (if validation corpus available).
- Extracted Mass2Motif distributions show biochemically plausible fragment/loss associations (e.g., losses of 18 (H₂O), 44 (CO₂), or common neutral losses specific to compound class).
- Motif-topic distributions are not uniformly distributed; some motifs are rare and others common, reflecting expected spectrum heterogeneity.
- Convergence curve shows no divergence (objective increasing) or extreme oscillations, which indicate too-high learning rates or ill-conditioned initialization.

## Limitations

- LDA convergence and motif quality are sensitive to corpus composition; imbalanced datasets (e.g., one compound family dominating) may produce biased motifs.
- No single 'correct' hyperparameter set exists; optimal values depend on spectral complexity, dataset size, and downstream annotation requirements.
- Convergence curves alone do not guarantee motif interpretability; convergence is necessary but not sufficient for chemical validity.
- Computational cost scales with n_motifs and n_iterations; very large n_motifs (>50) or n_iterations (>500) may be prohibitive without GPU acceleration.
- The original MS2LDA paper (2016) used fixed hyperparameters; this tool's improved usability allows flexible tuning, but guidance on optimal ranges for different MS/MS acquisition modes (DDA, DIA, SWATH) is limited in the literature.

## Evidence

- [other] Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs): "Initialize an LDA model with specified hyperparameters (alpha, beta) and the desired number of topics (n_motifs)."
- [other] Train the LDA model on the corpus for the specified number of iterations (n_iterations), recording convergence metrics: "Train the LDA model on the corpus for the specified number of iterations (n_iterations), recording convergence metrics."
- [other] Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact: "Generate and save the convergence curve (convergence_curve.png) showing LDA objective or likelihood across iterations as a quality assurance artifact."
- [methods] MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns: "MS2LDA uses Latent Dirichlet Allocation (LDA) to infer which motifs are most likely to explain the observed fragmentation patterns"
- [methods] Learn Mass2Motifs that describe recurring fragmentation patterns from processed spectra: "Learn Mass2Motifs that describe recurring fragmentation patterns"
