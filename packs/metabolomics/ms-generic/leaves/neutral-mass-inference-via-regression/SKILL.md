---
name: neutral-mass-inference-via-regression
description: Use when use this skill after khipu has assigned observed ions to grid
  positions (isotope and adduct combinations). Apply it when you have a connected
  subnetwork of feature ions that have been matched to known isotope and adduct patterns
  and need to estimate the neutral mass of the parent compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3172
  tools:
  - Python 3
  - networkx
  - mass2chem
  - treelib
  - metDataModel
  - khipu
  - Python 3 (scipy.stats or sklearn.linear_model)
  techniques:
  - mass-spectrometry
  license_tier: restricted
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
- Khipu is developed as an open source Python 3 package
- The graph operations are supported by the networkx library
- Khipu uses our package mass2chem for search functions
- tree visualization aided by the treelib library
- The data model of “empirical compound” is described in the metDataModel package.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neutral-mass-inference-via-regression

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Infer the neutral mass of a metabolite from observed ion m/z values by fitting a linear regression model using theoretical isotope and adduct mass offsets from the khipu grid. This skill is essential for converting degenerate ion networks into empirical compounds with a single assigned neutral mass in untargeted metabolomics.

## When to use

Use this skill after khipu has assigned observed ions to grid positions (isotope and adduct combinations). Apply it when you have a connected subnetwork of feature ions that have been matched to known isotope and adduct patterns and need to estimate the neutral mass of the parent compound. Typical trigger: you have ≥2 ions from the same khipu instance with known offsets relative to the neutral mass.

## When NOT to use

- Input contains only a single ion or ion type — regression requires ≥2 observations to estimate intercept meaningfully.
- Ions have not been assigned to a khipu grid or their isotope and adduct types are unknown.
- The khipu instance contains unresolved or misassigned ions (these are typically removed before regression).

## Inputs

- Set of observed ions with m/z values from a khipu instance
- Assigned grid positions (isotope type and adduct type) for each ion
- Theoretical khipu grid defining mass offsets for all isotope and adduct combinations

## Outputs

- Estimated neutral mass (regression intercept)
- Linear regression model fit statistics (R², residuals, coefficient estimates)

## How to apply

Extract all ions present in the khipu instance and their assigned grid positions (isotope and adduct offsets). Retrieve the theoretical khipu grid that defines the expected mass differences for all isotope and adduct patterns relative to the neutral mass. Formulate a linear regression model where the theoretical grid offsets are predictors (X) and the observed ion m/z values are the response variable (y). Fit the model using all available ions to estimate the neutral mass as the regression intercept. Validate the result by checking coefficient consistency across ions and ensuring the fitted intercept falls within a chemically reasonable range (typically 50–2000 m/z for metabolites).

## Related tools

- **khipu** (Constructs the theoretical grid, assigns ions to grid positions, and partitions ions into subnetworks before neutral mass regression is applied.) — https://github.com/shuzhao-li/khipu
- **mass2chem** (Provides search functions and mass interpretation utilities that support ion matching and grid construction within khipu.) — https://github.com/shuzhao-li-lab/mass2chem
- **networkx** (Partitions pattern-matched ion pairs into connected subnetworks; each subnetwork is then processed as a single khipu instance for neutral mass inference.)
- **Python 3 (scipy.stats or sklearn.linear_model)** (Provides linear regression implementation for fitting the neutral mass model.)

## Examples

```
from khipu import Khipu; khipu_instance = Khipu(ions_list); neutral_mass = khipu_instance.infer_neutral_mass_by_regression()
```

## Evaluation signals

- The regression intercept (neutral mass) is positive and falls within 50–2000 m/z range for typical metabolites.
- R² and residual diagnostics show good fit; residuals are normally distributed with no systematic pattern.
- Coefficient estimates are consistent across fitted ions (no extreme or contradictory slopes for equivalent isotope/adduct pairs).
- The inferred neutral mass is stable when subsets of ions are excluded (leave-one-out validation).
- Predicted m/z values for each ion (using fitted neutral mass + offset) match observed m/z within the specified ppm tolerance (typically ≤5 ppm).

## Limitations

- Regression assumes the khipu grid offsets are accurate and complete; errors or missing isotope/adduct definitions propagate into the neutral mass estimate.
- Performance degrades with small numbers of ions (n < 3); use caution when inferring from only 2 ions or when some ions are outliers or misassigned.
- Some ions may come into the initial network by mistakes or unresolved signals and are removed from the established khipu, potentially biasing the regression if misclassification occurs before the fit.
- The model does not account for systematic measurement error or instrument mass calibration bias; users should verify neutral masses against external standards or databases.
- Linear regression assumes additive errors and independence of observations; violations (e.g., correlated measurement noise across isotopologs) can inflate confidence intervals.

## Evidence

- [other] Neutral mass inference is performed via linear regression by using the available ions matched to the theoretical khipu grid, which contains the mass offsets for each isotope and adduct combination relative to the neutral mass.: "Neutral mass inference is performed via linear regression by using the available ions matched to the theoretical khipu grid, which contains the mass offsets for each isotope and adduct combination"
- [other] 1. Extract the set of ions present in the khipu instance and their assigned grid positions (isotope and adduct offsets). 2. Retrieve the theoretical khipu grid defining the expected mass differences for all isotope and adduct patterns. 3. Formulate a linear regression model with the theoretical grid offsets as predictors and the observed ion m/z values as the response variable. 4. Fit the model using all available ions to estimate the neutral mass (intercept) and validate coefficient consistency. 5. Return the inferred neutral mass as the regression intercept.: "Formulate a linear regression model with the theoretical grid offsets as predictors and the observed ion m/z values as the response variable. 4. Fit the model using all available ions to estimate the"
- [readme] Based on available ions and the theoretical khipu grid, the neutral mass can be obtained via linear regression.: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression."
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu.: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu"
