---
name: neutral-mass-derivation-from-mz
description: Use when after adduct configuration is complete and before querying formula
  databases. Use it whenever you have m/z peak lists from mass spectrometry data and
  need to identify the neutral mass underlying each observed ion, particularly when
  multiple adduct types are active in the same experiment.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0599
  tools:
  - MetaboShiny
  - R
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1007/s11306-020-01717-8
  title: MetaboShiny
evidence_spans:
- Welcome to the info page on MetaboShiny
- Welcome to the info page on MetaboShiny! We are currently on BioRXiv
- Through R
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboshiny_cq
    doi: 10.1007/s11306-020-01717-8
    title: MetaboShiny
  dedup_kept_from: coll_metaboshiny_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1007/s11306-020-01717-8
  all_source_dois:
  - 10.1007/s11306-020-01717-8
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# neutral-mass-derivation-from-mz

## Summary

Converts observed m/z values to neutral molecular mass by applying the inverse of configured adduct transformations (e.g., [M+H]+, [M+Na]+, [M-H]−). This step precedes formula database lookup and is essential for disambiguating which molecular formula corresponds to each observed peak.

## When to use

Apply this skill after adduct configuration is complete and before querying formula databases. Use it whenever you have m/z peak lists from mass spectrometry data and need to identify the neutral mass underlying each observed ion, particularly when multiple adduct types are active in the same experiment.

## When NOT to use

- Input m/z values are already neutral masses or have been pre-converted by external software—re-applying this skill will introduce double-correction errors.
- Adduct configuration has not been defined; attempting neutral mass derivation without adduct parameters will produce nonsensical results.
- You are working with intact molecular ion peaks that require no adduct correction (rare in typical LC-MS/MS workflows, but possible in some direct-injection experiments).

## Inputs

- m/z peak list (numeric array or table with m/z column)
- adduct configuration table (adduct names, masses, charge states)
- mass spectrometry mode (positive or negative ionization)

## Outputs

- neutral mass value per peak (numeric)
- adduct type assignment per peak (string, e.g. '[M+H]+', '[M+Na]+', '[M-H]−')
- tabulated results (observed m/z, neutral mass, adduct type, optional: mass error vs. reference if available)

## How to apply

For each configured adduct type (e.g., [M+H]+, [M+Na]+, [M-H]−), calculate the neutral mass by subtracting the adduct mass and restoring any lost or gained protons/electrons. For example, to recover neutral mass from [M+H]+ at observed m/z 400, subtract 1.00783 Da (proton mass); for [M+Na]+ at m/z 420, subtract 22.98977 Da (sodium mass minus proton). Apply this transformation to all peaks in the m/z peak list. The rationale is that metabolite databases store neutral masses; matching observed ions to database entries requires first recovering the neutral parent. Store results as neutral mass per peak, tagged with the inferred adduct type for traceability.

## Related tools

- **MetaboShiny** (Integrated shiny application that orchestrates adduct configuration and neutral mass derivation as part of the formula prediction and lookup workflow step.) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Primary scripting language used to implement adduct transformation calculations and mass arithmetic within MetaboShiny.)

## Evaluation signals

- Verify that neutral masses are mathematically correct: for each observed m/z and adduct pair, check that neutral_mass = observed_m_z - adduct_delta (or + for negative adducts), where adduct_delta is from the configured adduct table.
- Confirm that neutral masses fall within the expected biochemical range for the organism/sample type (typically 50–2000 Da for small metabolites).
- Check that the distribution of mass errors (theoretical neutral mass from a reference database minus derived neutral mass) is centered near zero and has width consistent with the configured ppm tolerance (e.g., ±5 ppm).
- Cross-validate: re-derive m/z from the output neutral mass and adduct type; result should match the input observed m/z within measurement precision.
- Ensure no peaks are lost or duplicated; count of output neutral mass records should equal count of input m/z peaks (one neutral mass per peak per adduct type tested).

## Limitations

- Adduct table must be accurate and complete; missing or incorrectly specified adduct masses will propagate errors into all downstream formula matching steps.
- Neutral mass derivation assumes that the observed m/z corresponds to exactly one of the configured adducts; ambiguous cases (e.g., overlapping m/z from different adducts of similar mass) require additional disambiguation logic not covered by this skill alone.
- High-mass peaks (m/z > 1000) or multiply charged ions (z > 1) require correct charge state specification in the adduct definition; the skill does not auto-detect charge.
- In-source fragmentation or unknown neutral loss can produce observed m/z values that do not correspond to any configured adduct; such peaks cannot be converted and may require manual inspection or filtering.

## Evidence

- [other] For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−).: "For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−)."
- [other] Formula prediction and lookup module positioned after adduct configuration in the analysis pipeline.: "positioned after adduct configuration and before isotope scoring in the analysis pipeline"
- [readme] Adduct configuration table with current definitions and rules for adduct calculation.: "The "Definitions" tab shows the current adduct table. Below the table is a field to import another adduct table. The "Rules" field shows the adduct rules that are used to calculate adducts when"
- [other] Return neutral masses tagged with adduct type and theoretical m/z for validation.: "Return and tabulate the top-ranked candidates with their assigned formula, adduct type, observed m/z, theoretical m/z, and mass error for each peak."
