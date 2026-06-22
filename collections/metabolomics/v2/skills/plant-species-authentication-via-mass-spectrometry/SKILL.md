---
name: plant-species-authentication-via-mass-spectrometry
description: Use when when you have mass spectrometry raw data (DI-MS or ASAP-MS format) from plant samples that are easily confused due to morphological similarity, or when you need to verify or authenticate the species identity of a plant material against a reference database.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3767
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - RapidMass
  - DI-MS
  - ASAP-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c05062
  all_source_dois:
  - 10.1021/acs.analchem.4c05062
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# plant-species-authentication-via-mass-spectrometry

## Summary

Authenticate and discriminate between morphologically similar plant species by applying mass spectrometry data (DI-MS or ASAP-MS) to RapidMass, which integrates automated peak detection, database search algorithms, and visual classification outputs. This skill enables species assignment of unknown plant samples with satisfactory accuracy even when visual or conventional morphological methods are inconclusive.

## When to use

When you have mass spectrometry raw data (DI-MS or ASAP-MS format) from plant samples that are easily confused due to morphological similarity, or when you need to verify or authenticate the species identity of a plant material against a reference database. This skill is particularly applicable in quality control, herbal material authentication, or species verification workflows where instrumental discrimination is more reliable than visual inspection.

## When NOT to use

- When your input is already a pre-processed feature table or extracted peak list—RapidMass requires raw DI-MS or ASAP-MS data as input.
- When you lack a suitable reference database of authenticated species spectra; RapidMass classification depends on database quality and completeness.
- When the plant material is not easily confused with other species or when morphological/visual methods are already definitive; the added complexity of mass spectrometry setup may be unnecessary.

## Inputs

- DI-MS (direct infusion mass spectrometry) raw data files
- ASAP-MS (atmospheric solids analysis probe mass spectrometry) raw data files
- Reference mass spectrometry database or library of known plant species spectra
- Ground-truth species labels (optional, for validation)

## Outputs

- Species classification assignments for unknown plant samples
- Score heatmap visualizing sample-to-reference similarity
- Classification plots showing discrimination between species
- Database search algorithm scores for each sample-reference pair
- Classification accuracy metrics (when ground truth is available)

## How to apply

Load your DI-MS or ASAP-MS mass spectrometry data files into RapidMass. The software automatically identifies interested MS peaks during data pre-processing, which standardizes and prepares the spectral features for classification. Next, execute one or more of RapidMass's built-in database search algorithms to score and classify your unknown samples against reference species spectra. The algorithms generate visual discrimination outputs (such as score heatmaps or classification plots) that directly assign species labels to unknowns. Finally, evaluate classification accuracy by comparing the RapidMass assignments to ground-truth species labels (if available) or by examining the confidence scores and visual separation in the discrimination plots to confirm satisfactory discrimination outcome.

## Related tools

- **RapidMass** (Primary software platform integrating data pre-processing, automated peak detection, database search algorithms, and visual discrimination output generation for species classification from mass spectrometry data.) — https://github.com/Katherine00689/RapidMass
- **DI-MS** (Instrument/data format: direct infusion mass spectrometry data acquisition and format supported by RapidMass for plant sample analysis.)
- **ASAP-MS** (Instrument/data format: atmospheric solids analysis probe mass spectrometry data acquisition and format supported by RapidMass for plant sample analysis.)

## Evaluation signals

- Species assignments are generated for all unknown samples in the input dataset (completeness).
- Classification accuracy (if ground truth is available) meets or exceeds the 'satisfactory results' threshold demonstrated in the RapidMass validation study on easily confused plant materials.
- Visual discrimination outputs (heatmaps, classification plots) show clear visual separation between different plant species, indicating confident and distinct assignments.
- Database search algorithm scores are reported for each sample-reference comparison, and unknown samples receive highest scores for their true species (or assigned species if unknown identity is not independently verified).
- The pre-processed spectral data show automatic identification and retention of relevant MS peaks (no spurious noise or complete loss of signal in visual inspection of peak lists).

## Limitations

- RapidMass performance is contingent on the quality, completeness, and representativeness of the reference database; species not in the database or with poor spectral representation may be misclassified.
- The skill assumes that easily confused plant materials can be discriminated via mass spectrometry; some species may have overlapping or indistinguishable MS signatures, limiting resolution.
- Visual interface and user-friendly design may obscure or simplify underlying algorithm choices; users without MS expertise may not be able to optimize or troubleshoot algorithm parameters.
- No changelog or version history was found in the repository documentation, limiting traceability of software updates and reproducibility across different software versions.

## Evidence

- [readme] The software integrates data pre-processing, analysis, and evaluation enabling direct discrimination of unknown sample species with intuitive visual outputs.: "This tool integrates data pre-processing, analysis, and evaluation, enabling direct discrimination of unknown sample species with intuitive visual outputs."
- [readme] RapidMass automatically identifies interested MS peaks and supports multiple instrument formats.: "the software provides automatic identification of interested MS peaks and supports data from multiple instruments, including DI-MS and ASAP-MS."
- [readme] Validation on easily confused plant materials demonstrated satisfactory species discrimination.: "The performance of RapidMass was validated using easily confused plant materials, with satisfactory results."
- [readme] The software offers several database search algorithms for unknown sample scoring.: "RapidMass offers several database search algorithms to achieve unknown sample scoring."
- [readme] RapidMass features a user-friendly interface accessible to non-programming users.: "RapidMass features a user-friendly, visual interface, making it accessible to users without programming expertise"
