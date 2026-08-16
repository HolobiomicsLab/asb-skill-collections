---
name: energy-based-formula-scoring
description: Use when you have an unknown MS/MS spectrum (precursor m/z and fragment peak list) and a set of candidate molecular formulae, and you need to rank them by likelihood without access to a spectrum database or precomputed fragmentation trees.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - SIRIUS
  - MIST-CF
  techniques:
  - LC-MS
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
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# energy-based-formula-scoring

## Summary

Score and rank candidate chemical formulae against tandem mass spectra using end-to-end energy-based neural modeling, without reliance on fragmentation tree databases or external spectrum libraries. This approach learns formula-spectrum agreement directly from MS/MS peak patterns and intensities.

## When to use

Apply this skill when you have an unknown MS/MS spectrum (precursor m/z and fragment peak list) and a set of candidate molecular formulae, and you need to rank them by likelihood without access to a spectrum database or precomputed fragmentation trees. This is particularly useful in de novo metabolite identification or when SIRIUS fragmentation trees are unavailable or undesirable.

## When NOT to use

- Input spectrum contains only the precursor ion and no fragment peaks — energy-based scoring requires fragment MS/MS data to learn formula-spectrum agreement.
- You are analyzing negative mode ionization data — MIST-CF currently supports only positive mode adducts.
- You need deterministic, fully explainable fragmentation pathways — energy-based neural scoring is learned empirically and does not produce human-readable fragmentation mechanisms.

## Inputs

- MS/MS spectrum (fragment peak list with m/z values and intensities)
- Candidate molecular formulae (as chemical strings, e.g., 'C6H12O6')
- Precursor m/z value
- Adduct type (e.g., [M+H]+, [M+Na]+, [M+K]+)

## Outputs

- Ranked list of candidate formulae with energy-based scores
- Score-sorted formula candidates for the unknown precursor mass

## How to apply

Load the MS/MS spectrum (m/z values and intensities of fragment peaks) and the candidate chemical formulae for the precursor mass. Use a formula transformer neural network trained on experimental MS/MS data to score the agreement between each candidate formula and the observed spectrum through energy-based modeling. The model learns patterns of which fragment masses and intensities are consistent with a given formula without explicitly computing fragmentation pathways. Rank candidates by decreasing score. The rationale is that learned energy-based scoring captures empirical fragmentation patterns directly from training data, avoiding the computational cost and potential brittleness of deterministic tree enumeration.

## Related tools

- **SIRIUS** (Used internally for formula enumeration (SIRIUS decomp) to generate candidate chemical subformulae; MIST-CF avoids using SIRIUS fragmentation trees for scoring) — https://bio.informatik.uni-jena.de/software/sirius/
- **MIST-CF** (Primary tool implementing the formula transformer neural network and energy-based scoring pipeline) — https://github.com/samgoldman97/mist-cf

## Examples

```
python src/mist_cf/mist_cf_score/predict_mgf.py --input demo_specs.mgf --model quickstart/mist_cf_model.pkl --output mist_cf_out/
```

## Evaluation signals

- Top-ranked formula matches the ground-truth molecular formula (when available) — check exact match or rank-1 accuracy on test spectra.
- Score distribution is monotonically decreasing across ranked candidates, with correct formula scoring higher than decoys or isomers.
- Model predictions generalize across different MS instruments and ionization conditions (validated on NPLIB1, NIST20, and CASMI 2022 datasets).
- Energy-based scores correlate with experimental MS/MS peak agreement — spectra with more intense/abundant fragment ions consistent with a formula receive higher scores.
- Inference time is substantially lower than SIRIUS fragmentation tree computation for large candidate sets (hundreds to thousands of formulae).

## Limitations

- Currently supports only positive mode ionization ([M+H]+, [M+Na]+, [M+K]+); negative mode is not yet implemented.
- Model performance may be reduced on high-resolution Orbitrap or other advanced instruments if training data was primarily lower-resolution (e.g., public NPLIB1 only); NIST20-trained models available upon request but require a NIST license.
- Requires pre-computed set of candidate formulae — does not enumerate all chemically valid formulae de novo; SIRIUS decomp or similar enumeration tool must be run first.
- Neural network-based scoring is learned empirically and cannot provide explicit fragmentation mechanisms or rationales for score differences between candidates.

## Evidence

- [readme] MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases.: "MIST-CF ranks chemical formula and adduct assignments for an unknown mass spectrum using an end-to-end energy based modeling approach, without referencing any spectrum databases."
- [readme] Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion.: "Instead of computing fragmentation trees, MIST-CF adopts a formula transformer neural network architecture and learns in a data dependent fashion."
- [readme] Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees): "Utilizing an internal chemical subformula assignment protocol (rather than SIRIUS fragmentation trees)"
- [other] MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks in the data preprocessing stage.: "MIST-CF uses an internal chemical subformula assignment protocol as an alternative to SIRIUS fragmentation trees for assigning chemical subformulae to fragment peaks"
- [readme] Considering multiple adduct types beyond [M+H]+ (still only positive mode): "Considering multiple adduct types beyond [M+H]+ (still only positive mode)"
