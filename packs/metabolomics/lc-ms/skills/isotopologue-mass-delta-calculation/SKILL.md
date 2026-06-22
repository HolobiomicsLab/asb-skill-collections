---
name: isotopologue-mass-delta-calculation
description: Use when when constructing a reference mass-matching framework for untargeted metabolomics or isotope-tracing LC-MS data, before pattern-matching observed features to isotopic and adduct variants.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0625
  tools:
  - mass2chem
  - Python 3
  - khipu
  techniques:
  - LC-MS
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
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotopologue-mass-delta-calculation

## Summary

Systematically compute theoretical m/z mass shifts for all combinations of stable isotope substitutions (13C, typically M0 through M6) and ionization adducts (M+H, M+NH4, M+Na, M+HCl+H, M+K, M+ACN+H), organizing results into a reference grid ('khipu grid') used to match observed LC-MS features to theoretical ion species and infer neutral mass via linear regression.

## When to use

When constructing a reference mass-matching framework for untargeted metabolomics or isotope-tracing LC-MS data, before pattern-matching observed features to isotopic and adduct variants. Specifically, generate a khipu grid when you have a neutral mass or chemical formula and need to predict all plausible m/z values across a defined isotope range and adduct set, in order to search an experimental feature table and build connected ion networks.

## When NOT to use

- Input is already a feature table with observed m/z values — use this skill to generate the reference grid before feature matching, not as a feature extraction tool.
- Adduct list or isotope range is unknown or experiment-specific and has not been validated — confirm adduct formation and isotope labeling strategy first.
- Mass precision of the LC-MS instrument is significantly coarser than the chosen ppm tolerance (e.g., instrument ± 50 ppm, grid tolerance ± 5 ppm) — reconcile tolerances before grid construction.

## Inputs

- neutral mass (Da) or chemical formula
- isotopologue range specification (e.g., M0 through M6)
- list of target adduct types with mass offsets (in Da)

## Outputs

- khipu grid: 7×6 matrix of theoretical m/z values (rows = isotopologues M0–M6, columns = adducts)
- structured table (JSON or tab-delimited) with m/z predictions for feature matching

## How to apply

Define the isotopologue series (typically M0 through M6, each differing by 1.00335 Da for 13C substitution). List the target adduct types with their precise mass offsets: M+H (+1.00783 Da), M+NH4 (+18.03383 Da), M+Na (+22.98922 Da), M+HCl+H (+36.99865 Da), M+K (+38.96315 Da), M+ACN+H (+42.03356 Da). For each isotopologue-adduct pair, calculate the theoretical m/z by adding the neutral mass (or formula mass) to the combined isotope and adduct mass offset. Organize results into a 7×6 matrix (rows = M0–M6, columns = six adduct types), with each cell containing the precise theoretical m/z value. This grid serves as the lookup table during feature matching; mass differences between observed features and grid rows/columns within a defined ppm tolerance (typically ≤ 5 ppm) indicate valid isotopic or adduct relationships.

## Related tools

- **mass2chem** (formula-to-mass conversion and search functions used to calculate m/z offsets and match features to theoretical grid values) — https://github.com/shuzhao-li-lab/mass2chem
- **Python 3** (scripting environment for defining isotopologue ranges, adduct mass offsets, and matrix computation)
- **khipu** (post-grid-construction: ingests the theoretical khipu grid and uses it to annotate feature networks and infer neutral masses via linear regression) — https://github.com/shuzhao-li/khipu

## Examples

```
# Python: construct isotopologue m/z grid using mass2chem
from mass2chem.mass2chem_engine import find_adducts_from_mass
neutral_mass = 180.063  # e.g., glucose
adduct_list = [('M+H', 1.007276), ('M+NH4', 18.033826), ('M+Na', 22.989276), ('M+HCl+H', 36.983976), ('M+K', 38.963158), ('M+ACN+H', 42.033825)]
isotope_delta = 1.00335  # 13C - 12C
grid = {}
for isotope_num in range(7):
    grid[f'M{isotope_num}'] = {adduct_name: neutral_mass + isotope_delta*isotope_num + offset for adduct_name, offset in adduct_list}
print(grid)
```

## Evaluation signals

- Grid dimensions are exactly 7 rows (M0–M6) × 6 columns (six adducts); all cells populated with numeric m/z values.
- Each isotopologue row increases by exactly 1.00335 Da relative to the previous row, consistent across all adduct columns.
- Adduct mass offsets match published values (M+H = 1.00783, M+NH4 = 18.03383, M+Na = 22.98922, M+HCl+H = 36.99865, M+K = 38.96315, M+ACN+H = 42.03356 Da); verify at least one cell by hand calculation.
- Grid matches observed feature m/z values in experimental data within defined ppm tolerance; feature pairs separated by predicted isotope or adduct shifts should align with network-matching expectations.
- Linear regression using grid values and observed ions yields a neutral mass with residuals (fit error) consistent with instrument mass accuracy.

## Limitations

- Grid assumes 13C isotope substitution only; other isotopes (2H, 15N, 18O) require separate grid extension or custom isotope pattern definitions.
- Adduct list is fixed; for non-standard or experiment-specific adducts (e.g., in-source clustering, uncommon salt complexes), grid must be manually extended or redefined by user.
- Grid does not account for in-source neutral loss, fragmentation, or multiply-charged ions; apply only to singly-charged adducts in typical LC-MS conditions.
- Mass precision depends on accurate neutral mass input; incorrect or rounded input masses propagate directly to all grid cells and degrade feature-matching sensitivity.
- Grid construction assumes uniform isotope enrichment (e.g., all M+1, M+2, etc. correspond to uniformly distributed 13C); non-uniform labeling (e.g., site-specific or partial 13C) requires separate pattern definitions.

## Evidence

- [other] Define the 13C isotopologues range as M0 through M6 (representing 0 to 6 carbon-13 substitutions, each differing by 1.00335 Da from the previous isotopologue).: "Define the 13C isotopologues range as M0 through M6 (representing 0 to 6 carbon-13 substitutions, each differing by 1.00335 Da from the previous isotopologue)."
- [other] Define the six adduct types with their respective mass offsets: M+H (+1.00783 Da), M+NH4 (+18.03383 Da), M+Na (+22.98922 Da), M+HCl+H (+36.99865 Da), M+K (+38.96315 Da), M+ACN+H (+42.03356 Da).: "Define the six adduct types with their respective mass offsets: M+H (+1.00783 Da), M+NH4 (+18.03383 Da), M+Na (+22.98922 Da), M+HCl+H (+36.99865 Da), M+K (+38.96315 Da), M+ACN+H (+42.03356 Da)."
- [other] For each combination of isotopologue and adduct type, calculate the theoretical m/z value using mass2chem or direct formula-to-mass conversion.: "For each combination of isotopologue and adduct type, calculate the theoretical m/z value using mass2chem or direct formula-to-mass conversion."
- [readme] Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression.: "Based on available ions and the theoretical "khipu grid", the neutral mass can be obtained via linear regression."
- [other] The khipu grid is constructed as a 7×6 matrix where rows represent isotopologues M0, 13C/12C×1 through 13C/12C×6, and columns represent adducts M+H[+], M+NH4[+], M+Na[+], M+HCl+H[+], M+K[+], M+ACN+H[+]: "The khipu grid is constructed as a 7×6 matrix where rows represent isotopologues M0, 13C/12C×1 through 13C/12C×6, and columns represent adducts M+H[+], M+NH4[+], M+Na[+], M+HCl+H[+], M+K[+],"
