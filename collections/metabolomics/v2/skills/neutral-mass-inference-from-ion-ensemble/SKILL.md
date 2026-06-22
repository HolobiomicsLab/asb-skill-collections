---
name: neutral-mass-inference-from-ion-ensemble
description: Use when you have a connected subnetwork of feature ions that have been validated as belonging to the same empirical compound (khipu instance), with isotope and adduct edges assigned, and you need to estimate the true neutral mass M0 rather than relying on any single observed m/z.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3438
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - networkx
  - treelib
  - mass2chem
  - Python 3
  - khipu (Weavor and Khipu classes)
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
- The graph operations are supported by the networkx library
- tree visualization aided by the treelib library
- Khipu uses our package mass2chem for search functions
- Khipu is developed as an open source Python 3 package
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

# neutral-mass-inference-from-ion-ensemble

## Summary

Infer the neutral mass of a compound from an ensemble of observed ions (adducts and isotopologues) by fitting their measured m/z values against a theoretical khipu grid using linear regression. This skill recovers the ground-truth neutral mass from degenerate ion populations in untargeted LC-MS data.

## When to use

You have a connected subnetwork of feature ions that have been validated as belonging to the same empirical compound (khipu instance), with isotope and adduct edges assigned, and you need to estimate the true neutral mass M0 rather than relying on any single observed m/z. This is especially valuable when the [M+H]+ or other primary adduct is weak, absent, or ambiguous.

## When NOT to use

- Khipu tree has not yet been constructed or validated—you are still in the feature-pair matching phase.
- Only a single ion (e.g., one [M+H]+ peak) is available; regression requires multiple ions to be meaningful.
- The feature table contains unfiltered noise or low-SNR ions; pre-filter by SNR > 100 or equivalent before khipu construction if data quality is poor.

## Inputs

- khipu instance (tree-structured subnetwork with assigned isotope and adduct edges)
- populated ion nodes with observed m/z values
- theoretical khipu grid (mass offsets for adduct types and isotope counts)

## Outputs

- inferred neutral mass M0 (float, in Da)
- linear regression fit quality metrics (e.g., R-squared, residuals)

## How to apply

After constructing a khipu tree with nodes assigned to isotope and adduct classes, collect all observed m/z values from the populated nodes. For each node, look up its theoretical m/z offset from the khipu grid (e.g., M0 + 1.007276 for [M+H]+, M0 + 2.010631 for M+1 13C [M+H]+). Set up a linear regression where the independent variable is the theoretical offset and the dependent variable is the observed m/z. Solve for the intercept, which is the neutral mass M0. Use only ions that passed redundancy inspection and tree optimization; exclude nodes flagged as mistakes or unresolved signals. The regression exploits all available ions simultaneously, reducing noise and increasing robustness compared to single-ion estimates.

## Related tools

- **networkx** (Supports graph construction and connected-component analysis to identify and validate the ion subnetwork before neutral mass inference)
- **mass2chem** (Provides search functions and pattern library to match feature pairs to isotope and adduct patterns, which are prerequisite to tree construction and regression setup) — https://github.com/shuzhao-li-lab/mass2chem
- **khipu (Weavor and Khipu classes)** (Manages khipu instance construction, tree optimization, and encapsulates the neutral mass inference workflow via linear regression) — https://github.com/shuzhao-li-lab/khipu
- **treelib** (Provides tree visualization to inspect the final tree structure and confirm node assignments before regression)

## Examples

```
khipu -i feature_table.tsv -o output_prefix --ppm 5 --rtol 10 -m pos
```

## Evaluation signals

- Regression R² ≥ 0.95 (high fit quality across the ion ensemble) indicates robust neutral mass estimate.
- Residuals (observed m/z − predicted m/z for each ion) should be small and randomly distributed around zero, not systematically offset by ion type.
- Inferred M0 should be consistent across multiple independent runs on the same khipu instance (reproducibility).
- M0 should fall within ±5 ppm of any independently measured or reference mass for the same compound, validating against external ground truth when available.
- Exclusion of redundant or low-quality nodes from the regression should not cause large jumps in M0 estimate (stability under node removal).

## Limitations

- Linear regression assumes all ions in the tree belong to the same neutral mass; if unresolved signals or false edges persist in the tree, M0 will be biased.
- Regression quality depends on diversity of observed adduct and isotope types; trees with only a few ion types or sparse populations may have high uncertainty.
- Systematic m/z calibration errors in the mass spectrometer are not corrected by this method and will shift M0 proportionally.
- Some ions may enter the initial network by mistakes or unresolved signals and are removed from the established khipu; these exclusions must occur before regression to avoid pulling M0 off-target.
- The method assumes the theoretical khipu grid (mass offsets for adducts, isotope shifts) is accurate; deviations due to instrumental noise or chemical artifacts will reduce fit quality.

## Evidence

- [readme] Based on available ions and the theoretical 'khipu grid', the neutral mass can be obtained via linear regression: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression"
- [readme] Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. They are removed from the established khipu: "Some ions may come into the initial network by mistakes or unresolved signals. They are removed from the established khipu"
- [intro] Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass"
