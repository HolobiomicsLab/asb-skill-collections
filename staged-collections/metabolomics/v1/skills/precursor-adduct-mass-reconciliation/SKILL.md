---
name: precursor-adduct-mass-reconciliation
description: Use when metabolomics LC-MS GC-MS untargeted lipidomics to reconcile precursor m/z and adduct ion assignments in MS/MS spectral libraries by deriving chemical structure from SMILES and comparing calculated vs. recorded masses.
when_to_use_negative:
- Spectra without valid SMILES annotation or molecular structure information cannot be reconciled via this method.
- Spectra with ambiguous or multiple possible SMILES representations where RDKit cannot compute a unique monoisotopic mass.
- Precursor m/z values that fall outside the range of any chemically plausible adduct (e.g. where calculated mass + all common adducts cannot account for the recorded m/z).
edam_operation: http://edamontology.org/operation_3800
edam_topics:
- http://edamontology.org/topic_0091
- http://edamontology.org/topic_3370
tools:
- name: matchms
  role: Orchestrates the library cleaning pipeline and wraps the 'Repair adduct and parent mass based on SMILES' filter as part of the structure annotation validation workflow
  repo: https://github.com/matchms/matchms
- name: RDKit
  role: Computes monoisotopic mass and chemical properties from SMILES strings to derive expected precursor m/z for each adduct type
- name: PubChem
  role: Source of canonical SMILES and InChI when annotations are derived from compound names prior to adduct reconciliation
provenance:
  source_task_ids:
  - task_001
  source_papers:
  - doi: 10.1186/s13321-024-00878-1
    title: Reproducible MS/MS library cleaning pipeline in matchms
schema_version: 0.2.0
derived_from:
- doi: 10.1186/s13321-024-00878-1
metadata:
  iri: https://w3id.org/holobiomicslab/asb-skill/precursor-adduct-mass-reconciliation@sha256:df5131cc0f1b4de69d464c4509686dd1830a77e29ca661a62b33d3b2b8161cba
---

# precursor-adduct-mass-reconciliation

## Summary

Reconcile precursor m/z and adduct ion assignments in MS/MS spectral libraries by deriving chemical structure from SMILES and comparing calculated vs. recorded masses. This skill repairs incorrect or missing adduct annotations that would otherwise cause spectra to be removed during library curation.

## When to use

Apply this skill when processing annotated MS/MS spectra where adduct ion type and precursor m/z are present or can be inferred, but plausibility checks between recorded precursor mass and structure-derived mass reveal discrepancies. Specifically, use this skill during library cleaning workflows to rescue spectra with reparable adduct/parent mass errors before they are filtered out—as demonstrated in the GNPS library where 52,084 spectra were repaired rather than discarded.

## When NOT to use

- Spectra without valid SMILES annotation or molecular structure information cannot be reconciled via this method.
- Spectra with ambiguous or multiple possible SMILES representations where RDKit cannot compute a unique monoisotopic mass.
- Precursor m/z values that fall outside the range of any chemically plausible adduct (e.g. where calculated mass + all common adducts cannot account for the recorded m/z).

## Inputs

- Annotated MS/MS spectra with SMILES structure annotation and recorded precursor m/z
- Recorded adduct ion type (if present)
- Monoisotopic mass derived from SMILES via RDKit

## Outputs

- Reconciled adduct ion assignment (e.g. [M+H]+, [M+Na]+, [M-H]−)
- Reconciled precursor m/z value
- Flag indicating whether adduct was repaired or was already correct
- Flag for spectra where no plausible adduct could be derived

## How to apply

Load SMILES string and recorded precursor m/z for each spectrum. Use RDKit to compute the monoisotopic mass of the neutral molecule from SMILES. For each common adduct ion type (e.g. [M+H]+, [M+Na]+, [M-H]−), calculate the expected precursor m/z by adding or subtracting the adduct mass. Compare the calculated expected m/z against the recorded precursor m/z: if they match within a small tolerance (the article does not specify the exact threshold, but the filter achieved 99.98% success rate with only 0.024% incorrect adducts among matched cases), assign or confirm the adduct. If the recorded adduct does not match the calculated mass, attempt to derive the correct adduct from the SMILES-derived mass. Flag spectra where no plausible adduct can be derived (the article reports 0.02% of spectra in this category). Output the repaired adduct ion assignment and reconciled precursor m/z for each spectrum.

## Related tools

- **matchms** (Orchestrates the library cleaning pipeline and wraps the 'Repair adduct and parent mass based on SMILES' filter as part of the structure annotation validation workflow) — https://github.com/matchms/matchms
- **RDKit** (Computes monoisotopic mass and chemical properties from SMILES strings to derive expected precursor m/z for each adduct type)
- **PubChem** (Source of canonical SMILES and InChI when annotations are derived from compound names prior to adduct reconciliation)

## Evaluation signals

- For each repaired spectrum, the recalculated precursor m/z (neutral mass + adduct) must match the recorded precursor m/z within tolerance; a 99.98% success rate with only 0.024% incorrect adducts is a baseline benchmark.
- The number of spectra with no derivable adduct should be rare (≤0.02% as observed in the GNPS dataset).
- Compare adduct assignments before and after repair: count how many spectra transitioned from an incorrect or missing adduct to a correct assignment, and verify these spectra would otherwise have been filtered out.
- Verify that repaired spectra retain valid ionmode metadata (e.g. positive or negative mode consistent with adduct charge) and that precursor m/z remains within the expected range for the given instrument.
- Cross-check a sample of repaired spectra against reference standards or alternative structure databases to confirm the assigned adduct and mass are chemically plausible.

## Limitations

- The filter cannot derive a correct adduct if the SMILES annotation is itself incorrect; reconciliation assumes the structure is correct and only fixes adduct/mass discrepancies.
- Some complex ion types (e.g. multimers, clusters, or unusual adducts) may not be covered by the standard adduct list, and may be incorrectly assigned or flagged as having no derivable adduct.
- The article does not report the exact m/z tolerance used for matching calculated vs. recorded precursor mass; this tolerance must be determined empirically or set based on instrument accuracy.
- Wrong chemical annotations that are consistent with the measured precursor mass will go unnoticed by this filter; plausibility checking of fragments is listed as a future expansion.

## Evidence

- [abstract] Repair adduct and parent mass based on SMILES filter logic and performance: "The 'Repair adduct and parent mass based on SMILES' filter did not derive an adduct for 0,02%. Of the 99,98% of the spectra, 0,024% of the spectra had an incorrect adduct"
- [abstract] Newly introduced repair functions saved 52,084 spectra from removal by repairing metadata: "combined the newly introduced repair functions repaired the metadata of 52,084"
- [abstract] RDKit is used to compute and compare chemical properties derived from SMILES: "SMILES, InChI and InChIKey are loaded by RDKit [18] and compared to each other"
- [abstract] Structure annotation validation is a core workflow step including adduct and precursor m/z comparison: "structure annotation validation through adduct, precursor m/z, and annotation comparison and harmonization"
- [discussion] Limitation: wrong annotations consistent with measured mass go unnoticed: "Wrong chemical annotations that are consistent with the measured mass, for instance, will go unnoticed in the current pipeline"
