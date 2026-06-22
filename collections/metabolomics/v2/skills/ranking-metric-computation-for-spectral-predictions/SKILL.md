---
name: ranking-metric-computation-for-spectral-predictions
description: Use when after generating ranked predictions of chemical formulas or subformulas for MS/MS spectra (from a neural network model like MIST-CF's formula transformer), compare predicted assignments against ground-truth reference labels to measure ranking quality.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3927
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - MIST
  - MIST-CF
  - SCARF
  - SIRIUS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- an extension of MIST for annotating MS1 precursor masses from MS/MS data
- MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach
- Utilizing sinusoidal formula embeddings as developed in our previous work SCARF
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf
schema_version: 0.2.0
---

# Ranking Metric Computation for Spectral Predictions

## Summary

Compute per-peak accuracy, exact-match rate per spectrum, and ranking metrics (e.g., fraction of correct subformulas in top-k predictions) to evaluate how well predicted chemical subformula or formula assignments match reference labels in MS/MS spectra. This skill quantifies the quality of candidate ranking without external databases or fragmentation tree computation.

## When to use

After generating ranked predictions of chemical formulas or subformulas for MS/MS spectra (from a neural network model like MIST-CF's formula transformer), compare predicted assignments against ground-truth reference labels to measure ranking quality. This is especially relevant when evaluating de novo formula inference in a held-out test set where you need to assess whether correct assignments appear at the top of the ranking list.

## When NOT to use

- Input predictions are unranked (e.g., a single point estimate with no confidence ordering); ranking metrics require an ordered candidate list.
- Ground-truth labels are unavailable or unreliable; ranking metrics require comparison against reference assignments.
- The task is MS1 precursor mass annotation only, without MS/MS fragmentation data; this skill is specific to fragment or precursor formula prediction from tandem spectra.

## Inputs

- MS/MS spectra with observed m/z peaks (from test dataset)
- Precursor m/z and precursor formula (ground truth) for each spectrum
- Ranked predictions of chemical formulas or subformulas per peak (from MIST-CF or similar ranking model)
- Reference chemical formula or subformula labels per peak

## Outputs

- Per-peak accuracy metric
- Exact-match rate per spectrum
- Top-k ranking metrics (fraction correct in top-k)
- Mean reciprocal rank (MRR) or similar ranking statistic
- Overall evaluation report with landmark errors on held-out set

## How to apply

For each spectrum in the held-out test dataset: (1) obtain the ranked list of predicted chemical formulas or subformulas (e.g., from MIST-CF's energy-based model) and the ground-truth reference label(s); (2) compute per-peak accuracy as the fraction of peaks where the top-ranked prediction matches the reference; (3) compute exact-match rate per spectrum as 1 if all peaks in a spectrum have correct top-ranked predictions, 0 otherwise; (4) compute ranking metrics such as the fraction of spectra where the correct formula appears in the top-k predictions (e.g., top-5, top-10), or mean reciprocal rank (MRR) of the correct formula across all spectra; (5) aggregate these metrics across the entire held-out set to produce precision, recall, and ranking statistics. These metrics reveal both whether the model ranks candidates correctly and how far down the ranking list one must search to find the ground-truth assignment.

## Related tools

- **MIST-CF** (Neural network-based formula transformer that generates ranked chemical formula and subformula predictions for MS/MS fragment peaks; outputs are fed into ranking metric computation.) — https://github.com/samgoldman97/mist-cf
- **MIST** (Parent model for MIST-CF; provides the core formula transformer architecture and baseline for comparison of ranking performance.)
- **SIRIUS** (Baseline tool for formula enumeration and fragmentation tree computation; used as a reference method for comparative ranking evaluation (e.g., comparison with SIRIUS on test data).) — https://bio.informatik.uni-jena.de/software/sirius/

## Examples

```
python analysis/evaluate_pred.py --predictions mist_cf_out/predictions.json --references test_set_labels.json --top_k 5 10 20 --output eval_report.txt
```

## Evaluation signals

- Per-peak accuracy should be consistent across different subsets of the test set (no anomalous drops for specific m/z ranges or precursor masses).
- Exact-match rate per spectrum should monotonically increase (or remain stable) as top-k threshold increases; if correct formula is in top-10, it should also be in top-20.
- Mean reciprocal rank (MRR) should be high (e.g., > 0.7) if the model is well-calibrated; MRR close to 1.0 indicates correct formulas ranked first.
- Comparison with baseline methods (e.g., SIRIUS) should show MIST-CF achieving equal or better top-k accuracy without external spectrum database queries.
- Landmark errors (e.g., spectra where correct formula is ranked outside top-100) should be documented and traced to specific peak properties (e.g., low m/z, high noise, rare precursor mass).

## Limitations

- Ranking metrics assume a single ground-truth reference label per peak; spectra with isobaric or ambiguous formulas may have multiple valid assignments not captured in the metric.
- Top-k metrics are sensitive to the choice of k; different applications may require different thresholds (e.g., metabolomics pipelines may tolerate top-100, while high-confidence identification requires top-5).
- Per-peak accuracy assumes perfect peak picking and mass calibration; errors in peak detection or m/z measurement will artificially lower metrics even if the model's ranking is correct.
- The skill evaluates ranking quality only on the held-out test set; generalization to out-of-distribution spectra (e.g., different instruments, ionization modes, or chemical classes) is not measured.
- Exact-match rate per spectrum is a strict metric that penalizes even a single incorrect peak assignment; it may not reflect usability in exploratory metabolomics where partial matches are informative.

## Evidence

- [other] Compare predicted subformula assignments against reference labels and compute per-peak accuracy, exact-match rate per spectrum, and ranking metrics (e.g., fraction of correct subformulas in top-k predictions).: "compute per-peak accuracy, exact-match rate per spectrum, and ranking metrics (e.g., fraction of correct subformulas in top-k predictions)"
- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases"
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion"
- [other] Report evaluation metrics and landmark errors on the held-out set.: "Report evaluation metrics and landmark errors on the held-out set"
- [other] Apply the MIST-CF internal subformula assignment protocol (neural network-based formula transformer) to rank candidate subformulas for each observed fragment peak, conditioned on the precursor formula and observed m/z value.: "rank candidate subformulas for each observed fragment peak, conditioned on the precursor formula and observed m/z value"
