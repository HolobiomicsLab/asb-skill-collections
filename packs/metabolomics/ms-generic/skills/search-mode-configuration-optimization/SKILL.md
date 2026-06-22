---
name: search-mode-configuration-optimization
description: Use when when you have a calibrated FT-ICR mass spectrum (e.g., ESI-NEG mode) and need to decide between rapid single-assignment (first_hit=True) and exhaustive multi-assignment (first_hit=False) modes.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3647
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - matplotlib
  techniques:
  - mass-spectrometry
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters import MSParameters']
- import pandas as pd
- pandas [section=results; evidence='import pandas as pd']
- import numpy as np
- numpy [section=results; evidence='import numpy as np']
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corems
    doi: 10.5281/zenodo.14009575
    title: corems
  dedup_kept_from: coll_corems
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.5281/zenodo.14009575
  all_source_dois:
  - 10.5281/zenodo.14009575
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# search-mode-configuration-optimization

## Summary

Configuring and comparing molecular formula search modes (first-hit vs. all-hits) to understand how prioritization strategies affect assignment counts, score distributions, and computational efficiency. This skill is essential when optimizing molecular formula annotation workflows for different analytical goals—e.g., rapid screening vs. comprehensive assignment.

## When to use

When you have a calibrated FT-ICR mass spectrum (e.g., ESI-NEG mode) and need to decide between rapid single-assignment (first_hit=True) and exhaustive multi-assignment (first_hit=False) modes. Use this skill if your research question centers on how search mode affects the number and quality of molecular formula candidates assigned to each m/z peak, or if you are benchmarking CoreMS SearchMolecularFormulas performance across different prioritization strategies.

## When NOT to use

- Your input spectrum is already processed or centroided at a different resolving power—first_hit vs. all_hits comparison is most meaningful on raw or calibrated high-resolution FT data.
- You are performing targeted analysis on a known set of compounds where single-candidate assignment is sufficient; the skill is intended for exploratory or benchmarking workflows.
- Your workflow requires isotopic fine structure calculation; SearchMolecularFormulas first_hit mode may skip isotope refinement steps needed for some applications.

## Inputs

- Calibrated FT-ICR mass spectrum (Bruker CompassXtract .d, Thermo .raw, or CoreMS .hdf5)
- Molecular formula reference database file (.ref format, e.g., SRFA.ref)
- CoreMS MSParameters configuration object

## Outputs

- Assignment count statistics (total assignments per mode)
- Score distribution metrics (mean, median, std, min, max) per mode
- Comparison summary table (CSV) contrasting first_hit=True vs. first_hit=False results

## How to apply

Load your calibrated mass spectrum from a vendor format (Bruker .d, Thermo .raw, or CoreMS .hdf5) and reference molecular formula database (e.g., SRFA.ref). Configure CoreMS SearchMolecularFormulas with first_hit=True and execute formula assignment on the spectrum, extracting and tabulating the count of assignments and score statistics (mean, median, std, min, max). Repeat the same assignment workflow with first_hit=False on the same spectrum. Compare the two assignment modes by generating a summary table contrasting counts and score distributions. The rationale is that first_hit=True prioritizes speed by returning the highest-scoring candidate only, while first_hit=False returns all candidates within the search space, enabling assessment of score spread and confidence in peak assignments.

## Related tools

- **CoreMS** (Core framework providing SearchMolecularFormulas class with configurable first_hit parameter; handles calibrated spectrum I/O and formula assignment logic) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Tabulation, aggregation, and export of assignment counts and score distribution statistics to CSV)
- **numpy** (Vectorized computation of score distribution metrics (mean, median, std, min, max))
- **matplotlib** (Visualization of score distribution comparisons between first_hit modes (histograms, boxplots))
- **Docker** (Reproducible containerized environment for CoreMS, supporting consistent parameter configuration across runs)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; import pandas as pd; MSParameters.molecular_search.first_hit = True; assignments_true = spectrum.search_molecular_formulas(); MSParameters.molecular_search.first_hit = False; assignments_false = spectrum.search_molecular_formulas(); stats = pd.DataFrame({'mode': ['first_hit=True', 'first_hit=False'], 'count': [len(assignments_true), len(assignments_false)], 'mean_score': [assignments_true.scores.mean(), assignments_false.scores.mean()]}); stats.to_csv('comparison.csv')
```

## Evaluation signals

- Assignment counts from first_hit=True are ≤ those from first_hit=False (first_hit=True returns at most one candidate per peak)
- Mean and median scores from first_hit=True are ≥ those from first_hit=False (best candidate is prioritized when first_hit=True)
- Score standard deviation is lower in first_hit=True mode (single or very few assignments per peak vs. distribution across all candidates)
- CSV output is well-formed and contains all expected columns (m/z, count_first_hit_true, count_first_hit_false, mean_score_true, mean_score_false, etc.)
- Comparison table rows match the number of peaks in the input spectrum; no peaks should be missing or duplicated

## Limitations

- SearchMolecularFormulas first_hit behavior depends on the order of candidate generation and may not be deterministic across different molecular formula database versions or search space definitions.
- Comparison of score distributions is only valid if both modes run on the same calibrated spectrum, with identical MSParameters (mass tolerance, charge states, heteroatom counts, etc.), otherwise differences reflect parameter changes rather than search mode effects.
- The skill assumes the reference database (.ref file) is complete and correctly formatted; corrupted or incomplete databases will skew assignment counts and score statistics.
- Performance gains from first_hit=True are spectrum-dependent and may not translate to wall-clock time savings if spectrum I/O and calibration dominate runtime.

## Evidence

- [other] SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes.: "SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes."
- [other] Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode.: "Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode."
- [readme] CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis.: "CoreMS is a comprehensive mass spectrometry framework for software development and data analysis of small molecules analysis."
- [readme] Automatic molecular formulae assignments algorithm for ESI(-) MS for natural organic matter analysis: "Automatic molecular formulae assignments algorithm for ESI(-) MS for natural organic matter analysis"
- [other] Load the calibrated mass spectrum from ESI_NEG_SRFA.d dataset and reference file SRFA.ref.: "Load the calibrated mass spectrum from ESI_NEG_SRFA.d dataset and reference file SRFA.ref."
