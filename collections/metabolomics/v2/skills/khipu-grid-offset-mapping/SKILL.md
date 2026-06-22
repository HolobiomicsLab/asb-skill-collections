---
name: khipu-grid-offset-mapping
description: Use when you have a set of ions detected in LC-MS data that are suspected to derive from the same neutral compound via different isotope and adduct patterns. Use this skill after ions have been matched to isotope and adduct patterns and assigned to grid positions (isotope row and adduct column).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python 3
  - networkx
  - mass2chem
  - Python 3 with networkx and scipy.stats
  - metDataModel
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
- Khipu is developed as an open source Python 3 package
- The graph operations are supported by the networkx library
- Khipu uses our package mass2chem for search functions
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_khipu_cq
    doi: 10.1021/acs.analchem.2c05810
    title: khipu
  dedup_kept_from: coll_khipu_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.2c05810
  all_source_dois:
  - 10.1021/acs.analchem.2c05810
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# khipu-grid-offset-mapping

## Summary

Maps observed ion m/z values to a theoretical khipu grid of isotope and adduct mass offsets, then infers the neutral mass of a compound via linear regression using the matched grid positions. This skill enables systematic annotation of degenerate ions (isotopologues and adducts) relative to a single neutral parent compound.

## When to use

You have a set of ions detected in LC-MS data that are suspected to derive from the same neutral compound via different isotope and adduct patterns. Use this skill after ions have been matched to isotope and adduct patterns and assigned to grid positions (isotope row and adduct column). The skill is particularly valuable when you have multiple ions from the same khipu instance and need to infer the true neutral mass to validate or refine your ion assignments.

## When NOT to use

- Only one ion is available in the khipu instance; linear regression requires at least 2 observations and is unreliable with fewer than 3–4.
- Ions have not yet been assigned to grid positions or the isotope/adduct annotations are ambiguous or unresolved.
- The set of ions is suspected to contain multiple neutral compounds; this skill assumes a single neutral mass and will produce incorrect results if the ion set is heterogeneous.

## Inputs

- Set of ions with assigned khipu grid positions (isotope index, adduct type, observed m/z)
- Theoretical khipu grid (table of mass offsets indexed by isotope and adduct)
- Mass precision parameter (ppm tolerance, e.g., 5 ppm)

## Outputs

- Inferred neutral mass (regression intercept)
- Confidence interval or standard error for neutral mass estimate
- Regression fit quality metrics (R², residual standard error)
- Per-ion residuals indicating fit consistency

## How to apply

First, extract all ions present in the khipu instance and retrieve their assigned grid positions (isotope type and adduct type). Load the theoretical khipu grid containing the mass offset for each (isotope, adduct) pair relative to the neutral mass—for example, the offset for M+H[+] at M0 is 1.007276 Da, for 13C/12C with M+Na[+] is 23.992631 Da, and so on. Formulate a linear regression model where the theoretical grid offsets are the predictors (X) and the observed m/z values are the response (y). Fit the model using all available ions; the regression intercept estimates the neutral mass. Validate the fit by checking that coefficient magnitudes are consistent with the expected mass offsets and that residuals are small relative to the mass precision (typically parts-per-million). Return the inferred neutral mass as the intercept, along with confidence bounds from the regression fit.

## Related tools

- **mass2chem** (Provides mass search and lookup functions to match observed m/z values against theoretical isotope and adduct patterns and grid definitions.) — https://github.com/shuzhao-li-lab/mass2chem
- **Python 3 with networkx and scipy.stats** (Linear regression fitting and statistical inference for neutral mass estimation.)
- **metDataModel** (Defines the data structure and representation of empirical compound and khipu instances that hold ion assignments and grid mappings.) — https://github.com/shuzhao-li-lab/metDataModel

## Examples

```
from khipu.main import Khipu; k = Khipu(feature_table='yeast_neg.tsv', mode='neg', ppm=5); k.weave(); neutral_mass = k.infer_neutral_mass_via_regression(khipu_instance=k.khipus[0]); print(f'Inferred neutral mass: {neutral_mass:.6f} Da')
```

## Evaluation signals

- The inferred neutral mass is within the expected mass precision (e.g., ±5 ppm) of the known or reference neutral mass if available.
- Regression R² is > 0.95, indicating that the linear model explains >95% of variance in the observed m/z values.
- Per-ion residuals (observed m/z minus predicted m/z) are small and randomly distributed, with no systematic bias toward high or low m/z.
- The regression intercept (neutral mass) is stable and consistent when subsets of ions are withheld (leave-one-out or bootstrap validation).
- Fitted coefficients for each grid offset match the theoretical offsets within measurement uncertainty, validating that the regression model is capturing the correct isotope and adduct contributions.

## Limitations

- Linear regression assumes that all ion m/z values are observed with independent, normally distributed errors; violations (e.g., systematic bias in adduct detection) can yield biased neutral mass estimates.
- The method relies on an accurate theoretical khipu grid; errors or incompleteness in the grid definition will propagate to the neutral mass inference.
- Ions assigned to rare or ambiguous grid positions may have outlier m/z values that inflate residuals and reduce fit quality; outlier detection or robust regression may be needed.
- If some ions derive from unrelated neutral compounds or contamination, the regression will be pulled toward an erroneous consensus neutral mass; pre-filtering of ions to ensure homogeneity is critical.

## Evidence

- [readme] Based on available ions and the theoretical 'khipu grid', the neutral mass can be obtained via linear regression: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression"
- [other] Neutral mass inference is performed via linear regression by using the available ions matched to the theoretical khipu grid, which contains the mass offsets for each isotope and adduct combination relative to the neutral mass.: "Neutral mass inference is performed via linear regression by using the available ions matched to the theoretical khipu grid, which contains the mass offsets for each isotope and adduct combination"
- [other] Formulate a linear regression model with the theoretical grid offsets as predictors and the observed ion m/z values as the response variable. Fit the model using all available ions to estimate the neutral mass (intercept) and validate coefficient consistency.: "Formulate a linear regression model with the theoretical grid offsets as predictors and the observed ion m/z values as the response variable. Fit the model using all available ions to estimate the"
- [readme] Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [readme] Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass"
