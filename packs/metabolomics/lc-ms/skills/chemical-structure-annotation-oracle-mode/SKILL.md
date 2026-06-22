---
name: chemical-structure-annotation-oracle-mode
description: Use when you have a known compound structure with validated MS/MS spectrum and a structural analog (modified version) with its own MS/MS spectrum, and you need to assess whether a modification site prediction method correctly identifies which atoms were altered.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3802
  edam_topics:
  - http://edamontology.org/topic_0593
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0154
  tools:
  - ModiFinder
  - BasicEvaluationEngine
  - Python
  - RDKit
  - CosineAlignmentEngine
  - MAGMaAnnotationEngine
  - GNPS
  techniques:
  - LC-MS
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

# chemical-structure-annotation-oracle-mode

## Summary

Compute quantitative modification site localization scores (is_max and average_distance) by aligning tandem mass spectra of a known compound with its modified analog and evaluating predicted modification probabilities against ground-truth structural differences. This skill evaluates the accuracy of ModiFinder's site predictions under controlled spectral alignment conditions.

## When to use

You have a known compound structure with validated MS/MS spectrum and a structural analog (modified version) with its own MS/MS spectrum, and you need to assess whether a modification site prediction method correctly identifies which atoms were altered. Use this skill when you want to compute oracle-mode evaluation metrics (is_max: whether the highest-probability site matches the true modification; average_distance: mean graph edit distance from predictions to ground truth) to benchmark site localization performance.

## When NOT to use

- You do not have ground-truth structural information (true modification sites); oracle-mode evaluation requires knowing exactly which atoms changed.
- Your compounds lack validated MS/MS spectra or precursor mass/charge annotations; missing or low-quality spectral data will cause alignment and probability generation to fail or produce unreliable scores.
- You are performing de novo modification discovery where no reference compound is available; this skill requires paired known-and-modified structures.

## Inputs

- known_compound_spectrum (MS/MS peaks as [[mz, intensity], ...], precursor_mz, precursor_charge, adduct, SMILES)
- modified_compound_spectrum (MS/MS peaks, precursor_mz, precursor_charge, adduct, optional SMILES)
- compound_accessions (GNPS library identifiers, e.g., CCMSLIB00011906190, CCMSLIB00011906105)

## Outputs

- is_max_score (float, 0.0–1.0; 1.0 if top-ranked site matches ground truth)
- average_distance_score (float, typically 0.0–1.0+; lower indicates better prediction accuracy)
- modification_site_probabilities (vector of atom-level or bond-level probability values)
- evaluation_results_json (structured output with both metrics and intermediate vectors)

## How to apply

Load both the known and modified compound spectra from GNPS using strict mass tolerance (mz_tolerance=0.01, ppm_tolerance=40) and peak filtering (ratio_to_base_peak=0.01, normalize_peaks=True). Instantiate ModiFinder with CosineAlignmentEngine for spectral matching and MAGMaAnnotationEngine with fragment annotation (breaks=3). Call mf.generate_probabilities() to compute atom-level modification site probabilities. Then instantiate BasicEvaluationEngine and invoke evaluate_single(analog_structure, target_structure, probabilities) twice—once with default_method='average_distance' and once with evaluation_method='is_max'—to retrieve both metrics. Write the resulting scores and probability vector to a results file for downstream analysis and comparison against baseline methods.

## Related tools

- **ModiFinder** (Main framework for generating modification site probabilities via tandem mass spectral alignment and annotation) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **BasicEvaluationEngine** (Computes is_max and average_distance oracle-mode evaluation scores by comparing predicted probabilities to ground-truth structural differences) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **CosineAlignmentEngine** (Aligns MS/MS peaks between known and modified compound spectra using modified cosine similarity) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **MAGMaAnnotationEngine** (Annotates aligned fragments with molecular structure fragmentation patterns (breaks=3 for default depth)) — https://github.com/Wang-Bioinformatics-Lab/ModiFinder_base
- **RDKit** (Underlying library for molecular graph representation and structure comparison) — http://www.rdkit.org/
- **Python** (Scripting environment; ModiFinder requires Python ≥3.9)
- **GNPS** (Data source for fetching validated compound spectra and metadata by accession ID) — https://gnps.ucsd.edu

## Examples

```
from modifinder import ModiFinder, CosineAlignmentEngine, MAGMaAnnotationEngine, BasicEvaluationEngine, Compound; import json; s1 = Compound(spectrum=[[100.0, 50], [200.0, 100]], precursor_mz=500.0, precursor_charge=1, adduct='[M+H]+', smiles='CC(C)C'); s2 = Compound(spectrum=[[100.0, 45], [215.0, 95]], precursor_mz=515.0, precursor_charge=1, adduct='[M+H]+', smiles='CC(C)CO'); mf = ModiFinder(s1, s2, alignment_engine=CosineAlignmentEngine(), annotation_engine=MAGMaAnnotationEngine(breaks=3)); probs = mf.generate_probabilities(); ev = BasicEvaluationEngine(default_method='average_distance'); is_max_score = ev.evaluate_single(s1.smiles, s2.smiles, probs, evaluation_method='is_max'); avg_dist_score = ev.evaluate_single(s1.smiles, s2.smiles, probs, evaluation_method='average_distance'); json.dump({'is_max': is_max_score, 'average_distance': avg_dist_score, 'probabilities': probs}, open('evaluation_results.json', 'w'))
```

## Evaluation signals

- is_max score equals 1.0 when the atom (or bond) with the highest modification probability corresponds exactly to the true modification site as determined by SMILES comparison or manual curation.
- average_distance score reflects graph edit distance; lower values (closer to 0) indicate that predicted probability ranks align better with true modification locations; values around 0.5 or below suggest good prediction quality.
- The modification_site_probabilities vector sums to 1.0 or represents a valid probability distribution over atoms/bonds; no NaN or infinite values present.
- Intermediate alignment peaks (from CosineAlignmentEngine) show non-zero matches between known and modified spectra with cosine similarity above the configured threshold, indicating successful spectral alignment.
- Reproducibility: running the same known and modified compound pair with identical parameters (mz_tolerance=0.01, ppm_tolerance=40, normalize_peaks=True, breaks=3) yields identical is_max and average_distance scores across runs.

## Limitations

- Oracle-mode evaluation requires perfect or near-perfect ground-truth annotations; if the true modification site is ambiguous or if SMILES differ only in implicit hydrogen or aromaticity representation, scores may be artificially deflated.
- Performance depends critically on spectral quality and alignment success; low signal-to-noise spectra or incomplete fragmentation patterns may prevent CosineAlignmentEngine from finding matching peaks, leading to uninformative probability distributions.
- The average_distance metric is sensitive to the choice of graph representation (atoms, bonds, or hybrid); changing the graph model used by BasicEvaluationEngine may yield different scores for the same chemical modification.
- ModiFinder is under active development; API and metric definitions may change in future versions, affecting reproducibility and comparability of historical results.

## Evidence

- [other] ModiFinder achieves BasicEvaluationEngine scores of is_max = 1.0 and average_distance = 0.514 under the default Modified Cosine + MAGMa condition.: "ModiFinder achieves BasicEvaluationEngine scores of is_max = 1.0 and average_distance = 0.514 under the default Modified Cosine + MAGMa condition."
- [other] Load known compound and modified compound with specified tolerances and peak filtering settings: "Load known compound (CCMSLIB00011906190) and modified compound (CCMSLIB00011906105) from GNPS with mz_tolerance=0.01, ppm_tolerance=40, ratio_to_base_peak=0.01, normalize_peaks=True."
- [other] Create ModiFinder with specified alignment and annotation engines: "Create ModiFinder instance with CosineAlignmentEngine and MAGMaAnnotationEngine (breaks=3, default parameters)."
- [other] Generate modification probabilities and evaluate with both metrics: "Generate modification site probabilities via mf.generate_probabilities(). Instantiate BasicEvaluationEngine with default_method='average_distance'. Call evaluate_single(analog_structure,"
- [intro] ModiFinder is a tool for site localization of structural modifications using MS/MS data.: "ModiFinder is a tool for site localization of structural modifications using MS/MS data."
- [readme] Core API overview and expected input/output structure from README: "ModiFinder Object... Pass these to a ModiFinder Object... Collect dictionary results: peaksObj, fragmentsObj = siteLocator.get_result()"
