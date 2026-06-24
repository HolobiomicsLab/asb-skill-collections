---
name: mass-spectrometry-ionization-mode-handling
description: Use when when you have a feature table from LC-MS preprocessed data (e.g.
  from asari v1.9.2) and need to annotate ions and infer neutral mass.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3630
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0091
  tools:
  - mass2chem
  - Python 3
  - khipu
  - asari
  - networkx
  - treelib
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.2c05810
  title: khipu
evidence_spans:
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrometry-ionization-mode-handling

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Specify and apply ionization mode (positive or negative) as a parameter to khipu's pre-annotation workflow, which determines which adduct patterns and isotope patterns are searched against the LC-MS feature list and inferred in the resulting empirical compounds. This is essential for correctly interpreting degenerate ions and neutral mass inference in untargeted metabolomics data.

## When to use

When you have a feature table from LC-MS preprocessed data (e.g. from asari v1.9.2) and need to annotate ions and infer neutral mass. You must specify ionization mode (positive or negative) as input to the khipu command-line tool or library, because the adduct and isotope patterns searched are mode-specific: positive mode includes M+H[+], M+NH4[+], M+Na[+], M+HCl+H[+], M+K[+], M+ACN+H[+], while negative mode would use different patterns. Failure to match mode with your instrument acquisition will produce incorrect mass assignments and empirical compound groupings.

## When NOT to use

- Input is already a fully annotated compound table with confirmed adducts and neutral masses; mode selection is only relevant during initial pre-annotation.
- You are analyzing a mixed-mode or polarity-switching LC-MS experiment with both positive and negative ions in a single run; you must run khipu separately for each polarity and merge results afterward.
- Your instrument records very-high-resolution data (e.g. Orbitrap, FTICR) where you plan to use exact elemental composition rather than adduct-pattern matching; khipu mode is optimized for adduct/isotope pattern searches, not de novo composition inference.

## Inputs

- Tab-delimited feature table (e.g. .tsv from asari v1.9.2) with columns: feature ID, m/z, retention time, followed by intensity columns
- Ionization mode parameter: 'pos' or 'neg'

## Outputs

- Annotated empirical compounds in JSON format
- Annotated empirical compounds in tab-delimited format (.tsv)
- Inferred neutral masses and ion relationships grouped by khipu tree structure

## How to apply

Pass the `--mode` parameter (pos or neg) to the khipu command-line interface or set the mode argument when instantiating the Khipu class. The mode gates which theoretical khipu grid (a 7×6 matrix of m/z offsets for isotopologues M0–M6 and adduct types) is used to search for pattern-matched feature pairs in the input table. For each feature pair in the table, khipu compares observed m/z differences against the theoretical grid entries for the selected mode; only matching pairs (within ppm tolerance, default or user-specified) are retained in the initial network. The mode choice also influences which ions are assigned to the adduct trunk and isotopic branches during the tree-building and linear regression steps for neutral mass inference. Document the mode used in your analysis and validate that the resulting empirical compounds show adducts and isotope patterns consistent with your ionization polarity.

## Related tools

- **khipu** (Main pre-annotation library; ionization mode parameter controls which adduct patterns are matched against features and how neutral mass is inferred via linear regression against the theoretical khipu grid.) — https://github.com/shuzhao-li-lab/khipu
- **asari** (Upstream feature detection and preprocessing tool; produces the feature table (.tsv) that khipu takes as input; output tables are mode-specific (e.g. ecoli_pos.tsv, yeast_neg).) — https://github.com/shuzhao-li/asari
- **mass2chem** (Provides mass-to-formula conversion and search utilities used by khipu for pattern matching and adduct offset calculation; mode-specific adduct masses are defined here.) — https://github.com/shuzhao-li-lab/mass2chem
- **networkx** (Graph operations library used to construct and partition the initial feature pair network before converting to optimal tree structure.)
- **treelib** (Tree visualization library used to display the final khipu tree structure (isotope and adduct edges) in plain text and Jupyter notebooks.)

## Examples

```
khipu -m pos -i ecoli_pos.tsv -o ecoli_pos_annotated --ppm 5
```

## Evaluation signals

- Check that the output empirical compounds contain only adducts appropriate to the specified mode (e.g. pos mode should include M+H, M+NH4, M+Na, M+K, M+ACN+H, not M-H or M+Cl, which are negative-mode patterns).
- Validate that inferred neutral masses are consistent by checking linear regression fit quality; neutral mass should be obtainable via linear regression from multiple observed ions using the theoretical khipu grid for the selected mode.
- Inspect the khipu tree visualization to confirm that isotope edges (13C/12C shifts of ~1.00335 Da) and adduct edges (mode-specific offsets like +1.008 for M+H in pos mode) are properly separated and assigned.
- Compare empirical compound neutral masses inferred from pos mode vs. neg mode runs on the same sample; neutral masses should agree within measurement error, confirming that mode choice was correct and consistent.
- Verify that feature pairs rejected during network pruning (removed as mistakes or unresolved signals) do not correspond to true adducts by inspecting the rejected subnetwork; they should show inconsistent m/z shifts relative to the theoretical khipu grid for the mode.

## Limitations

- Khipu mode parameter is binary (pos or neg) and assumes a single ionization polarity per run; polarity-switching experiments require separate khipu runs and manual merging of results.
- The theoretical khipu grid used for mode selection is initialized with a fixed set of six adduct types per mode; if your experiment generates unexpected adducts (e.g. radical cations, multi-charged ions, or rare adducts like M+2Na or M+Mg), mode-based pattern matching will miss them unless custom isotope and adduct patterns are supplied (see README demo notebooks).
- Mode selection does not account for ion suppression, contamination, or instrumental drift; feature quality should be filtered upstream (e.g. SNR > 100 for cleaner demos) before mode-dependent pre-annotation.
- The ppm tolerance parameter (default or user-specified) is applied uniformly across all m/z values regardless of mass range; high-mass features may accumulate larger absolute errors, leading to missed or spurious mode-dependent adduct assignments if ppm tolerance is not tuned.

## Evidence

- [readme] mode of ionization, pos or neg: "optional arguments:
    -v, --version         print version and exit
    -m MODE, --mode MODE  mode of ionization, pos or neg"
- [readme] Start with an initial list of isotope patterns and adduct patterns: "Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern"
- [readme] The khipu grid showing six adducts for positive mode: "Initial grid may look like this:

                   M+H[+]   M+NH4[+]   M+Na[+]   M+HCl+H[+]   M+K[+]   M+ACN+H[+]
    M0           1.007276  18.033826  22.989276  36.983976  38.963158  42.033825"
- [readme] Based on available ions and the theoretical khipu grid, neutral mass obtained via linear regression: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression"
- [readme] Different applications require different parameters including mode: "Different applications may require different parameters. A web server for isotope tracing data (described in [Mitchell et al (2024) Journal of the American Society for Mass Spectrometry."
- [readme] The yeast_neg table filtered by SNR for cleaner demo: "The yeast_neg table is features that are filted by SNR > 100 to serve as a cleaner demo"
- [readme] Pre-annotation tool to annotate degenerate ions: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass"
