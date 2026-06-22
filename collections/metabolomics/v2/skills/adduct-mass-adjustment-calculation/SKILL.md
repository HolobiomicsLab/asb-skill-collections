---
name: adduct-mass-adjustment-calculation
description: Use when you have a set of in silico-predicted compounds (with SMILES structures) and an experimental metabolomics peak list (m/z values), and you need to filter predictions to only those that could plausibly be detected.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  tools:
  - RDKit
  - mordred
  - pytest
  - MINE-Database Filter base class
derived_from:
- doi: 10.1186/s12859-023-05149-8
  title: Pickaxe
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_pickaxe_cq
    doi: 10.1186/s12859-023-05149-8
    title: Pickaxe
  dedup_kept_from: coll_pickaxe_cq
schema_version: 0.2.0
---

# adduct-mass-adjustment-calculation

## Summary

Calculate neutral masses of generated compounds by adjusting their molecular weights for specified adduct forms (e.g., [M+H]+, [M-H]−), enabling mass-based matching against experimental metabolomics peak lists. This skill is essential for filtering predicted compounds to only those detectable in untargeted mass spectrometry experiments.

## When to use

You have a set of in silico-predicted compounds (with SMILES structures) and an experimental metabolomics peak list (m/z values), and you need to filter predictions to only those that could plausibly be detected. Adduct-mass adjustment is the prerequisite step: you must compute the expected m/z for each predicted compound under the ionization modes present in your experiment (e.g., protonation, deprotonation, or complex adducts like [M+Na]+), then compare these adjusted masses to the observed peaks within your mass_tolerance (in Da).

## When NOT to use

- The metabolomics dataset contains only identified peaks (already annotated with known compound identifiers); use target filtering instead to match against known structures.
- You lack SMILES representations or have incomplete molecular structures; the skill cannot compute neutral masses without valid chemical structure input.
- The mass_tolerance is not calibrated to your instrument's resolution; applying an incorrect tolerance (e.g., ±100 Da on a high-resolution instrument) will either remove all compounds (too tight) or retain almost all (too loose), rendering the filter ineffective.

## Inputs

- compound dictionaries containing SMILES strings (at each generation of network expansion)
- metabolomics peak-list CSV file with m/z values and optional retention time columns
- list of possible_adducts (e.g., [1.008, -1.008, 22.989] for [M+H]+, [M-H]−, [M+Na]+)
- mass_tolerance in Da (e.g., 0.01 for 10 ppm on a 1000 m/z ion)
- optional retention_time_tolerance window in minutes

## Outputs

- set of compound IDs to filter out (those with no adduct-adjusted mass matching any peak within tolerance)
- filtering statistics: count of compounds retained, count removed, and distribution of matches per adduct type (optional, via _post_print)

## How to apply

For each compound in the predicted set, extract its SMILES string and compute its neutral molecular weight using RDKit's molecular weight calculation. For each adduct in the specified possible_adducts list, apply the adduct's mass offset to the neutral weight to obtain the expected m/z value. Compare this adjusted m/z against all peaks in the metabolomics peak-list CSV (extracting the m/z column) using a tolerance window of ±mass_tolerance Da. A compound is retained if at least one of its adduct-adjusted masses matches any peak within tolerance; otherwise it is filtered out. Optionally, if retention_time_tolerance is specified, apply an additional constraint that the predicted compound's retention time (estimated via mordred molecular descriptors) must fall within the observed peak's retention time window. Document the number of compounds retained vs. removed at each generation to enable post-hoc evaluation of filter stringency.

## Related tools

- **RDKit** (Compute neutral molecular weight from SMILES; calculate adduct-adjusted masses for comparison against m/z peaks) — https://rdkit.org/docs/api-docs.html
- **mordred** (Optional: predict compound retention time using molecular descriptors for additional RT-based filtering constraint)
- **pytest** (Unit test adduct calculations against reference peaks and edge cases (empty peak lists, out-of-tolerance masses, multiple adduct forms)) — https://docs.pytest.org/en/stable/
- **MINE-Database Filter base class** (Inherit from Filter in minedatabase/filters.py; implement _choose_cpds_to_filter and optional _post_print for logging filter statistics) — https://github.com/tyo-nu/MINE-Database

## Examples

```
from rdkit import Chem; from rdkit.Chem import Descriptors; smiles = 'CC(=O)O'; mol = Chem.MolFromSmiles(smiles); mw = Descriptors.MolWt(mol); adducts = [1.008, -1.008]; adjusted_masses = [mw + a for a in adducts]; print(adjusted_masses)
```

## Evaluation signals

- Verify that filter_name returns a non-empty string identifying the metabolomics filter.
- Verify that _choose_cpds_to_filter returns a Python set (or set-like object) of compound IDs; confirm no ID appears twice and all IDs correspond to actual compounds in the generation.
- For a reference set of known peaks with calibrated masses, confirm that compounds with neutral masses within mass_tolerance of a peak (after adduct adjustment) are retained and those outside the tolerance are removed.
- Check that _post_print logs filtering statistics (count before/after, match distribution by adduct type) and that these counts sum correctly across all generations.
- Test edge cases: empty peak-list (all compounds removed), peak-list with no matches (all compounds removed), single adduct vs. multiple adducts (confirm all adducts are tested for each compound).

## Limitations

- The metabolomics filter assumes that all unidentified peaks in the input CSV are relevant biological signals; false-positive peaks (contaminants, artifacts) will cause legitimate compounds to be incorrectly filtered out.
- Adduct-adjusted mass calculation does not account for isotopologue shifts, in-source fragmentation, or multiply-charged ions; only single-charge adducts are supported.
- Retention time prediction via mordred descriptors is optional and may be unreliable if the retention time model was not trained on the same chromatographic method; applying RT filtering without validation may remove true positives.
- The filter operates on unidentified peaks only; pre-identified peaks are ignored, which may lead to redundant filtering if a peak is both identified and unidentified in the dataset.

## Evidence

- [other] The metabolomics filter requires four core parameters: (1) met_data_path specifying a CSV of detected peaks; (2) possible_adducts listing adducts to add to each mass; (3) mass_tolerance in Da defining the matching window; and optionally (4) retention time prediction using mordred descriptors.: "The metabolomics filter requires four core parameters: (1) met_data_path specifying a CSV of detected peaks; (2) possible_adducts listing adducts to add to each mass; (3) mass_tolerance in Da"
- [other] Implement _choose_cpds_to_filter to iterate over compound dictionaries at each generation, compute adduct-adjusted neutral masses (using RDKit molecular weight from SMILES), and compare each against the peak-list m/z values using the mass_tolerance threshold.: "Implement _choose_cpds_to_filter to iterate over compound dictionaries at each generation, compute adduct-adjusted neutral masses (using RDKit molecular weight from SMILES), and compare each against"
- [intro] It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks: "It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks"
- [other] Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools.: "Default filters are created using RDKit, a python library providing a collection of cheminformatic tools."
- [other] Only unidentified peaks in the metabolomics data are used for filtering.: "Only unidentified peaks in the metabolomics data are used for filtering."
