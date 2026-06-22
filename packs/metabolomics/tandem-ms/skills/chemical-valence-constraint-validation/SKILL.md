---
name: chemical-valence-constraint-validation
description: Use when when you have enumerated a large pool of candidate chemical subformulae for observed fragment peaks (m/z values) within a mass tolerance window and need to eliminate chemically invalid candidates before ranking.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0611
  tools:
  - SIRIUS
  - MIST-CF
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jcim.3c01082
  title: mistcf
evidence_spans:
- Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mistcf_cq
    doi: 10.1021/acs.jcim.3c01082
    title: mistcf
  dedup_kept_from: coll_mistcf_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jcim.3c01082
  all_source_dois:
  - 10.1021/acs.jcim.3c01082
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-valence-constraint-validation

## Summary

Filter candidate chemical subformulae by applying chemical validity constraints (valence rules and atom count limits) to eliminate chemically implausible fragment assignments. This is a critical preprocessing step in de novo chemical formula inference from tandem mass spectra that reduces the search space before energy-based ranking.

## When to use

When you have enumerated a large pool of candidate chemical subformulae for observed fragment peaks (m/z values) within a mass tolerance window and need to eliminate chemically invalid candidates before ranking. This is especially important in the MIST-CF preprocessing stage, where multiple adduct types and formula candidates are considered and computational efficiency depends on early filtering of implausible assignments.

## When NOT to use

- If candidate subformulae have already been validated by an external tool (e.g., SIRIUS fragmentation trees) and you only need to rank them—applying constraint validation a second time adds no information and wastes computation.
- If you are working with custom or exotic chemistry (e.g., organometallic compounds, radicals, unusual oxidation states) where standard valence rules do not apply; manual curation or domain-specific rules are required.
- If your fragment peak list contains mostly noise or artifacts rather than true chemical fragments; garbage input will produce garbage output regardless of constraint filtering.

## Inputs

- fragment peak list with m/z values and intensities
- candidate chemical subformulae (as strings or parsed formula objects) enumerated within mass tolerance window
- mass tolerance threshold (in ppm or Da)

## Outputs

- filtered list of chemically valid candidate subformulae per fragment peak
- peak-to-formula mapping table (intermediate structured table for downstream ranking)

## How to apply

For each fragment peak and its enumerated candidate subformulae (generated via SIRIUS decomp or similar formula enumeration), apply two constraint layers: (1) valence rules—check that each atom in the candidate formula satisfies standard oxidation state and bonding constraints (e.g., carbon valence ≤ 4, oxygen ≤ 2, nitrogen ≤ 3 in neutral molecules); (2) atom count limits—reject candidates with biologically or chemically unreasonable element ratios (e.g., excessive heteroatoms, implausible hydrogen counts given the heavy atom composition). Discard any candidate failing either constraint. The remaining candidates proceed to energy-based scoring and ranking. This filtering step is deterministic and prior to any machine learning model invocation, making it a fast and interpretable quality gate.

## Related tools

- **SIRIUS** (Provides the dynamic programming algorithm (SIRIUS decomp) to enumerate all potential chemical formulae for an observed m/z mass; valence constraints are applied post-enumeration to filter candidates before ranking) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (Implements the complete chemical subformula assignment workflow including valence constraint validation as part of data preprocessing prior to transformer-based ranking) — https://github.com/samgoldman97/mist-cf

## Evaluation signals

- Verify that all output candidates obey standard valence rules (e.g., no carbon with >4 bonds, no oxygen with >2 bonds); audit a random sample of rejected candidates to confirm they violate constraints.
- Check that the filtered candidate list is smaller than the unfiltered list (constraint filtering is non-trivial); quantify the reduction rate (e.g., 30–50% of candidates typically filtered).
- Cross-validate that downstream energy-based ranking does not assign high scores to chemically implausible formulae; if it does, constraint filtering may be too permissive.
- For known-compound spectra, confirm that the ground-truth chemical formula survives constraint filtering (false negatives should be rare or zero).
- Inspect the distribution of atom counts in filtered candidates vs. rejected candidates; rejected candidates should show obvious extremes (e.g., unrealistic H/C ratios, excessive halogens).

## Limitations

- Valence rule sets are tuned for neutral organic molecules in positive ionization mode; inorganic compounds, charged species, and radicals may require domain-specific constraint variants not addressed in the MIST-CF paper.
- Atom count limits are heuristic and data-driven; they may be overly permissive for rare scaffolds or overly restrictive for exotic natural products, leading to false negatives.
- The constraint validation step is deterministic and cannot learn exceptions from training data; machine learning-based filtering or post-hoc adjustment by the ranking model may better capture edge cases.
- MIST-CF currently supports only positive ionization mode; negative ionization mode (where valence rules differ) is not yet supported and would require separate constraint sets.

## Evidence

- [other] For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window.: "For each fragment peak, enumerate all valid chemical subformulae within the mass tolerance window."
- [other] Apply chemical validity constraints (valence rules, atom count limits) to filter candidates.: "Apply chemical validity constraints (valence rules, atom count limits) to filter candidates."
- [other] MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage.: "MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
