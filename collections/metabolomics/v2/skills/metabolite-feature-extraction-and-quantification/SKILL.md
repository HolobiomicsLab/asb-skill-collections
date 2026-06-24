---
name: metabolite-feature-extraction-and-quantification
description: Use when after retention-time correction and data alignment have been
  completed on centroided LC-MS data (mzML or mzXML format).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3629
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - MetCohort
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.4c04906
  title: MetCohort
evidence_spans:
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data
  processing tool for large-scale metabolomics and exposomics
- MetCohort is an untargeted liquid chromatography-mass spectrometry (LC-MS) data
  processing tool
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metcohort_cq
    doi: 10.1021/acs.analchem.4c04906
    title: MetCohort
  dedup_kept_from: coll_metcohort_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.4c04906
  all_source_dois:
  - 10.1021/acs.analchem.4c04906
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# metabolite-feature-extraction-and-quantification

## Summary

Peak detection and feature table generation from retention-time–corrected LC-MS data, producing a quantitative matrix of detected metabolites with m/z, retention time, and intensity values across all samples. This skill is essential for converting processed LC-MS raw data into a structured, downstream-analysis-ready feature matrix suitable for statistical and annotation workflows.

## When to use

Apply this skill after retention-time correction and data alignment have been completed on centroided LC-MS data (mzML or mzXML format). Use it when you need to identify and quantify individual chromatographic peaks across a cohort of samples, with particular importance for large-scale metabolomics or exposomics studies where false positive and false negative rates must be simultaneously minimized.

## When NOT to use

- Input data is not centroided (MetCohort requires centroided spectra for accurate peak detection)
- No quality control samples have been designated; ROI matrix construction depends on QC-derived regions
- Raw data has not undergone retention-time alignment; misaligned data will produce fragmented or spurious features

## Inputs

- Retention-time–corrected LC-MS data in mzML or mzXML format
- At least one labelled quality control (QC) file
- Data alignment parameters and reference file from prior alignment stage
- Optional: targeted extraction table in xlsx format for compounds of interest

## Outputs

- Feature table (CSV or mzTab format) containing detected peaks with m/z, retention time, intensity values, and sample-wise quantification
- Feature detection visualization (chromatograms with integration regions)
- Feature metadata (reference file apex m/z and retention time per feature)
- Optional: feature data export in .pkd format for session persistence

## How to apply

Load RT-corrected LC-MS data into MetCohort and configure peak detection parameters: set the minimum proportion of non-zero peaks across samples (default 80%), allowed m/z deviation (default 0.01 Da for ROI detection), minimum continuous non-zero points (default 3), maximum continuous zero points (default 10), and maximum chromatographic peak width (default 15 s). Select a reference QC file to define feature m/z and retention time representation. Adjust the entropy coefficient (0–1; default 0.8) to control the score threshold for feature determination—lower values for large-scale studies to increase feature recovery. Apply the centWave-based ROI detection algorithm to identify regions of interest, then perform feature integration across the ROI matrix. Visualize results and export the feature table in CSV or mzTab format, preserving retention time, m/z, and intensity for each detected feature.

## Related tools

- **MetCohort** (Integrated platform for feature detection via centWave algorithm, ROI matrix construction, and feature integration with entropy-based scoring) — https://github.com/JunYang2021/MetCohort

## Evaluation signals

- Feature table contains no null entries for m/z or retention time; intensity values are numeric and non-negative
- Proportion of features with non-zero peaks meets or exceeds the specified minimum threshold (default 80% across samples)
- Feature count and intensity distribution are consistent with expected metabolome complexity; absence of systematic bimodality or truncation in intensity distribution
- Cross-validation against reference QC samples shows reproducible m/z and retention time values within mass accuracy specification (typically ±5 ppm for Orbitrap, ±0.01 Da for QTOF)
- Visualization confirms that integration regions (shaded chromatograms) align with actual peak boundaries and do not artificially merge or fragment coeluting features

## Limitations

- Peak detection accuracy is highly dependent on prior data alignment quality; poor retention-time alignment will result in reduced feature count and degraded integration
- Feature detection of isomers or coeluting compounds may be inferior to untargeted mode, and integration accuracy can be compromised for unresolved peaks
- Entropy coefficient requires manual optimization for large-scale studies; default value (0.8) may be too stringent, requiring downward adjustment to recover weak but real features
- Small-scale studies (few QC files) benefit from increased minimum continuous non-zero points to reduce noise, but this reduces feature sensitivity
- The algorithm assumes that at least one QC file has been properly designated; absence of high-quality QC data will compromise ROI matrix reliability

## Evidence

- [other] Peak detection is performed as a sequential step after data correction, and the resulting feature detection outputs are visualized in the software and can be saved for subsequent analysis.: "Peak detection is performed as a sequential step after data correction, and the resulting feature detection outputs are visualized in the software and can be saved for subsequent analysis."
- [intro] With innovative and robust data correction and feature detection algorithm, MetCohort have a low false positive and false negative rate simultaneously. Feature table of high quality is generated: "With innovative and robust data correction and feature detection algorithm, MetCohort have a low false positive and false negative rate simultaneously. Feature table of high quality is generated"
- [other] Generate a feature table containing detected peaks with retention time, m/z, and intensity values.: "Generate a feature table containing detected peaks with retention time, m/z, and intensity values."
- [other] Apply peak detection algorithm to identify features across all samples, using the robust feature detection algorithm integrated in MetCohort to achieve precise peak picking.: "Apply peak detection algorithm to identify features across all samples, using the robust feature detection algorithm integrated in MetCohort to achieve precise peak picking."
- [readme] Minimum number of non-zero peaks in a feature: Non-zero peaks should not exceed the specified proportion of all the samples. Default value is 80%.: "Minimum number of non-zero peaks in a feature: Non-zero peaks should not exceed the specified proportion of all the samples. Default value is 80%."
- [readme] Delta m/z: Allowed m/z deviation in the process of ROI detection and ROI matrix construction. Default value is 0.01.: "Delta m/z: Allowed m/z deviation in the process of ROI detection and ROI matrix construction. Default value is 0.01."
- [readme] Entropy coefficient: A value ranging from 0 to 1 that controls the score threshold for feature determination in the ROI matrix. A larger entropy coefficient corresponds to a higher threshold. The default value is set to 0.8. For large-scale sample processing, users are advised to adjust this value lower.: "Entropy coefficient: A value ranging from 0 to 1 that controls the score threshold for feature determination in the ROI matrix. A larger entropy coefficient corresponds to a higher threshold. The"
- [readme] The feature detection of isomers or coeluting compounds and integration in targeted extraction may be worse than the untargeted mode.: "The feature detection of isomers or coeluting compounds and integration in targeted extraction may be worse than the untargeted mode."
- [readme] good alignment can make the true features being more easily identified and integrated. A bad data alignment can reduce the feature numbers and negatively affect feature integration.: "good alignment can make the true features being more easily identified and integrated. A bad data alignment can reduce the feature numbers and negatively affect feature integration."
