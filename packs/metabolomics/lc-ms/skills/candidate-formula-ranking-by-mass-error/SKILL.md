---
name: candidate-formula-ranking-by-mass-error
description: Use when after querying a formula database (KEGG, PubChem, or user-supplied) with neutral mass values derived from observed m/z peaks and adduct transformations, when multiple candidate formulae fall within the configured mass tolerance window (ppm or Da) and you need to rank them by likelihood.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3731
  edam_topics:
  - http://edamontology.org/topic_0218
  - http://edamontology.org/topic_3370
  tools:
  - MetaboShiny
  - R
  techniques:
  - LC-MS
  - NMR
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

# candidate-formula-ranking-by-mass-error

## Summary

Rank molecular formula candidates retrieved from metabolite databases by mass error and chemical plausibility, selecting the top-ranked formulas for each observed m/z peak. This skill filters and prioritizes formula predictions after neutral mass calculation and database lookup, improving confidence in molecular annotations.

## When to use

After querying a formula database (KEGG, PubChem, or user-supplied) with neutral mass values derived from observed m/z peaks and adduct transformations, when multiple candidate formulae fall within the configured mass tolerance window (ppm or Da) and you need to rank them by likelihood before proceeding to isotope scoring or downstream analysis.

## When NOT to use

- Input m/z values are already annotated with high-confidence formula assignments from orthogonal methods (e.g., NMR or MS/MS fragmentation); ranking candidates is redundant.
- No database is available or configured for the sample type (e.g., rare metabolites not covered by KEGG or PubChem).
- Mass tolerance is so wide (e.g., >50 ppm) that hundreds of candidates are retrieved per peak; ranking becomes unreliable without additional filtering criteria or MS/MS data.

## Inputs

- observed m/z peak list (numeric values with intensity)
- neutral mass values (derived from m/z and adduct transformations)
- configured adduct definitions (e.g., [M+H]+, [M+Na]+, [M-H]−)
- mass tolerance window (ppm or Da)
- formula database with molecular formulae and exact monoisotopic masses
- chemical plausibility rule definitions (element ratio ranges, H-deficiency bounds)

## Outputs

- ranked candidate formula table (peak ID, formula, adduct type, observed m/z, theoretical m/z, mass error)
- top-ranked formula assignment per peak
- mass error scores (ppm or Da) for each candidate
- chemical plausibility scores or flags

## How to apply

For each neutral mass calculated from an observed m/z value and its adduct type, retrieve all molecular formulae from the database that fall within the specified mass tolerance (typically 5–10 ppm). Rank candidates by: (1) smallest absolute mass error in ppm or Da between theoretical and observed m/z, and (2) chemical plausibility rules such as element ratio constraints (e.g., C:H:N:O ratios consistent with known metabolites) and hydrogen deficiency thresholds. Return the top-ranked candidate(s) for each peak along with tabulated formula, adduct type, observed m/z, theoretical m/z, and mass error. The rationale is that lower mass error combined with chemical validity increases the probability of correct formula assignment in subsequent annotation steps.

## Related tools

- **MetaboShiny** (Provides the formula prediction and lookup module with configurable mass tolerance, database queries, and candidate ranking interface integrated into the metabolomics workflow pipeline.) — https://github.com/joannawolthuis/MetaboShiny
- **R** (Executes the formula ranking logic, database queries, and mass error calculations within MetaboShiny.)

## Evaluation signals

- Mass error for top-ranked formula is below the configured tolerance (ppm or Da) for every peak.
- Top-ranked formula chemical plausibility score meets or exceeds defined thresholds (e.g., element ratios within acceptable range).
- No duplicate formulae appear in the ranked output for the same peak.
- Ranked candidate list order is monotonically increasing by mass error magnitude.
- Downstream isotope scoring or manual validation confirms that top-ranked formulas match expected metabolite classes for the sample type.

## Limitations

- Mass error ranking alone cannot distinguish between isomeric formulae with identical exact mass; additional MS/MS fragmentation or NMR data is needed.
- Chemical plausibility rules are heuristic and may exclude valid metabolites if rules are too restrictive, or include implausible candidates if rules are too permissive.
- Database coverage varies: rare or newly synthesized metabolites may not be present in public databases (KEGG, PubChem), leading to no candidate matches despite correct neutral mass calculation.
- Very small mass tolerance windows (e.g., <2 ppm) may yield zero candidates for some peaks due to instrumental calibration drift or database rounding errors.

## Evidence

- [other] Formula prediction and lookup module workflow: "For each m/z value, calculate the neutral mass by applying the inverse of each configured adduct transformation (e.g., [M+H]+, [M+Na]+, [M-H]−). Query the formula database (KEGG, PubChem, or"
- [other] Workflow positioning: "MetaboShiny includes a configurable formula prediction and lookup step that operates as part of the workflow settings, positioned after adduct configuration and before isotope scoring in the analysis"
- [other] Output format: "Return and tabulate the top-ranked candidates with their assigned formula, adduct type, observed m/z, theoretical m/z, and mass error for each peak."
- [readme] Formula prediction and lookup parameter configuration: "Here you can set the parameters and rules to use when predicting chemical formulas."
