---
name: species-authentication-classification-evaluation
description: Use when when you have high-throughput mass spectrometry data (DI-MS, ASAP-MS, LDI-MS, or other ambient ionization formats) from unknown biological samples and need to determine their species identity against a curated reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_0625
  - http://edamontology.org/topic_3520
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
  - LDI-MS
derived_from:
- doi: 10.1021/acs.analchem.4c05062
  title: RapidMass
evidence_spans:
- We have developed a versatile software platform, RapidMass.
- We have developed a versatile software platform, RapidMass
- supports data from multiple instruments, including DI-MS and ASAP-MS
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_rapidmass_cq
    doi: 10.1021/acs.analchem.4c05062
    title: RapidMass
  dedup_kept_from: coll_rapidmass_cq
schema_version: 0.2.0
---

# species-authentication-classification-evaluation

## Summary

A workflow for authenticating unknown biological samples by classifying them against a reference database using mass spectrometry peak profiles and database search scoring algorithms. This skill combines pre-processing, peak identification, database matching, and accuracy evaluation to assign species labels with confidence metrics.

## When to use

When you have high-throughput mass spectrometry data (DI-MS, ASAP-MS, LDI-MS, or other ambient ionization formats) from unknown biological samples and need to determine their species identity against a curated reference database. This skill is especially valuable when samples are from easily confused or morphologically similar species, or when rapid, objective authentication is required without relying on visual or morphological inspection.

## When NOT to use

- Input data is already a pre-processed feature table or peak matrix — skip directly to database search and classification steps.
- Reference database is absent, incomplete, or not representative of the species expected in unknowns — authentication will fail or produce unreliable assignments.
- Mass spectrometry data quality is severely compromised (e.g., extreme noise, baseline drift, or instrumental malfunction) — pre-processing cannot recover meaningful peak profiles.

## Inputs

- Raw mass spectrometry spectral data in mzML, mzXML, or native vendor instrument format
- Reference species database with annotated peak profiles from validated standards
- Ground-truth species labels for unknown samples (optional, for evaluation)

## Outputs

- Species assignment with classification confidence scores for each unknown sample
- Visual discrimination outputs (score heatmap, classification plot)
- Accuracy metrics (classification rate, confusion matrix) when ground-truth labels are available
- Ranked list of candidate species matches per sample

## How to apply

Load mass spectrometry data in supported formats (mzML, mzXML, or native vendor formats) into RapidMass. Apply automatic data pre-processing including noise filtering, baseline correction, and peak detection to normalize the spectral profiles. Execute RapidMass's database search algorithm(s) to score and classify each unknown sample against reference species spectra, producing a ranked list of candidate matches with similarity scores. Generate visual discrimination outputs (score heatmap, classification plot) to inspect classification confidence and pattern consistency. Evaluate the resulting species assignments against ground-truth labels (when available) by computing accuracy metrics such as classification rate and confusion patterns. Compare performance metrics to the established validation baseline for your instrument type (e.g., the DI-MS/ASAP-MS baseline reported in the article) to confirm satisfactory discrimination quality.

## Related tools

- **RapidMass** (Integrated graphical platform for data pre-processing, peak detection, database search, and species classification with visual output generation) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Direct infusion mass spectrometry instrument for acquiring spectral data on plant materials and other biological samples)
- **ASAP-MS** (Ambient solid analysis probe mass spectrometry instrument for acquiring spectral data without sample preparation)
- **LDI-MS** (Laser desorption/ionization mass spectrometry instrument for acquiring spectral data from solid or semi-solid samples)

## Evaluation signals

- Classification accuracy against ground-truth species labels meets or exceeds the established validation baseline for the instrument type (e.g., satisfactory discrimination on easily confused plant materials as documented in the article).
- Visual discrimination outputs (heatmap, classification plot) show clear separation between reference species clusters and consistent assignment of unknown samples to a single species or tight group of species.
- Database search scores for correct species assignments are significantly higher than scores for incorrect species, indicating high confidence in the match.
- Confusion matrix shows minimal off-diagonal entries (misclassifications), especially between the most easily confused species pairs.
- Peak detection successfully identifies interested MS peaks across all samples with consistent m/z values and intensities within expected ranges for the given instrument platform.

## Limitations

- RapidMass is designed for easily confused plant materials and has been validated primarily on such samples; performance on other organism types (animals, microbes, fungi) is not explicitly demonstrated in the article.
- Authentication accuracy is dependent on the completeness and representativeness of the reference database; rare species or samples with atypical peak profiles may be misassigned or not matched.
- The skill requires access to calibrated, well-maintained mass spectrometry instruments (DI-MS, ASAP-MS, LDI-MS, or compatible platforms); results may degrade with instrument drift or poor calibration.
- Pre-processing parameters (noise filtering, baseline correction, peak detection thresholds) are applied uniformly; highly variable sample types or instruments may require method optimization or manual parameter adjustment.

## Evidence

- [other] Load mass-spectrometry data (DI-MS or ASAP-MS format) for the plant sample set into RapidMass. Apply data pre-processing including automatic identification of interested MS peaks. Execute database search algorithm(s) to score and classify unknown samples against reference species.: "Load mass-spectrometry data (DI-MS or ASAP-MS format) for the plant sample set into RapidMass. Apply data pre-processing including automatic identification of interested MS peaks. Execute database"
- [other] Generate visual discrimination output (e.g., score heatmap, classification plot) and record species assignments. Evaluate classification accuracy against ground-truth species labels and document satisfactory discrimination outcome.: "Generate visual discrimination output (e.g., score heatmap, classification plot) and record species assignments. Evaluate classification accuracy against ground-truth species labels and document"
- [other] RapidMass is designed to support LDI-MS alongside other high-throughput mass spectrometry methodologies beyond the validated DI-MS and ASAP-MS instruments.: "RapidMass is designed to support LDI-MS alongside other high-throughput mass spectrometry methodologies beyond the validated DI-MS and ASAP-MS instruments."
- [other] Integrate LDI-MS data import capability into RapidMass by extending the file parser to recognize and load LDI-MS spectral formats (mzML, mzXML, or native vendor formats).: "Integrate LDI-MS data import capability into RapidMass by extending the file parser to recognize and load LDI-MS spectral formats (mzML, mzXML, or native vendor formats)."
- [intro] RapidMass offers several database search algorithms to achieve unknown sample scoring: "RapidMass offers several database search algorithms to achieve unknown sample scoring"
- [readme] The performance of RapidMass was validated using easily confused plant materials, with satisfactory results.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
