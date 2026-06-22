---
name: ion-adduct-isotope-pattern-matching
description: Use when you have a preprocessed feature table (m/z, retention time, intensities) from LC-MS and need to group features into empirical compounds.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - networkx
  - treelib
  - mass2chem
  - metDataModel
  - Python 3
  - khipu
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# ion-adduct-isotope-pattern-matching

## Summary

Systematically search a feature table against a library of known isotope and adduct mass offsets to identify all feature pairs that match expected ion relationships. This foundational step populates a feature network that is later partitioned into empirical compounds, enabling neutral mass inference and degenerate ion annotation in untargeted LC-MS metabolomics.

## When to use

You have a preprocessed feature table (m/z, retention time, intensities) from LC-MS and need to group features into empirical compounds. Apply this skill when the input features lack compound annotations and you need to resolve relationships between isotopologue variants, adduct forms, and multiply-charged ions of the same neutral molecule. This is the entry point before network partitioning and tree construction.

## When NOT to use

- Input features are already annotated with neutral masses and compound IDs—pattern matching is redundant.
- Feature table is from a targeted method with known precursor m/z values; use targeted lookup instead.
- Mass calibration error exceeds the ppm tolerance; recalibrate raw data first.
- Retention time dimension is absent or unreliable; orthogonal matching becomes ambiguous.

## Inputs

- feature table (tab-delimited text: feature ID, m/z, retention time, intensity columns)
- ionization mode (pos or neg)
- mass tolerance threshold (ppm)
- retention time tolerance (rtol, arbitrary unit)
- khipu grid (isotope and adduct pattern library with m/z offsets)

## Outputs

- matched feature pair edge list (feature_id_1, feature_id_2, pattern_type, m/z_difference, offset_error)
- network graph object (networkx) with feature nodes and pattern-matched edges

## How to apply

Initialize a khipu grid containing theoretical m/z offsets for standard isotope patterns (13C/12C at +2.0106 Da, +3.0140 Da, etc.) and adduct types (M+H[+], M+Na[+], M+NH4[+], M+K[+], M+ACN+H[+], M+HCl+H[+]) specific to your ionization mode (positive or negative). Use mass2chem to execute pairwise searches across the feature table, comparing observed m/z differences against each grid offset within a user-specified mass tolerance (typically 5–10 ppm). Record all feature pairs where the m/z difference matches a grid offset within tolerance and retention time difference is negligible (rtol parameter, tool-dependent). Trim the initial adduct set to reduce ambiguity in downstream assembly. Output a complete edge list of all matched pairs, which becomes the foundation for network construction.

## Related tools

- **mass2chem** (Provides pairwise search functions to identify feature pairs matching isotope and adduct patterns within mass tolerance) — https://github.com/shuzhao-li-lab/mass2chem
- **networkx** (Constructs and manages the overall feature network graph after all pairs are matched)
- **khipu** (Orchestrates the full workflow including pattern matching, network construction, and subsequent tree assembly) — https://github.com/shuzhao-li/khipu

## Examples

```
khipu -i testdata/ecoli_pos.tsv -o ecoli_annotation --ppm 5 --rtol 10 -m pos
```

## Evaluation signals

- All feature pairs in the output edge list have m/z differences within ppm tolerance of a grid offset; check: abs(observed_mz_diff - grid_offset) ≤ (grid_offset × ppm_tolerance / 1e6).
- No duplicate edges exist; the edge list is a set of unique (feature_id_1, feature_id_2) tuples.
- Retention time differences for matched pairs are below rtol threshold; no pairs spanning unrelated chromatographic regions.
- Ratio of matched pairs to total possible pairs (combinatorial) is reasonable for the sample complexity; very sparse matches may indicate miscalibration or excessive tolerance; very dense matches may indicate over-matching.
- Downstream network partitioning yields connected subnetworks (khipu instances) with consistent adduct trunk and isotopic branches; if too many singleton nodes or disconnected fragments result, re-examine pattern matching stringency.

## Limitations

- Initial adduct patterns are ambiguous and require trimming; some common adducts may not be in the default grid and need user customization (see demo notebooks).
- The method assumes relatively simple adduct structures; complex salt dimers or unusual protonation states not in the grid will be missed.
- Retention time alignment is heuristic; features with unusual or drifting rtime may be incorrectly separated or merged.
- High mass error or poor mass calibration will cause systematic false negatives; mass precision should be ≤ 5 ppm for reliable matching.
- Ambiguous matches—e.g., a 2.01 Da difference could match either a 13C isotope (M+0) or an M+H[+] shifted by ~2 Da depending on the isotope pattern—are resolved in downstream tree optimization but may still create spurious edges initially.

## Evidence

- [readme] Start with an initial list of isotope patterns and adduct patterns; search feature list to get all pairs that match any of the pattern.: "Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern"
- [readme] The graph operations are supported by the networkx library; Khipu uses mass2chem for search functions.: "The graph operations are supported by the networkx library, tree visualization aided by the treelib library. Khipu uses our package mass2chem for search functions"
- [other] Running khipu command-line tool produces two output files: a JSON file and a tab-delimited file containing annotated empirical compounds.: "This will output pre-annotation to two files of JSON and tab delimited formats, this_test.json and this_test.tsv."
- [readme] The initial adduct patterns are trimmed to reduce ambiguity.: "The initial adduct patterns are trimmed to reduce ambiguity."
- [readme] Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks.: "Connect all pattern-matched feature pairs to an overall network, which is further partitioned into connected subnetworks"
