---
name: chemical-mass-tolerance-matching
description: Use when when you have a metabolomics peak list (m/z values with optional retention times) from LC-MS or GC-MS and want to filter a computationally expanded chemical library to only compounds whose calculated masses (accounting for ionization adducts) fall within a defined tolerance of observed.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0602
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_2258
  tools:
  - RDKit
  - Python
  - pytest
  - mordred
  techniques:
  - LC-MS
  - GC-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1186/s12859-023-05149-8
  all_source_dois:
  - 10.1186/s12859-023-05149-8
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# chemical-mass-tolerance-matching

## Summary

Match generated compounds to experimental metabolomics peaks by comparing adduct-adjusted neutral masses within a specified mass tolerance window (Da). This skill filters compound libraries to retain only those with masses consistent with detected peaks, enabling hypothesis-driven metabolite discovery.

## When to use

When you have a metabolomics peak list (m/z values with optional retention times) from LC-MS or GC-MS and want to filter a computationally expanded chemical library to only compounds whose calculated masses (accounting for ionization adducts) fall within a defined tolerance of observed peaks. Apply this before each generation in reaction network expansion to reduce computational burden while maintaining experimental grounding.

## When NOT to use

- Input metabolomics peak list is already annotated with compound identities — use target filtering or similarity-based filtering instead.
- Mass tolerance is unknown or cannot be determined from instrument specifications — validate instrument mass accuracy (ppm or Da) before setting tolerance.
- Compound library contains only identified compounds or has no SMILES data — molecular weight cannot be computed without valid SMILES.

## Inputs

- metabolomics peak list (CSV with m/z values, optionally retention times)
- compound library (dictionaries with SMILES, compound IDs)
- mass_tolerance parameter (float, in Da)
- possible_adducts list (strings, e.g. '[M+H]+', '[M+Na]+')
- optional: retention_time_tolerance (float, in seconds or minutes)

## Outputs

- set of compound IDs to filter out (those NOT matching peaks)
- optionally: filtering statistics (count of peaks matched, compounds retained/removed per generation)

## How to apply

Parse the metabolomics CSV peak-list to extract m/z values and optional retention time windows. For each compound in the library, compute its neutral mass from SMILES using RDKit molecular weight. Add each adduct mass from the possible_adducts list to the neutral mass. Compare each adduct-adjusted mass against all peak m/z values using the mass_tolerance threshold (in Da) as a matching window. Retain only compounds where at least one adduct form falls within tolerance of at least one peak. Optionally filter retained compounds further by retention time prediction using mordred descriptors. Return the set of compound IDs to remove (those NOT matching any peak). Log filtering statistics to track how many compounds were retained vs. rejected at each generation.

## Related tools

- **RDKit** (Compute molecular weight from SMILES to generate neutral masses for adduct calculation; used for cheminformatic calculations of mass and optional mordred descriptors for retention time prediction.) — https://rdkit.org/docs/api-docs.html
- **Python** (Primary language for implementing the MetabolomicsFilter subclass, CSV parsing, mass comparison logic, and integration with the Filter base class.) — https://github.com/tyo-nu/MINE-Database
- **pytest** (Unit testing framework for validating edge cases (empty peak lists, out-of-tolerance masses, multiple adduct forms) and verifying correct compound retention/removal.) — https://docs.pytest.org/en/stable/
- **mordred** (Optional: compute molecular descriptors for retention time prediction to enable secondary filtering on predicted RT within specified tolerance.)

## Examples

```
from minedatabase.filters import MetabolomicsFilter; mf = MetabolomicsFilter(mass_tolerance=0.01, metabolomics_file='peaks.csv', possible_adducts=['[M+H]+', '[M+Na]+']); filtered_ids = mf._choose_cpds_to_filter(compounds_dict)
```

## Evaluation signals

- filter_name() returns a non-empty string identifier for the filter.
- _choose_cpds_to_filter() returns a set of compound IDs (not compounds themselves); verify set type and no duplicates.
- Compounds with masses (neutral + adduct) within mass_tolerance of any peak are retained; compounds outside all tolerance windows are removed.
- Unit tests pass for edge cases: empty peak list (returns all compound IDs), single peak with multiple adducts matching (correct set returned), out-of-tolerance masses (correctly excluded).
- Pre/post print methods log the count of peaks successfully matched and the fraction of compounds retained, enabling sanity check on filtering stringency.

## Limitations

- Requires accurate mass tolerance specification in Da; incorrect tolerance leads to either retention of false positives or loss of true metabolites.
- Only unidentified peaks in the metabolomics data are used for filtering — pre-identified peaks must be excluded from the peak list to avoid circularity.
- Adduct prediction assumes all possible_adducts are equally likely; if certain ionization pathways are dominant in the instrument, filtering may miss or retain compounds incorrectly.
- Retention time prediction using mordred descriptors requires a trained retention time model; without one, RT filtering must be omitted.
- SMILES parsing errors or invalid structures in the compound library will cause RDKit molecular weight calculation to fail, silently excluding those compounds.

## Evidence

- [other] The metabolomics filter requires four core parameters: (1) met_data_path specifying a CSV of detected peaks; (2) possible_adducts listing adducts to add to each mass; (3) mass_tolerance in Da defining the matching window; and optionally (4) retention time prediction using mordred descriptors.: "met_data_path specifying a CSV of detected peaks; (2) possible_adducts listing adducts to add to each mass; (3) mass_tolerance in Da defining the matching window"
- [other] In __init__, accept mass_tolerance (Da), metabolomics_file path, and optional retention_time_tolerance; store these as instance attributes. Implement _choose_cpds_to_filter to iterate over compound dictionaries at each generation, compute adduct-adjusted neutral masses (using RDKit molecular weight from SMILES), and compare each against the peak-list m/z values using the mass_tolerance threshold.: "compute adduct-adjusted neutral masses (using RDKit molecular weight from SMILES), and compare each against the peak-list m/z values using the mass_tolerance threshold"
- [intro] It will force pickaxe to only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks: "only keep compounds with masses (and, optionally, retention time (RT)) within a set tolerance of a list of peaks"
- [other] Only unidentified peaks in the metabolomics data are used for filtering.: "Only unidentified peaks in the metabolomics data are used for filtering"
- [other] Return a set of compound IDs to filter out (those NOT matching any peak within tolerance).: "Return a set of compound IDs to filter out (those NOT matching any peak within tolerance)"
- [other] Write pytest unit tests in tests/test_unit/test_filters.py covering edge cases (empty peak-list, out-of-tolerance masses, multiple adduct forms).: "Write pytest unit tests in tests/test_unit/test_filters.py covering edge cases (empty peak-list, out-of-tolerance masses, multiple adduct forms)"
- [other] Default filters are created using RDKit, a python library providing a collection of cheminformatic tools.: "Default filters are created using [RDKit](https://rdkit.org/docs/api-docs.html), a python library providing a collection of cheminformatic tools"
