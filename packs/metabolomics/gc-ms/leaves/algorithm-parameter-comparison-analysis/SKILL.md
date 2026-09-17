---
name: algorithm-parameter-comparison-analysis
description: Use when when you need to evaluate how a specific algorithm parameter
  (such as SearchMolecularFormulas first_hit mode) affects the quantity and quality
  of molecular formula assignments on a given spectrum or dataset.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Docker
  - CoreMS
  - pandas
  - numpy
  - matplotlib
  techniques:
  - GC-MS
  - NMR
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.5281/zenodo.14009575
  title: corems
evidence_spans:
- from corems.encapsulation.factory.parameters import MSParameters
- CoreMS [section=results; evidence='from corems.encapsulation.factory.parameters
  import MSParameters']
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

# algorithm-parameter-comparison-analysis

## Summary

Systematically compare molecular formula assignment behavior by running the same algorithm with different parameter configurations (e.g., first-hit vs. all-hits modes) and contrasting assignment counts, score distributions, and quality metrics. This skill enables evidence-based parameter tuning for mass spectrometry annotation workflows.

## When to use

When you need to evaluate how a specific algorithm parameter (such as SearchMolecularFormulas first_hit mode) affects the quantity and quality of molecular formula assignments on a given spectrum or dataset. Use this when the output sensitivity/specificity trade-off is unknown or when optimizing assignment behavior for a particular sample type (e.g., natural organic matter like SRFA).

## When NOT to use

- When the spectrum has not yet been calibrated or baseline-corrected; calibration is a prerequisite for meaningful formula assignment comparison.
- When only a single parameter variant is available or when the algorithm does not support the parameter variation you wish to test.
- When the input mass spectrum is from a different ionization mode or chemical class (e.g., positive-ion ESI or GC-MS) than the reference database; mismatches invalidate comparative conclusions.

## Inputs

- Calibrated mass spectrum (Bruker .d format, e.g., ESI_NEG_SRFA.d)
- Molecular reference file (e.g., SRFA.ref)
- MSParameters configuration object with algorithm parameters

## Outputs

- Tabulated assignment counts per mode (integer)
- Score distribution statistics per mode (mean, median, std, min, max)
- Comparison summary table (CSV format)
- Visualization of score distributions (matplotlib plots)

## How to apply

Load a calibrated mass spectrum from an instrument-specific format (e.g., ESI_NEG_SRFA.d Bruker Solarix data) and a reference file (e.g., SRFA.ref). Configure the SearchMolecularFormulas algorithm with the first parameter variant (e.g., first_hit=True) and execute formula assignment, then repeat with the alternative configuration (e.g., first_hit=False) on the identical spectrum. Extract assignment counts and score distribution statistics (mean, median, std, min, max) for each mode using pandas and numpy. Generate a comparison summary table contrasting both modes side-by-side and save as CSV, allowing direct inspection of how the parameter choice alters assignment behavior—e.g., whether first-hit prioritization reduces candidate count while preserving high-confidence matches.

## Related tools

- **CoreMS** (Provides SearchMolecularFormulas algorithm, MSParameters configuration, mass spectrum I/O, and calibration functions) — https://github.com/EMSL-Computing/CoreMS
- **pandas** (Tabulation, aggregation, and export of assignment counts and score statistics to CSV)
- **numpy** (Numerical computation of distribution statistics (mean, median, std, min, max))
- **matplotlib** (Visualization of score distributions for comparative inspection)
- **Docker** (Containerization of the CoreMS environment for reproducible execution)

## Examples

```
from corems.encapsulation.factory.parameters import MSParameters; ms = load_spectrum('ESI_NEG_SRFA.d', 'SRFA.ref'); results_first_hit = [ms.run(SearchMolecularFormulas(first_hit=True)) for s in [ms]]; results_all_hits = [ms.run(SearchMolecularFormulas(first_hit=False)) for s in [ms]]; comparison = pd.DataFrame({'mode': ['first_hit=True', 'first_hit=False'], 'assignment_count': [len(results_first_hit[0]), len(results_all_hits[0])], 'mean_score': [np.mean([x.score for x in results_first_hit[0]]), np.mean([x.score for x in results_all_hits[0]])]}); comparison.to_csv('formula_assignment_comparison.csv', index=False)
```

## Evaluation signals

- Assignment count differs between first_hit=True and first_hit=False modes (if parameter has intended effect, counts should diverge)
- Score distribution statistics (mean, median, std) are numerically distinct between modes, indicating parameter influence on ranking/filtering
- Comparison table is non-empty and contains valid numeric entries for all computed statistics (schema check: no NaN or missing values in critical columns)
- CSV output is machine-readable and can be re-loaded as a pandas DataFrame without errors (format validation)
- Score ranges (min, max) are physically plausible for the algorithm (e.g., normalized scores should fall within [0, 1] or a known range)

## Limitations

- The comparison is sensitive to the reference database contents and calibration quality; poor calibration or incomplete reference data will bias both modes similarly, masking parameter effects.
- first_hit mode may introduce bias toward abundant or low-mass-error candidates, which may not reflect true chemical composition; user must judge whether this trade-off suits their scientific question.
- Comparison of assignment counts alone does not reveal correctness—both modes may assign incorrect formulas; validation against independent methods (e.g., tandem MS, NMR) is required for accuracy assessment.
- The skill assumes the same spectrum is processed twice; if preprocessing (noise threshold, calibration) differs between runs, comparison validity is compromised.

## Evidence

- [other] SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes.: "SearchMolecularFormulas can be run with first_hit parameter set to True or False, enabling comparison of assignment behavior under different prioritization modes."
- [other] Configure SearchMolecularFormulas with first_hit=True and execute formula assignment on the spectrum. 3. Configure SearchMolecularFormulas with first_hit=False and execute formula assignment on the same spectrum. 4. Extract and tabulate assignment counts and score distribution statistics (mean, median, std, min, max) for each mode.: "Configure SearchMolecularFormulas with first_hit=True and execute formula assignment on the spectrum. Configure SearchMolecularFormulas with first_hit=False and execute formula assignment on the same"
- [other] Load the calibrated mass spectrum from ESI_NEG_SRFA.d dataset and reference file SRFA.ref.: "Load the calibrated mass spectrum from ESI_NEG_SRFA.d dataset and reference file SRFA.ref."
- [readme] Automatic molecular formulae assignments algorithm for ESI(-) MS for natural organic matter analysis: "Automatic molecular formulae assignments algorithm for ESI(-) MS for natural organic matter analysis"
- [other] from corems.encapsulation.factory.parameters import MSParameters; import pandas as pd; import numpy as np; from matplotlib import pyplot: "from corems.encapsulation.factory.parameters import MSParameters; import pandas as pd; import numpy as np; from matplotlib import pyplot"
