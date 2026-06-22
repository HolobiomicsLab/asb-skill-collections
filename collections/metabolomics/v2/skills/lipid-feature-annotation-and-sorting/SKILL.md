---
name: lipid-feature-annotation-and-sorting
description: Use when after quantifying ion images in LipidQMap and before exporting to HDF5 format, when you need to organize per-feature metadata (lipid ID, class, adduct, m/z, internal standard flag) into aligned datasets that can be linked to intensity data via dimension scales and sorted for reproducible.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3520
  tools:
  - LipidQMap
  - Cardinal
derived_from:
- doi: 10.1101/2025.10.15.682422v1
  title: LipidQMap
evidence_spans:
- LipidQMap writes MSI exports as HDF5 containers
- LipidQMap writes MSI exports as HDF5 containers that follow the [`Cardinal::HDF5`](https://cardinalmsi.org) conventions.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidqmap_cq
    doi: 10.1101/2025.10.15.682422v1
    title: LipidQMap
  dedup_kept_from: coll_lipidqmap_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1101/2025.10.15.682422v1
  all_source_dois:
  - 10.1101/2025.10.15.682422v1
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# lipid-feature-annotation-and-sorting

## Summary

Annotate quantified lipid features with chemical identity metadata (lipid class, adduct form, neutral mass, m/z) and sort them by m/z for HDF5 export, ensuring machine-readable and standardized feature organization in MSI data containers.

## When to use

After quantifying ion images in LipidQMap and before exporting to HDF5 format, when you need to organize per-feature metadata (lipid ID, class, adduct, m/z, internal standard flag) into aligned datasets that can be linked to intensity data via dimension scales and sorted for reproducible retrieval.

## When NOT to use

- Input features are already sorted and linked via dimension scales in an existing HDF5 container — skip re-annotation and re-sorting to avoid data duplication.
- Lipid identity metadata is not available or cannot be reliably matched to m/z values — annotation will be incomplete or erroneous; resolve identifications first.
- Export format does not require Cardinal::HDF5 compliance (e.g., flat CSV or unstructured image stack) — this annotation workflow is specific to structured HDF5 schemas.

## Inputs

- quantified ion image intensities (feature-by-pixel matrix, n_features × n_pixels, float32)
- lipid feature catalog with chemical annotations (lipid ID, class, adduct, neutral mass, m/z)
- internal standard designation flags per feature (boolean or TRUE/FALSE)

## Outputs

- featureData HDF5 group with datasets: feature_index (int64), feature_id (UTF-8), lipid_class (UTF-8), adduct (UTF-8), neutral_id (UTF-8), mz (float32, sorted ascending), is_standard (bool)
- dimension scale linking intensity axis 0 to featureData/feature_index
- group attribute 'columns' listing all dataset names in featureData

## How to apply

For each quantified lipid feature in the dataset, construct a per-feature metadata row containing: feature_index (int64), feature_id (UTF-8 lipid identifier), lipid_class (UTF-8 class name), adduct (UTF-8 adduct formula), neutral_id (UTF-8 reference mass identifier), mz (float32 measured m/z), and is_standard (boolean). Sort all feature datasets in ascending order by m/z value to establish a consistent feature axis order. Write these datasets into the featureData HDF5 group, aligning axis 0 of the intensity array (n_features × n_pixels) with featureData rows. Attach dimension scales linking intensity axis 0 to the featureData/feature_index dataset, and add group-level metadata listing the column names. This enables Cardinal-compatible feature lookup and cross-linking with external lipid databases.

## Related tools

- **LipidQMap** (Generates quantified ion images and lipid feature list (ID, class, adduct, m/z) for annotation and HDF5 export) — https://github.com/swinnenteam/LipidQMap
- **Cardinal** (Defines the HDF5 schema (Cardinal::HDF5 convention) that specifies featureData group structure and dimension scale linking) — https://cardinalmsi.org

## Evaluation signals

- All feature metadata datasets (feature_index, feature_id, lipid_class, adduct, neutral_id, mz, is_standard) exist in the featureData group with correct dtypes (int64, UTF-8 strings, float32, bool).
- Feature rows are sorted in ascending order by mz; verify mz[i] ≤ mz[i+1] for all i.
- Dataset shapes align: all featureData datasets have length n_features, matching intensity matrix axis 0.
- Dimension scale is correctly attached: intensity.dims[0] references featureData/feature_index with scale labels.
- Group attribute 'columns' lists all dataset names present in featureData (e.g., ['feature_index', 'feature_id', 'lipid_class', 'adduct', 'neutral_id', 'mz', 'is_standard']).

## Limitations

- Feature annotation relies on accurate lipid identification from the input catalog; mismatched m/z or erroneous lipid assignments propagate into the HDF5 output.
- Sorting by m/z alone does not account for isobaric features (same m/z, different identities); post-hoc filtering or manual curation may be needed for disambiguation.
- Sparse or incomplete metadata (e.g., missing neutral_id or unknown adduct) must be handled consistently (e.g., empty strings or 'NA' placeholders) to maintain schema validity.
- No changelog or versioning in the current LipidQMap release; feature annotation logic may change between versions without backwards-compatibility guarantees.

## Evidence

- [methods] Populate the featureData group with per-feature metadata datasets (feature_index as int64, feature_id and lipid_class and adduct and neutral_id as UTF-8 strings, mz as float32 for sorting, is_standard as bool) aligned with intensity axis 0, sorted ascending by mz; add group attribute columns.: "Populate the featureData group with per-feature metadata datasets (feature_index as int64, feature_id and lipid_class and adduct and neutral_id as UTF-8 strings, mz as float32 for sorting,"
- [methods] LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data.: "LipidQMap writes MSI exports as HDF5 containers that follow the Cardinal::HDF5 conventions, enabling standardized storage and interchange of quantified imaging data."
- [readme] Shows ion images for an easily editable list of lipids (list is read from an excel file).: "Shows ion images for an easily editable list of lipids (list is read from an excel file)."
- [readme] Each row in the Excel database represents a different species, and the file should contain the following columns: ID, Class, Neutral Formula, Adducts, M-2 Isotope, Na+ Isotope, Is standard, Standard amount (pmol / mm2), IS.: "Each row in the Excel database represents a different species, and the file should contain the following columns (the column titles need to match exactly): ID, Class, Neutral Formula, Adducts, M-2"
