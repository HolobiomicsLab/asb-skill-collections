---
name: analyte-metadata-hierarchical-indexing
description: Use when after applying a stringent Q-value quality filter (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - ResultsLoader
  - MassDash
  - Streamlit
  techniques:
  - tandem-MS
derived_from:
- doi: 10.1021/acs.jproteome.4c00026
  title: MassDash
evidence_spans:
- ResultsLoader
- MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)
- ':mod:`massdash.loaders`: Classes for loading data'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_massdash_cq
    doi: 10.1021/acs.jproteome.4c00026
    title: MassDash
  dedup_kept_from: coll_massdash_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.jproteome.4c00026
  all_source_dois:
  - 10.1021/acs.jproteome.4c00026
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# analyte-metadata-hierarchical-indexing

## Summary

Build hierarchical lookup structures indexed by protein, peptide sequence, and charge state to enable three-level cascading drop-down selection of high-confidence analytes in mass spectrometry visualization interfaces. This skill transforms filtered feature identification data into a navigable metadata hierarchy suitable for interactive GUI-based analyte selection.

## When to use

After applying a stringent Q-value quality filter (e.g., ≤1% feature Q-value threshold) to a set of identified features from Data-Independent Acquisition mass spectrometry search results, and when you need to populate a multi-level drop-down selection interface that constrains user choices to protein → peptide → charge state progression.

## When NOT to use

- Input is already a curated or pre-selected set of analytes (no filtering needed); use this skill only when starting from raw search results.
- The analysis requires flat (non-hierarchical) analyte lists or does not involve user-facing GUI selection.
- Features have missing or inconsistent metadata (protein, peptide, or charge state); metadata must be complete and structured.

## Inputs

- Search results file containing feature identification data with Q-value scores (format: mzML, mzXML, or vendor-specific; via ResultsLoader)
- Q-value quality threshold (numeric, e.g., 0.01 for 1%)
- Feature metadata: protein names/IDs, peptide sequences, charge states

## Outputs

- Hierarchical lookup structure indexed by [protein][peptide][charge_state]
- Filtered analyte collection with metadata preserved for GUI population
- Three-level drop-down selection boxes populated with protein → peptide → charge state hierarchy

## How to apply

Extract analyte metadata (protein identifier, peptide sequence, charge state) from each feature passing the Q-value quality cutoff using a MassDash ResultsLoader or format-specific loader matching your upstream search software. Construct a nested hierarchical index by first grouping by protein, then by peptide sequence within each protein, then by charge state within each peptide. This three-level structure enables efficient cascading selection: when a user selects a protein, only peptides from that protein appear in the second box; when a peptide is selected, only charge states for that peptide appear in the third box. The hierarchy reduces cognitive load and prevents invalid analyte combinations from being selected, while maintaining the link between the user's selection and the underlying feature data (Q-values, transitions, spectra) needed for downstream visualization.

## Related tools

- **MassDash** (Python package providing ResultsLoader for parsing search results and modular data structures for analyte indexing; hosts the Streamlit GUI that displays the hierarchical drop-down selection interface) — https://github.com/Roestlab/massdash
- **ResultsLoader** (MassDash loader module for ingesting feature identification data and associated Q-value scores from upstream search software) — https://github.com/Roestlab/massdash
- **Streamlit** (Web framework used by MassDash to render the GUI including the three-level cascading drop-down selection boxes)

## Examples

```
# Pseudocode using MassDash Python API
from massdash.loaders import ResultsLoader
loader = ResultsLoader('search_results.tsv')
features = loader.load()
filtered = features[features['q_value'] <= 0.01]
hierarchy = {}
for _, row in filtered.iterrows():
    protein = row['protein']
    peptide = row['peptide_sequence']
    charge = row['charge_state']
    if protein not in hierarchy:
        hierarchy[protein] = {}
    if peptide not in hierarchy[protein]:
        hierarchy[protein][peptide] = []
    if charge not in hierarchy[protein][peptide]:
        hierarchy[protein][peptide].append(charge)
```

## Evaluation signals

- Verify that all analytes in the hierarchy passed the Q-value cutoff (no features with Q-value > threshold are present).
- Check that protein-peptide-charge state relationships are consistent and non-redundant (no duplicate triplets or orphaned entries).
- Confirm that selecting a protein in the GUI dynamically populates only peptides observed in that protein; selecting a peptide shows only charge states for that peptide.
- Validate that the number of analytes in the hierarchy equals the count of unique (protein, peptide, charge_state) triplets in the filtered feature set.
- Ensure that the hierarchical index preserves links to original feature data (Q-values, ion transitions, spectra) for downstream visualization and peak picking tasks.

## Limitations

- The hierarchy is only as complete as the upstream search results; missing metadata for protein, peptide sequence, or charge state will result in exclusion from the indexed structure.
- Large feature sets may result in deep or wide hierarchies that become unwieldy in GUI rendering; performance depends on the number of unique proteins, peptides, and charge states.
- The 1% Q-value threshold (or any fixed threshold) is arbitrary and may be too stringent or too lenient depending on the complexity and quality of the DIA experiment; users may need to adjust the cutoff empirically.
- Charge state inference and assignment depend on accurate m/z and mass calibration in the upstream search software; errors in charge state assignment will propagate to the hierarchy.

## Evidence

- [other] Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface.: "Extract analyte metadata (protein, peptide sequence, charge state) for each passing feature and build hierarchical lookup structures for the three-level drop-down selection interface"
- [other] the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%: "the analytes populated in the drop down selection boxes are filtered based on the feature Q-value of 1%"
- [other] MassDash filters analytes populated in drop-down selection boxes based on a 1% feature Q-value threshold, restricting the available analytes to only those passing this quality cutoff.: "MassDash filters analytes populated in drop-down selection boxes based on a 1% feature Q-value threshold, restricting the available analytes to only those passing this quality cutoff"
- [other] Return filtered analyte collection indexed by protein, peptide, and charge state for dynamic population of the GUI selection boxes.: "Return filtered analyte collection indexed by protein, peptide, and charge state for dynamic population of the GUI selection boxes"
- [other] MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI): "MassDash is a modular and flexible python package that has a streamlit graphical user interface (GUI)"
