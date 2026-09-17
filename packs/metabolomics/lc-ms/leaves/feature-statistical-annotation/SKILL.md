---
name: feature-statistical-annotation
description: Use when after LC-MS feature detection, alignment, and quantification
  are complete and you have a feature table with m/z and retention time attributes.
  Use this skill when you have access to a reference list of molecules of interest
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3631
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - KNIME Analytics Platform
  - OpenMS
  - GNPS (Global Natural Products Social Molecular Networking)
  - ili app
  techniques:
  - LC-MS
  - MS-imaging
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1038/nprot.2017.122
  title: 3D molecular cartography (Optimus / 'ili)
evidence_spans: []
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_3d_molecular_cartography_optimus_ili_cq
    doi: 10.1038/nprot.2017.122
    title: 3D molecular cartography (Optimus / 'ili)
  dedup_kept_from: coll_3d_molecular_cartography_optimus_ili_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/nprot.2017.122
  all_source_dois:
  - 10.1038/nprot.2017.122
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-statistical-annotation

## Summary

Putative molecular annotation of LC-MS features by m/z and retention time matching to a curated list of molecules of interest, implementing Metabolomics Standards Initiative level 2 compound identification. This skill enables assignment of chemical identities to detected features without requiring MS/MS validation, facilitating downstream metabolite cartography and biomarker discovery.

## When to use

After LC-MS feature detection, alignment, and quantification are complete and you have a feature table with m/z and retention time attributes. Use this skill when you have access to a reference list of molecules of interest (e.g., from GNPS MS/MS library matching or a manually curated CSV of candidate compounds) and need to assign putative chemical identities to enable interpretation of spatial or temporal patterns across samples.

## When NOT to use

- When MS/MS spectra are not available for high-confidence validation, if your analysis goal requires MSI level 3 or higher (confirmed identity by library spectral match or chemical standard).
- When no curated reference molecule list is available or when the reference list does not overlap substantially with expected metabolites in your sample matrix.
- When feature detection, alignment, and quantification have not yet been completed, or when input feature table lacks accurate m/z or retention time calibration.

## Inputs

- LC-MS feature table (with m/z, retention time, and intensity columns)
- Reference molecule list in CSV format or exported from GNPS (containing m/z, retention time, and compound names)
- Experimental design file (to contextualize feature provenance across runs)

## Outputs

- Annotated feature table with putative compound assignments and match confidence scores
- Annotation log with m/z error and RT drift for each matched feature
- Spatial map metadata enriched with compound identity annotations for visualization

## How to apply

Load the feature table (with m/z and retention time for each feature) and a reference molecule list into KNIME. Execute m/z-RT matching by comparing each feature's mass and elution time to the reference compounds within specified tolerance windows (typically mass tolerance in ppm and RT tolerance in seconds, though exact thresholds are not specified in the workflow documentation). The workflow implements matching at the Metabolomics Standards Initiative level 2 (putatively annotated compounds), meaning identities are based on accurate m/z and RT alignment but require downstream MS/MS validation for confirmation. Export the annotated feature table with assigned compound names and match scores. Validate output by checking that all matched features have m/z error and RT drift within expected instrument calibration ranges and that no feature is assigned multiple conflicting identities.

## Related tools

- **KNIME Analytics Platform** (Workflow engine for executing m/z-RT matching logic and managing feature-to-compound mapping) — https://www.knime.org
- **OpenMS** (Underlying LC-MS feature detection and quantification algorithms that produce the m/z and RT values used for annotation matching) — http://www.openms.de
- **GNPS (Global Natural Products Social Molecular Networking)** (Source of MS/MS spectral library matches and export of reference molecule lists for m/z-RT annotation) — http://gnps.ucsd.edu/
- **ili app** (Downstream visualization tool for spatial mapping of annotated molecular features on 2D and 3D coordinate systems) — https://github.com/ili-toolbox/ili

## Evaluation signals

- All matched features have m/z error within instrument mass calibration tolerance (e.g., < 5 ppm for high-resolution MS).
- Retention time drift between feature and reference compound is within expected LC method variation (typically ± 0.5–2 min depending on gradient length and column stability).
- No feature is assigned to multiple conflicting compound identities; ambiguous matches are flagged or excluded per user-defined confidence threshold.
- Annotated features align spatially or temporally with known biological or experimental patterns (e.g., known biomarkers co-localize in tissue cartography; internal standards appear in expected runs).
- Output annotation metadata schema matches expected columns (feature_id, matched_compound_name, m/z_error, rt_drift, match_score) and contains no null values for matched features.

## Limitations

- Annotation is putative (MSI level 2) and requires MS/MS validation for definitive compound confirmation; MS/MS validation is not currently provided in Optimus.
- Accuracy depends critically on the completeness and accuracy of the reference molecule list; missing or mis-annotated reference compounds will lead to false negatives or false positives.
- M/z and RT matching is sensitive to LC-MS instrument calibration state; poorly calibrated instruments may produce excessive m/z error or RT drift, reducing successful matches.
- No built-in handling of isomers or isobars; features with identical m/z and overlapping RT windows cannot be disambiguated by m/z-RT matching alone.
- Matching tolerance windows must be manually configured by the user; no automated tolerance determination is described in the workflow documentation.

## Evidence

- [readme] Putative molecular annotation of detected features by mz-RT matching to a list of molecules of interest. This implements a molecular identification at the level putatively annotated compounds, corresponding to the level 2 of the Metabolomics Standards Initiative: "Putative molecular annotation of detected features by mz-RT matching to a list of molecules of interest. This implements a molecular identification at the level *putatively annotated compounds*,"
- [readme] The list of molecules of interest can be directly exported from GNPS as a result of MS/MS matching against spectral libraries available at GNPS. Alternatively, the list can be provided as a CSV file created manually.: "The list of molecules of interest can be directly exported from GNPS as a result of MS/MS matching against spectral libraries available at GNPS. Alternatively, the list can be provided as a CSV file"
- [readme] Note that MS/MS validation of putative annotations is needed (currently not provided in Optimus).: "Note that MS/MS validation of putative annotations is needed (currently not provided in Optimus)."
- [other] The Optimus workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables for analysis and spatial mapping.: "The Optimus workflow requires an experimental design file and a stub input file as inputs to process LC-MS feature tables for analysis and spatial mapping."
