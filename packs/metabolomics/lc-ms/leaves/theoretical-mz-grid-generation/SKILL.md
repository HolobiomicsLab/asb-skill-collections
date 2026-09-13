---
name: theoretical-mz-grid-generation
description: Use when you have a feature table from untargeted LC-MS (m/z, retention
  time, intensity) and need to annotate which observed m/z values correspond to isotopologues
  and adducts of the same neutral compound.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0091
  tools:
  - mass2chem
  - Python 3
  - khipu
  - metDataModel
  - asari
  techniques:
  - LC-MS
  license_tier: restricted
  provenance_tier: literature
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

# theoretical-mz-grid-generation

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Construct a reference m/z grid spanning isotopologues (M0 through M+n 13C) and adduct types to establish theoretical mass offsets for pattern matching and neutral mass inference in LC-MS metabolomics. This grid serves as the foundation for matching observed feature pairs to ion relationships and extracting neutral compound mass via linear regression.

## When to use

You have a feature table from untargeted LC-MS (m/z, retention time, intensity) and need to annotate which observed m/z values correspond to isotopologues and adducts of the same neutral compound. Generate this grid before searching the feature list for pattern matches, or when validating that observed ions align to expected isotope and adduct relationships within a specified ppm tolerance.

## When NOT to use

- Input is already a feature table that has been pre-processed by another tool (e.g. asari or xcms) — use khipu directly on the preprocessed table instead of regenerating the grid.
- You have targeted MS/MS data with known compound identities — target annotation is more appropriate than untargeted pattern matching.
- The observed feature list contains fewer than ~3 ions per neutral compound; insufficient coverage to fit neutral mass accurately via linear regression.

## Inputs

- neutral mass of a target compound (monoisotopic mass in Da)
- range of isotopologues to model (integer count of 13C substitutions, typically 0–6)
- list of target adduct types with their mass offsets (JSON or dict)
- mass precision tolerance in ppm (integer, typically 10–20 ppm)

## Outputs

- theoretical m/z grid as a 2D matrix or table (rows = isotopologues M0–M6, columns = adduct types)
- JSON or TSV export of grid with labeled rows and columns for reference
- per-ion assignment of isotopologue index and adduct type
- inferred neutral mass from linear regression fit to observed ions against the grid

## How to apply

Define the isotopologue range (typically M0 through M6, representing 0–6 carbon-13 substitutions, each offset by 1.00335 Da from the previous). Define the target adduct types with their mass offsets (e.g., M+H +1.00783 Da, M+NH4 +18.03383 Da, M+Na +22.98922 Da, M+HCl+H +36.99865 Da, M+K +38.96315 Da, M+ACN+H +42.03356 Da). For each isotopologue–adduct pair, calculate the theoretical m/z using mass2chem or direct formula-to-mass arithmetic. Organize results into a 7×6 matrix (rows = M0–M6 isotopologues, columns = six adduct types). Once constructed, use this grid to search the feature list for all m/z pairs that match any isotope or adduct offset within the specified ppm tolerance (default 10 ppm in khipu). Re-align observed isotope patterns against the grid to infer neutral mass via linear regression, and remove ions that do not fit the expected grid as outliers or noise.

## Related tools

- **mass2chem** (converts neutral compound formula or mass to m/z; used for grid calculation and search functions) — https://github.com/shuzhao-li-lab/mass2chem
- **khipu** (applies the theoretical grid to partition feature networks, assign ions to grid cells, and infer neutral mass) — https://github.com/shuzhao-li-lab/khipu
- **metDataModel** (provides data model for empirical compound representation and grid annotation output) — https://github.com/shuzhao-li-lab/metDataModel
- **asari** (downstream preprocessing tool that uses khipu-generated grids for preannotation of feature tables) — https://github.com/shuzhao-li/asari

## Examples

```
from khipu.core import Khipu; grid = Khipu.construct_grid(neutral_mass=200.0, isotope_range=7, adducts=['M+H', 'M+NH4', 'M+Na', 'M+K'], ppm_tolerance=10); print(grid.to_dataframe())
```

## Evaluation signals

- Grid dimensions are correct: 7 rows (M0–M6) × 6 columns (adduct types), with no missing cells.
- Each cell m/z value is calculated correctly: neutral_mass + isotope_offset + adduct_offset, verified against mass2chem or independent formula-to-mass calculator.
- When applied to feature list, at least 50–70% of ion pairs from the same neutral compound match a grid offset within ppm tolerance, indicating good coverage.
- Inferred neutral mass (from linear regression fit of observed ions to grid) differs from true neutral mass by ≤ 5 ppm, demonstrating accurate mass extraction.
- No spurious isotope or adduct edges are generated; i.e., the grid correctly distinguishes between M0+H and M1+NH4, which may have similar m/z but different isotopic patterns.

## Limitations

- Grid is constructed for a single neutral mass at a time; re-application to a new compound requires recalculation or use of a reference database.
- Grid assumes uniform 13C isotope shift (1.00335 Da); does not model other stable isotopes (2H, 15N, 18O, 34S) unless adduct offsets are manually extended.
- Adduct patterns are predefined; if a sample contains an unexpected adduct or derivatization, the grid will not match those ions and they will be rejected or form spurious clusters.
- Linear regression for neutral mass inference requires at least 3–4 observed ions per compound; sparse or noisy data may yield biased estimates.
- Some ions may enter the initial network by mistakes or unresolved signals and are removed; edge-case ions are sent to form new clusters rather than annotated to the main grid.

## Evidence

- [other] The khipu grid is constructed as a 7×6 matrix where rows represent isotopologues M0, 13C/12C×1 through 13C/12C×6, and columns represent adducts M+H[+], M+NH4[+], M+Na[+], M+HCl+H[+], M+K[+], M+ACN+H[+], with each cell containing the theoretical m/z mass shift value: "The khipu grid is constructed as a 7×6 matrix where rows represent isotopologues M0, 13C/12C×1 through 13C/12C×6, and columns represent adducts M+H[+], M+NH4[+], M+Na[+], M+HCl+H[+], M+K[+],"
- [other] Define the 13C isotopologues range as M0 through M6 (representing 0 to 6 carbon-13 substitutions, each differing by 1.00335 Da from the previous isotopologue): "Define the 13C isotopologues range as M0 through M6 (representing 0 to 6 carbon-13 substitutions, each differing by 1.00335 Da from the previous isotopologue)"
- [other] For each combination of isotopologue and adduct type, calculate the theoretical m/z value using mass2chem or direct formula-to-mass conversion: "For each combination of isotopologue and adduct type, calculate the theoretical m/z value using mass2chem or direct formula-to-mass conversion"
- [readme] Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern: "Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern"
- [readme] Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression"
- [readme] Khipu uses our package mass2chem for search functions: "Khipu uses our package mass2chem for search functions"
- [readme] Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu: "Some ions may come into the initial network by mistakes or unresolved signals. The are removed from the established khipu, and sent off to form a new khipu"
