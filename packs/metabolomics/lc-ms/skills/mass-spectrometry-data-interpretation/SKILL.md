---
name: mass-spectrometry-data-interpretation
description: Use when you have a set of ions already matched to a khipu instance (i.e., ions whose isotope and adduct assignments are known and positioned on the theoretical khipu grid), and you need to estimate the neutral mass of the parent compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3435
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Python 3
  - networkx
  - mass2chem
  - metDataModel
  - khipu
  - Python 3 (scipy.stats / numpy.linalg)
  techniques:
  - LC-MS
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
  - build: coll_dbdipy_cq
    doi: 10.1093/bioinformatics/btad088/7036334
    title: DBDIpy
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

# Neutral Mass Inference via Linear Regression on Khipu Grid

## Summary

This skill infers the neutral mass of a compound from observed LC-MS ions using linear regression, where the theoretical khipu grid (containing mass offsets for isotope and adduct patterns) serves as predictors and observed m/z values are the response. It bridges ion annotation to neutral mass recovery in untargeted metabolomics workflows.

## When to use

Apply this skill when you have a set of ions already matched to a khipu instance (i.e., ions whose isotope and adduct assignments are known and positioned on the theoretical khipu grid), and you need to estimate the neutral mass of the parent compound. This is the final inference step after ions have been partitioned into an optimal tree structure and assigned to grid positions.

## When NOT to use

- Ions have not yet been assigned to grid positions or isotope/adduct types are uncertain — complete grid assignment first.
- Only a single ion is available — linear regression requires multiple ions to produce a stable estimate.
- The khipu contains primarily outlier or misassigned ions; remove or filter aberrant signals before regression.

## Inputs

- Set of ions assigned to khipu instance (m/z values with known isotope and adduct labels)
- Theoretical khipu grid (mass offsets for isotope and adduct patterns relative to neutral mass)
- Grid position assignments for each ion (isotope index and adduct type)

## Outputs

- Inferred neutral mass (regression intercept, in Daltons)
- Regression model coefficients (for validation)
- Residuals for each ion (for quality assessment)

## How to apply

Extract all ions present in the khipu instance and their assigned grid positions (isotope and adduct offsets from the theoretical khipu grid). Retrieve the theoretical khipu grid that defines expected mass differences (in Daltons) for all isotope and adduct combinations relative to neutral mass (M+0). Formulate a linear regression model where each ion's observed m/z value is the response variable, and the corresponding grid offset is the predictor. Fit the model using all available ions in the khipu; the regression intercept estimates the neutral mass. Validate that coefficient consistency is maintained across ions and that residuals are small relative to mass precision (typically ≤ 5 ppm tolerance). Return the inferred neutral mass as the regression intercept.

## Related tools

- **networkx** (Graph construction and partitioning of ion networks into connected subnetworks prior to khipu instance formation)
- **mass2chem** (Search and matching functions to identify ions that fit isotope and adduct patterns against the feature list) — https://github.com/shuzhao-li-lab/mass2chem
- **metDataModel** (Data model representation of empirical compound (khipu instance) and grid assignments) — https://github.com/shuzhao-li-lab/metDataModel
- **khipu** (Primary package implementing khipu tree construction, grid assignment, and neutral mass inference) — https://github.com/shuzhao-li/khipu
- **Python 3 (scipy.stats / numpy.linalg)** (Linear regression fitting and matrix operations for model estimation)

## Examples

```
from khipu import Khipu; khipu_instance = Khipu(ions, grid); neutral_mass = khipu_instance.infer_neutral_mass_by_regression()
```

## Evaluation signals

- Regression intercept (inferred neutral mass) is positive and lies within the expected m/z range for the compound class (e.g., 50–2000 Da for typical metabolites).
- Residuals for all ions are small relative to mass tolerance threshold (typically ≤ 5 ppm, or ≤ 0.005 × neutral_mass in Da).
- Coefficient consistency: regression slope and other parameters are stable when ions are added or removed incrementally (jackknife or leave-one-out cross-validation).
- Inferred neutral mass is consistent across multiple khipu instances if the same compound is represented by independent ion networks (e.g., different adduct types or isotope branches).
- Output neutral mass matches expected mass from reference database or matches the mass of a known metabolite with high confidence.

## Limitations

- Linear regression assumes the theoretical khipu grid offsets are accurate; errors in grid definition propagate to neutral mass estimates.
- Requires at least 2–3 reliable ions assigned to the khipu; sparse ion networks produce unstable or biased estimates.
- Ion m/z measurement error (instrumental noise, calibration drift) directly affects regression accuracy; high-precision mass spectrometry (sub-ppm) is assumed.
- Outlier ions (e.g., from unresolved signals or mistakes in initial network construction) bias the regression; the README notes these are 'removed from the established khipu, and sent off to form a new khipu'.
- Does not account for non-linear relationships or systematic bias in adduct formation; assumes simple additive offset model.

## Evidence

- [other] Neutral mass inference is performed via linear regression by using the available ions matched to the theoretical khipu grid, which contains the mass offsets for each isotope and adduct combination relative to the neutral mass.: "Neutral mass inference is performed via linear regression by using the available ions matched to the theoretical khipu grid, which contains the mass offsets for each isotope and adduct combination"
- [other] Extract the set of ions present in the khipu instance and their assigned grid positions (isotope and adduct offsets). Retrieve the theoretical khipu grid defining the expected mass differences for all isotope and adduct patterns. Formulate a linear regression model with the theoretical grid offsets as predictors and the observed ion m/z values as the response variable. Fit the model using all available ions to estimate the neutral mass (intercept) and validate coefficient consistency.: "Extract the set of ions present in the khipu instance and their assigned grid positions (isotope and adduct offsets). Retrieve the theoretical khipu grid defining the expected mass differences for"
- [readme] Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression.: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression."
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu.: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu."
- [readme] The graph operations are supported by the networkx library, tree visualization aided by the treelib library. Khipu uses our package mass2chem for search functions.: "The graph operations are supported by the networkx library, tree visualization aided by the treelib library. Khipu uses our package mass2chem for search functions."
