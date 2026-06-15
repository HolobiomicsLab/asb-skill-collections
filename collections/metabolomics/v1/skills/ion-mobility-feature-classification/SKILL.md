---
name: ion-mobility-feature-classification
description: Use when you have raw or processed TWIM-MS data (arrival time and m/z pairs) from multiple lipid, protein, or metabolite classes and need to classify features by biomolecular type before—or instead of—performing feature identification.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Python
  - MOCCal
  - DEIMoS
derived_from:
- doi: 10.1021/acs.analchem.3c04290
  title: moccal
evidence_spans:
- MOCCal, or Multi-Omic CCS Calibrator, is a Python application
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_moccal
    doi: 10.1021/acs.analchem.3c04290
    title: moccal
  dedup_kept_from: coll_moccal
schema_version: 0.2.0
---

# ion-mobility-feature-classification

## Summary

Assigns biomolecular class labels (e.g., lipid, protein, carbohydrate) to TWIM-MS features based on their physico-chemical properties (arrival time and m/z) without requiring prior feature identification. This enables immediate class-stratified analysis and class-specific CCS calibration on unidentified experimental data.

## When to use

You have raw or processed TWIM-MS data (arrival time and m/z pairs) from multiple lipid, protein, or metabolite classes and need to classify features by biomolecular type before—or instead of—performing feature identification. Use this when you want to perform class-specific CCS calibration or generate class-indexed feature tables without external database lookups or prior peak annotation.

## When NOT to use

- Input is already a validated, identified feature table (features linked to known compounds via database or MS/MS); classification adds no value.
- You require species-level identification (e.g., which specific lipid species) rather than class-level categorization (e.g., 'lipid' vs. 'protein').
- Data lacks both arrival time and m/z values, or arrival time is corrupted; the algorithm requires both physico-chemical dimensions.

## Inputs

- TWIM-MS experimental data in RawDT format (raw arrival time and m/z from ion mobility mass spectrometry instrument files)
- TWIM-MS experimental data in UserDT format (processed arrival time and m/z values in tabular form)
- Feature list with m/z and arrival time columns (one row per observed feature)

## Outputs

- Feature table indexed by feature identifier with assigned biomolecular class labels
- Class-indexed feature assignments (one row per feature, columns for feature ID and class)
- Feature-to-class mapping suitable for downstream class-specific CCS calculations

## How to apply

Load your TWIM-MS experimental data in either RawDT format (raw instrument files requiring DEIMoS preprocessing) or UserDT format (pre-processed arrival time and m/z tables). Execute MOCCal's biomolecular class-assignment algorithm, which classifies each feature by analyzing its physico-chemical properties (arrival time, m/z, and intrinsic physical characteristics that correlate with molecular class). The algorithm assigns a discrete class label to each feature. Compile the results into a tabular output indexed by feature identifier, with one row per feature and columns for feature ID and assigned class label. The class assignments enable downstream workflows such as class-specific CCS calibration or stratified statistical analysis without requiring prior MS/MS identification or database matching.

## Related tools

- **MOCCal** (Core application that implements biomolecular class assignment algorithm and performs CCS calibration; available as both Python script and standalone executable) — https://github.com/HinesLab/MOCCal
- **DEIMoS** (PNNL preprocessing tool required for RawDT workflow; converts raw ion mobility mass spectrometry data to arrival time and m/z format) — http://github.com/pnnl/deimos

## Examples

```
python MOCCal.py --input_file experimental_features.csv --input_format UserDT --output_dir ./Output
```

## Evaluation signals

- Every feature in the input dataset receives exactly one class label in the output (completeness).
- Class distribution is consistent with expected multi-omic composition (e.g., lipids represent majority in lipid-rich samples, proteins in proteomic samples).
- Assigned classes correlate visually with m/z and arrival time ranges (e.g., high m/z features predominate in lipid or protein classes; small metabolites cluster separately).
- Output table schema matches expected format: one row per feature, with feature ID and class columns; no missing or null class assignments.
- Class assignments remain stable across repeated runs on the same input data (reproducibility).

## Limitations

- Class assignment algorithm does not identify specific compounds or species; it stratifies only by broad biomolecular class (e.g., lipid, protein, carbohydrate, metabolite).
- Accuracy depends on arrival time measurement quality; TWIM instruments record arrival time (ion reaches detector) rather than true drift time (ion residence in mobility cell), and this distinction may affect some assignments.
- Algorithm assumes features conform to physico-chemical property distributions of the training class set; unusual or heavily modified molecules may be misclassified.
- No changelog available, making it unclear which algorithm versions correspond to published benchmarks.

## Evidence

- [other] MOCCal performs experimental data biomolecular class assignment as a core functionality alongside CCS calibration and class-specific CCS calculations.: "MOCCal performs experimental data biomolecular class assignment as a core functionality alongside CCS calibration and class-specific CCS calculations."
- [other] Load experimental TWIM-MS data (arrival time and m/z values) from RawDT or UserDT input format. Execute MOCCal's biomolecular class-assignment algorithm to classify each feature based on its physico-chemical properties. Compile assigned class labels into a tabular output indexed by feature identifier, with one row per feature and columns for feature ID and assigned class.: "Load experimental TWIM-MS data (arrival time and m/z values) from RawDT or UserDT input format. Execute MOCCal's biomolecular class-assignment algorithm to classify each feature based on its"
- [intro] MOCCal offers class assignment and CCS calculations without need for identifying the features first: "MOCCal offers class assignment and CCS calculations without need for identifying the features first"
- [readme] TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time).: "TWIM platforms record the time at which the ion reaches the detector (arrival time) rather than the time an ion spends within the TWIM cell (drift time)."
- [readme] After DEIMoS is set up, you can then run MOCCal_RawDT.py in the DEIMoS virtual environment.: "After DEIMoS is set up, you can then run MOCCal_RawDT.py in the DEIMoS virtual environment."
