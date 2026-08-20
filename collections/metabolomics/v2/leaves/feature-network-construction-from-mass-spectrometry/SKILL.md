---
name: feature-network-construction-from-mass-spectrometry
description: 'Use when you have a preprocessed feature table (tab-delimited: feature
  ID, m/z, retention time, intensity columns) from LC-MS data and need to annotate
  which observed features represent the same underlying compound via isotope or adduct
  relationships.'
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3436
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3370
  tools:
  - networkx
  - treelib
  - mass2chem
  - metDataModel
  - Python 3
  - asari
  - khipu
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
- The graph operations are supported by the networkx library
- tree visualization aided by the treelib library
- Khipu uses our package mass2chem for search functions
- The data model of “empirical compound” is described in the metDataModel package.
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-network-construction-from-mass-spectrometry

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Build and partition a feature network from untargeted LC-MS data by matching observed m/z and retention time pairs against theoretical isotope and adduct patterns, then resolve the connected subnetworks into optimized tree structures (khipus) that represent empirical compounds with inferred neutral mass. This skill enables systematic annotation of degenerate ions and their relationships in both regular metabolomics and stable isotope tracing experiments.

## When to use

Apply this skill when you have a preprocessed feature table (tab-delimited: feature ID, m/z, retention time, intensity columns) from LC-MS data and need to annotate which observed features represent the same underlying compound via isotope or adduct relationships. Use it as a pre-annotation step before targeted database searching or when analyzing isotope labeling or chemical derivatization experiments where the same parent structure appears in multiple ion forms.

## When NOT to use

- Input is raw mass spectrometry data (mzML, mzXML, raw instrument files) rather than a preprocessed feature table — use a peak-picking and feature detection tool first (e.g., asari).
- You need fragmentation-based structural annotation — this skill only performs mass-based pre-annotation of ion relationships; use complementary database or in silico MS/MS matching tools for chemical structure assignment.
- Feature table has already been grouped into empirical compounds by another pre-annotation tool and you are confident in those assignments — applying khipu a second time may introduce conflicting or redundant annotations.

## Inputs

- Tab-delimited feature table (columns: feature_id, m/z, retention_time, [intensity_columns])
- Ionization mode specification (positive or negative)
- Mass tolerance parameter (ppm)
- Retention time tolerance parameter (arbitrary units, tool-dependent)

## Outputs

- JSON file containing annotated empirical compounds with tree structure and ion assignments
- Tab-delimited empirical compounds table with neutral mass and adduct assignments
- Feature-to-empirical-compound mapping

## How to apply

Load the feature table into khipu's command-line interface or Python library and execute the pattern-matching algorithm against a predefined khipu grid (default includes common positive or negative ion adducts: M+H, M+Na, M+NH4, M+K, etc., and 13C isotopologue shifts). This identifies all feature pairs matching any isotope or adduct pattern within specified mass tolerance (ppm) and retention time tolerance (rtol). Connect all pattern-matched pairs into an overall network and partition into connected subnetworks using networkx graph operations. For each subnetwork, remove redundant nodes (nodes explained by other nodes in the tree), separate isotope from adduct edges, and optimize an adduct trunk with an assigned root by maximizing the number of nodes explained. Apply linear regression using the theoretical khipu grid to infer the neutral mass from all available ions in each tree. Export the resulting empirical compounds and their annotations to JSON and tab-delimited formats. Decisions: set --ppm to match your instrument calibration (e.g., 5 ppm for accurate mass), --rtol to your preprocessing tool's alignment precision, and --mode (pos or neg) to match your ionization method.

## Related tools

- **networkx** (Performs graph partitioning and connected subnetwork identification from pattern-matched feature pairs)
- **treelib** (Supports tree visualization and structural representation of khipu instances in plain text and enhanced formats)
- **mass2chem** (Provides mass search and chemical interpretation utilities for isotope and adduct pattern matching) — https://github.com/shuzhao-li-lab/mass2chem
- **metDataModel** (Defines the data model and schema for empirical compounds output by khipu) — https://github.com/shuzhao-li-lab/metDataModel
- **asari** (Upstream peak detection and feature table generation tool that feeds into khipu for pre-annotation) — https://github.com/shuzhao-li/asari
- **khipu** (Main command-line tool and Python library implementing the feature network construction and tree optimization algorithm) — https://github.com/shuzhao-li-lab/khipu

## Examples

```
khipu -i testdata/ecoli_pos.tsv -o ecoli_annotation --ppm 5 --rtol 0.5
```

## Evaluation signals

- Output JSON and TSV files conform to the metDataModel schema for empirical compounds and contain all input features assigned to exactly one khipu instance or marked as unassigned unresolved signals.
- All features in high-confidence khipus obey the theoretical khipu grid: each ion's m/z matches (within ±ppm tolerance) the neutral mass plus the expected mass shift of its assigned adduct/isotope combination.
- Neutral mass inference via linear regression achieves low residual error across assigned ions (residual variance should be <0.1 Da² for high-confidence trees), indicating consistent isotope and adduct labeling.
- Retention time alignment within each khipu is tight (all features in a tree share similar retention time within rtol), confirming they represent co-eluting molecular species.
- No feature appears in multiple khipu instances, and the count of unresolved signals is small relative to total features (typically <5–10% depending on data quality and SNR filtering).

## Limitations

- Ion species may enter the initial network by mistakes or unresolved signals and are removed during tree optimization; these orphaned signals are sent to form separate khipus, potentially reducing annotation completeness for low-abundance or ambiguous features.
- The default khipu grid covers only common adducts and isotope patterns; less frequent modifications (e.g., unusual derivatizations, multi-adducts, or non-standard labeling) require custom pattern definition.
- Accuracy depends on mass calibration and chromatographic alignment precision — miscalibrated data (>ppm tolerance errors) or poor retention time reproducibility will fragment true empirical compounds into separate khipus.
- Linear regression neutral mass inference assumes all assigned ions are correct; systematic misassignment of adduct types can propagate to incorrect neutral mass estimates.
- Tool is optimized for singly charged ions; multiply charged species (common in ESI-MS of large biomolecules) are not addressed by the default algorithm.

## Evidence

- [readme] Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern.: "Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern"
- [readme] Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks.: "Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks"
- [readme] Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure.: "Each subnetwork becomes a khipu instance. The subnetwork is inspected, redundant nodes removed, and converted to an optimal tree structure"
- [readme] Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression.: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression"
- [readme] Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass.: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass"
- [readme] Users can use a feature table from any preprocessing tool as input and get annotated empirical compounds in JSON and tab delimited formats.: "Users can use a feature table from any preprocessing tool as input and get annotated empirical compounds in JSON and tab delimited formats"
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu.: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu"
