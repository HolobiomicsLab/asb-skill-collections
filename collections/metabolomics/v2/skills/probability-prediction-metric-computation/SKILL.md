---
name: probability-prediction-metric-computation
description: Use when after running ModiFinder's probability generation on a known compound–modified compound pair, you have a vector of per-atom modification probabilities and need to validate whether the predicted probability peaks align with the true modification sites.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3407
  - http://edamontology.org/topic_3520
  tools:
  - ModiFinder
  - BasicEvaluationEngine
  - Python
  - RDKit
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/jasms.4c00061
  title: ModiFinder
evidence_spans:
- mf = ModiFinder(known_compound, modified_compound, mz_tolerance=0.01, ppm_tolerance=40)
- mf = ModiFinder(known_compound, modified_compound, helpers=helpers_array, **args)
- eval_engine = BasicEvaluationEngine(default_method="is_max")
- eval_engine = BasicEvaluationEngine(default_method="average_distance")
- ModiFinder requires Python 3.9 or above.
- ModiFinder requires Python 3.9 or above
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_modifinder_cq
    doi: 10.1021/jasms.4c00061
    title: ModiFinder
  dedup_kept_from: coll_modifinder_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/jasms.4c00061
  all_source_dois:
  - 10.1021/jasms.4c00061
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Probability-Prediction Metric Computation

## Summary

Compute evaluation metrics (is_max and average_distance) that quantify how well predicted modification site probability distributions match ground-truth structural modifications. This skill bridges probabilistic predictions from spectral alignment to interpretable performance scores.

## When to use

After running ModiFinder's probability generation on a known compound–modified compound pair, you have a vector of per-atom modification probabilities and need to validate whether the predicted probability peaks align with the true modification sites. Use this skill when you have both (1) predicted probabilities from mf.generate_probabilities() and (2) annotated structures with known modification locations.

## When NOT to use

- Probabilities have not yet been generated (must run mf.generate_probabilities() first).
- Ground-truth modification sites are unknown or unlabeled in the input structures.
- Input probability vector length does not match the number of atoms in the target structure (will raise a dimension mismatch error).

## Inputs

- Analog compound structure (RDKit Mol object or SMILES string)
- Modified compound structure (RDKit Mol object or SMILES string)
- Modification site probability vector (1D array of floats, length = number of atoms)

## Outputs

- is_max score (float, 0–1; 1.0 if highest probability atom is a true modification site)
- average_distance score (float, typically 0–1; 1.0 if predictions perfectly match ground truth)
- Evaluation results JSON (includes both scores and intermediate probability data)

## How to apply

Instantiate BasicEvaluationEngine and call evaluate_single() with three arguments: the analog (known) structure, the target (modified) structure, and the probability vector. The engine computes two complementary metrics: is_max checks whether the highest probability is assigned to a true modification site (binary/presence metric), and average_distance measures the mean graph-edit distance from predicted high-probability atoms to the nearest true modification atom (continuous/proximity metric). Run the evaluation twice—once with default_method='average_distance' and once with evaluation_method='is_max'—to obtain both scores. The scores range from 0–1, with 1.0 indicating perfect alignment of predictions to ground truth; average_distance penalizes off-target predictions by their topological distance in the molecular graph.

## Related tools

- **ModiFinder** (Generates modification site probabilities via generate_probabilities(); required upstream step before metric computation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **BasicEvaluationEngine** (Core evaluation component that computes is_max and average_distance scores from structures and probabilities) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Molecular structure representation and graph-based distance calculations used by the evaluation engine) — http://www.rdkit.org/
- **Python** (Runtime environment for instantiating and invoking BasicEvaluationEngine)

## Examples

```
from modifinder import BasicEvaluationEngine; evaluator = BasicEvaluationEngine(default_method='average_distance'); is_max_score = evaluator.evaluate_single(analog_structure, target_structure, probabilities, evaluation_method='is_max'); avg_dist_score = evaluator.evaluate_single(analog_structure, target_structure, probabilities, evaluation_method='average_distance')
```

## Evaluation signals

- Both is_max and average_distance scores are in the valid range [0.0, 1.0].
- is_max = 1.0 when the atom with maximum probability is a true modification site; is_max < 1.0 otherwise.
- average_distance scores inversely correlate with the graph-edit distance between predicted and true modification atoms; closer topological proximity yields higher scores.
- Probability vector sums to a normalized value consistent with the alignment engine's output (check intermediate JSON for consistency).
- Results are reproducible: identical structures and probability inputs yield identical metric outputs across multiple invocations.

## Limitations

- Requires ground-truth annotation of modification sites in both input structures; metric cannot be computed if true sites are ambiguous or unknown.
- average_distance metric depends on molecular graph topology and atom indexing; structural isomers or tautomers with identical molecular formula may yield different scores despite similar chemistry.
- Performance is sensitive to the quality and specificity of the upstream probability generation (ModiFinder's alignment and annotation); garbage probabilities will produce low scores regardless of evaluation engine correctness.
- The metric assumes a single primary modification site; compounds with multiple simultaneous modifications may have diluted probability mass, reducing both scores even if predictions are chemically plausible.

## Evidence

- [other] research_question excerpt from task_id=task_002: "What are the BasicEvaluationEngine scores (is_max and average_distance) for ModiFinder's modification site predictions under the default Modified Cosine + MAGMa condition?"
- [other] workflow step 3 and 4 from task_id=task_002: "Generate modification site probabilities via mf.generate_probabilities(). 4. Instantiate BasicEvaluationEngine with default_method='average_distance'."
- [other] workflow step 5 from task_id=task_002: "Call evaluate_single(analog_structure, target_structure, probabilities) to compute average_distance score; call again with evaluation_method='is_max' to compute is_max score."
- [other] finding from task_id=task_002: "ModiFinder achieves BasicEvaluationEngine scores of is_max = 1.0 and average_distance = 0.514 under the default Modified Cosine + MAGMa condition."
- [readme] Core API documentation from README: "Pass these to a ModiFinder Object ... Collect dictionary results: peaksObj, fragmentsObj = siteLocator.get_result()"
