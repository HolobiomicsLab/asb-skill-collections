---
name: empirical-compound-annotation-and-representation
description: Use when you have a tab-delimited feature table (m/z, retention time,
  intensities) from LC-MS preprocessing and need to group related ions (isotopologues,
  adducts, in-source fragments) into compound-level annotations with inferred neutral
  mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3799
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
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
  provenance_tier: literature
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

# empirical-compound-annotation-and-representation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Annotate degenerate ions in LC-MS feature tables as structured empirical compounds by identifying isotope and adduct relationships, inferring neutral mass via linear regression, and representing them as optimized tree structures. This skill applies to regular LC-MS metabolomics and enables analysis of isotope tracing and chemical labeling experiments.

## When to use

Apply this skill when you have a tab-delimited feature table (m/z, retention time, intensities) from LC-MS preprocessing and need to group related ions (isotopologues, adducts, in-source fragments) into compound-level annotations with inferred neutral mass. Typical triggers: (1) you are performing untargeted metabolomics and require pre-annotation before statistical analysis or database matching; (2) you are analyzing stable isotope tracing or chemical labeling data and need to link labeled and unlabeled variants; (3) you want to reduce redundancy in feature tables by consolidating degenerate ions.

## When NOT to use

- Input is already an annotated database match or curated compound list (khipu is for pre-annotation, not refinement of known metabolites).
- Feature table has low mass precision (>10 ppm error) or poor retention time alignment, leading to spurious pattern matches.
- Data come from data-dependent MS/MS or targeted SRM experiments where ion relationships are already resolved by selection (khipu targets untargeted, degenerate ion discovery).
- Sample contains highly complex mixtures with dense feature clustering (>1000 features per m/z window) where pattern matching may produce unreliable subnetworks.

## Inputs

- tab-delimited feature table with columns: feature ID, m/z, retention time, followed by intensity columns
- ionization mode flag (pos or neg)
- mass tolerance in ppm (default ~5 ppm for high-resolution MS)
- retention time tolerance threshold (rtol, unit dependent on preprocessing tool)
- optional: custom isotope and adduct pattern grid

## Outputs

- JSON file with annotated empirical compounds (tree structure, neutral mass, assigned ions)
- tab-delimited empirical compounds table (neutral mass, adduct assignments, isotope counts)
- plain-text tree and network visualizations (optional, via Jupyter)

## How to apply

Load a tab-delimited feature table into khipu and execute the annotation workflow in six steps: (1) Search the feature list against an initial grid of isotope patterns (e.g., 13C/12C mass shifts) and adduct patterns (e.g., [M+H]+, [M+Na]+, [M+NH4]+) to identify all pattern-matched feature pairs. (2) Connect all matched pairs into an overall network and partition into connected subnetworks using graph operations. (3) Convert each subnetwork into a khipu instance, remove redundant nodes, and establish an optimal tree structure by separating isotope edges (vertical branches) from adduct edges (horizontal trunk). (4) Establish a trunk of adducts with an optimized root and linear path by maximizing the number of nodes explained, assigning isotopic branches to the trunk. (5) Infer neutral mass via linear regression based on available ion m/z values and the theoretical khipu grid. (6) Export annotated empirical compounds as JSON and tab-delimited formats. Key parameters: mass precision (default mz_tolerance_ppm), retention time tolerance (rtol), ionization mode (pos/neg). Rationale: the tree structure exploits the hierarchical nature of isotope and adduct relationships, enabling unambiguous neutral mass inference and reducing false positives from unresolved signals.

## Related tools

- **networkx** (graph partitioning of pattern-matched feature pairs into connected subnetworks)
- **treelib** (tree structure representation and plain-text visualization of empirical compounds)
- **mass2chem** (mass-based search functions for isotope and adduct pattern matching) — https://github.com/shuzhao-li-lab/mass2chem
- **metDataModel** (data model specification and serialization for empirical compound objects) — https://github.com/shuzhao-li-lab/metDataModel
- **asari** (parent preprocessing pipeline that calls khipu for pre-annotation of feature tables) — https://github.com/shuzhao-li/asari
- **khipu** (core command-line and library implementation of the empirical compound annotation algorithm) — https://github.com/shuzhao-li-lab/khipu

## Examples

```
khipu -i testdata/ecoli_pos.tsv -o ecoli_annotated --ppm 5 --mode pos
```

## Evaluation signals

- Output JSON and TSV files are well-formed and contain empirical compound records with non-null neutral_mass, ion_list, and tree_structure fields.
- Neutral mass inferred by linear regression has residual error <5 ppm when validated against known reference compounds or database entries.
- All ions assigned to an empirical compound match the theoretical m/z of their annotated adduct/isotope relative to the inferred neutral mass (within ppm tolerance).
- Network partitioning produces a number of empirical compounds consistent with expected biological complexity (e.g., 50–500 for typical metabolomics samples); excessive fragmentation (>10× feature count) suggests over-sensitive parameters.
- Redundant nodes are removed: no two ions in the final tree share identical or near-identical m/z (within 2× ppm tolerance), and no duplicate neutral mass estimates exist across empirical compounds.

## Limitations

- Performance degrades on feature tables with high-density m/z regions (>1000 features per 100 ppm window) where pattern matching may incorrectly link unrelated ions.
- Ions arising from mistakes or unresolved signals are removed from the established khipu and spawned as new khipus; manual curation may be required to merge or discard spurious low-confidence empirical compounds.
- Linear regression for neutral mass inference assumes at least 2 ions per empirical compound; single-ion khipus lack mass validation and are flagged as low-confidence.
- Default adduct and isotope grids are tuned for Orbitrap-class instruments (~5 ppm mass accuracy); lower-resolution instruments (e.g., Quadrupole-TOF, ~10 ppm) may require parameter adjustment.
- Retention time tolerance (rtol) is tool-dependent and must be user-specified; no universal default exists across preprocessing platforms.

## Evidence

- [intro] Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass"
- [readme] Running khipu produces two output files: JSON and tab-delimited annotations: "This will output pre-annotation to two files of JSON and tab delimited formats, this_test.json and this_test.tsv."
- [readme] Six-step workflow for empirical compound construction: "1. Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern. 2. Connect all pattern-matched"
- [readme] Linear regression infers neutral mass from ions and theoretical grid: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression."
- [readme] Applies to regular LC-MS and isotope tracing experiments: "This applies to regular LC-MS data, but also enables easy analysis of isotope tracing and chemical labeling data."
- [readme] Input format and parameter specification: "Input tables are tab delimited text files. The first columns are feature ID, m/z, rtime, followed by intensities."
- [readme] Ions removed from established khipu are spawned as new khipus: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu"
- [readme] Tree optimization separates isotope and adduct edges: "Separate isotope edges and adduct edges. The isotope edges form their own groups by shared nodes, each group belong to one adduct type. Each group of connected isotope edges is treated as one"
