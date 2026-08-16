---
name: thermodynamic-index-calculation
description: Use when after molecular formula assignment and filtering of FT-ICR MS
  peaks, when you have elemental composition (C, H, O, N, S, P counts) and need to
  characterize metabolite thermodynamic stability, degree of oxidation, aromaticity,
  and unsaturation to compare compound reactivity across samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0593
  tools:
  - NumPy
  - pandas
  - Formularity
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1186/s40168-023-01476-3
  title: MetaboDirect
evidence_spans:
- requires the Python dependencies NumPy [40], pandas [41, 42]
- The MetaboDirect pipeline was developed in Python 3.8 [38] and R 4.0.2 [39] and
  is available to install through the Python Package Index... It requires the Python
  dependencies NumPy
- It requires the Python dependencies NumPy [40], pandas [41, 42]
- it has been designed to work with the output file (in .csv format) generated directly
  by Formularity [24] which uses FT-ICR MS data in .xml format
- it has been designed to work with the output file (in .csv format) generated directly
  by Formularity [24]
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metabodirect_cq
    doi: 10.1186/s40168-023-01476-3
    title: MetaboDirect
  dedup_kept_from: coll_metabodirect_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s40168-023-01476-3
  all_source_dois:
  - 10.1186/s40168-023-01476-3
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# thermodynamic-index-calculation

## Summary

Calculate thermodynamic and molecular indices (DBE, GFE, AImod, NOSC) from assigned FT-ICR MS molecular formulas to characterize metabolite properties including saturation, lability, and oxidation state. These indices enable rapid assessment of compound degradability and structural complexity across large peak datasets.

## When to use

Apply this skill after molecular formula assignment and filtering of FT-ICR MS peaks, when you have elemental composition (C, H, O, N, S, P counts) and need to characterize metabolite thermodynamic stability, degree of oxidation, aromaticity, and unsaturation to compare compound reactivity across samples or predict microbial degradation potential.

## When NOT to use

- Input peaks lack assigned molecular formulas or elemental composition data—indices cannot be calculated without this foundation.
- Peak data has not been filtered for isotopic contamination (13C) or formula assignment error (>0.5 ppm)—indices on low-confidence peaks will propagate uncertainty.
- Downstream analysis requires isomer-level differentiation—these indices are composition-based and cannot distinguish chemical isomers.

## Inputs

- Filtered peak abundance matrix (CSV) with m/z, assigned molecular formula, and elemental composition (C, H, O, N, S, P atom counts)

## Outputs

- CSV table with columns: m/z, molecular formula, NOSC (nominal oxidation state of carbon), GFE (Gibbs free energy of carbon oxidation), AImod (modified aromaticity index), DBE (double-bond equivalent), peak intensity

## How to apply

For each peak with a valid assigned molecular formula, sequentially compute four indices from elemental composition using the equations in Supplementary Table 2: (1) nominal oxidation state of carbon (NOSC) reflects the average oxidation state of all carbons and predicts lability; (2) Gibbs free energy of carbon oxidation (GFE or ΔG°C-ox) derived from NOSC indicates thermodynamic degradation likelihood—more negative values suggest greater microbial oxidation potential; (3) modified Aromaticity Index (AImod) quantifies carbon-to-carbon double bond density and aromatic ring prevalence; (4) double-bond equivalent (DBE) counts total unsaturation and aromatic structures. Export results as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity. All peaks with valid formulas must receive all four index values with no missing or NaN entries.

## Related tools

- **NumPy** (Vectorized arithmetic for element-wise computation of NOSC, GFE, AImod, DBE across peak arrays)
- **pandas** (Loading filtered peak data, organizing elemental composition columns, and exporting indexed results as CSV)
- **Formularity** (Upstream tool for signal processing and molecular formula assignment from raw FT-ICR MS data prior to index calculation)

## Evaluation signals

- All peaks with valid assigned molecular formulas receive exactly four index values (NOSC, GFE, AImod, DBE); no peaks missing any index.
- No NaN or infinite values in output; indices fall within expected biological ranges (e.g., NOSC typically −2 to +1; DBE ≥ 0 and proportional to molecular weight).
- Indices vary monotonically with elemental composition changes: increasing carbon and aromatic character raises DBE and AImod; increasing oxygen content increases NOSC (more oxidized); index values are internally consistent (e.g., high DBE correlates with high AImod for aromatic compounds).
- CSV output rows match input peak count exactly; m/z and molecular formula columns are identical between input and output.
- Indices computed for reference standards (e.g., lipids, carbohydrates, lignin) match literature-reported or manually verified values, confirming equation implementation.

## Limitations

- FT-ICR MS cannot distinguish chemical isomers; thus indices reflect only elemental composition and cannot capture structural isomerism or regioisomerism that may affect actual thermodynamic stability.
- Index equations assume organic matter in natural aquatic/terrestrial systems; applicability to other domains (synthetic organics, plasma samples) not validated in article.
- Indices are composition-based estimates; actual compound reactivity also depends on physical factors (bioavailability, particle association, pH, ionic strength) not captured by formula-derived indices.
- Peak intensity data may be subject to ion suppression or enhancement in direct-injection MS, affecting downstream interpretation of relative compound abundance—indices themselves are unaffected but their use in abundance-weighted comparisons may be biased.

## Evidence

- [other] MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental composition of assigned molecular formulas: "MetaboDirect calculates thermodynamic indices including double-bond equivalent (DBE), Gibbs free energy (GFE), aromaticity index (AI), and nominal oxidation state of carbon (NOSC) from the elemental"
- [other] For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2. Calculate Gibbs free energy (ΔG°C-ox or GFE) for each peak from NOSC to determine degradation likelihood using the equation in Supplementary Table 2.: "For each peak's elemental composition, calculate the nominal oxidation state of carbon (NOSC) using the elemental composition equation from Supplementary Table 2. 3. Calculate Gibbs free energy"
- [other] Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation. Calculate double bond equivalent (DBE) representing molecular unsaturation and aromatic structure presence from elemental composition using Supplementary Table 2 equation.: "Calculate modified Aromaticity Index (AImod) reflecting carbon-to-carbon double bond density from elemental composition using Supplementary Table 2 equation. 5. Calculate double bond equivalent (DBE)"
- [other] Validation: all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter.: "Validation: all peaks with valid molecular formulas receive four index values; no missing or NaN values in output; indices fall within expected biological ranges for organic matter."
- [other] Export computed indices as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity.: "Export computed indices as a CSV table with columns for m/z, molecular formula, NOSC, GFE, AImod, DBE, and peak intensity."
