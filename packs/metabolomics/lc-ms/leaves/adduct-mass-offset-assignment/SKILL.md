---
name: adduct-mass-offset-assignment
description: Use when when you have an LC-MS feature table with m/z and retention time columns and need to identify which observed ions correspond to the same neutral compound under different ionization conditions and isotopic enrichment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0769
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# Adduct Mass Offset Assignment

## Summary

Construct and populate a theoretical khipu grid that maps all combinations of isotopologues (M0 through M+6 ¹³C substitutions) and common ionization adducts (M+H, M+NH₄, M+Na, M+HCl+H, M+K, M+ACN+H) to their theoretical m/z mass shift values. This grid serves as the reference basis for matching observed LC-MS features to ion species and inferring neutral masses via linear regression.

## When to use

When you have an LC-MS feature table with m/z and retention time columns and need to identify which observed ions correspond to the same neutral compound under different ionization conditions and isotopic enrichment. Use this skill before network construction and tree assembly to enable systematic pattern matching of isotope and adduct pairs against the feature list.

## When NOT to use

- Input is already an annotated feature table with ion species and neutral mass already assigned — use this skill only during pre-annotation.
- Only negative-mode or alternative ionization methods are employed; the grid is optimized for positive-mode ESI adducts and does not transfer directly.
- Isotope tracing experiment requires custom isotopologue patterns beyond M0–M6 range (e.g., heavy atom labeling with ¹⁵N or ³⁴S); modify the grid definition rather than applying the standard grid.

## Inputs

- Isotopologue definition (M0 through M6; carbon-13 mass difference: 1.00335 Da)
- Adduct type list with exact proton affinity and mass offsets (M+H, M+NH₄, M+Na, M+HCl+H, M+K, M+ACN+H)
- Mass calibration or reference mass database (via mass2chem or equivalent)

## Outputs

- Theoretical khipu grid: 7×6 matrix of m/z mass shift values (isotopologues × adducts)
- Tabular or structured matrix representation (JSON or tab-delimited format)
- Pattern list ready for feature table search operations

## How to apply

First, define the isotopologue range as M0 through M6, where each step represents one ¹³C substitution with a mass difference of 1.00335 Da per carbon. Second, specify the six adduct types with their exact mass offsets: M+H (+1.007276 Da), M+NH₄ (+18.033826 Da), M+Na (+22.989276 Da), M+HCl+H (+36.983976 Da), M+K (+38.963158 Da), M+ACN+H (+42.033825 Da). Third, for each isotopologue-adduct combination, calculate the theoretical m/z mass shift using mass2chem or direct formula-to-mass conversion. Organize results into a 7×6 matrix (rows = M0–M6 isotopologues, columns = six adducts). This grid becomes the reference standard against which observed feature m/z pairs are matched in subsequent pattern-matching steps; mismatches identify measurement noise or unresolved signals to be removed.

## Related tools

- **mass2chem** (Performs theoretical m/z and formula-to-mass conversions for each isotopologue-adduct pair to populate grid cells) — https://github.com/shuzhao-li-lab/mass2chem
- **khipu** (Consumes the theoretical grid as a reference standard for pattern matching observed feature pairs against isotope and adduct edges) — https://github.com/shuzhao-li-lab/khipu
- **Python 3** (Implements grid construction logic and matrix organization)

## Examples

```
from mass2chem import mass_shift; adducts = [('M+H', 1.007276), ('M+NH4', 18.033826), ('M+Na', 22.989276)]; isotopes = [0 + i*1.00335 for i in range(7)]; grid = [[mass_shift(iso, ad[1]) for ad in adducts] for iso in isotopes]; print(grid)
```

## Evaluation signals

- Grid dimensions are exactly 7 rows (M0–M6) × 6 columns (six adduct types); verify no missing cells.
- Each cell contains a numerical m/z mass shift value; check for NaN or infinite values.
- Column offsets follow the specified adduct masses: M+H ≈ 1.007, M+NH₄ ≈ 18.034, M+Na ≈ 22.989, M+HCl+H ≈ 36.984, M+K ≈ 38.963, M+ACN+H ≈ 42.034 Da (within ±0.001 Da tolerance).
- Row spacing (difference between consecutive isotopologues in each column) is uniform at 1.00335 Da ± 0.001 Da per row.
- Observed feature m/z values match grid entries when searched with specified ppm tolerance (default or user-defined), indicating correct alignment.

## Limitations

- Grid is optimized for positive-mode ESI ionization; negative-mode or MALDI ionization requires separate adduct definitions.
- Assumes natural abundance ¹³C isotope ratio; does not account for non-uniform enrichment in labeled samples without custom pattern definition.
- Theoretical grid does not include multimeric ions, in-source fragmentation, or other complex ion forms that may appear in real LC-MS data.
- Linear regression inference of neutral mass (downstream step) requires at least 2–3 observed ions from the grid to be reliable; sparse ion observation may produce large regression errors.

## Evidence

- [other] Define the 13C isotopologues range as M0 through M6 (representing 0 to 6 carbon-13 substitutions, each differing by 1.00335 Da from the previous isotopologue).: "Define the 13C isotopologues range as M0 through M6 (representing 0 to 6 carbon-13 substitutions, each differing by 1.00335 Da from the previous isotopologue)"
- [other] Define the six adduct types with their respective mass offsets: M+H (+1.00783 Da), M+NH4 (+18.03383 Da), M+Na (+22.98922 Da), M+HCl+H (+36.99865 Da), M+K (+38.96315 Da), M+ACN+H (+42.03356 Da).: "Define the six adduct types with their respective mass offsets: M+H (+1.00783 Da), M+NH4 (+18.03383 Da), M+Na (+22.98922 Da), M+HCl+H (+36.99865 Da), M+K (+38.96315 Da), M+ACN+H (+42.03356 Da)"
- [other] For each combination of isotopologue and adduct type, calculate the theoretical m/z value using mass2chem or direct formula-to-mass conversion. Organize results into a 7×6 grid (rows = M0–M6 isotopologues, columns = six adducts) and output as a structured table or matrix.: "For each combination of isotopologue and adduct type, calculate the theoretical m/z value using mass2chem or direct formula-to-mass conversion. Organize results into a 7×6 grid (rows = M0–M6"
- [readme] Based on available ions and the theoretical 'khipu grid', the neutral mass can be obtained via linear regression.: "Based on available ions and the theoretical 'khipu grid', the neutral mass can be obtained via linear regression"
- [readme] Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern.: "Start with an initial list of isotope patterns and adduct patterns (see khipu grid below). Search feature list to get all pairs that match any of the pattern"
- [readme] Khipu uses our package mass2chem for search functions.: "Khipu uses our package mass2chem for search functions"
